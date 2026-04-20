# MFAOutbound

## Overview

API calls related to Outbound MFA policies.

### Available Operations

* [mfa_outbound_policies_create](#mfa_outbound_policies_create) - Add Outbound MFA Policy
* [mfa_outbound_policies_get](#mfa_outbound_policies_get) - Get Outbound MFA Policy
* [mfa_outbound_policies_update](#mfa_outbound_policies_update) - Update Outbound MFA Policy
* [mfa_outbound_policies_delete](#mfa_outbound_policies_delete) - Remove Outbound MFA Policy

## mfa_outbound_policies_create

Returns a the properties of outbound MFA policy created.

### Example Usage

<!-- UsageSnippet language="python" operationID="MFAOutboundPolicies_Create" method="post" path="/protection/reactive-policies/outbound" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.mfa_outbound.mfa_outbound_policies_create(additional_ports_list=[
        {},
    ], dst_entity_info={
        "id": "<id>",
    }, dst_port="<value>", fallback_to_logged_on_user=False, mfa_methods=[
        4,
    ], override_builtins=True, protocol_type=183056, rule_duration=4, src_entity_infos=[
        {
            "id": "<id>",
        },
    ], src_process_names=[], src_user_infos=[], state=2)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `additional_ports_list`                                                                                                         | List[[models.PortsList](../../models/portslist.md)]                                                                             | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `dst_entity_info`                                                                                                               | [models.ReactivePolicyOutboundBodyDstEntityInfo](../../models/reactivepolicyoutboundbodydstentityinfo.md)                       | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `dst_port`                                                                                                                      | *str*                                                                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `fallback_to_logged_on_user`                                                                                                    | *bool*                                                                                                                          | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `mfa_methods`                                                                                                                   | List[[models.MfaMethods](../../models/mfamethods.md)]                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `override_builtins`                                                                                                             | *bool*                                                                                                                          | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `protocol_type`                                                                                                                 | *int*                                                                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `rule_duration`                                                                                                                 | [models.RuleDuration](../../models/ruleduration.md)                                                                             | :heavy_check_mark:                                                                                                              | * '1' - Hour<br/>* '2' - Day<br/>* '3' - Week<br/>* '4' - Month<br/>* '5' - Never<br/>* '6' - 4 hours<br/>* '7' - 12 hours<br/>* '8' - 8 hours<br/> |
| `src_entity_infos`                                                                                                              | List[[models.ReactivePolicyOutboundBodySrcEntityInfo](../../models/reactivepolicyoutboundbodysrcentityinfo.md)]                 | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `src_process_names`                                                                                                             | List[*str*]                                                                                                                     | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `src_user_infos`                                                                                                                | List[[models.ReactivePolicyOutboundBodySrcUserInfo](../../models/reactivepolicyoutboundbodysrcuserinfo.md)]                     | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `state`                                                                                                                         | [models.ReactivePolicyState](../../models/reactivepolicystate.md)                                                               | :heavy_check_mark:                                                                                                              | * '1' - Enabled<br/>* '2' - Disabled<br/>                                                                                       |
| `change_ticket`                                                                                                                 | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `description`                                                                                                                   | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `dst_process_names`                                                                                                             | List[*str*]                                                                                                                     | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `excluded_src_entity_infos`                                                                                                     | List[[models.ReactivePolicyOutboundBodyExcludedSrcEntityInfo](../../models/reactivepolicyoutboundbodyexcludedsrcentityinfo.md)] | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `excluded_src_processes`                                                                                                        | List[*str*]                                                                                                                     | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `name`                                                                                                                          | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `restrict_to_originated_user`                                                                                                   | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `restrict_login_to_originating_user`                                                                                            | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `use_default_idp`                                                                                                               | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `use_occasional_mfa`                                                                                                            | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[models.ReactivePolicyItem](../../models/reactivepolicyitem.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## mfa_outbound_policies_get

Returns the properties of an outbound MFA policy.

### Example Usage

<!-- UsageSnippet language="python" operationID="MFAOutboundPolicies_Get" method="get" path="/protection/reactive-policies/outbound/{reactivePolicyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.mfa_outbound.mfa_outbound_policies_get(id="aaae3397-b969-4d1f-8b20-21fec67c6867")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the MFA policy                                            |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ReactivePolicyResponse](../../models/reactivepolicyresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## mfa_outbound_policies_update

Returns the updated properties of an outbound MFA policy.

### Example Usage

<!-- UsageSnippet language="python" operationID="MFAOutboundPolicies_Update" method="put" path="/protection/reactive-policies/outbound/{reactivePolicyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.mfa_outbound.mfa_outbound_policies_update(id="3e5a2210-3d45-4a84-b77b-498e43156c22", additional_ports_list=[
        {},
    ], dst_entity_info={
        "id": "<id>",
    }, dst_port="<value>", fallback_to_logged_on_user=True, mfa_methods=[
        6,
    ], override_builtins=False, protocol_type=602852, rule_duration=2, src_entity_infos=[
        {
            "id": "<id>",
        },
    ], src_process_names=[
        "<value 1>",
        "<value 2>",
    ], src_user_infos=[
        {
            "id": "<id>",
        },
    ], state=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                                                                            | *str*                                                                                                                           | :heavy_check_mark:                                                                                                              | The id of the MFA policy                                                                                                        |
| `additional_ports_list`                                                                                                         | List[[models.PortsList](../../models/portslist.md)]                                                                             | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `dst_entity_info`                                                                                                               | [models.ReactivePolicyOutboundBodyDstEntityInfo](../../models/reactivepolicyoutboundbodydstentityinfo.md)                       | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `dst_port`                                                                                                                      | *str*                                                                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `fallback_to_logged_on_user`                                                                                                    | *bool*                                                                                                                          | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `mfa_methods`                                                                                                                   | List[[models.MfaMethods](../../models/mfamethods.md)]                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `override_builtins`                                                                                                             | *bool*                                                                                                                          | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `protocol_type`                                                                                                                 | *int*                                                                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `rule_duration`                                                                                                                 | [models.RuleDuration](../../models/ruleduration.md)                                                                             | :heavy_check_mark:                                                                                                              | * '1' - Hour<br/>* '2' - Day<br/>* '3' - Week<br/>* '4' - Month<br/>* '5' - Never<br/>* '6' - 4 hours<br/>* '7' - 12 hours<br/>* '8' - 8 hours<br/> |
| `src_entity_infos`                                                                                                              | List[[models.ReactivePolicyOutboundBodySrcEntityInfo](../../models/reactivepolicyoutboundbodysrcentityinfo.md)]                 | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `src_process_names`                                                                                                             | List[*str*]                                                                                                                     | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `src_user_infos`                                                                                                                | List[[models.ReactivePolicyOutboundBodySrcUserInfo](../../models/reactivepolicyoutboundbodysrcuserinfo.md)]                     | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `state`                                                                                                                         | [models.ReactivePolicyState](../../models/reactivepolicystate.md)                                                               | :heavy_check_mark:                                                                                                              | * '1' - Enabled<br/>* '2' - Disabled<br/>                                                                                       |
| `change_ticket`                                                                                                                 | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `description`                                                                                                                   | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `dst_process_names`                                                                                                             | List[*str*]                                                                                                                     | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `excluded_src_entity_infos`                                                                                                     | List[[models.ReactivePolicyOutboundBodyExcludedSrcEntityInfo](../../models/reactivepolicyoutboundbodyexcludedsrcentityinfo.md)] | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `excluded_src_processes`                                                                                                        | List[*str*]                                                                                                                     | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `name`                                                                                                                          | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `restrict_to_originated_user`                                                                                                   | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `restrict_login_to_originating_user`                                                                                            | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `use_default_idp`                                                                                                               | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `use_occasional_mfa`                                                                                                            | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[models.ReactivePolicyItem](../../models/reactivepolicyitem.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## mfa_outbound_policies_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="MFAOutboundPolicies_Delete" method="delete" path="/protection/reactive-policies/outbound/{reactivePolicyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.mfa_outbound.mfa_outbound_policies_delete(id="24ddde68-802d-4b25-a92c-ebc061be425f")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the MFA policy                                            |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |