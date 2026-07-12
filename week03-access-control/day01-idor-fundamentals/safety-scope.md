# Safety Scope

## Authorized target

Testing is authorized only against:

- `http://127.0.0.1:8010`

The intentionally vulnerable server must bind exclusively to:

```text
127.0.0.1:8010
Prohibited targets

The following are outside scope:

public websites,
external IP addresses,
university or workplace systems,
third-party applications,
unrelated local services,
other devices on the local network.
Authorized activity

The lab demonstrates read and write IDOR behavior between two fictional users:

Alice
Bob

Only the demo documents created by this local application may be accessed or modified.

Evidence handling

Committed evidence must not contain real:

session cookies,
authentication tokens,
passwords,
private keys,
TryHackMe flags,
challenge answers.

Cookie values must be replaced with:

session=REDACTED
Stop condition

Testing stops immediately if the destination is not exactly 127.0.0.1:8010.

The application must never bind to 0.0.0.0.
