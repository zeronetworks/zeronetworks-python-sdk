"""Tests for the Inbound Rules module.

RuleAction: 1=Allow, 2=Block, 3=Force Block
RuleState:  1=Enabled, 2=Disabled
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
    ASSET_ID_2,
    RULE_ID,
    RULE_ITEM_RESPONSE,
    RULE_CREATE_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
)

PORTS_LIST = [PortsList(protocol_type=6, ports="443")]


class TestInboundRulesCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_CREATE_RESPONSE))
        res = sdk.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert res.item is not None

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            captured["body"] = json.loads(req.content)
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert captured["method"] == "POST"
        assert "inbound" in captured["path"]
        assert captured["body"]["localEntityId"] == ASSET_ID
        assert captured["body"]["remoteEntityIdsList"] == [ASSET_ID_2]

    def test_create_with_optional_fields(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["chrome.exe"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
            description="My inbound rule",
            name="Test Rule",
            change_ticket="TICKET-123",
        )
        assert captured["body"]["description"] == "My inbound rule"
        assert captured["body"]["name"] == "Test Rule"
        assert captured["body"]["changeTicket"] == "TICKET-123"

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.rules_inbound.inbound_rules_create(
                action=1,
                local_entity_id=ASSET_ID,
                local_processes_list=["*"],
                ports_list=PORTS_LIST,
                remote_entity_ids_list=[ASSET_ID_2],
                state=1,
            )
        assert exc_info.value.status_code == 400

    def test_create_block_action(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rules_create(
            action=2,  # Block
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert captured["body"]["action"] == 2

    def test_create_disabled_state(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=2,  # Disabled
        )
        assert captured["body"]["state"] == 2


class TestInboundRulesGet:
    def test_get_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_ITEM_RESPONSE))
        res = sdk.rules_inbound.inbound_rule_get(id=RULE_ID)
        assert res.item is not None

    def test_get_sends_get_with_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, RULE_ITEM_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rule_get(id=RULE_ID)
        assert captured["method"] == "GET"
        assert RULE_ID in captured["path"]

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.rules_inbound.inbound_rule_get(id="nonexistent")
        assert exc_info.value.status_code == 404


class TestInboundRulesUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rule_update(
            id=RULE_ID,
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert captured["method"] == "PUT"
        assert RULE_ID in captured["path"]

    def test_update_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_CREATE_RESPONSE))
        res = sdk.rules_inbound.inbound_rule_update(
            id=RULE_ID,
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert res.item is not None


class TestInboundRulesDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.rules_inbound.inbound_rule_delete(id=RULE_ID)
        assert captured["method"] == "DELETE"
        assert RULE_ID in captured["path"]

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.rules_inbound.inbound_rule_delete(id="ghost")
