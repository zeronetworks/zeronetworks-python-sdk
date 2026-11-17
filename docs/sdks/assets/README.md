# Assets

## Overview

API calls related to Assets.

### Available Operations

* [assets_search](#assets_search) - Search Asset by FQDN

## assets_search

Returns an assetId.

### Example Usage

<!-- UsageSnippet language="python" operationID="Assets_Search" method="get" path="/assets/searchId" -->
```python
import os
from zeronetworks import Zeronetworks


with Zeronetworks(
    api_key=os.getenv("ZERONETWORKS_API_KEY"),
) as z_client:

    res = z_client.assets.assets_search(fqdn="server.domain.local")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `fqdn`                                                              | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | fully qualified domain name                                         | server.domain.local                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.AssetIDSearch](../../models/assetidsearch.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.Error                    | 400, 401, 403, 404              | application/json                |
| errors.Error                    | 500                             | application/json                |
| errors.ZeronetworksDefaultError | 4XX, 5XX                        | \*/\*                           |