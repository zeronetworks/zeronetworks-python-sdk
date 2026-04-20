# AEExclusions

## Overview

API calls related to AE Exclusions.

### Available Operations

* [ae_exclusions_inbound_create](#ae_exclusions_inbound_create) - Create AE Exclusion Inbound
* [ae_exclusions_inbound_get](#ae_exclusions_inbound_get) - Get AE Exclusion
* [ae_exclusions_inbound_delete](#ae_exclusions_inbound_delete) - Delete Automation Engine Inbound exclusions
* [ae_exclusions_inbound_update](#ae_exclusions_inbound_update) - Update AE Exclusion
* [ae_exclusions_outbound_create](#ae_exclusions_outbound_create) - Create AE Exclusion Outbound
* [ae_exclusions_outbound_get](#ae_exclusions_outbound_get) - Get AE Exclusion
* [ae_exclusions_outbound_delete](#ae_exclusions_outbound_delete) - Delete Automation Engine Outbound exclusions
* [ae_exclusions_outbound_update](#ae_exclusions_outbound_update) - Update AE Exclusion

## ae_exclusions_inbound_create

Returns the properties of the created AE Exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsInbound_Create" method="post" path="/protection/ae-exclusions/inbound" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_inbound_create(local_entity_id="<id>", local_processes_list=[
        "<value 1>",
        "<value 2>",
    ], ports_list=[
        {},
    ], remote_entity_ids_list=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                 | Type                                                                                                                                                                                                                                                      | Required                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `local_entity_id`                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `local_processes_list`                                                                                                                                                                                                                                    | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `ports_list`                                                                                                                                                                                                                                              | List[[models.PortsList](../../models/portslist.md)]                                                                                                                                                                                                       | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `remote_entity_ids_list`                                                                                                                                                                                                                                  | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `action`                                                                                                                                                                                                                                                  | [Optional[models.ActionType]](../../models/actiontype.md)                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Allow<br/>* '2' - Block<br/>                                                                                                                                                                                                                      |
| `description`                                                                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `excluded_local_ids_list`                                                                                                                                                                                                                                 | List[*str*]                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `ip_sec_opt`                                                                                                                                                                                                                                              | [Optional[models.IPSecOpt]](../../models/ipsecopt.md)                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                        | * For allow rule only.<br/>* '1' - Off<br/>* '2' - Null encapsulation connections<br/>* '3' - Authenticated and integrity-protected connections<br/>* '4' - Encrypted connections and dynamically negotiate encryption (inbound rule only)<br/>* '5' - Encrypted connections<br/> |
| `state`                                                                                                                                                                                                                                                   | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/>                                                                |
| `src_users_list`                                                                                                                                                                                                                                          | List[[models.SrcUsersList](../../models/srcuserslist.md)]                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `retries`                                                                                                                                                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                        | Configuration to override the default retry behavior of the client.                                                                                                                                                                                       |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 409              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_inbound_get

Returns the properties of the update AE exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsInbound_Get" method="get" path="/protection/ae-exclusions/inbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_inbound_get(id="d37077dc-0660-454d-81a0-f52f491fd5b8")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the rule                                                  | d37077dc-0660-454d-81a0-f52f491fd5b8                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_inbound_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsInbound_Delete" method="delete" path="/protection/ae-exclusions/inbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.ae_exclusions.ae_exclusions_inbound_delete(id="d37077dc-0660-454d-81a0-f52f491fd5b8")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the rule                                                  | d37077dc-0660-454d-81a0-f52f491fd5b8                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_inbound_update

Returns the properties of the update AE exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsInbound_Update" method="put" path="/protection/ae-exclusions/inbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_inbound_update(id="d37077dc-0660-454d-81a0-f52f491fd5b8", local_entity_id="<id>", local_processes_list=[], ports_list=[
        {},
    ], remote_entity_ids_list=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                 | Type                                                                                                                                                                                                                                                      | Required                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                               | Example                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                                                                                                                                                                                                      | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | The id of the rule                                                                                                                                                                                                                                        | d37077dc-0660-454d-81a0-f52f491fd5b8                                                                                                                                                                                                                      |
| `local_entity_id`                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `local_processes_list`                                                                                                                                                                                                                                    | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `ports_list`                                                                                                                                                                                                                                              | List[[models.PortsList](../../models/portslist.md)]                                                                                                                                                                                                       | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `remote_entity_ids_list`                                                                                                                                                                                                                                  | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `action`                                                                                                                                                                                                                                                  | [Optional[models.ActionType]](../../models/actiontype.md)                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Allow<br/>* '2' - Block<br/>                                                                                                                                                                                                                      |                                                                                                                                                                                                                                                           |
| `description`                                                                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `excluded_local_ids_list`                                                                                                                                                                                                                                 | List[*str*]                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `ip_sec_opt`                                                                                                                                                                                                                                              | [Optional[models.IPSecOpt]](../../models/ipsecopt.md)                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                        | * For allow rule only.<br/>* '1' - Off<br/>* '2' - Null encapsulation connections<br/>* '3' - Authenticated and integrity-protected connections<br/>* '4' - Encrypted connections and dynamically negotiate encryption (inbound rule only)<br/>* '5' - Encrypted connections<br/> |                                                                                                                                                                                                                                                           |
| `state`                                                                                                                                                                                                                                                   | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/>                                                                |                                                                                                                                                                                                                                                           |
| `src_users_list`                                                                                                                                                                                                                                          | List[[models.SrcUsersList](../../models/srcuserslist.md)]                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `retries`                                                                                                                                                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                        | Configuration to override the default retry behavior of the client.                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_outbound_create

Returns the properties of the created AE Exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsOutbound_Create" method="post" path="/protection/ae-exclusions/outbound" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_outbound_create(local_entity_id="<id>", local_processes_list=[
        "<value 1>",
        "<value 2>",
    ], ports_list=[], remote_entity_ids_list=[
        "<value 1>",
        "<value 2>",
        "<value 3>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                 | Type                                                                                                                                                                                                                                                      | Required                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `local_entity_id`                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `local_processes_list`                                                                                                                                                                                                                                    | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `ports_list`                                                                                                                                                                                                                                              | List[[models.PortsList](../../models/portslist.md)]                                                                                                                                                                                                       | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `remote_entity_ids_list`                                                                                                                                                                                                                                  | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `action`                                                                                                                                                                                                                                                  | [Optional[models.ActionType]](../../models/actiontype.md)                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Allow<br/>* '2' - Block<br/>                                                                                                                                                                                                                      |
| `description`                                                                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `excluded_local_ids_list`                                                                                                                                                                                                                                 | List[*str*]                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `ip_sec_opt`                                                                                                                                                                                                                                              | [Optional[models.IPSecOpt]](../../models/ipsecopt.md)                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                        | * For allow rule only.<br/>* '1' - Off<br/>* '2' - Null encapsulation connections<br/>* '3' - Authenticated and integrity-protected connections<br/>* '4' - Encrypted connections and dynamically negotiate encryption (inbound rule only)<br/>* '5' - Encrypted connections<br/> |
| `state`                                                                                                                                                                                                                                                   | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/>                                                                |
| `src_users_list`                                                                                                                                                                                                                                          | List[[models.SrcUsersList](../../models/srcuserslist.md)]                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |
| `retries`                                                                                                                                                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                        | Configuration to override the default retry behavior of the client.                                                                                                                                                                                       |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 409              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_outbound_get

Returns the properties of the update AE exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsOutbound_Get" method="get" path="/protection/ae-exclusions/outbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_outbound_get(id="d37077dc-0660-454d-81a0-f52f491fd5b8")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the rule                                                  | d37077dc-0660-454d-81a0-f52f491fd5b8                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_outbound_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsOutbound_Delete" method="delete" path="/protection/ae-exclusions/outbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.ae_exclusions.ae_exclusions_outbound_delete(id="d37077dc-0660-454d-81a0-f52f491fd5b8")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | The id of the rule                                                  | d37077dc-0660-454d-81a0-f52f491fd5b8                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## ae_exclusions_outbound_update

Returns the properties of the update AE exclusion.

### Example Usage

<!-- UsageSnippet language="python" operationID="AEExclusionsOutbound_Update" method="put" path="/protection/ae-exclusions/outbound/{ruleId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.ae_exclusions.ae_exclusions_outbound_update(id="d37077dc-0660-454d-81a0-f52f491fd5b8", local_entity_id="<id>", local_processes_list=[
        "<value 1>",
        "<value 2>",
    ], ports_list=[], remote_entity_ids_list=[
        "<value 1>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                 | Type                                                                                                                                                                                                                                                      | Required                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                               | Example                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                                                                                                                                                                                                      | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | The id of the rule                                                                                                                                                                                                                                        | d37077dc-0660-454d-81a0-f52f491fd5b8                                                                                                                                                                                                                      |
| `local_entity_id`                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `local_processes_list`                                                                                                                                                                                                                                    | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `ports_list`                                                                                                                                                                                                                                              | List[[models.PortsList](../../models/portslist.md)]                                                                                                                                                                                                       | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `remote_entity_ids_list`                                                                                                                                                                                                                                  | List[*str*]                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `action`                                                                                                                                                                                                                                                  | [Optional[models.ActionType]](../../models/actiontype.md)                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Allow<br/>* '2' - Block<br/>                                                                                                                                                                                                                      |                                                                                                                                                                                                                                                           |
| `description`                                                                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `excluded_local_ids_list`                                                                                                                                                                                                                                 | List[*str*]                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `ip_sec_opt`                                                                                                                                                                                                                                              | [Optional[models.IPSecOpt]](../../models/ipsecopt.md)                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                        | * For allow rule only.<br/>* '1' - Off<br/>* '2' - Null encapsulation connections<br/>* '3' - Authenticated and integrity-protected connections<br/>* '4' - Encrypted connections and dynamically negotiate encryption (inbound rule only)<br/>* '5' - Encrypted connections<br/> |                                                                                                                                                                                                                                                           |
| `state`                                                                                                                                                                                                                                                   | [Optional[models.RuleState]](../../models/rulestate.md)                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                        | * '1' - Enabled<br/>* '2' - Disabled<br/>* '3' - Deleted By User<br/>* '4' - Pending Review<br/>* '5' - Pending Review Auto<br/>* '6' - Rejected by User<br/>* '7' - Excluded by User<br/>                                                                |                                                                                                                                                                                                                                                           |
| `src_users_list`                                                                                                                                                                                                                                          | List[[models.SrcUsersList](../../models/srcuserslist.md)]                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                        | N/A                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |
| `retries`                                                                                                                                                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                        | Configuration to override the default retry behavior of the client.                                                                                                                                                                                       |                                                                                                                                                                                                                                                           |

### Response

**[models.AeExclusionRuleResponse](../../models/aeexclusionruleresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |