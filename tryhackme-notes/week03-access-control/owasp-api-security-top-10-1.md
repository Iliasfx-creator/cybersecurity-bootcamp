# OWASP API Security Top 10 — 1

Status: Started

## Concepts

### Broken Object Level Authorization

BOLA occurs when an API accepts an object identifier from the client but does
not verify whether the authenticated actor is authorized to access that
specific object.

Authentication alone is insufficient. The API must evaluate the relationship
between the actor, action, and requested object on every request.

Identifiers may be sequential, encoded, hashed, or random. Their format does
not replace object-level authorization.

### Broken Function Level Authorization

Broken Function Level Authorization occurs when a user can invoke a function
that should be restricted to a different role.

Examples include administrative user management, configuration changes, or
privileged write and delete operations.

Hiding the function from the interface does not protect the backend endpoint.

## Testing methodology

1. Establish the normal authorized request.
2. Identify the acting user, requested action, and target object.
3. Replay the request without authentication.
4. Replay it with a lower-privileged identity.
5. Modify one identifier, function, or method at a time.
6. Compare status codes, response bodies, and application side effects.
7. Verify that denied writes leave application state unchanged.
8. Record the missing server-side authorization decision.

## Mistakes to avoid

- Treating possession of an object ID as proof of authorization.
- Assuming an unguessable identifier prevents unauthorized access.
- Testing only successful requests.
- Relying only on the HTTP status without checking side effects.
- Assuming that a function is protected because it is hidden from the UI.
- Changing multiple request components at the same time.

## Lessons learned

BOLA is primarily an object-level authorization failure, while BFLA is a
function or role-level authorization failure.

A secure API commonly needs both ownership checks and role checks.

Authorization must be evaluated server-side on every request and immediately
before the protected read or mutation.

## Remediation

- Deny access by default.
- Derive the actor and role from trusted server-side session data.
- Enforce object ownership or relationship checks.
- Enforce role checks for privileged functions.
- Centralize authorization decisions.
- Allow only required HTTP methods.
- Add positive and negative authorization tests.
- Verify that denied operations do not modify state.

## Evidence handling

Challenge answers, flags, target addresses, session values, and credentials are
intentionally omitted.
