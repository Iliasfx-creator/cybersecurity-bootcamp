# Secure Authorization Source Notes

## Sources

- PortSwigger Web Security Academy — Access Control, Prevention
- OWASP Authorization Cheat Sheet

## Deny by default

Deny by default means that access is rejected unless a specific policy rule
explicitly permits the actor to perform the requested action.

The application must not assume that an unhandled route, role, action, or
resource should be accessible. Unknown roles and unknown actions are denied.

This makes the secure outcome the fallback when the application changes or a
developer forgets to create a new permission rule.

## Enforcement at the action endpoint

Authorization must be checked at the endpoint that reads or changes the
protected resource.

A hidden button, protected menu, previous workflow step, or frontend route does
not protect the backend operation. A client can construct requests directly.

For an update, the application must authenticate the actor, locate the
resource, authorize the actor for that resource and action, and only then
perform the mutation.

## RBAC and object-level authorization

Role-Based Access Control grants capabilities according to a server-managed
role. In this project, the admin role can read and update every document and
can change user roles.

Ownership authorization applies to individual resources. Alice and Bob have
the same user role, but Alice may access only Alice's documents and Bob may
access only Bob's documents.

RBAC alone cannot express this horizontal restriction. The policy therefore
combines role checks with ownership checks.

## Why negative tests are required

Positive tests show that intended functionality works. They do not prove that
forbidden paths are blocked.

Negative tests verify that:

- unauthenticated requests are rejected,
- users cannot access another user's objects,
- non-admin users cannot invoke admin operations,
- client-supplied roles are ignored,
- alternative methods are rejected,
- denied updates do not change application state.

The state check after a denied update is essential because an error response
alone does not prove that the mutation did not happen.

## 403 and 404 decisions

HTTP 403 is appropriate when the requester is authenticated, the operation is
known, and the server can safely reveal that the requester lacks the required
privilege. This project uses 403 for a non-admin attempting an administrative
operation.

HTTP 404 is appropriate when revealing the existence of a protected object
would help enumeration. This project returns the same 404 response for a
nonexistent document and a document owned by another user.

HTTP 401 is used when authentication is missing or invalid. HTTP 400 is used
for malformed identifiers, and HTTP 405 is used when a known endpoint receives
an unsupported method.

## References

- https://portswigger.net/web-security/access-control#how-to-prevent-access-control-vulnerabilities
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
