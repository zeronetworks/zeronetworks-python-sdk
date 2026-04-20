"""Tests for the Outbound MFA Policies module.

ReactivePolicyState: 1=Enabled, 2=Disabled
RuleDuration: 1=Hour, 2=Day, 3=Week, 4=Month, 5=Never, 6=4h, 7=12h, 8=8h
MfaMethods: 1=SMS, 2=Email, 3=Duo, 4=Browser, 5=No MFA
"""

import json
import httpx
import pytest
from zeronetworks import errors
from zeronetworks.models import (
    ReactivePolicyOutboundBodyDstEntityInfo,
    ReactivePolicyOutboundBodySrcEntityInfo,
    ReactivePolicyOutboundBodySrcUserInfo,
)
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    ASSET_ID_2,
    MFA_POLICY_ID,
    MFA_POLICY_RESPONSE,
    MFA_POLICY_GET_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
)

MFA_OUT_CREATE_KWARGS = dict(
    additional_ports_list=[],
    dst_entity_info=ReactivePolicyOutboundBodyDstEntityInfo(id=ASSET_ID),
    dst_port="443",
    fallback_to_logged_on_user=False,
    mfa_methods=[4],  # Browser
    override_builtins=False,
    protocol_type=6,
    rule_duration=5,  # Never
    src_entity_infos=[ReactivePolicyOutboundBodySrcEntityInfo(id=ASSET_ID_2)],
    src_process_names=["*"],
    src_user_infos=[ReactivePolicyOutboundBodySrcUserInfo(id="u:i:TestUser01")],
    state=1,  # Enabled
)


class TestMFAOutboundCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_RESPONSE))
        res = sdk.mfa_outbound.mfa_outbound_policies_create(**MFA_OUT_CREATE_KWARGS)
        assert res.item is not None

    def test_create_hits_outbound_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_create(**MFA_OUT_CREATE_KWARGS)
        assert "outbound" in captured["path"]

    def test_create_sends_correct_body(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_create(**MFA_OUT_CREATE_KWARGS)
        body = captured["body"]
        assert body["dstPort"] == "443"
        assert body["protocolType"] == 6
        assert body["mfaMethods"] == [4]
        assert body["overrideBuiltins"] is False

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.mfa_outbound.mfa_outbound_policies_create(**MFA_OUT_CREATE_KWARGS)
        assert exc_info.value.status_code == 400

    def test_create_with_name_and_description(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_create(
            **{**MFA_OUT_CREATE_KWARGS, "name": "Outbound MFA", "description": "test"}
        )
        assert captured["body"]["name"] == "Outbound MFA"
        assert captured["body"]["description"] == "test"

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_create(**MFA_OUT_CREATE_KWARGS)
        assert captured["method"] == "POST"


class TestMFAOutboundGet:
    def test_get_returns_items(self):
        # mfa_outbound_policies_get returns ReactivePolicyResponse with .items
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_GET_RESPONSE))
        res = sdk.mfa_outbound.mfa_outbound_policies_get(id=MFA_POLICY_ID)
        assert res.items is not None

    def test_get_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, MFA_POLICY_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_get(id=MFA_POLICY_ID)
        assert MFA_POLICY_ID in captured["path"]

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.mfa_outbound.mfa_outbound_policies_get(id="ghost")


class TestMFAOutboundUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_update(id=MFA_POLICY_ID, **MFA_OUT_CREATE_KWARGS)
        assert captured["method"] == "PUT"

    def test_update_returns_item(self):
        # update returns ReactivePolicyItem with .item
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_RESPONSE))
        res = sdk.mfa_outbound.mfa_outbound_policies_update(
            id=MFA_POLICY_ID, **MFA_OUT_CREATE_KWARGS
        )
        assert res.item is not None


class TestMFAOutboundDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.mfa_outbound.mfa_outbound_policies_delete(id=MFA_POLICY_ID)
        assert captured["method"] == "DELETE"
        assert MFA_POLICY_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.mfa_outbound.mfa_outbound_policies_delete(id="ghost")
