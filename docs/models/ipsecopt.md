# IPSecOpt

* For allow rule only.
* '1' - Off
* '2' - Null encapsulation connections
* '3' - Authenticated and integrity-protected connections
* '4' - Encrypted connections and dynamically negotiate encryption (inbound rule only)
* '5' - Encrypted connections


## Example Usage

```python
from zeronetworks.models import IPSecOpt

# Open enum: unrecognized values are captured as UnrecognizedInt
value: IPSecOpt = 1
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `1`
- `2`
- `3`
- `4`
- `5`
