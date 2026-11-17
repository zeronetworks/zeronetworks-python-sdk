# Testing the Zero Networks Python SDK

## Overview

The test suite has two modes that can be used independently or together:

| Mode | What runs | Network calls | Speed |
|---|---|---|---|
| **Mock** (default) | `test_*.py` (except `test_live.py`) | None — HTTP is intercepted | Fast (~2 s) |
| **Live** | `test_live.py` | Real Zero Networks API | Slow, requires credentials |

---

## Running tests

### Prerequisites

```bash
pip install pytest pytest-asyncio
pip install -e .          # install the SDK itself
```

### Mock tests (default)

```bash
python -m pytest tests/ -v
```

This runs all 147 mock tests against local mock transports. No API key or network
access is required.

To run a single module:

```bash
python -m pytest tests/test_assets.py -v
python -m pytest tests/test_rules_inbound.py -v
```

To run a specific test:

```bash
python -m pytest tests/test_ae_exclusions.py::TestAEExclusionsInbound::test_create_ports_list_serialized -v
```

### Live integration tests

Live tests call the real API and create/delete actual resources in your tenant.
Each test cleans up after itself even on failure.

**Required environment variables:**

| Variable | Description |
|---|---|
| `ZERONETWORKS_LIVE=1` | Enables live tests (they are skipped otherwise) |
| `ZERONETWORKS_API_KEY` | Your API key |

**Optional environment variables:**

| Variable | Description | Default |
|---|---|---|
| `ZERONETWORKS_SERVER_URL` | Override the API base URL | Production portal |
| `ZN_ASSET_FQDN_1` | FQDN of a first test asset | *(required for most live tests)* |
| `ZN_ASSET_FQDN_2` | FQDN of a second test asset | *(required for most live tests)* |
| `ZN_USER_ID` | Entity ID of a user for policy tests | `u:a:anyUser` |
| `ZN_MFA_OUTBOUND_DST_ID` | Destination entity ID valid for outbound MFA policies | *(outbound MFA test skips if the asset is rejected)* |

**Example — target a dev environment:**

```bash
export ZERONETWORKS_LIVE=1
export ZERONETWORKS_API_KEY="your-api-key-here"
export ZERONETWORKS_SERVER_URL="https://portal-dev.zeronetworks.com/api/v1"
export ZN_ASSET_FQDN_1="rdc01.domain.local"
export ZN_ASSET_FQDN_2="ts01.domain.local"
export ZN_USER_ID="u:i:AbCd1234"

python -m pytest tests/test_live.py -v
```

**Run both mock and live together:**

```bash
python -m pytest tests/ -v
```

---

## Architecture

### Mock tests

The mock tests (`test_assets.py`, `test_groups_custom.py`, etc.) test
SDK behaviour without making any network calls. They work by replacing the
underlying `httpx` transport with a `MockTransport` that intercepts every
request and returns a pre-configured `httpx.Response`.

```
Test code
  └── client_with(handler)           # builds a Zeronetworks client
        └── httpx.Client(transport=MockTransport(handler))
              └── handler(request)   # your lambda / function
                    └── make_response(200, {...})
```

The handler receives the raw `httpx.Request` so tests can inspect the HTTP
method, URL path, query parameters, and request body — verifying the SDK
serialises correctly without ever touching the network.

**Key helpers in `conftest.py`:**

| Helper | Purpose |
|---|---|
| `client_with(handler)` | Build a mock-transport client from any callable |
| `make_response(status, body)` | Build an `httpx.Response` from a dict |
| `MockTransport` | `httpx.BaseTransport` that delegates to a handler |

### Live tests (`test_live.py`)

Live tests use a real `Zeronetworks` client instantiated from environment
variables. They are collected by pytest but skipped unless `ZERONETWORKS_LIVE=1`
is set.

Every test that mutates state uses a pytest fixture with `yield` to guarantee
cleanup:

```python
@pytest.fixture
def live_custom_group(live_client):
    res = live_client.groups_custom.custom_groups_create(name="[pytest] Temp")
    yield res                                          # test runs here
    live_client.groups_custom.custom_groups_delete(id=res.entity.id)
```

All resources created by live tests are named with the `[pytest]` prefix so
they are easy to identify and manually clean up if a test run is interrupted.
Resources are created **disabled** (`state=2`) wherever the API allows it.

#### 1.1.0 coverage

The bottom of `test_live.py` covers features added with spec 1.26.9:

| Class | What it checks |
|---|---|
| `TestLiveStaleConflict` | `zn_expected_updated_at` with a current value succeeds; with a stale value, update/delete raise `errors.StaleConflictError` (409) and leave the object untouched (inbound rules, internal access policy) |
| `TestLiveRuleFields` | `rule_category` round-trips; `src_user_infos` is populated (regression for the 1.0.x `srcUsersInfos` field name) |
| `TestLiveCustomGroupEntity` | `custom_groups_get` returns `GroupEntity` / `Group` |
| `TestLiveMFAPolicies` | Inbound and outbound MFA policy create → get → delete |
| `TestLiveRPCRules` | RPC rule create → get → delete |

