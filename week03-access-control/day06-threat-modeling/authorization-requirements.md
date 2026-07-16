
Testable Security Requirements
SR-01 — Concealed cross-tenant read denial

Given an authenticated user belonging to tenant A
When the user requests a valid document identifier belonging to tenant B
Then the API must return the same concealed denial used for a nonexistent
document and must not disclose document properties.

SR-02 — Cross-tenant mutation safety

Given a tenant-A user and a tenant-B document
When the user attempts to update or delete the tenant-B document
Then the request must be denied before mutation and the stored document must
remain unchanged.

SR-03 — Allowed same-tenant object action

Given a user authorized to edit a document inside the user's tenant
When the user submits an allowed document update
Then only the allowlisted properties must change and the action must be
attributed to that user.

SR-04 — Mass-assignment resistance

Given a normal document or profile update
When the client adds tenant_id, owner_id, role, or support-only properties
Then the server must reject or ignore those properties and must derive security
attributes from trusted server-side state.

SR-05 — Property-level response authorization

Given a user who may read an object but not its internal properties
When the API serializes that object
Then billing secrets, internal notes, storage keys and administrative
properties must be absent from the response.

SR-06 — Function-level export authorization

Given an authenticated normal user
When the user directly requests an organization export
Then the endpoint must deny the operation and no export job or output object
must be created.

SR-07 — Support function authorization

Given an actor without current support-administrator permission
When the actor invokes a cross-tenant support endpoint
Then the operation must be denied regardless of URL, method, header, or
frontend visibility.

SR-08 — Session revocation

Given an authenticated browser session
When that session is logged out or administratively revoked
Then every later replay of the same session must fail authentication.

SR-09 — Immediate role downgrade

Given a tenant administrator with an active session
When the role is downgraded to user
Then the next privileged request using the existing session must be denied.

SR-10 — Invitation binding

Given an invitation bound to one recipient, tenant, role and expiry
When any bound value is changed, the token expires, is revoked, or has already
been consumed
Then invitation acceptance must fail without creating membership.

SR-11 — API-version policy parity

Given an operation denied by the central authorization policy through
/api/v2
When the equivalent operation is attempted through /api/v1
Then /api/v1 must produce an equivalent denial or be unavailable.

SR-12 — Auditable privileged actions

Given an authorized tenant or support administrator
When a role, export, invitation, billing or cross-tenant action is attempted
Then an audit event must contain actor, target tenant, action, result,
timestamp, reason where required, and correlation identifier.

SR-13 — Resource limits

Given an authenticated tenant user
When the user exceeds configured export, upload, pagination or concurrency
limits
Then the service must return a controlled limit response without creating
additional expensive work.

SR-14 — Client tenant value is not authority

Given a tenant-A session
When the client supplies tenant B in a query parameter, body or header
Then the supplied value must not change the actor's authorized tenant context.

SR-15 — Scoped storage authorization

Given an authorized document download
When the backend creates storage access
Then the authorization must be limited to the approved object, operation and
short validity period.
