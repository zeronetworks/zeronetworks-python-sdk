# GroupsCustom

## Overview

API calls related to Custom Groups.

### Available Operations

* [custom_groups_create](#custom_groups_create) - Create Custom Group
* [custom_groups_get](#custom_groups_get) - Get a custom group
* [custom_groups_update](#custom_groups_update) - Update Custom Group
* [custom_groups_delete](#custom_groups_delete) - Delete Custom Group
* [custom_group_members_list](#custom_group_members_list) - List Custom Group members
* [custom_groups_members_add](#custom_groups_members_add) - Add Custom Group members
* [custom_groups_members_delete](#custom_groups_members_delete) - Delete Custom Group members

## custom_groups_create

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroups_Create" method="post" path="/groups/custom" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.groups_custom.custom_groups_create(name="<value>", members_id=[
        "g:c:ab124as2",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `description`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `members_id`                                                        | List[*str*]                                                         | :heavy_minus_sign:                                                  | members id                                                          | [<br/>"g:c:ab124as2"<br/>]                                          |
| `conditions`                                                        | [Optional[models.GroupConditions]](../../models/groupconditions.md) | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.CustomGroupResponse](../../models/customgroupresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 409              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_groups_get

Returns the properties of an custom group.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroups_Get" method="get" path="/groups/custom/{groupId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.groups_custom.custom_groups_get(id="g:t:01445453")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.CustomGroupResponse](../../models/customgroupresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_groups_update

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroups_Update" method="put" path="/groups/custom/{groupId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.groups_custom.custom_groups_update(id="g:t:01445453", name="<value>", members_id=[
        "g:c:ab124as2",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `description`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `members_id`                                                        | List[*str*]                                                         | :heavy_minus_sign:                                                  | members id                                                          | [<br/>"g:c:ab124as2"<br/>]                                          |
| `conditions`                                                        | [Optional[models.GroupConditions]](../../models/groupconditions.md) | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.CustomGroupResponse](../../models/customgroupresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_groups_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroups_Delete" method="delete" path="/groups/custom/{groupId}" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.groups_custom.custom_groups_delete(id="g:t:01445453")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_group_members_list

Returns a list of all members

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroupMembers_List" method="get" path="/groups/custom/{groupId}/members" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.groups_custom.custom_group_members_list(id="g:t:01445453")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GroupMembersList](../../models/groupmemberslist.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_groups_members_add

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroupsMembers_Add" method="put" path="/groups/custom/{groupId}/members" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    res = z_client.groups_custom.custom_groups_members_add(id="g:t:01445453", members_id=[
        "g:c:ab124as2",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `members_id`                                                        | List[*str*]                                                         | :heavy_check_mark:                                                  | members id                                                          | [<br/>"g:c:ab124as2"<br/>]                                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.EmptyResponse](../../models/emptyresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |

## custom_groups_members_delete

Returns an empty object.

### Example Usage

<!-- UsageSnippet language="python" operationID="CustomGroupsMembers_Delete" method="delete" path="/groups/custom/{groupId}/members" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY", ""),
) as z_client:

    z_client.groups_custom.custom_groups_members_delete(id="g:t:01445453", members_id=[
        "g:c:ab124as2",
    ])

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `id`                                                                | *str*                                                               | :heavy_check_mark:                                                  | groupId to filter on                                                | g:t:01445453                                                        |
| `members_id`                                                        | List[*str*]                                                         | :heavy_check_mark:                                                  | members id                                                          | [<br/>"g:c:ab124as2"<br/>]                                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403                   | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |