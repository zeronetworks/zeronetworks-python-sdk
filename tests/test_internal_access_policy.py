"""Tests for the Internal Access Policy module.

RuleState:    1=Enabled, 2=Disabled
RuleDuration: 1=Hour, 2=Day, 3=Week, 4=Month, 5=Never, 6=4h, 7=12h, 8=8h
"""

import json
import httpx
import pytest
from zeronetworks import errors
from zeronetworks.models import PortsList
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    IAP_ID,
    IAP_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
)

IAP_CREATE_KWARGS = dict(
    dst_asset_id=ASSET_ID,
    dst_ports_list=[PortsList(protocol_type=6, ports="22")],
    dst_process_names_list=["*"],
    name="Test IAP",
    rule_duration=5,  # Never
    src_user_ids_list=["u:i:TestUser01"],
)


class TestInternalAccessPolicyCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, IAP_RESPONSE))
        res = sdk.internal_access_policy.internal_access_policy_create(**IAP_CREATE_KWARGS)
        assert res.item is not None

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(**IAP_CREATE_KWARGS)
        assert captured["method"] == "POST"
        assert "internal" in captured["path"].lower()
        body = captured["body"]
        assert body["dstAssetId"] == ASSET_ID
        assert body["name"] == "Test IAP"

    def test_create_ports_list_serialized(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(**IAP_CREATE_KWARGS)
        ports = captured["body"]["dstPortsList"]
        assert len(ports) == 1
        assert ports[0]["protocolType"] == 6
        assert ports[0]["ports"] == "22"

    def test_create_with_optional_state(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(
            **{**IAP_CREATE_KWARGS, "state": 2}  # Disabled
        )
        assert captured["body"]["state"] == 2

    def test_create_with_description(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(
            **{**IAP_CREATE_KWARGS, "description": "My IAP"}
        )
        assert captured["body"]["description"] == "My IAP"

    def test_create_with_multiple_users(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(
            **{**IAP_CREATE_KWARGS, "src_user_ids_list": ["u:i:User01", "u:i:User02"]}
        )
        assert len(captured["body"]["srcUserIdsList"]) == 2

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.internal_access_policy.internal_access_policy_create(**IAP_CREATE_KWARGS)
        assert exc_info.value.status_code == 400

    def test_create_ports_as_typed_dict(self):
        sdk = client_with(lambda req: make_response(200, IAP_RESPONSE))
        res = sdk.internal_access_policy.internal_access_policy_create(
            **{**IAP_CREATE_KWARGS, "dst_ports_list": [{"protocol_type": 6, "ports": "22"}]}
        )
        assert res.item is not None

    def test_create_multiple_ports(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_create(
            **{
                **IAP_CREATE_KWARGS,
                "dst_ports_list": [
                    PortsList(protocol_type=6, ports="22"),
                    PortsList(protocol_type=6, ports="3389"),
                ],
            }
        )
        assert len(captured["body"]["dstPortsList"]) == 2


class TestInternalAccessPolicyGet:
    def test_get_returns_item(self):
        sdk = client_with(lambda req: make_response(200, IAP_RESPONSE))
        res = sdk.internal_access_policy.internal_access_policy_get(id=IAP_ID)
        assert res.item is not None

    def test_get_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_get(id=IAP_ID)
        assert IAP_ID in captured["path"]

    def test_get_sends_get_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_get(id=IAP_ID)
        assert captured["method"] == "GET"

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.internal_access_policy.internal_access_policy_get(id="ghost")
        assert exc_info.value.status_code == 404


class TestInternalAccessPolicyUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, IAP_RESPONSE)

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_update(id=IAP_ID, **IAP_CREATE_KWARGS)
        assert captured["method"] == "PUT"
        assert IAP_ID in captured["path"]

    def test_update_returns_item(self):
        sdk = client_with(lambda req: make_response(200, IAP_RESPONSE))
        res = sdk.internal_access_policy.internal_access_policy_update(
            id=IAP_ID, **IAP_CREATE_KWARGS
        )
        assert res.item is not None


class TestInternalAccessPolicyDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.internal_access_policy.internal_access_policy_delete(id=IAP_ID)
        assert captured["method"] == "DELETE"
        assert IAP_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.internal_access_policy.internal_access_policy_delete(id="ghost")
