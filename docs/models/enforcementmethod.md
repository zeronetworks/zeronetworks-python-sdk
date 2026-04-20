# EnforcementMethod

Possible values:
  * '1' - Linux IP Tables
  * '2' - Linux NF Tables
  * '3' - Windows Firewall
  * '4' - Windows WFP


## Example Usage

```python
from zeronetworks.models import EnforcementMethod

# Open enum: unrecognized values are captured as UnrecognizedInt
value: EnforcementMethod = 0
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `0`
- `1`
- `2`
- `3`
- `4`
