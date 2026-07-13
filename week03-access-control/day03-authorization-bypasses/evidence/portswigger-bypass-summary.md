# PortSwigger Authorization Bypass Summary

## URL-based access control can be circumvented

Status: Solved

### Intended authorization policy

Only administrators should reach and use administrative functionality.

### Normal denied request

A lower-privileged request to the canonical administrative route was denied.

### Trusted layer

A frontend or intermediary URL filter was trusted to protect the backend
functionality.

### Client-controlled input

An alternative routing instruction supplied through the request.

### Bypass category

URL-based and platform-routing authorization bypass.

### Root cause

The frontend and backend determined the effective route from different request
components. Authorization was not enforced by the backend operation itself.

### Correct remediation

Apply authorization inside every privileged backend handler, use consistent
path canonicalization across layers, and reject unnecessary route-override
inputs.

### Mistake or difficulty

I initially modified too much of the request and produced an invalid-host
response. Starting from a clean captured request and changing one component at
a time made the routing discrepancy clear.

## Method-based access control can be circumvented

Status: Solved

### Intended authorization policy

Only administrators should be able to modify user roles.

### Normal denied request

The normal state-changing request was denied when replayed with a
lower-privileged identity.

### Trusted layer

A method-specific authorization rule.

### Client-controlled input

The HTTP method used to invoke the operation.

### Bypass category

Method-based authorization bypass.

### Root cause

The application enforced authorization for one method but accepted an
alternative method that reached the same operation without an equivalent
check.

### Correct remediation

Allow only the required methods and apply the same server-side role check to
every method that can reach the state-changing operation.

### Mistake or difficulty

My initial test used an account whose role had already been changed during the
normal flow. Resetting the lab and obtaining a fresh lower-privileged session
produced a valid test baseline.

## Multi-step process with no access control on one step

Status: Solved

### Intended authorization policy

Only administrators should complete the workflow that changes a user's role.

### Normal denied request

A lower-privileged user could not legitimately begin the protected
administrative workflow.

### Trusted layer

The application trusted the order of the workflow and assumed that reaching
the confirmation step meant earlier authorization had succeeded.

### Client-controlled input

A direct request to the final state-changing step.

### Bypass category

Multi-step workflow authorization bypass.

### Root cause

The final action did not independently verify the requester's authorization.

### Correct remediation

Authenticate and authorize the final state-changing request, maintain trusted
workflow state server-side, and revalidate all sensitive parameters before
committing the action.

### Mistake or difficulty

The main difficulty was distinguishing the review request from the request
that actually committed the role change.

## Referer-based access control

Status: Solved

### Intended authorization policy

Only administrators should be able to invoke the role-management operation.

### Normal denied request

A lower-privileged request without the expected administrative navigation
context was denied.

### Trusted layer

The server trusted the Referer header as evidence that the request originated
from an administrative page.

### Client-controlled input

The Referer header.

### Bypass category

Header-based authorization bypass.

### Root cause

Client-controlled navigation metadata was treated as proof of administrative
privilege instead of checking the authenticated user's role.

### Correct remediation

Derive identity and role from trusted server-side data and authorize the
requested operation directly. Do not use Referer as proof of authorization.

### Mistake or difficulty

I first had to distinguish the request that loaded the administrative page
from the request that performed the privileged action.
