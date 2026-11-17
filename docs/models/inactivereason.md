# InactiveReason

* '1' - Duplicated in asset repository
* '2' - Manually set as inactive
* '3' - None
* '4' - Disabled in asset repository
* '5' - Inactive in asset repository
* '6' - Deleted in asset repository
* '7' - Sync disabled
* '8' - Resource group inactive


## Example Usage

```python
from zeronetworks.models import InactiveReason

# Open enum: unrecognized values are captured as UnrecognizedInt
value: InactiveReason = 1
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `1`
- `2`
- `3`
- `4`
- `5`
- `6`
- `7`
- `8`
