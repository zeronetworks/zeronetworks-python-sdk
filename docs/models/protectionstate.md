# ProtectionState

* '0' - Unspecified
* '1' - Unsegmented
* '2' - Unsegmenting
* '3' - Segmented
* '4' - Segmenting
* '5' - Learning until
* '6' - forced_unprotected
* '7' - Unsegmenting' - Due to Policy
* '8' - Segmented' - Due to Policy
* '9' - Segmenting- Due to Policy
* '10' - Learning until' - Due to Policy
* '11' - Learning done
* '12' - Learning done- Due to Policy
* '13' - APPLYING_QUEUE_WITH_BLOCKS
* '14' - APPLYING_QUEUE_WITH_BLOCKS_DUE_TO_POLICY
* '15' - QUEUED_WITH_BLOCKS
* '16' - QUEUED_WITH_BLOCKS_DUE_TO_POLICY
* '17' - QUEUED_WITH_BLOCKS_DONE
* '18' - QUEUED_WITH_BLOCKS_DUE_TO_POLICY_DONE


## Example Usage

```python
from zeronetworks.models import ProtectionState

# Open enum: unrecognized values are captured as UnrecognizedInt
value: ProtectionState = 0
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
- `13`
- `14`
- `15`
- `16`
- `17`
- `18`
