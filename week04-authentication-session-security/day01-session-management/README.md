# Week 4 — Day 1: Session Management Engineering & Testing

This loopback-only lab demonstrates an engineered session lifecycle with opaque
identifiers, server-side state, rotation, expiration, revocation, cookie-only
transport, and privacy-preserving logs.

## Safety and scope

- The server binds only to `127.0.0.1:8013`.
- It is intentionally a session-management lab, not a production authentication
  service. The `/login` route uses a simplified local identity selection flow.
- Only `alice`, `bob`, and `admin` exist in local in-memory data.
- No external system or completed Week 3 project is modified.
- Real passwords, cookies, tokens, flags, and target IPs must never be committed.

## Project structure

```text
day01-session-management/
├── README.md
├── app/
│   ├── __init__.py
│   ├── server.py
│   └── session_manager.py
├── docs/
│   ├── burp-capture-guide.md
│   ├── portswigger-study-notes.md
│   ├── security-review.md
│   ├── session-lifecycle.md
│   ├── source-notes.md
│   └── threat-control-test-matrix.md
├── evidence/
│   ├── automated-test-results.txt
│   └── burp/
└── tests/
    └── test_session_management.py
```

## Security properties

- Session IDs contain 32 random bytes generated with `secrets.token_bytes`, an
  operating-system-backed CSPRNG. Hex encoding produces 64 characters while
  preserving 256 bits of entropy.
- Tokens are opaque; identity, tenant, role, privilege level, timestamps, and
  revocation state remain in the server-side store.
- The request handler reads a session ID only from the `session` cookie.
- Authentication and privilege changes replace the identifier and invalidate
  the previous one.
- Idle and absolute expiration are enforced by the server using an injectable
  clock.
- Logout revokes the record and instructs the browser to delete the cookie.
- Logs contain a keyed HMAC fingerprint, never the complete token.

## Run the automated tests

From this directory:

```bash
python3 tests/test_session_management.py
```

The suite uses only Python's standard library and does not sleep. It currently
contains 38 tests, including negative tests for fixation, replay, forgery,
alternative token transport, client-supplied roles, and expiration.

## Run the local server

```bash
python3 app/server.py
```

The expected message is:

```text
Session lab listening on http://127.0.0.1:8013 (local HTTP mode)
```

Keep that terminal open while using Burp. Stop the server with `Ctrl+C`.

## Local and production cookie modes

Local HTTP mode intentionally omits `Secure`, because a browser normally sends
a Secure cookie only over HTTPS. Production behind HTTPS would use:

```bash
python3 app/server.py --secure-cookie
```

That command demonstrates the production header configuration; it should not be
used for the plain-HTTP Burp exercise because the browser may withhold the
cookie. Both modes set `HttpOnly`, `SameSite=Lax`, and `Path=/`.

## Local endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/session/prelogin` | Issue or replace an anonymous pre-login session |
| `POST` | `/login` | Replace any presented token with an authenticated token |
| `GET` | `/me` | Return identity and role from server-side session state |
| `POST` | `/session/step-up` | Rotate an administrator session after privilege elevation |
| `GET` | `/admin` | Require the server-side admin role and elevated state |
| `POST` | `/logout` | Revoke server-side state and clear the cookie |
| `GET` | `/health` | Non-sensitive health response |

## Completion checklist

- [x] Separate loopback-only implementation
- [x] CSPRNG opaque tokens and server-side state
- [x] Rotation, idle timeout, absolute timeout, and logout revocation
- [x] Fake clock and at least 20 automated tests
- [x] Lifecycle, threat mapping, source notes, and security review
- [x] Five Burp comparisons captured and sanitized
- [x] TryHackMe Session Management completed to 100%
- [x] Up to two previously unsolved PortSwigger persistent-session labs reviewed
- [x] Final redaction scan, commit, and push

## References

- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [PortSwigger authentication: other mechanisms](https://portswigger.net/web-security/authentication/other-mechanisms)
