# Engineering Source Notes

## Entropy and unpredictability

Entropy describes how much uncertainty an attacker must overcome. Character
count describes representation length. They are related only when every encoded
symbol comes from an independent unpredictable source. A 64-character token
made from predictable data can still have almost no useful entropy.

This lab requests 32 random bytes from Python's `secrets.token_bytes`. The
`secrets` module is intended for security tokens and uses the operating system's
cryptographically secure random source. The bytes are hex-encoded only for safe
cookie transport. Encoding doubles the visible length to 64 characters but does
not create additional entropy; the original entropy remains 256 bits.

Uniqueness is checked against the active server-side store even though a random
collision at this size is extraordinarily unlikely.

## Opaque identifiers and server-side state

A session token should act as a lookup key, not as a portable user record. It
must not expose a username, tenant, role, or authorization decision. This keeps
the client from editing trusted fields and lets the server revoke or change a
session immediately.

The local store maps an opaque token to identity, tenant, role, authentication
level, timestamps, and state. Only a safe fingerprint is exposed for log
correlation.

## Cookie-only exchange

The handler reads the identifier only from the `session` cookie. Query
parameters, custom headers, and Bearer headers are ignored. Supporting multiple
transport mechanisms increases the chance that a token appears in browser
history, access logs, analytics, referrers, or copied URLs.

## Cookie attributes

- `HttpOnly` prevents browser JavaScript from reading the cookie. It limits one
  important token-theft path but does not stop the browser from sending the
  cookie with a forged request.
- `Secure` restricts cookie transmission to HTTPS. It is required in production
  but normally prevents the cookie from working on this plain local HTTP lab.
- `SameSite=Lax` reduces some cross-site cookie sending. It is a useful layer,
  not a substitute for request-specific CSRF protection.
- `Path=/` gives the session one consistent application-wide scope.

## Rotation

Authentication replaces any pre-login identifier, including one supplied by an
attacker. Privilege elevation also revokes the old identifier and issues a new
one. Otherwise a token learned before the security context changed could retain
the newly gained authority.

Rotation keeps the original absolute expiry deadline. Repeated rotation must not
turn an absolute lifetime into an indefinitely renewable session.

## Idle and absolute expiration

The idle deadline measures inactivity since the last accepted request. Normal
activity refreshes it. The absolute deadline is measured from authentication
and expires regardless of activity. Both checks run server-side before a
session is accepted.

Tests inject `FakeClock`; they advance logical time instead of waiting in real
time. This makes boundary conditions deterministic and fast.

## Logout and revocation

Deleting a browser cookie alone is insufficient because a copied cookie could
still be replayed. Logout first marks the server record revoked and then returns
`Max-Age=0` so the browser removes its copy. Replay of the old identifier is
rejected.

## Safe session logging

Complete tokens are authentication secrets and must not appear in log messages.
This lab produces a shortened HMAC-SHA-256 fingerprint under a secret logging
key. The value supports event correlation without making the original token
recoverable or usable as authentication.

The HTTP handler also suppresses the default full request-target log because a
mistaken query parameter could otherwise leak a token into logs.

## References

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [Python `secrets` documentation](https://docs.python.org/3/library/secrets.html)
