"""Mock tests for features added in SDK 1.1.0 (spec 1.26.9).

- zn-expected-updated-at header + 409 StaleConflictError on PUT/DELETE
- rule.ruleCategory, rule.srcUserInfos (renamed from srcUsersInfos)
- custom group GET returns GroupEntity
- anyOf user/group infos on rules, RPC rules and MFA policies
"""

import json
import httpx
import pytest
from zeronetworks import errors, models
from zeronetworks.models import PortsList
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    ASSET_ID_2,
    GROUP_ID,
    IAP_ID,
    MFA_POLICY_ID,
    MFA_POLICY_ITEM,
    RPC_RULE_ID,
    RPC_RULE_ITEM,
    RULE_ID,
    RULE_ITEM,
)

UPDATED_AT = 1_700_000_000_000

STALE_BODY = {
    "error": "Conflict",
    "message": "object was modified",
    "code": "stale",
    "updatedAt": UPDATED_AT + 5,
    "updatedBy": {"id": "u:a:someone", "name": "someone"},
    "isDeleted": False,
}

RULE_UPDATE_KWARGS = dict(
    action=1,
    local_entity_id=ASSET_ID,
    local_processes_list=["*"],
    ports_list=[PortsList(protocol_type=6, ports="443")],
    remote_entity_ids_list=[ASSET_ID_2],
    state=1,
)


def _capture(captured, status=200, body=None):
    def handler(req: httpx.Request) -> httpx.Response:
        captured["method"] = req.method
        captured["path"] = req.url.path
        captured["headers"] = req.headers
        captured["body"] = json.loads(req.content) if req.content else None
        return make_response(status, body if body is not None else {"item": RULE_ITEM})
    return handler


# ---------------------------------------------------------------------------
# zn-expected-updated-at
# ---------------------------------------------------------------------------

class TestExpectedUpdatedAtHeader:
    def test_rule_update_sends_header(self):
        captured = {}
        sdk = client_with(_capture(captured))
        sdk.rules_inbound.inbound_rule_update(
            id=RULE_ID, zn_expected_updated_at=UPDATED_AT, **RULE_UPDATE_KWARGS
        )
        assert captured["headers"]["zn-expected-updated-at"] == str(UPDATED_AT)

    def test_rule_update_omits_header_by_default(self):
        captured = {}
        sdk = client_with(_capture(captured))
        sdk.rules_inbound.inbound_rule_update(id=RULE_ID, **RULE_UPDATE_KWARGS)
        assert "zn-expected-updated-at" not in captured["headers"]

    def test_rule_delete_sends_header(self):
        captured = {}
        sdk = client_with(_capture(captured, body={}))
        sdk.rules_outbound.outbound_rule_delete(id=RULE_ID, zn_expected_updated_at=UPDATED_AT)
        assert captured["method"] == "DELETE"
        assert captured["headers"]["zn-expected-updated-at"] == str(UPDATED_AT)

    def test_iap_delete_sends_header(self):
        captured = {}
        sdk = client_with(_capture(captured, body={}))
        sdk.internal_access_policy.internal_access_policy_delete(
            id=IAP_ID, zn_expected_updated_at=UPDATED_AT
        )
        assert captured["headers"]["zn-expected-updated-at"] == str(UPDATED_AT)


class TestStaleConflictError:
    def test_rule_update_409_raises_stale_conflict(self):
        sdk = client_with(lambda req: make_response(409, STALE_BODY))
        with pytest.raises(errors.StaleConflictError) as exc:
            sdk.rules_inbound.inbound_rule_update(
                id=RULE_ID, zn_expected_updated_at=UPDATED_AT, **RULE_UPDATE_KWARGS
            )
        err = exc.value
        assert err.raw_response.status_code == 409
        assert err.data.code == "stale"
        assert err.data.updated_at == UPDATED_AT + 5
        assert err.data.updated_by.id == "u:a:someone"
        assert err.data.is_deleted is False

    def test_stale_conflict_is_a_zeronetworks_error(self):
        sdk = client_with(lambda req: make_response(409, STALE_BODY))
        with pytest.raises(errors.ZeronetworksError):
            sdk.rules_rpc.rpc_rule_delete(id=RPC_RULE_ID, zn_expected_updated_at=UPDATED_AT)

    def test_deleted_object_conflict(self):
        body = {**STALE_BODY, "isDeleted": True, "deletedAt": UPDATED_AT + 9,
                "deletedBy": {"id": "u:a:other", "name": "other"}}
        sdk = client_with(lambda req: make_response(409, body))
        with pytest.raises(errors.StaleConflictError) as exc:
            sdk.mfa_inbound.mfa_inbound_policies_delete(
                id=MFA_POLICY_ID, zn_expected_updated_at=UPDATED_AT
            )
        assert exc.value.data.is_deleted is True
        assert exc.value.data.deleted_by.id == "u:a:other"


