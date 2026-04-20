# HealthStatus

* '0' - Unspecified
* '1' - Healthy
* '2' - Error
* '3' - Warning
* '4' - N/A
* '5' - Retrying
* '6' - Blocker


## Example Usage

```python
from zeronetworks.models import HealthStatus

# Open enum: unrecognized values are captured as UnrecognizedInt
value: HealthStatus = 0
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
