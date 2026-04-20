# RuleClass

* '1' - Trivial
* '2' - Permissive
* '3' - Privileged
* '4' - Critical
* '5' - System
* '6' - Preventative
* '8' - Dangerous


## Example Usage

```python
from zeronetworks.models import RuleClass

# Open enum: unrecognized values are captured as UnrecognizedInt
value: RuleClass = 1
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `1`
- `2`
- `3`
- `4`
- `5`
- `6`
- `8`
