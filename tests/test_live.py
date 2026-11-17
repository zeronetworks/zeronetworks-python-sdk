"""Live integration tests – run against a real Zero Networks API.

These tests are skipped by default. To enable them:

    export ZERONETWORKS_LIVE=1
    export ZERONETWORKS_API_KEY=<your-api-key>
    export ZERONETWORKS_SERVER_URL=https://portal-dev.zeronetworks.com/api/v1  # optional
    export ZN_ASSET_FQDN_1=rdc01.domain.local
    export ZN_ASSET_FQDN_2=ts01.domain.local
    export ZN_USER_ID=u:i:AbCd1234      # optional, defaults to any-user group

    python -m pytest tests/test_live.py -v

Every test that creates a resource cleans it up in a finally block (or via a
pytest fixture that yields and tears down), so the tests leave no debris in
the tenant even on failure.
"""

import time

import pytest
from zeronetworks import Zeronetworks, errors, models
from zeronetworks.models import (
    PortsList,
    ReactivePolicyInboundBodyDstEntityInfo,
    ReactivePolicyInboundBodySrcEntityInfo,
    ReactivePolicyInboundBodySrcUserInfo,
    ReactivePolicyOutboundBodyDstEntityInfo,
    ReactivePolicyOutboundBodySrcEntityInfo,
    ReactivePolicyOutboundBodySrcUserInfo,
    SrcUsersList,
)
from tests.conftest import LIVE_MFA_OUTBOUND_DST, LIVE_USER_ID

# All tests in this module require the live marker
pytestmark = pytest.mark.live


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

class TestLiveAssets:
    def test_search_known_asset(self, live_client, live_asset_ids):
        asset_id, _ = live_asset_ids
        assert asset_id.startswith("a:")

    def test_search_unknown_fqdn_raises_404(self, live_client):
        with pytest.raises(errors.Error) as exc:
            live_client.assets.assets_search(fqdn="this.host.does.not.exist.invalid")
        assert exc.value.raw_response.status_code == 404

    def test_search_without_fqdn_raises_400(self, live_client):
        # API: "asset identifier is unrecognized"
        with pytest.raises(errors.Error) as exc:
            live_client.assets.assets_search()
        assert exc.value.raw_response.status_code == 400


# ---------------------------------------------------------------------------
# Custom Groups  (full create → get → update → delete lifecycle)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_custom_group(live_client):
    """Create a temporary custom group and delete it after the test."""
    res = live_client.groups_custom.custom_groups_create(
        name="[pytest] Temp Group",
        description="Created by the automated test suite – safe to delete",
    )
    group_id = res.entity.id
    yield res
    try:
        live_client.groups_custom.custom_groups_delete(id=group_id)
    except Exception:
        pass  # already deleted by the test itself


class TestLiveCustomGroups:
    def test_create_and_get(self, live_client, live_custom_group):
        group_id = live_custom_group.entity.id
        res = live_client.groups_custom.custom_groups_get(id=group_id)
        assert res.entity is not None
        assert res.entity.id == group_id

    def test_update_name(self, live_client, live_custom_group):
        group_id = live_custom_group.entity.id
        res = live_client.groups_custom.custom_groups_update(
            id=group_id,
            name="[pytest] Temp Group (updated)",
            description="Updated by automated test suite",
        )
        assert res.entity is not None
        assert res.entity.id == group_id

    def test_add_and_remove_member(self, live_client, live_asset_ids, live_custom_group):
        group_id = live_custom_group.entity.id
        asset_id, _ = live_asset_ids

        live_client.groups_custom.custom_groups_members_add(
            id=group_id, members_id=[asset_id]
        )
        members = live_client.groups_custom.custom_group_members_list(id=group_id)
        assert asset_id in (members.members_id or [])

        live_client.groups_custom.custom_groups_members_delete(
            id=group_id, members_id=[asset_id]
        )

    def test_delete(self, live_client):
        res = live_client.groups_custom.custom_groups_create(
            name="[pytest] Delete Me",
        )
        group_id = res.entity.id
        live_client.groups_custom.custom_groups_delete(id=group_id)
        # Custom groups are soft-deleted (marked inactive), so GET still returns them.
        # Deleting again is rejected once the group is inactive.
        with pytest.raises(errors.ZeronetworksError):
            live_client.groups_custom.custom_groups_delete(id=group_id)

    def test_get_nonexistent_raises(self, live_client):
        with pytest.raises(errors.ZeronetworksError):
            live_client.groups_custom.custom_groups_get(id="g:c:doesnotexist")