# ---------------------------------------------------------------------------
# Rule fields
# ---------------------------------------------------------------------------

class TestRuleFields:
    def test_create_sends_rule_category(self):
        captured = {}
        sdk = client_with(_capture(captured))
        sdk.rules_inbound.inbound_rules_create(**RULE_UPDATE_KWARGS, rule_category=4)  # FQDN
        assert captured["body"]["ruleCategory"] == 4

    def test_get_parses_new_rule_fields(self):
        item = {
            **RULE_ITEM,
            "ruleCategory": 1,
            "firewallId": "fw-1",
            "firewall": {"id": "fw-1", "name": "Edge FW"},
            "updatedAt": UPDATED_AT,
            "srcUserInfos": [{"id": "u:i:User01", "name": "Alice"}],
        }
        sdk = client_with(lambda req: make_response(200, {"item": item}))
        got = sdk.rules_inbound.inbound_rule_get(id=RULE_ID).item
        assert got.rule_category == 1
        assert got.firewall_id == "fw-1"
        assert got.firewall.name == "Edge FW"
        assert got.updated_at == UPDATED_AT
        assert [u.id for u in got.src_user_infos] == ["u:i:User01"]

    def test_unknown_rule_category_does_not_break_parsing(self):
        item = {**RULE_ITEM, "ruleCategory": 99}
        sdk = client_with(lambda req: make_response(200, {"item": item}))
        got = sdk.rules_inbound.inbound_rule_get(id=RULE_ID).item
        assert got.id == RULE_ID


# ---------------------------------------------------------------------------
# Custom group GET → GroupEntity
# ---------------------------------------------------------------------------

class TestCustomGroupGetEntity:
    def test_get_returns_group_entity(self):
        body = {"entity": {
            "id": GROUP_ID,
            "name": "Test Group",
            "type": "custom",
            "source": 1,
            "hasNetworkProtectionPolicy": True,
            "hasIdentityProtectionPolicy": False,
            "externalId": "ext-1",
        }}
        sdk = client_with(lambda req: make_response(200, body))
        res = sdk.groups_custom.custom_groups_get(id=GROUP_ID)
        assert isinstance(res, models.GroupEntity)
        assert res.entity.id == GROUP_ID
        assert res.entity.has_network_protection_policy is True
        assert res.entity.external_id == "ext-1"


# ---------------------------------------------------------------------------
# anyOf entity infos
# ---------------------------------------------------------------------------

class TestAnyOfEntityInfos:
    def test_mfa_src_user_infos_accepts_group_and_user(self):
        item = {**MFA_POLICY_ITEM, "srcUserInfos": [
            {"id": "g:a:Group1", "name": "Admins"},
            {"id": "u:i:User01", "name": "Alice"},
        ]}
        sdk = client_with(lambda req: make_response(200, {"items": item}))
        got = sdk.mfa_inbound.mfa_inbound_policies_get(id=MFA_POLICY_ID).items
        assert [u.id for u in got.src_user_infos] == ["g:a:Group1", "u:i:User01"]

    def test_rpc_rule_asset_infos(self):
        item = {
            **RPC_RULE_ITEM,
            "localAssetInfo": {"id": ASSET_ID, "name": "host1"},
            "remoteAssetInfos": [{"id": ASSET_ID_2, "name": "host2"}],
        }
        sdk = client_with(lambda req: make_response(200, {"item": item}))
        got = sdk.rules_rpc.rpc_rule_get(id=RPC_RULE_ID).item
        assert got.local_asset_info.id == ASSET_ID
        assert got.remote_asset_infos[0].id == ASSET_ID_2
