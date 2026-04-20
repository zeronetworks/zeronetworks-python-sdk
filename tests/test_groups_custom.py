"""Tests for the Custom Groups module."""

import json
import httpx
import pytest
from zeronetworks import errors
from zeronetworks.models import PortsList
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    GROUP_ID,
    CUSTOM_GROUP_RESPONSE,
    CUSTOM_GROUP_ENTITY,
    ERROR_BODY_400,
    ERROR_BODY_404,
)


class TestCustomGroupsCreate:
    def test_create_returns_entity(self):
        sdk = client_with(lambda req: make_response(200, CUSTOM_GROUP_RESPONSE))
        res = sdk.groups_custom.custom_groups_create(
            name="Test Group", description="A test group"
        )
        assert res.entity is not None
        assert res.entity.id == GROUP_ID

    def test_create_sends_post(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["body"] = json.loads(req.content)
            return make_response(200, CUSTOM_GROUP_RESPONSE)

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_create(
            name="My Group", description="Desc"
        )
        assert captured["method"] == "POST"
        assert captured["body"]["name"] == "My Group"
        assert captured["body"]["description"] == "Desc"

    def test_create_without_description(self):
        sdk = client_with(lambda req: make_response(200, CUSTOM_GROUP_RESPONSE))
        res = sdk.groups_custom.custom_groups_create(name="Minimal Group")
        assert res.entity is not None

    def test_create_with_members(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["body"] = json.loads(req.content)
            return make_response(200, CUSTOM_GROUP_RESPONSE)

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_create(
            name="Group With Members", members_id=[ASSET_ID]
        )
        assert ASSET_ID in captured["body"]["membersId"]

    def test_create_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.groups_custom.custom_groups_create(name="Bad")
        assert exc_info.value.status_code == 400


class TestCustomGroupsGet:
    def test_get_returns_entity(self):
        sdk = client_with(lambda req: make_response(200, CUSTOM_GROUP_RESPONSE))
        res = sdk.groups_custom.custom_groups_get(id=GROUP_ID)
        assert res.entity is not None
        assert res.entity.id == GROUP_ID

    def test_get_sends_get_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, CUSTOM_GROUP_RESPONSE)

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_get(id=GROUP_ID)
        assert captured["method"] == "GET"
        assert GROUP_ID in captured["path"]

    def test_get_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.groups_custom.custom_groups_get(id="nonexistent")
        assert exc_info.value.status_code == 404


class TestCustomGroupsUpdate:
    def test_update_returns_entity(self):
        sdk = client_with(lambda req: make_response(200, CUSTOM_GROUP_RESPONSE))
        res = sdk.groups_custom.custom_groups_update(
            id=GROUP_ID, name="Updated Name", description="Updated desc"
        )
        assert res.entity is not None

    def test_update_sends_put(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["body"] = json.loads(req.content)
            return make_response(200, CUSTOM_GROUP_RESPONSE)

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_update(
            id=GROUP_ID, name="New Name"
        )
        assert captured["method"] == "PUT"
        assert captured["body"]["name"] == "New Name"


class TestCustomGroupsDelete:
    def test_delete_succeeds(self):
        sdk = client_with(lambda req: make_response(200, {}))
        # Should not raise
        sdk.groups_custom.custom_groups_delete(id=GROUP_ID)

    def test_delete_sends_delete_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["path"] = req.url.path
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_delete(id=GROUP_ID)
        assert captured["method"] == "DELETE"
        assert GROUP_ID in captured["path"]

    def test_delete_404_raises_error(self):
        # custom_groups_delete only handles 400/401/403/500 as errors.Error;
        # 404 falls through to ZeronetworksDefaultError.
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.ZeronetworksError):
            sdk.groups_custom.custom_groups_delete(id="ghost-id")


class TestCustomGroupMembers:
    def test_members_list(self):
        response = {"membersId": [ASSET_ID]}
        sdk = client_with(lambda req: make_response(200, response))
        res = sdk.groups_custom.custom_group_members_list(id=GROUP_ID)
        assert res.members_id is not None

    def test_members_add_sends_put(self):
        # The SDK uses PUT (not POST) for adding members.
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            captured["body"] = json.loads(req.content)
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_members_add(id=GROUP_ID, members_id=[ASSET_ID])
        assert captured["method"] == "PUT"
        assert ASSET_ID in captured["body"]["membersId"]

    def test_members_delete_sends_delete(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, {})

        sdk = client_with(handler)
        sdk.groups_custom.custom_groups_members_delete(
            id=GROUP_ID, members_id=[ASSET_ID]
        )
        assert captured["method"] == "DELETE"
