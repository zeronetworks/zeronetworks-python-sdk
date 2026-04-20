"""Tests for SDK instantiation and configuration."""

import httpx
import pytest
from zeronetworks import Zeronetworks
from tests.conftest import MockTransport, make_response, ASSET_SEARCH_RESPONSE


class TestSDKInit:
    def test_init_with_api_key(self):
        sdk = Zeronetworks(api_key="my-key")
        assert sdk is not None
        sdk.sdk_configuration.client.close()

    def test_init_with_callable_api_key(self):
        sdk = Zeronetworks(api_key=lambda: "dynamic-key")
        assert sdk is not None
        sdk.sdk_configuration.client.close()

    def test_init_with_custom_server_url(self):
        sdk = Zeronetworks(
            api_key="key",
            server_url="https://custom.example.com/api",
        )
        assert sdk is not None
        sdk.sdk_configuration.client.close()

    def test_init_with_custom_http_client(self):
        transport = MockTransport(lambda req: make_response(200, ASSET_SEARCH_RESPONSE))
        http = httpx.Client(transport=transport)
        sdk = Zeronetworks(api_key="key", client=http)
        res = sdk.assets.assets_search(fqdn="host.example.local")
        assert res.asset_id is not None

    def test_context_manager_sync(self):
        transport = MockTransport(lambda req: make_response(200, ASSET_SEARCH_RESPONSE))
        http = httpx.Client(transport=transport)
        with Zeronetworks(api_key="key", client=http) as sdk:
            res = sdk.assets.assets_search(fqdn="host.example.local")
            assert res.asset_id is not None

    def test_sub_sdk_lazy_load(self):
        sdk = Zeronetworks(api_key="key")
        assert sdk.assets is not None
        assert sdk.groups_custom is not None
        assert sdk.ae_exclusions is not None
        assert sdk.rules_inbound is not None
        assert sdk.rules_outbound is not None
        assert sdk.rules_rpc is not None
        assert sdk.mfa_inbound is not None
        assert sdk.mfa_outbound is not None
        assert sdk.internal_access_policy is not None
        sdk.sdk_configuration.client.close()

    def test_authorization_header_sent(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["auth"] = req.headers.get("Authorization")
            return make_response(200, ASSET_SEARCH_RESPONSE)

        transport = MockTransport(handler)
        http = httpx.Client(transport=transport)
        sdk = Zeronetworks(api_key="test-secret", client=http)
        sdk.assets.assets_search(fqdn="host.example.local")
        assert captured.get("auth") is not None
        assert "test-secret" in captured["auth"]

    def test_custom_http_headers_sent(self):
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["x-custom"] = req.headers.get("x-custom-header")
            return make_response(200, ASSET_SEARCH_RESPONSE)

        transport = MockTransport(handler)
        http = httpx.Client(transport=transport)
        sdk = Zeronetworks(api_key="key", client=http)
        sdk.assets.assets_search(
            fqdn="host.example.local",
            http_headers={"x-custom-header": "hello"},
        )
        assert captured.get("x-custom") == "hello"
