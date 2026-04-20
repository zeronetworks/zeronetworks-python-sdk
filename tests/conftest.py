"""Shared fixtures and helpers for the Zero Networks SDK test suite.

Mode selection
--------------
By default all tests run against local mock transports (no network calls).
Set the following environment variables to run against a real API instead:

    ZERONETWORKS_API_KEY      – required for live mode
    ZERONETWORKS_SERVER_URL   – optional, defaults to the production portal URL
    ZERONETWORKS_LIVE=1       – opt-in flag; live tests are skipped unless set

Live tests also read asset / resource IDs from the environment so they can
target objects that already exist in your tenant:

    ZN_ASSET_FQDN_1           – FQDN of a first test asset (e.g. "rdc01.domain.local")
    ZN_ASSET_FQDN_2           – FQDN of a second test asset
    ZN_USER_ID                 – a valid user entity ID (e.g. "u:i:AbCd1234")
"""

import json
import os
import httpx
import pytest
from zeronetworks import Zeronetworks

# ---------------------------------------------------------------------------
# Environment-driven configuration
# ---------------------------------------------------------------------------

LIVE = os.getenv("ZERONETWORKS_LIVE", "0").strip() in ("1", "true", "yes")
API_KEY = os.getenv("ZERONETWORKS_API_KEY", "")
SERVER_URL = os.getenv("ZERONETWORKS_SERVER_URL", "")  # empty → SDK default

# Asset / user IDs used by live integration tests
LIVE_FQDN_1 = os.getenv("ZN_ASSET_FQDN_1", "")
LIVE_FQDN_2 = os.getenv("ZN_ASSET_FQDN_2", "")
LIVE_USER_ID = os.getenv("ZN_USER_ID", "u:a:anyUser")  # "any user" group works for most rules

# ---------------------------------------------------------------------------
# pytest markers
# ---------------------------------------------------------------------------

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: mark test as requiring a real Zero Networks API (skipped by default)",
    )


def pytest_collection_modifyitems(config, items):
    if LIVE:
        return  # run everything
    skip_live = pytest.mark.skip(reason="live API tests disabled – set ZERONETWORKS_LIVE=1")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

class MockTransport(httpx.BaseTransport):
    """Intercepts HTTP requests and returns a pre-configured response."""

    def __init__(self, handler):
        self._handler = handler

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self._handler(request)


def make_response(status_code: int, body: dict | str | None = None) -> httpx.Response:
    """Build an httpx.Response with JSON or empty body."""
    if body is None:
        content = b""
        headers = {"content-type": "application/json"}
    elif isinstance(body, str):
        content = body.encode()
        headers = {"content-type": "application/json"}
    else:
        content = json.dumps(body).encode()
        headers = {"content-type": "application/json"}
    return httpx.Response(status_code, content=content, headers=headers)


def client_with(handler) -> Zeronetworks:
    """Create a Zeronetworks SDK client whose HTTP calls are handled by *handler*."""
    transport = MockTransport(handler)
    http_client = httpx.Client(transport=transport)
    return Zeronetworks(api_key="test-api-key", client=http_client)


# ---------------------------------------------------------------------------
# Live client fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def live_client() -> Zeronetworks:
    """A real Zeronetworks client for integration tests.

    Requires ZERONETWORKS_API_KEY to be set. Optionally reads
    ZERONETWORKS_SERVER_URL to target a non-production environment.
    """
    if not API_KEY:
        pytest.skip("ZERONETWORKS_API_KEY not set – skipping live test")
    kwargs = {"api_key": API_KEY}
    if SERVER_URL:
        kwargs["server_url"] = SERVER_URL
    return Zeronetworks(**kwargs)


@pytest.fixture(scope="session")
def live_asset_ids(live_client) -> tuple[str, str]:
    """Resolve the two test asset FQDNs to asset IDs via the real API.

    Falls back to the FQDN strings themselves if the env vars are not set,
    which will cause tests that need valid IDs to fail descriptively.
    """
    if not LIVE_FQDN_1 or not LIVE_FQDN_2:
        pytest.skip(
            "ZN_ASSET_FQDN_1 and ZN_ASSET_FQDN_2 must be set for live asset tests"
        )
    res1 = live_client.assets.assets_search(fqdn=LIVE_FQDN_1)
    res2 = live_client.assets.assets_search(fqdn=LIVE_FQDN_2)
    assert res1.asset_id, f"No asset found for FQDN {LIVE_FQDN_1!r}"
    assert res2.asset_id, f"No asset found for FQDN {LIVE_FQDN_2!r}"
    return res1.asset_id, res2.asset_id


# ---------------------------------------------------------------------------
# Canned JSON payloads reused across mock tests
# ---------------------------------------------------------------------------

