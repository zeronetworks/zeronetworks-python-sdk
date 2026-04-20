<!-- Start SDK Example Usage [usage] -->
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