# ---------------------------------------------------------------------------
# AE Exclusions – inbound (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_ae_exclusion_inbound(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.ae_exclusions.ae_exclusions_inbound_create(
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19999")],
        remote_entity_ids_list=[asset_id_2],
        description="[pytest] temp inbound AE exclusion",
    )
    excl_id = res.item.id
    yield res
    try:
        live_client.ae_exclusions.ae_exclusions_inbound_delete(id=excl_id)
    except Exception:
        pass


class TestLiveAEExclusionsInbound:
    def test_create_and_get(self, live_client, live_ae_exclusion_inbound):
        excl_id = live_ae_exclusion_inbound.item.id
        res = live_client.ae_exclusions.ae_exclusions_inbound_get(id=excl_id)
        assert res.item is not None
        assert res.item.id == excl_id

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29998")],
            remote_entity_ids_list=[asset_id_2],
            description="[pytest] delete-me inbound AE exclusion",
        )
        excl_id = res.item.id
        live_client.ae_exclusions.ae_exclusions_inbound_delete(id=excl_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.ae_exclusions.ae_exclusions_inbound_get(id=excl_id)


# ---------------------------------------------------------------------------
# AE Exclusions – outbound (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_ae_exclusion_outbound(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.ae_exclusions.ae_exclusions_outbound_create(
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19998")],
        remote_entity_ids_list=[asset_id_2],
        description="[pytest] temp outbound AE exclusion",
    )
    excl_id = res.item.id
    yield res
    try:
        live_client.ae_exclusions.ae_exclusions_outbound_delete(id=excl_id)
    except Exception:
        pass


class TestLiveAEExclusionsOutbound:
    def test_create_and_get(self, live_client, live_ae_exclusion_outbound):
        excl_id = live_ae_exclusion_outbound.item.id
        res = live_client.ae_exclusions.ae_exclusions_outbound_get(id=excl_id)
        assert res.item is not None
        assert res.item.id == excl_id


# ---------------------------------------------------------------------------
# Inbound Rules (create → get → update → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_inbound_rule(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.rules_inbound.inbound_rules_create(
        action=1,  # Allow
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19997")],
        remote_entity_ids_list=[asset_id_2],
        state=2,  # Disabled – safer for test rules
        description="[pytest] temp inbound rule",
    )
    rule_id = res.item.id
    yield res
    try:
        live_client.rules_inbound.inbound_rule_delete(id=rule_id)
    except Exception:
        pass


class TestLiveRulesInbound:
    def test_create_and_get(self, live_client, live_inbound_rule):
        rule_id = live_inbound_rule.item.id
        res = live_client.rules_inbound.inbound_rule_get(id=rule_id)
        assert res.item is not None
        assert res.item.id == rule_id

    def test_update(self, live_client, live_inbound_rule, live_asset_ids):
        rule_id = live_inbound_rule.item.id
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_inbound.inbound_rule_update(
            id=rule_id,
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="19997")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] updated inbound rule",
        )
        assert res.item is not None

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29997")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] delete-me inbound rule",
        )
        rule_id = res.item.id
        live_client.rules_inbound.inbound_rule_delete(id=rule_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.rules_inbound.inbound_rule_get(id=rule_id)


# ---------------------------------------------------------------------------
# Outbound Rules (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_outbound_rule(live_client, live_asset_ids):
    asset_id, asset_id_2 = live_asset_ids
    res = live_client.rules_outbound.outbound_rules_create(
        action=1,
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports="19996")],
        remote_entity_ids_list=[asset_id_2],
        state=2,
        description="[pytest] temp outbound rule",
    )
    rule_id = res.item.id
    yield res
    try:
        live_client.rules_outbound.outbound_rule_delete(id=rule_id)
    except Exception:
        pass


