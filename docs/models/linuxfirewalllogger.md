# LinuxFirewallLogger

Possible values:
  * '1' - Rsyslog
  * '2' - Ulogd2


## Example Usage

```python
from zeronetworks.models import LinuxFirewallLogger

# Open enum: unrecognized values are captured as UnrecognizedInt
value: LinuxFirewallLogger = 0
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `0`
- `1`
- `2`
