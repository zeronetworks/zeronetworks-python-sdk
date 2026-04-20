"""Tests for the RPC Rules module.

RuleAction: 1=Allow, 2=Block, 3=Force Block
RuleState:  1=Enabled, 2=Disabled
protocols_list: 1=RPC over SMB, 2=RPC over TCP
"""

import json
import httpx
import pytest
from zeronetworks import errors
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    ASSET_ID_2,
    RPC_RULE_ID,
    RPC_RULE_RESPONSE,
    RPC_RULE_GET_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
)

RPC_CREATE_KWARGS = dict(
    action=1,  # Allow
    description="Test RPC rule",
    excluded_asset_ids_list=[],
    interface_uuids_list=["rpcAnyInterface"],
    local_asset_id=ASSET_ID,
    op_numbers_list=[0],
    protocols_list=[2],  # RPC over TCP
    remote_asset_ids_list=[ASSET_ID_2],
    state=1,  # Enabled
    user_ids_list=["u:i:TestUser01"],
)


class TestRPCRulesCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RPC_RULE_RESPONSE))
        res = sdk.rules_rpc.rpc_rules_create(**RPC_CREATE_KWARGS)
        assert res.item is not None

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            captured["body"] = json.loads(req.content)
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rules_create(**RPC_CREATE_KWARGS)
        assert captured["method"] == "POST"
        assert "rpc" in captured["path"]
        body = captured["body"]
        assert body["localAssetId"] == ASSET_ID
        assert body["description"] == "Test RPC rule"
        assert body["interfaceUuidsList"] == ["rpcAnyInterface"]

    def test_create_with_expiry(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rules_create(**{**RPC_CREATE_KWARGS, "expires_at": 9999000000000})
        assert captured["body"]["expiresAt"] == 9999000000000

    def test_create_with_name(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rules_create(**{**RPC_CREATE_KWARGS, "name": "Named RPC Rule"})
        assert captured["body"]["name"] == "Named RPC Rule"

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.rules_rpc.rpc_rules_create(**RPC_CREATE_KWARGS)
        assert exc_info.value.status_code == 400

    def test_create_protocols_list_serialized(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rules_create(**{**RPC_CREATE_KWARGS, "protocols_list": [1, 2]})
        assert captured["body"]["protocolsList"] == [1, 2]

    def test_create_block_action(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rules_create(**{**RPC_CREATE_KWARGS, "action": 2})  # Block
        assert captured["body"]["action"] == 2


class TestRPCRulesGet:
    def test_get_returns_body(self):
        sdk = client_with(lambda req: make_response(200, RPC_RULE_GET_RESPONSE))
        res = sdk.rules_rpc.rpc_rule_get(id=RPC_RULE_ID)
        assert res is not None

    def test_get_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, RPC_RULE_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rule_get(id=RPC_RULE_ID)
        assert RPC_RULE_ID in captured["path"]

    def test_get_sends_get_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, RPC_RULE_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rule_get(id=RPC_RULE_ID)
        assert captured["method"] == "GET"

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.rules_rpc.rpc_rule_get(id="ghost")


class TestRPCRulesUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, RPC_RULE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rule_update(id=RPC_RULE_ID, **RPC_CREATE_KWARGS)
        assert captured["method"] == "PUT"
        assert RPC_RULE_ID in captured["path"]

    def test_update_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RPC_RULE_RESPONSE))
        res = sdk.rules_rpc.rpc_rule_update(id=RPC_RULE_ID, **RPC_CREATE_KWARGS)
        assert res.item is not None


class TestRPCRulesDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.rules_rpc.rpc_rule_delete(id=RPC_RULE_ID)
        assert captured["method"] == "DELETE"
        assert RPC_RULE_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.rules_rpc.rpc_rule_delete(id="ghost")
