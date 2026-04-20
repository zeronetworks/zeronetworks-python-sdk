"""Tests for the AE Exclusions module (inbound and outbound)."""

import json
import httpx
import pytest
from zeronetworks import errors
from zeronetworks.models import PortsList, RuleAction, RuleState
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    ASSET_ID_2,
    AE_EXCL_ID,
    AE_EXCLUSION_GET_RESPONSE,
    AE_EXCLUSION_CREATE_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
)

PORTS_LIST = [PortsList(protocol_type=6, ports="1234")]


class TestAEExclusionsInbound:
    def test_create_returns_rule(self):
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_CREATE_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert res.item is not None

    def test_create_sends_post_with_body(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            captured["body"] = json.loads(req.content)
            return make_response(200, AE_EXCLUSION_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            description="test exclusion",
        )
        assert captured["method"] == "POST"
        assert "inbound" in captured["path"]
        body = captured["body"]
        assert body["localEntityId"] == ASSET_ID
        assert body["localProcessesList"] == ["*"]
        assert body["remoteEntityIdsList"] == [ASSET_ID_2]
        assert body["description"] == "test exclusion"

    def test_create_ports_list_serialized(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, AE_EXCLUSION_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=[PortsList(protocol_type=6, ports="443")],
            remote_entity_ids_list=[ASSET_ID_2],
        )
        ports = captured["body"]["portsList"]
        assert len(ports) == 1
        assert ports[0]["protocolType"] == 6
        assert ports[0]["ports"] == "443"

    def test_create_ports_list_as_typed_dict(self):
        """Ports list can be passed as plain dicts (TypedDict style)."""
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_CREATE_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=[{"protocol_type": 6, "ports": "8080"}],
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert res.item is not None

    def test_get_returns_item(self):
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_GET_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_inbound_get(id=AE_EXCL_ID)
        assert res.item is not None

    def test_get_path_contains_id(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, AE_EXCLUSION_GET_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_get(id=AE_EXCL_ID)
        assert AE_EXCL_ID in captured["path"]

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.ae_exclusions.ae_exclusions_inbound_get(id="ghost")
        assert exc_info.value.status_code == 404

    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_delete(id=AE_EXCL_ID)
        assert captured["method"] == "DELETE"
        assert AE_EXCL_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.ae_exclusions.ae_exclusions_inbound_delete(id="ghost")

    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, AE_EXCLUSION_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_update(
            id=AE_EXCL_ID,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert captured["method"] == "PUT"

    def test_create_with_multiple_ports(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, AE_EXCLUSION_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_inbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=[
                PortsList(protocol_type=6, ports="80"),
                PortsList(protocol_type=6, ports="443"),
                PortsList(protocol_type=17, ports="53"),
            ],
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert len(captured["body"]["portsList"]) == 3


class TestAEExclusionsOutbound:
    def test_create_returns_rule(self):
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_CREATE_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_outbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert res.item is not None

    def test_create_hits_outbound_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, AE_EXCLUSION_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_outbound_create(
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert "outbound" in captured["path"]

    def test_get_returns_item(self):
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_GET_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_outbound_get(id=AE_EXCL_ID)
        assert res.item is not None

    def test_delete_outbound(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.ae_exclusions.ae_exclusions_outbound_delete(id=AE_EXCL_ID)
        assert captured["method"] == "DELETE"

    def test_update_outbound(self):
        sdk = client_with(lambda req: make_response(200, AE_EXCLUSION_CREATE_RESPONSE))
        res = sdk.ae_exclusions.ae_exclusions_outbound_update(
            id=AE_EXCL_ID,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
        )
        assert res.item is not None
