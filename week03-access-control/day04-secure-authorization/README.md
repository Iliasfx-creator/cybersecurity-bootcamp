# Week 3 — Day 4: Secure Authorization Engineering

## Objective

This project converts the intentionally vulnerable Day 1 IDOR application into
a separate secure authorization implementation.

The application combines role-based authorization with object ownership and
enforces policy server-side at the endpoint that performs each operation.

## Architecture

The centralized policy is located in:

```text
app/authorization.py
```

The policy evaluates:

actor + action + resource

Access is denied unless a rule explicitly permits the operation.

The HTTP endpoints are implemented in:

app/server.py
Actors
Actor	Server-side role
Alice	user
Bob	user
Administrator	admin

Roles are loaded from server-side user data. Query parameters, request bodies,
and headers cannot assign privileges to the acting user.

Resources
Document	Owner
101	Alice
102	Alice
201	Bob
202	Bob

Alice and Bob can read and update only their own documents.

The administrator can read and update every document.

Routes
Method	Route	Purpose
POST	/demo-login	Creates a local demonstration session
POST	/logout	Invalidates the current session
GET	/documents	Lists documents permitted by policy
GET	/document?id=	Reads one permitted document
POST	/document/update	Updates one permitted document
POST	/admin/users/role	Changes a user's role

Unsupported methods for known routes return HTTP 405.

Authorization rules
Unauthenticated requests are denied.
Normal users can access only documents they own.
Administrators can access every document.
Only administrators can change user roles.
Client-supplied requester roles are ignored.
Unknown actions are denied by default.
Authorization occurs before every protected mutation.
Foreign and nonexistent documents return the same response.
HTTP status policy
400 — malformed identifier or invalid input.
401 — missing or invalid authentication.
403 — authenticated actor lacks permission for a known privileged function.
404 — unknown route, nonexistent object, or concealed foreign object.
405 — known endpoint requested with an unsupported HTTP method.
Running the server

From the repository root:

python3 -u week03-access-control/day04-secure-authorization/app/server.py

The server listens only on:

http://127.0.0.1:8011
Running the tests

With the server running in another terminal:

python3 week03-access-control/day04-secure-authorization/tests/authorization_tests.py

Expected result:

Passed: 11
Failed: 0
Evidence

The evidence directory contains:

complete automated test output,
a denied object-level request,
an allowed administrator request.

All saved session and password values are redacted.

Safety and limitations

This is a local educational application.

The demo login is not production authentication. Data and sessions exist only
in memory. The application does not implement HTTPS, persistent storage,
password verification, CSRF protection, rate limiting, or production session
management.

The server must not be exposed outside the local authorized environment.