ASSET_ID = "a:a:AbCdEf12"
ASSET_ID_2 = "a:a:GhIjKl34"
RULE_ID = "r:i:TestRule1"
GROUP_ID = "g:c:TestGrp1"
MFA_POLICY_ID = "mfa:i:TestPol1"
IAP_ID = "p:i:TestIap01"
AE_EXCL_ID = "e:i:TestExcl1"
RPC_RULE_ID = "rpc:i:TestRpc1"

ASSET_SEARCH_RESPONSE = {"assetId": ASSET_ID}

CUSTOM_GROUP_ENTITY = {
    "id": GROUP_ID,
    "name": "Test Group",
    "description": "A test group",
    "guid": "00000000-0000-0000-0000-000000000001",
    "createdAt": 0,
    "directMembersCount": 0,
    "domain": "example.local",
    "hasProtectionPolicy": False,
    "principalName": "Test Group",
    "role": 0,
    "sid": "S-1-5-21-0",
}
CUSTOM_GROUP_RESPONSE = {"entity": CUSTOM_GROUP_ENTITY}

RULE_ITEM = {
    "id": RULE_ID,
    "action": 1,
    "state": 1,
    "localEntityId": ASSET_ID,
    "localProcessesList": ["*"],
    "portsList": [{"protocolType": 6, "ports": "443"}],
    "remoteEntityIdsList": [ASSET_ID_2],
}
RULE_ITEM_RESPONSE = {"item": RULE_ITEM}
RULE_CREATE_RESPONSE = {"item": RULE_ITEM}

AE_EXCLUSION_ITEM = {
    "id": AE_EXCL_ID,
    "localEntityId": ASSET_ID,
    "localProcessesList": ["*"],
    "portsList": [{"protocolType": 6, "ports": "1234"}],
    "remoteEntityIdsList": [ASSET_ID_2],
    "state": 1,
}
AE_EXCLUSION_GET_RESPONSE = {"item": AE_EXCLUSION_ITEM}
AE_EXCLUSION_CREATE_RESPONSE = {"item": AE_EXCLUSION_ITEM}

MFA_POLICY_ITEM = {
    "id": MFA_POLICY_ID,
    "dstPort": "443",
    "protocolType": 6,
    "state": 1,
    "ruleDuration": 5,
    "mfaMethods": [4],
    "overrideBuiltins": False,
    "fallbackToLoggedOnUser": False,
    "dstEntityInfo": {"id": ASSET_ID},
    "srcEntityInfos": [{"id": ASSET_ID_2}],
    "srcUserInfos": [{"id": "u:i:TestUser01"}],
    "srcProcessNames": ["*"],
    "dstProcessNames": ["*"],
    "additionalPortsList": [],
}
MFA_POLICY_RESPONSE = {"item": MFA_POLICY_ITEM}   # create/update → ReactivePolicyItem
MFA_POLICY_GET_RESPONSE = {"items": MFA_POLICY_ITEM}  # get → ReactivePolicyResponse

IAP_ITEM = {
    "id": IAP_ID,
    "name": "Test IAP",
    "dstAssetId": ASSET_ID,
    "dstPortsList": [{"protocolType": 6, "ports": "22"}],
    "dstProcessNamesList": ["*"],
    "srcUserIdsList": ["u:i:TestUser01"],
    "ruleDuration": 5,
    "state": 1,
}
IAP_RESPONSE = {"item": IAP_ITEM}

RPC_RULE_ITEM = {
    "id": RPC_RULE_ID,
    "action": 1,
    "description": "Test RPC rule",
    "state": 1,
    "localAssetId": ASSET_ID,
    "remoteAssetIdsList": [ASSET_ID_2],
    "excludedAssetIdsList": [],
    "interfaceUuidsList": ["rpcAnyInterface"],
    "opNumbersList": [0],
    "protocolsList": [2],
    "userIdsList": ["u:i:TestUser01"],
}
RPC_RULE_RESPONSE = {"item": RPC_RULE_ITEM}
RPC_RULE_GET_RESPONSE = RPC_RULE_ITEM  # rpc_rule_get returns the body directly

ERROR_BODY_400 = {"error": "Bad Request", "message": "Invalid parameters"}
ERROR_BODY_404 = {"error": "Not Found", "message": "Resource not found"}
ERROR_BODY_401 = {"error": "Unauthorized", "message": "Missing or invalid API key"}


@pytest.fixture
def zn_client():
    """Return a Zeronetworks client that always returns 200 for any request.
    Individual tests should call client_with() with their own handler instead."""
    return client_with(lambda req: make_response(200, ASSET_SEARCH_RESPONSE))
