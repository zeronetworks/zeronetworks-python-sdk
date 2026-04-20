# RuleState

* '1' - Enabled
* '2' - Disabled
* '3' - Deleted By User
* '4' - Pending Review
* '5' - Pending Review Auto
* '6' - Rejected by User
* '7' - Excluded by User


## Example Usage

```python
from zeronetworks.models import RuleState

# Open enum: unrecognized values are captured as UnrecognizedInt
value: RuleState = 1
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
