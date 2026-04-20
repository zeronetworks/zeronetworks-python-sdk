"""Tests for the Outbound Rules module.

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


class TestOutboundRulesCreate:
    def test_create_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_CREATE_RESPONSE))
        res = sdk.rules_outbound.outbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert res.item is not None

    def test_create_hits_outbound_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_outbound.outbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert "outbound" in captured["path"]

    def test_create_with_expiry(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_outbound.outbound_rules_create(
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
            expires_at=9999999999000,
        )
        assert captured["body"]["expiresAt"] == 9999999999000

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.rules_outbound.outbound_rules_create(
                action=1,
                local_entity_id=ASSET_ID,
                local_processes_list=["*"],
                ports_list=PORTS_LIST,
                remote_entity_ids_list=[ASSET_ID_2],
                state=1,
            )
        assert exc_info.value.status_code == 400


class TestOutboundRulesGet:
    def test_get_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_ITEM_RESPONSE))
        res = sdk.rules_outbound.outbound_rule_get(id=RULE_ID)
        assert res.item is not None

    def test_get_id_in_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, RULE_ITEM_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_outbound.outbound_rule_get(id=RULE_ID)
        assert RULE_ID in captured["path"]

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.rules_outbound.outbound_rule_get(id="ghost")


class TestOutboundRulesUpdate:
    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, RULE_CREATE_RESPONSE)

        sdk = client_with(handler)
        sdk.rules_outbound.outbound_rule_update(
            id=RULE_ID,
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert captured["method"] == "PUT"

    def test_update_returns_item(self):
        sdk = client_with(lambda req: make_response(200, RULE_CREATE_RESPONSE))
        res = sdk.rules_outbound.outbound_rule_update(
            id=RULE_ID,
            action=1,
            local_entity_id=ASSET_ID,
            local_processes_list=["*"],
            ports_list=PORTS_LIST,
            remote_entity_ids_list=[ASSET_ID_2],
            state=1,
        )
        assert res.item is not None


class TestOutboundRulesDelete:
    def test_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.rules_outbound.outbound_rule_delete(id=RULE_ID)
        assert captured["method"] == "DELETE"

    def test_delete_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error):
            sdk.rules_outbound.outbound_rule_delete(id="ghost")
