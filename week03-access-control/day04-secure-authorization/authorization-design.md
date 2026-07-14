# Authorization Design

## Design objective

The design must prevent both horizontal and vertical privilege escalation.

Horizontal protection ensures that Alice and Bob can access only their own
documents.

Vertical protection ensures that only the administrator can invoke role
management.

## Policy location

The central authorization policy is implemented in:

```text
app/authorization.py
```

The function accepts:

is_authorized(actor, action, resource=None)

It returns only an allow or deny decision.

HTTP response handling remains in the endpoint because the same denial can be
represented differently depending on context. A foreign document is concealed
with 404, while a denied administrative operation returns 403.

Trusted inputs

The actor's identity comes from the session cookie.

The session value is resolved through the server-side session store to a
username. The username is then resolved through the server-side user store to
a role.

The policy does not read requester privileges from:

query parameters,
form fields,
custom role headers,
hidden fields,
frontend state.
Policy actions

The policy defines explicit actions:

list documents,
read document,
update document,
change user role.

Any unknown actor, role, action, or incomplete resource context is denied.

Document authorization

For document reads and updates, access is allowed when:

actor is administrator
OR
document owner equals actor username

A valid document identifier alone never grants access.

Role-management authorization

Role management requires the actor's trusted server-side role to be admin.

The requested new role is client input because it describes the intended
target state. It does not describe the privileges of the acting user.

The actor is authorized before the requested role change is applied.

Endpoint enforcement flow

Protected endpoints follow this order:

Resolve the authenticated actor.
Validate the supplied object identifier or input.
Locate the requested resource.
Ask the centralized policy for the actor/action/resource decision.
Return a safe denial when authorization fails.
Perform the read or mutation only after authorization succeeds.
Mutation safety

A denied update returns before the assignment that changes document content.

Automated tests read the resource after a denied update and verify that its
content remains unchanged.

This catches failures where the server might return an error after already
performing the mutation.

Method enforcement

Each known route has an explicit allowed method.

Known routes invoked through an alternative method return 405 and an Allow
header. Alternative methods cannot reach the state-changing handler.

Object concealment

Foreign and nonexistent documents return the same 404 response.

This reduces object enumeration and avoids confirming that another user's
document exists.

Deny by default

The final policy outcome for any unmatched condition is deny.

New functionality therefore requires an explicit policy decision before it can
become accessible.