class TestLiveRulesOutbound:
    def test_create_and_get(self, live_client, live_outbound_rule):
        rule_id = live_outbound_rule.item.id
        res = live_client.rules_outbound.outbound_rule_get(id=rule_id)
        assert res.item is not None
        assert res.item.id == rule_id

    def test_delete(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_outbound.outbound_rules_create(
            action=1,
            local_entity_id=asset_id,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="29996")],
            remote_entity_ids_list=[asset_id_2],
            state=2,
            description="[pytest] delete-me outbound rule",
        )
        rule_id = res.item.id
        live_client.rules_outbound.outbound_rule_delete(id=rule_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.rules_outbound.outbound_rule_get(id=rule_id)


# ---------------------------------------------------------------------------
# Internal Access Policies (create → get → delete)
# ---------------------------------------------------------------------------

@pytest.fixture
def live_iap(live_client, live_asset_ids):
    asset_id, _ = live_asset_ids
    res = live_client.internal_access_policy.internal_access_policy_create(
        dst_asset_id=asset_id,
        dst_ports_list=[PortsList(protocol_type=6, ports="22")],
        dst_process_names_list=["*"],
        name="[pytest] Temp IAP",
        rule_duration=1,  # Hour – IAP rejects "Never"
        src_user_ids_list=[LIVE_USER_ID],
        state=2,  # Disabled
        description="Created by automated test suite – safe to delete",
    )
    iap_id = res.item.id
    yield res
    try:
        live_client.internal_access_policy.internal_access_policy_delete(id=iap_id)
    except Exception:
        pass


class TestLiveInternalAccessPolicy:
    def test_create_and_get(self, live_client, live_iap):
        iap_id = live_iap.item.id
        res = live_client.internal_access_policy.internal_access_policy_get(id=iap_id)
        assert res.item is not None
        assert res.item.id == iap_id

    def test_update(self, live_client, live_iap, live_asset_ids):
        iap_id = live_iap.item.id
        asset_id, _ = live_asset_ids
        res = live_client.internal_access_policy.internal_access_policy_update(
            id=iap_id,
            dst_asset_id=asset_id,
            dst_ports_list=[PortsList(protocol_type=6, ports="22")],
            dst_process_names_list=["*"],
            name="[pytest] Temp IAP (updated)",
            rule_duration=1,  # Hour – IAP rejects 'Never'
            src_user_ids_list=[LIVE_USER_ID],
            state=2,
        )
        assert res.item is not None

    def test_delete(self, live_client, live_asset_ids):
        asset_id, _ = live_asset_ids
        res = live_client.internal_access_policy.internal_access_policy_create(
            dst_asset_id=asset_id,
            dst_ports_list=[PortsList(protocol_type=6, ports="22")],
            dst_process_names_list=["*"],
            name="[pytest] Delete Me IAP",
            rule_duration=1,  # Hour – IAP rejects 'Never'
            state=2,  # required by the API despite the spec
            src_user_ids_list=[LIVE_USER_ID],
        )
        iap_id = res.item.id
        live_client.internal_access_policy.internal_access_policy_delete(id=iap_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.internal_access_policy.internal_access_policy_get(id=iap_id)


# ===========================================================================
# 1.1.0 features (spec 1.26.9)
# ===========================================================================

def _inbound_rule_kwargs(asset_id, asset_id_2, port, description, **extra):
    return dict(
        action=1,
        local_entity_id=asset_id,
        local_processes_list=["*"],
        ports_list=[PortsList(protocol_type=6, ports=port)],
        remote_entity_ids_list=[asset_id_2],
        state=2,  # Disabled
        description=description,
        **extra,
    )


def _wait_for_new_millis(ts):
    """Make sure the next write lands on a later updatedAt than *ts*."""
    while int(time.time() * 1000) <= ts:
        time.sleep(0.005)


# ---------------------------------------------------------------------------
# Optimistic concurrency: zn-expected-updated-at → 409 StaleConflictError
# ---------------------------------------------------------------------------

class TestLiveStaleConflict:
    def test_inbound_rule_update_with_current_updated_at_succeeds(
        self, live_client, live_inbound_rule, live_asset_ids
    ):
        asset_id, asset_id_2 = live_asset_ids
        rule_id = live_inbound_rule.item.id
        current = live_client.rules_inbound.inbound_rule_get(id=rule_id).item.updated_at
        assert current, "rule GET did not return updatedAt"
        res = live_client.rules_inbound.inbound_rule_update(
            id=rule_id,
            zn_expected_updated_at=current,
            **_inbound_rule_kwargs(asset_id, asset_id_2, "19997", "[pytest] fresh update"),
        )
        assert res.item is not None

    def test_inbound_rule_update_with_stale_updated_at_raises_409(
        self, live_client, live_inbound_rule, live_asset_ids
    ):
        asset_id, asset_id_2 = live_asset_ids
        rule_id = live_inbound_rule.item.id
        stale = live_client.rules_inbound.inbound_rule_get(id=rule_id).item.updated_at
        _wait_for_new_millis(stale)
        # Someone else changes the rule…
        live_client.rules_inbound.inbound_rule_update(
            id=rule_id,
            **_inbound_rule_kwargs(asset_id, asset_id_2, "19997", "[pytest] concurrent edit"),
        )
        # …so our update based on the old read must be rejected.
        with pytest.raises(errors.StaleConflictError) as exc:
            live_client.rules_inbound.inbound_rule_update(
                id=rule_id,
                zn_expected_updated_at=stale,
                **_inbound_rule_kwargs(asset_id, asset_id_2, "19997", "[pytest] stale edit"),
            )
        assert exc.value.raw_response.status_code == 409
        assert exc.value.data.updated_at and exc.value.data.updated_at > stale
        # The concurrent edit must still be in place
        after = live_client.rules_inbound.inbound_rule_get(id=rule_id).item
        assert after.description == "[pytest] concurrent edit"

    def test_inbound_rule_delete_with_stale_updated_at_raises_409(
        self, live_client, live_inbound_rule, live_asset_ids
    ):
        asset_id, asset_id_2 = live_asset_ids
        rule_id = live_inbound_rule.item.id
        stale = live_client.rules_inbound.inbound_rule_get(id=rule_id).item.updated_at
        _wait_for_new_millis(stale)
        live_client.rules_inbound.inbound_rule_update(
            id=rule_id,
            **_inbound_rule_kwargs(asset_id, asset_id_2, "19997", "[pytest] concurrent edit"),
        )
        with pytest.raises(errors.StaleConflictError):
            live_client.rules_inbound.inbound_rule_delete(id=rule_id, zn_expected_updated_at=stale)
        # Rule must survive the rejected delete
        assert live_client.rules_inbound.inbound_rule_get(id=rule_id).item.id == rule_id

    def test_iap_update_with_stale_updated_at_raises_409(self, live_client, live_iap, live_asset_ids):
        asset_id, _ = live_asset_ids
        iap_id = live_iap.item.id
        stale = live_client.internal_access_policy.internal_access_policy_get(id=iap_id).item.updated_at
        kwargs = dict(
            id=iap_id,
            dst_asset_id=asset_id,
            dst_ports_list=[PortsList(protocol_type=6, ports="22")],
            dst_process_names_list=["*"],
            rule_duration=1,  # Hour – IAP rejects 'Never'
            src_user_ids_list=[LIVE_USER_ID],
            state=2,
        )
        _wait_for_new_millis(stale)
        live_client.internal_access_policy.internal_access_policy_update(
            name="[pytest] Temp IAP (concurrent)", **kwargs
        )
        with pytest.raises(errors.StaleConflictError):
            live_client.internal_access_policy.internal_access_policy_update(
                name="[pytest] Temp IAP (stale)", zn_expected_updated_at=stale, **kwargs
            )


# ---------------------------------------------------------------------------
# New / renamed rule fields
# ---------------------------------------------------------------------------

class TestLiveRuleFields:
    def test_rule_category_round_trips(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_inbound.inbound_rules_create(
            **_inbound_rule_kwargs(
                asset_id, asset_id_2, "29995", "[pytest] rule category", rule_category=1  # IT
            )
        )
        rule_id = res.item.id
        try:
            got = live_client.rules_inbound.inbound_rule_get(id=rule_id).item
            assert got.rule_category == 1
        finally:
            live_client.rules_inbound.inbound_rule_delete(id=rule_id)

    def test_src_user_infos_populated(self, live_client, live_asset_ids):
        """Regression: 1.0.x read `srcUsersInfos`, the API sends `srcUserInfos`.

        Source users are only allowed on outbound rules
        (inbound → "Cannot create inbound rule with source users").
        """
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.rules_outbound.outbound_rules_create(
            **_inbound_rule_kwargs(
                asset_id, asset_id_2, "29994", "[pytest] src users",
                src_users_list=[SrcUsersList(id=LIVE_USER_ID)],
            )
        )
        rule_id = res.item.id
        try:
            got = live_client.rules_outbound.outbound_rule_get(id=rule_id).item
            assert got.src_user_infos, "srcUserInfos missing from rule GET"
            assert LIVE_USER_ID in [u.id for u in got.src_user_infos]
        finally:
            live_client.rules_outbound.outbound_rule_delete(id=rule_id)


# ---------------------------------------------------------------------------
# Custom group GET now returns GroupEntity
# ---------------------------------------------------------------------------

class TestLiveCustomGroupEntity:
    def test_get_returns_group_entity(self, live_client, live_custom_group):
        group_id = live_custom_group.entity.id
        res = live_client.groups_custom.custom_groups_get(id=group_id)
        assert isinstance(res, models.GroupEntity)
        assert isinstance(res.entity, models.Group)
        assert res.entity.name == "[pytest] Temp Group"


# ---------------------------------------------------------------------------
# MFA policies (create → get → delete), both directions
# ---------------------------------------------------------------------------

def _mfa_kwargs(asset_id, asset_id_2, dst_cls, src_cls, user_cls, port):
    return dict(
        additional_ports_list=[],
        dst_entity_info=dst_cls(id=asset_id),
        dst_port=port,
        dst_process_names=["*"],
        fallback_to_logged_on_user=False,
        mfa_methods=[4],  # Browser
        override_builtins=False,
        protocol_type=6,
        rule_duration=5,  # Never
        src_entity_infos=[src_cls(id=asset_id_2)],
        src_process_names=["*"],
        src_user_infos=[user_cls(id=LIVE_USER_ID)],
        state=2,  # Disabled
        description="[pytest] temp MFA policy – safe to delete",
    )


class TestLiveMFAPolicies:
    def test_inbound_lifecycle(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        res = live_client.mfa_inbound.mfa_inbound_policies_create(
            **_mfa_kwargs(
                asset_id, asset_id_2,
                ReactivePolicyInboundBodyDstEntityInfo,
                ReactivePolicyInboundBodySrcEntityInfo,
                ReactivePolicyInboundBodySrcUserInfo,
                "19993",
            )
        )
        pol_id = res.item.id
        try:
            got = live_client.mfa_inbound.mfa_inbound_policies_get(id=pol_id)
            assert got.items.id == pol_id
            assert got.items.src_user_infos  # anyOf group/user/idNamePair parses
        finally:
            live_client.mfa_inbound.mfa_inbound_policies_delete(id=pol_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.mfa_inbound.mfa_inbound_policies_get(id=pol_id)

    def test_outbound_lifecycle(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        dst_id = LIVE_MFA_OUTBOUND_DST or asset_id
        try:
            res = live_client.mfa_outbound.mfa_outbound_policies_create(
                **_mfa_kwargs(
                    dst_id, asset_id_2,
                    ReactivePolicyOutboundBodyDstEntityInfo,
                    ReactivePolicyOutboundBodySrcEntityInfo,
                    ReactivePolicyOutboundBodySrcUserInfo,
                    "19992",
                )
            )
        except errors.Error as e:
            if "destination entity not supported" in str(e) and not LIVE_MFA_OUTBOUND_DST:
                pytest.skip(
                    f"{dst_id} is not a valid outbound MFA destination – "
                    "set ZN_MFA_OUTBOUND_DST_ID to one your tenant allows"
                )
            raise
        pol_id = res.item.id
        try:
            got = live_client.mfa_outbound.mfa_outbound_policies_get(id=pol_id)
            assert got.items.id == pol_id
        finally:
            live_client.mfa_outbound.mfa_outbound_policies_delete(id=pol_id)


# ---------------------------------------------------------------------------
# RPC rules (create → get → delete)
# ---------------------------------------------------------------------------

def _create_rpc_rule(live_client, asset_id, asset_id_2):
    return live_client.rules_rpc.rpc_rules_create(
        action=1,
        description="[pytest] temp RPC rule – safe to delete",
        excluded_asset_ids_list=[],
        interface_uuids_list=["rpcAnyInterfaceId"],
        local_asset_id=asset_id,
        op_numbers_list=[0],
        protocols_list=[2],  # RPC over TCP
        remote_asset_ids_list=[asset_id_2],
        state=2,  # Disabled
        user_ids_list=[LIVE_USER_ID],
    )


class TestLiveRPCRules:
    def test_lifecycle(self, live_client, live_asset_ids):
        asset_id, asset_id_2 = live_asset_ids
        try:
            res = _create_rpc_rule(live_client, asset_id, asset_id_2)
        except errors.ZeronetworksDefaultError as e:
            if e.raw_response.status_code == 403:
                pytest.skip("API key lacks permission for RPC rules (403)")
            raise
        rule_id = res.item.id
        try:
            got = live_client.rules_rpc.rpc_rule_get(id=rule_id).item
            assert got.id == rule_id
            # localAssetInfo is now assetBasicInfo; remoteAssetInfos is anyOf
            if got.local_asset_info is not None:
                assert got.local_asset_info.id == asset_id
        finally:
            live_client.rules_rpc.rpc_rule_delete(id=rule_id)
        with pytest.raises(errors.ZeronetworksError):
            live_client.rules_rpc.rpc_rule_get(id=rule_id)
