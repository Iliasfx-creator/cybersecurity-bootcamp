# Security Review

## Review scope

This review covers:

- centralized authorization policy,
- document reads and updates,
- administrative role changes,
- client-controlled role inputs,
- alternative HTTP methods,
- invalid and nonexistent object identifiers,
- mutation behavior after denied requests.

## Security controls verified

### Authentication boundary

Protected routes require a valid server-generated session.

Unauthenticated requests return HTTP 401.

### Horizontal authorization

Alice and Bob can read and update only documents they own.

A foreign document is treated like a nonexistent document and returns HTTP 404.

### Vertical authorization

Only a server-side administrator role can invoke role management.

Normal users receive HTTP 403.

### Client-input trust

Requester roles supplied through query parameters, form fields, or headers are
ignored.

The acting role is resolved from server-side user data on every request.

### Centralized policy

Authorization decisions are made through one policy function.

Unknown actions and invalid actor contexts are denied by default.

### Method restrictions

Only explicitly supported methods are accepted for known routes.

Alternative methods return HTTP 405 and do not reach protected mutations.

### State integrity

Authorization is checked before document content is changed.

The automated test suite confirms that a denied update leaves the target
document unchanged.

### Input and object handling

Malformed identifiers return HTTP 400.

Nonexistent and unauthorized documents return HTTP 404 without exposing
foreign document data.

## Automated verification

The test suite covers:

- unauthenticated denial,
- Alice accessing Alice's document,
- Alice being denied Bob's document,
- preservation of data after denied update,
- Bob accessing Bob's document,
- non-admin administrative denial,
- administrator operation success,
- ignored client-supplied admin role,
- administrator access to all documents,
- alternative method rejection,
- invalid and nonexistent identifier handling.

Result:

```text
Passed: 11
Failed: 0
```

The complete output is stored in:

evidence/test-output.txt
Manual verification

Burp Suite evidence records:

a denied Alice-to-Bob document request,
an allowed administrator role-management request.

All stored session and password values are redacted.

Residual limitations

This remains a local educational implementation.

It uses a passwordless demo login, in-memory state, plain HTTP, and a
single-process server. It does not implement production session storage,
session rotation after privilege changes, CSRF protection, rate limiting,
persistent audit logging, or database transaction controls.

These limitations would need remediation before any production deployment.

Conclusion

The project satisfies the intended authorization policy for its defined local
scope.

Both ownership-based and role-based authorization are enforced server-side,
negative behavior is tested, unsupported methods are rejected, and denied
updates preserve application state.
