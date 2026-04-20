# AssetStatus

Possible asset status:
  * '1' - Not monitored
  * '2' - Segment server
  * '4' - Can't be monitored (unsupported OS)
  * '5' - Can't be monitored (unmonitorable)
  * '6' - Can't be monitored (unmonitorable)
  * '7' - Cloud connector
  * '8' - Not monitored (ansible unreachable)
  * '9' - Not monitored (cloud connector uninstalled)
  * '10' - Not monitored (cloud connector required)
  * '12' - Can't be monitored (inactive entity)
  * '13' - Stalked Externally
  * '14' - Lightweight Agent


## Example Usage

```python
from zeronetworks.models import AssetStatus

# Open enum: unrecognized values are captured as UnrecognizedInt
value: AssetStatus = 1
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `1`
- `2`
- `4`
- `5`
- `6`
- `7`
- `8`
- `9`
- `10`
- `12`
- `13`
- `14`
