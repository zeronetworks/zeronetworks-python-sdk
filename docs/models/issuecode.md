# IssueCode

* '0' - Unspecified
* '1' - Unknown
* '2' - Access Denied
* '3' - IO Device Issue
* '4' - DotNet 3.5
* '5' - WMI Corrupted
* '6' - URL Filtering
* '7' - Out of Space
* '8' - Unsupported HMAC
* '9' - Unsupported Encryption
* '10' - Setup Script Failed
* '11' - Slow MFA
* '12' - Unexpted GPO Rules
* '13' - Zero Networks GPO Rule Mismatch
* '14' - Audit Mismatch
* '15' - Asset ID Mismatch
* '16' - Unsupported HTTP Version
* '17' - Registry Marked for Deletion
* '18' - Unable to add to automation group
* '19' - Incorrect Username or Password
* '20' - RPC Open Source Installed
* '21' - Timeout during initialization
* '22' - Data collection timeout
* '23' - Not in Sudoers
* '24' - Invalid SSH Key
* '25' - Events Unavailable
* '26' - SSH Password Incorrect
* '27' - SSH Password Expired
* '28' - Segmneted Users not found
* '29' - Unsupported Python Versions
* '30' - Cound not query segmented users
* '31' - Switch unreachable
* '32' - Switch communication issue
* '33' - Interface protection resource exceeded
* '34' - Unsupported Package Manager
* '35' - Firewall disabled by GPO
* '36' - Linux firewall logs oversized
* '1000' - First blocker issue code
* '1001' - Cluster node ipv6 disabled
* '1002' - Local rules merge disallowed


## Example Usage

```python
from zeronetworks.models import IssueCode

# Open enum: unrecognized values are captured as UnrecognizedInt
value: IssueCode = 0
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
- `19`
- `20`
- `21`
- `22`
- `23`
- `24`
- `25`
- `26`
- `27`
- `28`
- `29`
- `30`
- `31`
- `32`
- `33`
- `34`
- `35`
- `36`
- `1000`
- `1001`
- `1002`
