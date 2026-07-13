# TryHackMe — Broken Access Control

Completion: 100%

## Topics Covered

- Access-control fundamentals
- Role-Based Access Control
- Attribute-Based Access Control
- Horizontal privilege escalation
- Vertical privilege escalation
- Application assessment
- HTTP request and response inspection with Burp Suite
- Access-control remediation

## RBAC

Role-Based Access Control assigns permissions according to roles such as user, moderator, or administrator.

RBAC is only effective when the server validates the authenticated user's real role before every protected action.

## ABAC

Attribute-Based Access Control makes authorization decisions using attributes such as:

- User identity or department
- Resource ownership
- Requested action
- Time, location, or application state

## Vertical Privilege Escalation

Vertical privilege escalation occurs when a lower-privileged user accesses functionality intended for a higher-privileged role.

Common causes include:

- Unprotected privileged endpoints
- Client-controlled role parameters
- Missing server-side authorization
- Reliance on hidden interface elements
- Inconsistent checks between related actions

## Assessment Method

1. Identify the available actors and roles.
2. Identify privileged functions and resources.
3. Capture requests using Burp Suite.
4. Determine which values influence authorization.
5. Compare expected and observed access.
6. Verify whether authorization is enforced server-side.
7. Document the missing control and appropriate remediation.

## Main Takeaway

The browser and all client-supplied values must be treated as untrusted. Authorization decisions should be made by the server using trusted identity, session, role, ownership, and contextual information.

## Redaction

No room answers, flags, credentials, IP addresses, cookies, or session values are stored in these notes.
