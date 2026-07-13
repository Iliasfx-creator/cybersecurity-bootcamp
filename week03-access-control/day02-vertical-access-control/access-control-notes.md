# Access Control Notes

## Authentication, Session Management, and Authorization

- Authentication verifies who the user is.
- Session management associates later HTTP requests with that authenticated user.
- Authorization determines whether the user may access a resource or perform an action.

Successful authentication does not automatically authorize every action.

## Vertical Access Control

Vertical access control restricts functionality according to the user's role or privilege level.

Example: an administrator may manage users, while a normal user must be denied access to user-management functions.

A normal user accessing administrator functionality is vertical privilege escalation.

## Horizontal Access Control

Horizontal access control restricts users to their own resources.

Example: one user may access their own account information but must not access another user's information.

## Context-Dependent Access Control

Context-dependent access control considers the application's current state or the order of actions.

Example: a customer may modify an order before payment but not after the payment has been completed.

## Unprotected Administrative Functionality

Removing an admin link from the interface does not protect the underlying endpoint. An attacker may discover and request the endpoint directly.

Authorization must be enforced by the server on both the administrative page and every privileged action.

## Security Through Obscurity

Hidden or unpredictable URLs may reduce discoverability, but they do not provide authorization.

Sensitive paths may be disclosed through:

- Client-side JavaScript
- HTML source
- Public metadata
- Application responses
- Browser or proxy history

Knowledge of a URL must never be treated as proof of authorization.

## Client-Controlled Authorization Information

Cookies, hidden fields, query parameters, and other browser-supplied values can be modified by the user.

The server should associate an opaque session identifier with trusted server-side user and role information. It must then verify the required permission for every protected request.

## Secure Design Principles

- Deny access by default.
- Enforce authorization server-side.
- Apply checks to every privileged endpoint.
- Use a centralized access-control mechanism.
- Follow least privilege.
- Do not rely on hidden links or unpredictable paths.
- Test access using multiple actors and roles.