Run just these:

```bash
python -m pytest tests/test_live.py -v -k "StaleConflict or RuleFields or CustomGroupEntity or MFAPolicies or RPCRules"
```

`TestLiveRuleFields::test_src_user_infos_populated` and the MFA tests use
`ZN_USER_ID`; set it to a real user ID in your tenant for meaningful results.
An exported-but-empty `ZN_USER_ID` falls back to `u:a:anyUser`.

---

## File structure

```
tests/
├── TESTING.md                      ← this file
├── __init__.py
├── conftest.py                     ← shared fixtures, mock helpers, live config
├── test_sdk_init.py                ← SDK instantiation & configuration
├── test_assets.py                  ← Assets module
├── test_groups_custom.py           ← Custom Groups module
├── test_ae_exclusions.py           ← AE Exclusions (inbound + outbound)
├── test_rules_inbound.py           ← Inbound Rules module
├── test_rules_outbound.py          ← Outbound Rules module
├── test_rules_rpc.py               ← RPC Rules module
├── test_mfa_inbound.py             ← Inbound MFA Policies module
├── test_mfa_outbound.py            ← Outbound MFA Policies module
├── test_internal_access_policy.py  ← Internal Access Policy module
├── test_v1_1_features.py           ← 1.1.0 features (stale-conflict 409, new fields)
└── test_live.py                    ← Live integration tests (skipped by default)
```

---

## What the mock tests verify

Each SDK module's tests cover:

- **Correct HTTP method** — GET / POST / PUT / DELETE is sent as expected
- **Correct URL path** — resource IDs appear in the path, endpoints are routed correctly
- **Request body serialisation** — Python field names map to the correct JSON keys
  (e.g. `protocol_type` → `protocolType`, `local_entity_id` → `localEntityId`)
- **Response deserialisation** — SDK model objects are populated from JSON
- **Error handling** — 400/401/403/404/500 responses raise `errors.Error`;
  other 4XX responses raise `errors.ZeronetworksDefaultError`
- **Optional fields** — optional parameters are omitted when not provided;
  present when supplied
- **Per-request overrides** — `server_url` and `http_headers` overrides work
- **Optimistic concurrency** — `zn_expected_updated_at` is sent as the
  `zn-expected-updated-at` header, and a 409 raises `errors.StaleConflictError`
  with `updated_at` / `updated_by` / `is_deleted` populated

### SDK type notes

The SDK types (`RuleAction`, `RuleState`, `RuleDuration`, etc.) are
`typing.Literal` integer unions — **not** Python enums. Use integer literals
directly:

| Concept | Values |
|---|---|
| `RuleAction` | `1`=Allow, `2`=Block, `3`=Force Block |
| `RuleState` | `1`=Enabled, `2`=Disabled |
| `RuleDuration` | `1`=Hour, `2`=Day, `3`=Week, `4`=Month, `5`=Never, `6`=4h, `7`=12h, `8`=8h |
| `ReactivePolicyState` | `1`=Enabled, `2`=Disabled |
| `MfaMethods` | `1`=SMS, `2`=Email, `3`=Duo, `4`=Browser, `5`=No MFA, `6`=MicrosoftAuthenticator, `7`=Okta |
| `Protocol` (port list) | `6`=TCP, `17`=UDP, `256`=Any |

### Response object shapes

Some response types differ between operations on the same resource:

| Operation | Module | Return type | Access |
|---|---|---|---|
| MFA create/update | inbound & outbound | `ReactivePolicyItem` | `.item` |
| MFA get | inbound & outbound | `ReactivePolicyResponse` | `.items` |
| All other create/get/update | all modules | various `*Item` / `*Response` | `.item` |

---

## Adding new tests

### Mock test

1. Add a test class to the relevant `test_<module>.py`.
2. Use `client_with(handler)` to create a mock client.
3. Capture what you need from the request, return a suitable response.

```python
def test_my_new_behaviour(self):
    captured = {}

    def handler(req: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(req.content)
        return make_response(200, MY_FIXTURE_RESPONSE)

    sdk = client_with(handler)
    res = sdk.some_module.some_method(param="value")
    assert captured["body"]["someField"] == "value"
    assert res.item is not None
```

### Live test

1. Add a test class (or method) to `test_live.py`.
2. Decorate with `@pytest.mark.live` (or rely on the module-level `pytestmark`).
3. Use the `live_client` fixture. If you create resources, use a `yield` fixture
   to ensure cleanup.

```python
class TestLiveMyNewFeature:
    def test_something(self, live_client, live_asset_ids):
        asset_id, _ = live_asset_ids
        res = live_client.some_module.some_method(asset_id=asset_id)
        assert res.item is not None
```
