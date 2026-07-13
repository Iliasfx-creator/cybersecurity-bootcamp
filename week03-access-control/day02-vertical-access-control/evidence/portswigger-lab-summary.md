# PortSwigger Lab Summary

## Unprotected admin functionality

Status: Solved

### Intended restriction

Administrative functionality should be accessible only to authorized administrators.

### Broken trust assumption

The application assumed that hiding the administrative path was sufficient protection.

### Discovery method

A publicly accessible application resource disclosed the existence of the administrative endpoint.

### Missing server-side control

The application did not verify authentication or administrator privileges before allowing access to privileged functionality.

### Remediation

Require authentication and enforce administrator authorization on both the admin page and every privileged action.

### Mistake or difficulty

The main difficulty was separating endpoint discovery from authorization. Discovering the endpoint should never be enough to gain access.

## Unprotected admin functionality with unpredictable URL

Status: Solved

### Intended restriction

Only administrators should be able to discover and access administrative functionality.

### Broken trust assumption

The application relied on an unpredictable URL as if it were an authorization mechanism.

### Discovery method

Client-side JavaScript disclosed the administrative path in an HTTP response.

### Missing server-side control

The server did not independently verify whether the requesting user had administrator privileges.

### Remediation

Keep authorization decisions server-side and enforce role checks for every administrative request.

### Mistake or difficulty

I initially focused on changing a client-side boolean value. The important issue was that the response disclosed the privileged path and the server did not protect it.

## User role controlled by request parameter

Status: Solved

### Intended restriction

An authenticated normal user should not be able to access administrator functionality.

### Broken trust assumption

The server trusted client-controlled role information supplied through a cookie.

### Discovery method

The login response and subsequent authenticated requests were examined using Burp Suite.

### Missing server-side control

The server did not retrieve and validate the user's actual role from trusted server-side data.

### Remediation

Use an opaque session identifier and load the authenticated user's permissions from trusted server-side storage. Enforce the required role on every privileged request.

### Mistake or difficulty

I initially examined the session identifier instead of the separate role-related value. This demonstrated the difference between session tracking and authorization information.

## Redaction

No passwords, session values, credentials, lab-specific URLs, or detailed solution values are included.
