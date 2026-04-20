# IdentityProtectionState

Possible asset status:
  * '0' - Unspecified
  * '1' - Unsegmented
  * '2' - Unspecified
  * '3' - Segmented
  * '4' - Unsegmented
  * '5' - In learning
  * '6' - Forced Unprotected
  * '7' - Forced Removing Protection
  * '8' - Protected Due To Policy
  * '9' - Applying Protection Due To Policy
  * '10' - In learning Due To Policy
  * '11' - Learning Done
  * '12' - In learning Due To Policy Done


## Example Usage

```python
from zeronetworks.models import IdentityProtectionState

# Open enum: unrecognized values are captured as UnrecognizedInt
value: IdentityProtectionState = 0
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `0`
- `1`
- `2`
- `3`
- `4`
- `5`
- `6`
- `7`
- `8`
- `9`
- `10`
- `11`
- `12`
