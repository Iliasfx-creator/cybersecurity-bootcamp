# TryHackMe — Session Management

Status: Completed (100%)

## Scope and redaction

- Record concepts, generic commands, mistakes, and lessons learned only.
- Do not include room answers, flags, target IP addresses, credentials, or real
  cookie values.
- Use `Cookie: session=REDACTED` and `Password: REDACTED` in every example.

## Concepts

- Authentication establishes an identity; authorization decides what that
  identity may do; session management preserves the authenticated context across
  requests.
- A session cookie should contain an opaque reference while identity, roles,
  expiry, and revocation state remain on the server.
- Predictable values, client-controlled privilege fields, missing rotation, and
  missing revocation turn a session token into an authorization bypass.
- Cookie flags reduce specific browser-side risks but do not replace server-side
  validation, CSRF protection, or lifecycle controls.
- Idle expiration limits unattended use; absolute expiration limits total token
  lifetime even during activity.

## Generic commands used

```bash
curl -i http://REDACTED-TARGET/
curl -i -H 'Cookie: session=REDACTED' http://REDACTED-TARGET/profile
curl -i -X POST -H 'Cookie: session=REDACTED' http://REDACTED-TARGET/logout
```

## Testing methodology

1. Capture the normal authenticated request and response.
2. Remove the cookie and observe the unauthenticated baseline.
3. Modify only one cookie or lifecycle property at a time.
4. Test old values after login, elevation, expiry, password change, and logout.
5. Confirm that denial changes no server state.
6. Sanitize notes before committing.

## Mistakes

- I initially changed only the visible client-side role and saw a different interface without trusted server data. The missing step was understanding that multiple client-side identity fields influenced the application flow.

## Lessons learned

- A cookie is only a transport container; its security depends on the server's
  issuance, validation, expiry, rotation, and revocation logic.
- Client-side identity and role values can alter the interface, but every protected endpoint must independently validate server-side session state and authorization.
