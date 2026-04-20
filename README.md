# zeronetworks

Developer-friendly & type-safe Python SDK specifically catered to leverage *zeronetworks* API.

[![Built by Speakeasy](https://img.shields.io/badge/Built_by-SPEAKEASY-374151?style=for-the-badge&labelColor=f3f4f6)](https://www.speakeasy.com/?utm_source=zeronetworks&utm_campaign=python)
[![License: MIT](https://img.shields.io/badge/LICENSE_//_MIT-3b5bdb?style=for-the-badge&labelColor=eff6ff)](https://opensource.org/licenses/MIT)


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/zeronetworks/zeronetworks). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

Zero Networks: APIs for Zero Networks
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [zeronetworks](#zeronetworks)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!TIP]
> To finish publishing your SDK to PyPI you must [run your first generation action](https://www.speakeasy.com/docs/github-setup#step-by-step-guide).


> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with *uv*, *pip*, or *poetry* package managers.

### uv

*uv* is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add git+<UNSET>.git
```

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from zeronetworks python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "zeronetworks",
# ]
# ///

from zeronetworks import Zeronetworks

sdk = Zeronetworks(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
import os
from zeronetworks import Zeronetworks

async def main():

    async with Zeronetworks(
        api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
    ) as z_client:

        res = await z_client.assets.assets_search_async(fqdn="server.domain.local")

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type   | Scheme  | Environment Variable   |
| --------- | ------ | ------- | ---------------------- |
| `api_key` | apiKey | API key | `ZERONETWORKS_API_KEY` |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [AEExclusions](docs/sdks/aeexclusions/README.md)

* [ae_exclusions_inbound_create](docs/sdks/aeexclusions/README.md#ae_exclusions_inbound_create) - Create AE Exclusion Inbound
* [ae_exclusions_inbound_get](docs/sdks/aeexclusions/README.md#ae_exclusions_inbound_get) - Get AE Exclusion
* [ae_exclusions_inbound_delete](docs/sdks/aeexclusions/README.md#ae_exclusions_inbound_delete) - Delete Automation Engine Inbound exclusions
* [ae_exclusions_inbound_update](docs/sdks/aeexclusions/README.md#ae_exclusions_inbound_update) - Update AE Exclusion
* [ae_exclusions_outbound_create](docs/sdks/aeexclusions/README.md#ae_exclusions_outbound_create) - Create AE Exclusion Outbound
* [ae_exclusions_outbound_get](docs/sdks/aeexclusions/README.md#ae_exclusions_outbound_get) - Get AE Exclusion
* [ae_exclusions_outbound_delete](docs/sdks/aeexclusions/README.md#ae_exclusions_outbound_delete) - Delete Automation Engine Outbound exclusions
* [ae_exclusions_outbound_update](docs/sdks/aeexclusions/README.md#ae_exclusions_outbound_update) - Update AE Exclusion

### [Assets](docs/sdks/assets/README.md)

* [assets_search](docs/sdks/assets/README.md#assets_search) - Search Asset by FQDN

### [GroupsCustom](docs/sdks/groupscustom/README.md)

* [custom_groups_create](docs/sdks/groupscustom/README.md#custom_groups_create) - Create Custom Group
* [custom_groups_get](docs/sdks/groupscustom/README.md#custom_groups_get) - Get a custom group
* [custom_groups_update](docs/sdks/groupscustom/README.md#custom_groups_update) - Update Custom Group
* [custom_groups_delete](docs/sdks/groupscustom/README.md#custom_groups_delete) - Delete Custom Group
* [custom_group_members_list](docs/sdks/groupscustom/README.md#custom_group_members_list) - List Custom Group members
* [custom_groups_members_add](docs/sdks/groupscustom/README.md#custom_groups_members_add) - Add Custom Group members
* [custom_groups_members_delete](docs/sdks/groupscustom/README.md#custom_groups_members_delete) - Delete Custom Group members

### [InternalAccessPolicy](docs/sdks/internalaccesspolicysdk/README.md)

* [internal_access_policy_create](docs/sdks/internalaccesspolicysdk/README.md#internal_access_policy_create) - Create an internal access policy
* [internal_access_policy_get](docs/sdks/internalaccesspolicysdk/README.md#internal_access_policy_get) - Get an Internal Access policy
* [internal_access_policy_update](docs/sdks/internalaccesspolicysdk/README.md#internal_access_policy_update) - Update an Internal Access policy
* [internal_access_policy_delete](docs/sdks/internalaccesspolicysdk/README.md#internal_access_policy_delete) - Delete an Internal Access policy

### [MFAInbound](docs/sdks/mfainbound/README.md)

* [mfa_inbound_policies_create](docs/sdks/mfainbound/README.md#mfa_inbound_policies_create) - Add Inbound MFA Policy
* [mfa_inbound_policies_get](docs/sdks/mfainbound/README.md#mfa_inbound_policies_get) - Get Inbound MFA Policy
* [mfa_inbound_policies_update](docs/sdks/mfainbound/README.md#mfa_inbound_policies_update) - Update Inbound MFA Policy
* [mfa_inbound_policies_delete](docs/sdks/mfainbound/README.md#mfa_inbound_policies_delete) - Remove Inbound MFA Policy

### [MFAOutbound](docs/sdks/mfaoutbound/README.md)

* [mfa_outbound_policies_create](docs/sdks/mfaoutbound/README.md#mfa_outbound_policies_create) - Add Outbound MFA Policy
* [mfa_outbound_policies_get](docs/sdks/mfaoutbound/README.md#mfa_outbound_policies_get) - Get Outbound MFA Policy
* [mfa_outbound_policies_update](docs/sdks/mfaoutbound/README.md#mfa_outbound_policies_update) - Update Outbound MFA Policy
* [mfa_outbound_policies_delete](docs/sdks/mfaoutbound/README.md#mfa_outbound_policies_delete) - Remove Outbound MFA Policy

### [RulesInbound](docs/sdks/rulesinbound/README.md)

* [inbound_rules_create](docs/sdks/rulesinbound/README.md#inbound_rules_create) - Create Inbound Rule
* [inbound_rule_get](docs/sdks/rulesinbound/README.md#inbound_rule_get) - Get Inbound Rule
* [inbound_rule_update](docs/sdks/rulesinbound/README.md#inbound_rule_update) - Update Inbound Rule
* [inbound_rule_delete](docs/sdks/rulesinbound/README.md#inbound_rule_delete) - Remove Inbound Rule

### [RulesOutbound](docs/sdks/rulesoutbound/README.md)

* [outbound_rules_create](docs/sdks/rulesoutbound/README.md#outbound_rules_create) - Create Outbound Rule
* [outbound_rule_get](docs/sdks/rulesoutbound/README.md#outbound_rule_get) - Get Outbound Rule
* [outbound_rule_update](docs/sdks/rulesoutbound/README.md#outbound_rule_update) - Update Outbound Rule
* [outbound_rule_delete](docs/sdks/rulesoutbound/README.md#outbound_rule_delete) - Remove Outbound Rule

### [RulesRPC](docs/sdks/rulesrpc/README.md)

* [rpc_rules_create](docs/sdks/rulesrpc/README.md#rpc_rules_create) - Create RPC Rule
* [rpc_rule_get](docs/sdks/rulesrpc/README.md#rpc_rule_get) - Get RPC Rule
* [rpc_rule_update](docs/sdks/rulesrpc/README.md#rpc_rule_update) - Update RPC Rule
* [rpc_rule_delete](docs/sdks/rulesrpc/README.md#rpc_rule_delete) - Remove RPC Rule

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import os
from zeronetworks import Zeronetworks
from zeronetworks.utils import BackoffStrategy, RetryConfig


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local",
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import os
from zeronetworks import Zeronetworks
from zeronetworks.utils import BackoffStrategy, RetryConfig


with Zeronetworks(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`ZeronetworksError`](./src/zeronetworks/errors/zeronetworkserror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
import os
from zeronetworks import Zeronetworks, errors


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:
    res = None
    try:

        res = z_client.assets.assets_search(fqdn="server.domain.local")

        # Handle response
        print(res)


    except errors.ZeronetworksError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.Error):
            print(e.data.error)  # Optional[str]
            print(e.data.message)  # Optional[str]
```

### Error Classes
**Primary errors:**
* [`ZeronetworksError`](./src/zeronetworks/errors/zeronetworkserror.py): The base class for HTTP error responses.
  * [`Error`](./src/zeronetworks/errors/error.py): Bad Request.

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`ZeronetworksError`](./src/zeronetworks/errors/zeronetworkserror.py)**:
* [`ResponseValidationError`](./src/zeronetworks/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Server Variables

The default server `https://portal.zeronetworks.com/v1/api` contains variables and is set to `https://portal.zeronetworks.com/v1/api` by default. To override default values, the following parameters are available when initializing the SDK client instance:

| Variable      | Parameter           | Default    | Description                          |
| ------------- | ------------------- | ---------- | ------------------------------------ |
| `CustomerURL` | `customer_url: str` | `"portal"` | this value is per customer / partner |

#### Example

```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    server_idx=0,
    customer_url="portal",
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)

```

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    server_url="https://portal.zeronetworks.com/v1/api",
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from zeronetworks import Zeronetworks
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Zeronetworks(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from zeronetworks import Zeronetworks
from zeronetworks.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Zeronetworks(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Zeronetworks` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
import os
from zeronetworks import Zeronetworks
def main():

    with Zeronetworks(
        api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
    ) as z_client:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Zeronetworks(
        api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
    ) as z_client:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from zeronetworks import Zeronetworks
import logging

logging.basicConfig(level=logging.DEBUG)
s = Zeronetworks(debug_logger=logging.getLogger("zeronetworks"))
```

You can also enable a default debug logger by setting an environment variable `ZERONETWORKS_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=zeronetworks&utm_campaign=python)
