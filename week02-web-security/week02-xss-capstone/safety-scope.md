# Safety Scope

## Authorized targets

Testing is authorized only against:

- `http://127.0.0.1:8005`
- `http://localhost:8005`

The server binds only to:

```text
127.0.0.1:8005
Prohibited targets

The following are outside scope:

public websites,
external IP addresses,
university or workplace systems,
third-party applications,
other devices on the local network,
services not created specifically for this lab.
Authorized payloads

The automated marker is:

<b>test-marker</b>

The browser-only local payload is:

<img src=x onerror=alert(1)>

The browser payload is used only to verify DOM behavior in the local application.

Evidence handling

Committed evidence must not contain:

passwords,
session cookies,
authentication tokens,
private keys,
TryHackMe flags,
challenge answers,
unrelated personal or system information.
Stop condition

Testing stops immediately if the destination is not exactly the authorized local application.

The intentionally vulnerable server must not be bound to 0.0.0.0 or exposed to another network.
