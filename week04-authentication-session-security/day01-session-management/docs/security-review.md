# Security Review

## Review scope

The review covers session issuance, storage, transport, validation, rotation,
expiration, revocation, logging, and the authorization context derived from a
session. The simplified local identity-selection step is not a production
authentication design.

## Positive findings

- The identifier is opaque and generated from 32 CSPRNG bytes.
- Identity, tenant, role, privilege level, and lifecycle state remain server-side.
- The application reads a session identifier only from the cookie.
- Authentication, re-authentication, and privilege elevation replace the token.
- Rotation cannot extend the original absolute lifetime.
- Both idle and absolute expiration are checked before accepting a request.
- Logout revokes state before returning a cookie-deletion instruction.
- Safe fingerprints support correlation without logging reusable secrets.
- Authorization ignores client-supplied roles and uses trusted session state.
- Session responses use `Cache-Control: no-store`.

## CSPRNG justification

`secrets.token_bytes(32)` is used in the production path. Python documents the
`secrets` module as suitable for cryptographically strong tokens and passwords,
using the operating system's strongest randomness source. Thirty-two bytes
provide 256 bits before encoding, exceeding the required 128-bit minimum.

The test suite patches this function once to prove that the implementation asks
for 32 bytes. Separate tests validate the encoded size and uniqueness. The
uniqueness test is not presented as proof of unpredictability; the CSPRNG choice
is the security argument.

## Cookie configuration review

Local plain HTTP emits:

```text
Set-Cookie: session=REDACTED_NEW; Path=/; HttpOnly; SameSite=Lax
```

Production HTTPS mode adds:

```text
Secure
```

Enabling `Secure` on the current `http://127.0.0.1` exercise could cause the
browser to withhold the cookie. Production must terminate HTTPS correctly and
enable `--secure-cookie`.

## Test review

The suite contains 38 deterministic tests. Time-dependent cases inject a fake
clock and never use `sleep`. It includes negative tests for forged values,
fixation, old-token replay, idle and absolute expiry, non-cookie transport,
client-controlled role claims, malformed input, unsupported methods, and unknown
routes.

The canonical evidence file is generated with:

```bash
python3 tests/test_session_management.py 2>&1 | tee evidence/automated-test-results.txt
```

## Residual risk and production work

- The in-memory store is lost on restart and is not appropriate for a clustered
  service. Production needs a shared, protected store with atomic rotation and
  expiration.
- `/login` is deliberately simplified. Production needs real credential or
  federated authentication, rate limiting, MFA policy, and re-authentication for
  sensitive elevation.
- `SameSite=Lax` is defense in depth, not complete CSRF protection. State-changing
  routes still need an application CSRF design.
- HTTPS, HSTS, proxy trust configuration, secret rotation, incident response,
  concurrent-session policy, and device/session management need deployment-level
  validation.
- Session-store availability and denial-of-service controls are outside this
  small local implementation.

## Review conclusion

The implementation meets the Day 1 engineering requirements for a loopback
training lab. Burp comparisons were completed and sanitized. Final completion depends on
sanitization review, the TryHackMe room, and the selected PortSwigger study/labs.
