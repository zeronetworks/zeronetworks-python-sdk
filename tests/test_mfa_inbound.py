"""Tests for the Inbound MFA Policies module.

ReactivePolicyState: 1=Enabled, 2=Disabled
RuleDuration: 1=Hour, 2=Day, 3=Week, 4=Month, 5=Never, 6=4h, 7=12h, 8=8h
MfaMethods: 1=SMS, 2=Email, 3=Duo, 4=Browser, 5=No MFA, 6=MicrosoftAuthenticator, 7=Okta
"""

import json
import httpx
import pytest
from zeronetworks import errors
from zeronetworks.models import (
    PortsList,
    ReactivePolicyInboundBodyDstEntityInfo,
    ReactivePolicyInboundBodySrcEntityInfo,
    ReactivePolicyInboundBodySrcUserInfo,
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

MFA_CREATE_KWARGS = dict(
    additional_ports_list=[],
    dst_entity_info=ReactivePolicyInboundBodyDstEntityInfo(id=ASSET_ID),
    dst_port="443",
    dst_process_names=["*"],
    fallback_to_logged_on_user=False,
    mfa_methods=[4],  # Browser
    override_builtins=False,
    protocol_type=6,
    rule_duration=5,  # Never
    src_entity_infos=[ReactivePolicyInboundBodySrcEntityInfo(id=ASSET_ID_2)],
    src_process_names=["*"],
    src_user_infos=[ReactivePolicyInboundBodySrcUserInfo(id="u:i:TestUser01")],
    state=1,  # Enabled
)


class TestMFAInboundCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_RESPONSE))
        res = sdk.mfa_inbound.mfa_inbound_policies_create(**MFA_CREATE_KWARGS)
        assert res.item is not None

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_create(**MFA_CREATE_KWARGS)
        assert captured["method"] == "POST"
        assert "reactive-policies" in captured["path"]
        assert "inbound" in captured["path"]
        body = captured["body"]
        assert body["dstPort"] == "443"
        assert body["protocolType"] == 6
        assert body["mfaMethods"] == [4]

    def test_create_with_description(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_create(
            **{**MFA_CREATE_KWARGS, "description": "My MFA policy"}
        )
        assert captured["body"]["description"] == "My MFA policy"

    def test_create_with_multiple_mfa_methods(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_create(
            **{**MFA_CREATE_KWARGS, "mfa_methods": [1, 2, 4]}  # SMS, Email, Browser
        )
        assert set(captured["body"]["mfaMethods"]) == {1, 2, 4}

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.mfa_inbound.mfa_inbound_policies_create(**MFA_CREATE_KWARGS)
        assert exc_info.value.status_code == 400

    def test_create_dst_entity_as_dict(self):
        """dst_entity_info can be passed as a plain dict."""
        kwargs = {**MFA_CREATE_KWARGS, "dst_entity_info": {"id": ASSET_ID}}
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_RESPONSE))
        res = sdk.mfa_inbound.mfa_inbound_policies_create(**kwargs)
        assert res.item is not None

    def test_create_rule_duration_serialized(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_create(
            **{**MFA_CREATE_KWARGS, "rule_duration": 1}  # Hour
        )
        assert captured["body"]["ruleDuration"] == 1


class TestMFAInboundGet:
    def test_get_returns_items(self):
        # mfa_inbound_policies_get returns ReactivePolicyResponse with .items
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_GET_RESPONSE))
        res = sdk.mfa_inbound.mfa_inbound_policies_get(id=MFA_POLICY_ID)
        assert res.items is not None

    def test_get_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, MFA_POLICY_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_get(id=MFA_POLICY_ID)
        assert MFA_POLICY_ID in captured["path"]

    def test_get_sends_get_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, MFA_POLICY_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_get(id=MFA_POLICY_ID)
        assert captured["method"] == "GET"

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.mfa_inbound.mfa_inbound_policies_get(id="ghost")
        assert exc_info.value.status_code == 404


class TestMFAInboundUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, MFA_POLICY_RESPONSE)

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_update(id=MFA_POLICY_ID, **MFA_CREATE_KWARGS)
        assert captured["method"] == "PUT"

    def test_update_returns_item(self):
        # update returns ReactivePolicyItem with .item
        sdk = client_with(lambda req: make_response(200, MFA_POLICY_RESPONSE))
        res = sdk.mfa_inbound.mfa_inbound_policies_update(id=MFA_POLICY_ID, **MFA_CREATE_KWARGS)
        assert res.item is not None


class TestMFAInboundDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.mfa_inbound.mfa_inbound_policies_delete(id=MFA_POLICY_ID)
        assert captured["method"] == "DELETE"
        assert MFA_POLICY_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.mfa_inbound.mfa_inbound_policies_delete(id="ghost")
