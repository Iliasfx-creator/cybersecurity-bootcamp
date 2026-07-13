# Authorization Bypass Notes

## Core authorization principle

Authentication establishes who the user is. Authorization determines whether
that user may perform a specific action on a specific resource under the
current conditions.

A reliable authorization decision should consider:

- actor,
- action,
- resource,
- role or ownership,
- relevant context.

The check must occur server-side at the endpoint that performs the sensitive
operation.

## URL-based access-control bypass

A frontend component may deny access to a protected URL while a backend
component determines the effective route from a different part of the request.

If these layers interpret routing information differently, a request can pass
the frontend filter but still reach a privileged backend handler.

This is a platform or routing misconfiguration. Protecting only the visible URL
does not protect the underlying operation.

### Correct design

- Canonicalize paths consistently.
- Reject unnecessary route-override inputs.
- Apply authorization inside the backend handler.
- Use the same authorization policy across proxies, gateways, and applications.

## Method-based access-control bypass

An application may correctly protect a state-changing operation when requested
with one HTTP method but accept another method without applying the same check.

The authorization policy belongs to the operation, not to one particular
request method.

### Correct design

- Explicitly allow only required HTTP methods.
- Reject unsupported methods.
- Apply identical authorization checks to every method capable of reaching the
  operation.
- Avoid using GET for state-changing actions.

## Multi-step workflow bypass

A sensitive workflow may contain input, review, and confirmation steps.
Protecting only the earlier steps is insufficient if the final state-changing
request can be submitted directly.

The final endpoint must not assume that an earlier page view proves
authorization.

### Correct design

- Authenticate and authorize the final action.
- Validate the workflow state server-side.
- Bind workflow state to the authenticated user.
- Revalidate important parameters before committing the change.

## Referer-based access-control bypass

The Referer header describes where a request appears to have originated, but it
is supplied by the client and can be modified or omitted.

It is not proof that the requester visited an authorized page and must never be
used as the primary authorization decision.

### Correct design

- Determine identity from a validated server-side session.
- Determine privilege from trusted server-side role data.
- Authorize the requested action directly.
- Treat origin-related headers only as supplementary security signals where
  appropriate, never as proof of privilege.

## URL-matching discrepancies

Different components may treat these paths differently:

- uppercase and lowercase characters,
- trailing slashes,
- repeated separators,
- encoded characters,
- decoded traversal sequences,
- alternate path representations.

Security controls and application routing must use the same normalized
representation.

## General remediation principles

- Deny access by default.
- Centralize authorization policy.
- Enforce authorization at the point of action.
- Check every read, create, update, and delete operation independently.
- Never treat obscurity, hidden links, hashes, or client-controlled metadata as
  authorization.
- Record authorization failures without exposing sensitive information.
