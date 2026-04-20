# InternalAccessPolicy

## Overview

### Available Operations

* [internal_access_policy_create](#internal_access_policy_create) - Create an internal access policy
* [internal_access_policy_get](#internal_access_policy_get) - Get an Internal Access policy
* [internal_access_policy_update](#internal_access_policy_update) - Update an Internal Access policy
* [internal_access_policy_delete](#internal_access_policy_delete) - Delete an Internal Access policy

## internal_access_policy_create

Returns a the internal access policy

### Example Usage

<!-- UsageSnippet language="python" operationID="InternalAccessPolicy_Create" method="post" path="/protection/internal-access/policies" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.internal_access_policy.internal_access_policy_create(dst_asset_id="<id>", dst_ports_list=[], dst_process_names_list=[
        "<value 1>",
    ], name="<value>", rule_duration=1, src_user_ids_list=[
        "<value 1>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                      | Type                                                                                                                                                           | Required                                                                                                                                                       | Description                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dst_asset_id`                                                                                                                                                 | *str*                                                                                                                                                          | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |
| `dst_ports_list`                                                                                                                                               | List[[models.PortsList](../../models/portslist.md)]                                                                                                            | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |
| `dst_process_names_list`                                                                                                                                       | List[*str*]                                                                                                                                                    | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |
| `name`                                                                                                                                                         | *str*                                                                                                                                                          | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |
| `rule_duration`                                                                                                                                                | [models.RuleDuration](../../models/ruleduration.md)                                                                                                            | :heavy_check_mark:                                                                                                                                             | * '1' - Hour<br/>* '2' - Day<br/>* '3' - Week<br/>* '4' - Month<br/>* '5' - Never<br/>* '6' - 4 hours<br/>* '7' - 12 hours<br/>* '8' - 8 hours<br/>            |
| `src_user_ids_list`                                                                                                                                            | List[*str*]                                                                                                                                                    | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |
| `change_ticket`                                                                                                                                                | *Optional[str]*                                                                                                                                                | :heavy_minus_sign:                                                                                                                                             | N/A                                                                                                                                                            |
| `description`                                                                                                                                                  | *Optional[str]*                                                                                                                                                | :heavy_minus_sign:                                                                                                                                             | N/A                                                                                                                                                            |
| `state`                                                                                                                                                        | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                        | :heavy_minus_sign:                                                                                                                                             | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/> |
| `retries`                                                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                               | :heavy_minus_sign:                                                                                                                                             | Configuration to override the default retry behavior of the client.                                                                                            |

### Response

**[models.InternalAccessPolicyItem](../../models/internalaccesspolicyitem.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## internal_access_policy_get

Returns an internal access policy.

### Example Usage

<!-- UsageSnippet language="python" operationID="InternalAccessPolicy_Get" method="get" path="/protection/internal-access/policies/{policyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.internal_access_policy.internal_access_policy_get(id="p:e:8199d54b")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | id of the external acess policy                                     | p:e:8199d54b                                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.InternalAccessPolicyItem](../../models/internalaccesspolicyitem.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## internal_access_policy_update

Returns an internal access policy.

### Example Usage

<!-- UsageSnippet language="python" operationID="InternalAccessPolicy_Update" method="put" path="/protection/internal-access/policies/{policyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.internal_access_policy.internal_access_policy_update(id="p:e:8199d54b", dst_asset_id="<id>", dst_ports_list=[], dst_process_names_list=[
        "<value 1>",
        "<value 2>",
    ], name="<value>", rule_duration=4, src_user_ids_list=[
        "<value 1>",
        "<value 2>",
        "<value 3>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                      | Type                                                                                                                                                           | Required                                                                                                                                                       | Description                                                                                                                                                    | Example                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                                                                                                           | *str*                                                                                                                                                          | :heavy_check_mark:                                                                                                                                             | id of the external acess policy                                                                                                                                | p:e:8199d54b                                                                                                                                                   |
| `dst_asset_id`                                                                                                                                                 | *str*                                                                                                                                                          | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `dst_ports_list`                                                                                                                                               | List[[models.PortsList](../../models/portslist.md)]                                                                                                            | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `dst_process_names_list`                                                                                                                                       | List[*str*]                                                                                                                                                    | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `name`                                                                                                                                                         | *str*                                                                                                                                                          | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `rule_duration`                                                                                                                                                | [models.RuleDuration](../../models/ruleduration.md)                                                                                                            | :heavy_check_mark:                                                                                                                                             | * '1' - Hour<br/>* '2' - Day<br/>* '3' - Week<br/>* '4' - Month<br/>* '5' - Never<br/>* '6' - 4 hours<br/>* '7' - 12 hours<br/>* '8' - 8 hours<br/>            |                                                                                                                                                                |
| `src_user_ids_list`                                                                                                                                            | List[*str*]                                                                                                                                                    | :heavy_check_mark:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `change_ticket`                                                                                                                                                | *Optional[str]*                                                                                                                                                | :heavy_minus_sign:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `description`                                                                                                                                                  | *Optional[str]*                                                                                                                                                | :heavy_minus_sign:                                                                                                                                             | N/A                                                                                                                                                            |                                                                                                                                                                |
| `state`                                                                                                                                                        | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                        | :heavy_minus_sign:                                                                                                                                             | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/> |                                                                                                                                                                |
| `retries`                                                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                               | :heavy_minus_sign:                                                                                                                                             | Configuration to override the default retry behavior of the client.                                                                                            |                                                                                                                                                                |

### Response

**[models.InternalAccessPolicyItem](../../models/internalaccesspolicyitem.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## internal_access_policy_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="InternalAccessPolicy_Delete" method="delete" path="/protection/internal-access/policies/{policyId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.internal_access_policy.internal_access_policy_delete(id="p:e:8199d54b")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | id of the external acess policy                                     | p:e:8199d54b                                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |