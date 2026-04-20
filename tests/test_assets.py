"""Tests for the Assets module."""

import httpx
import pytest
from zeronetworks import errors
from tests.conftest import (
    client_with,
    make_response,
    ASSET_ID,
    ASSET_SEARCH_RESPONSE,
    ERROR_BODY_400,
    ERROR_BODY_404,
    ERROR_BODY_401,
)


class TestAssetsSearch:
    def test_search_returns_asset_id(self):
        sdk = client_with(lambda req: make_response(200, ASSET_SEARCH_RESPONSE))
        res = sdk.assets.assets_search(fqdn="host.example.local")
        assert res.asset_id == ASSET_ID

    def test_search_without_fqdn(self):
        sdk = client_with(lambda req: make_response(200, {"assetId": None}))
        res = sdk.assets.assets_search()
        assert res.asset_id is None

    def test_search_sends_fqdn_query_param(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["url"] = str(req.url)
            return make_response(200, ASSET_SEARCH_RESPONSE)

        sdk = client_with(handler)
        sdk.assets.assets_search(fqdn="rdc01.domain.local")
        assert "fqdn=rdc01.domain.local" in captured["url"]

    def test_search_uses_get_method(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["method"] = req.method
            return make_response(200, ASSET_SEARCH_RESPONSE)

        sdk = client_with(handler)
        sdk.assets.assets_search(fqdn="host")
        assert captured["method"] == "GET"

    def test_search_hits_correct_path(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["path"] = req.url.path
            return make_response(200, ASSET_SEARCH_RESPONSE)

        sdk = client_with(handler)
        sdk.assets.assets_search(fqdn="host")
        assert "/assets/searchId" in captured["path"]

    def test_search_400_raises_error(self):
        sdk = client_with(lambda req: make_response(400, ERROR_BODY_400))
        with pytest.raises(errors.Error) as exc_info:
            sdk.assets.assets_search(fqdn="bad-host")
        assert exc_info.value.status_code == 400

    def test_search_401_raises_error(self):
        sdk = client_with(lambda req: make_response(401, ERROR_BODY_401))
        with pytest.raises(errors.Error) as exc_info:
            sdk.assets.assets_search(fqdn="host")
        assert exc_info.value.status_code == 401

    def test_search_404_raises_error(self):
        sdk = client_with(lambda req: make_response(404, ERROR_BODY_404))
        with pytest.raises(errors.Error) as exc_info:
            sdk.assets.assets_search(fqdn="nonexistent.host")
        assert exc_info.value.status_code == 404

    def test_search_500_raises_error(self):
        sdk = client_with(
            lambda req: make_response(500, {"error": "Internal Server Error", "message": "oops"})
        )
        with pytest.raises(errors.Error) as exc_info:
            sdk.assets.assets_search(fqdn="host")
        assert exc_info.value.status_code == 500

    def test_search_per_request_server_url_override(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["host"] = req.url.host
            return make_response(200, ASSET_SEARCH_RESPONSE)

        sdk = client_with(handler)
        sdk.assets.assets_search(
            fqdn="host",
            server_url="https://custom-server.example.com/api",
        )
        assert captured["host"] == "custom-server.example.com"
