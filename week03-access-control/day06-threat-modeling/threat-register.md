
AcmeDocs Threat Register
Rating approach

Likelihood and severity are qualitative design-review ratings:

Likelihood: Low, Medium or High
Severity: Medium, High or Critical

Every mitigation is connected to a verification test in
security-test-plan.md.

T-01 — Cross-tenant document disclosure
Component: Backend document API and database
Asset: Document contents and metadata
STRIDE category: Information Disclosure
Precondition: A tenant-A user has a valid session and learns a valid
document identifier belonging to tenant B.
Abuse case: The user changes the identifier in a legitimate read request
and receives tenant B's document.
Impact: Cross-company confidentiality breach and possible regulatory harm.
Likelihood: High
Severity: Critical
Mitigation: Resolve the tenant from trusted session membership and query
documents by both object identifier and authorized tenant. Return the same
concealed denial used for a nonexistent object.
Verification test: ST-01
Residual risk: Incorrect sharing relationships or migration data could
still associate an object with the wrong tenant.
T-02 — Cross-tenant document or storage mutation
Component: Document update/delete API and object storage
Asset: Documents and stored files
STRIDE category: Tampering
Precondition: A tenant-A user knows a tenant-B document or storage
identifier.
Abuse case: The user sends an update or delete request for the foreign
object and the backend applies the mutation.
Impact: Destruction or unauthorized alteration of another tenant's data.
Likelihood: High
Severity: Critical
Mitigation: Authorize actor, action, object and tenant immediately before
every mutation. Scope storage operations to an authorized document and verify
that denial occurs before any write.
Verification test: ST-02
Residual risk: Race conditions between authorization and mutation require
transactional enforcement.
T-03 — Mass assignment of tenant, owner or role
Component: JSON create/update handlers
Asset: Tenant boundaries, ownership and user roles
STRIDE category: Elevation of Privilege
Precondition: An authenticated user can submit additional JSON properties.
Abuse case: The user adds tenant_id, owner_id, role, or support
properties to a normal update and the object mapper persists them.
Impact: Tenant escape, ownership transfer or administrative privilege.
Likelihood: High
Severity: Critical
Mitigation: Use explicit request schemas and per-operation allowlists.
Derive tenant, owner and role from trusted server-side state and reject
unknown sensitive properties.
Verification test: ST-03
Residual risk: New writable properties may become sensitive as the product
evolves and require schema review.
T-04 — Unauthorized property disclosure
Component: API response serialization
Asset: Billing fields, internal notes, storage keys and user properties
STRIDE category: Information Disclosure
Precondition: The actor may legitimately read an object but is not
authorized for all of its properties.
Abuse case: The API returns an internal database object and relies on the
frontend to hide restricted fields.
Impact: Exposure of sensitive business, storage or account information.
Likelihood: Medium
Severity: High
Mitigation: Define response schemas per operation and role. Return only
properties required by the authorized use case.
Verification test: ST-04
Residual risk: Aggregated fields may still reveal sensitive relationships.
T-05 — Unauthorized organization export
Component: Organization-export API
Asset: Complete tenant document and membership dataset
STRIDE category: Elevation of Privilege
Precondition: A normal user discovers the export endpoint.
Abuse case: The user directly invokes the export function that is visible
only to tenant administrators in the frontend.
Impact: Bulk disclosure of tenant data.
Likelihood: Medium
Severity: Critical
Mitigation: Enforce current tenant-administrator permission in the export
endpoint and inside the asynchronous worker. Bind the job and output to the
authorized tenant.
Verification test: ST-05
Residual risk: A compromised tenant-administrator account retains
legitimate but high-impact export capability.
T-06 — Unauthorized support-administrator function
Component: Support administration API
Asset: Cross-tenant user and document administration
STRIDE category: Elevation of Privilege
Precondition: A tenant user or tenant administrator discovers a support
endpoint.
Abuse case: The actor invokes a cross-tenant support action because the
backend relies on a hidden UI or route.
Impact: Cross-tenant modification at platform scale.
Likelihood: Medium
Severity: Critical
Mitigation: Require current support-administrator permission, step-up
authentication, explicit target tenant, approved reason and audit event at
the endpoint performing the action.
Verification test: ST-06
Residual risk: Malicious or compromised support administrators require
monitoring and operational approval controls.
T-07 — Stolen or replayed browser session
Component: Session management
Asset: User identity and authorized session
STRIDE category: Spoofing
Precondition: An attacker obtains a valid session value.
Abuse case: The attacker replays the session from another browser after
password change, logout or suspicious activity.
Impact: Account impersonation and access to tenant resources.
Likelihood: Medium
Severity: High
Mitigation: Use secure, HttpOnly and SameSite cookies, session rotation,
limited lifetime, server-side revocation, logout invalidation and
risk-sensitive reauthentication.
Verification test: ST-07
Residual risk: A session may be abused before detection or revocation.
T-08 — Stale privileges after role downgrade
Component: Authorization cache and session state
Asset: Administrative functions
STRIDE category: Elevation of Privilege
Precondition: A tenant administrator is downgraded while an existing
session or token contains the old role.
Abuse case: The downgraded user continues creating invitations or exports
with cached privileges.
Impact: Unauthorized administrative actions after access removal.
Likelihood: High
Severity: High
Mitigation: Resolve current permissions on each privileged request or use
a server-side authorization version that invalidates stale sessions when
membership changes.
Verification test: ST-08
Residual risk: Distributed cache propagation may create a short,
documented revocation delay.
T-09 — Invitation manipulation or replay
Component: Invitation creation and acceptance workflow
Asset: Tenant membership and assigned role
STRIDE category: Spoofing
Precondition: An attacker receives, intercepts or is forwarded an
invitation link.
Abuse case: The attacker changes the tenant or role, accepts for a
different identity, reuses the token, or accepts after revocation.
Impact: Unauthorized tenant membership or privilege.
Likelihood: Medium
Severity: High
Mitigation: Bind a cryptographically random token to recipient, tenant,
role, expiry and one-time state. Store a token hash and validate every bound
value at acceptance.
Verification test: ST-09
Residual risk: Compromise of the invited email account can still permit
acceptance before revocation.
T-10 — Deprecated /api/v1 authorization bypass
Component: API gateway and legacy backend route
Asset: All tenant objects and privileged functions
STRIDE category: Elevation of Privilege
Precondition: /api/v1 remains reachable while security work focuses on
/api/v2.
Abuse case: An actor repeats a denied v2 operation through v1 and reaches
older authorization logic.
Impact: Reintroduction of BOLA, BOPLA or BFLA through a forgotten endpoint.
Likelihood: High
Severity: Critical
Mitigation: Route both versions through one central authorization policy,
maintain an endpoint inventory, run parity tests and retire v1 with a defined
deadline.
Verification test: ST-10
Residual risk: Unknown clients may delay retirement and extend exposure.
T-11 — Audit-log tampering or missing attribution
Component: Backend and audit-log service
Asset: Security investigation evidence
STRIDE category: Repudiation
Precondition: A privileged action can omit actor, tenant, target, reason or
request identifiers, or an operator can modify stored events.
Abuse case: A support administrator changes tenant data without a
trustworthy record and later denies the action.
Impact: Failed investigations, weak accountability and compliance risk.
Likelihood: Medium
Severity: High
Mitigation: Generate audit events server-side with authenticated actor,
target tenant, action, result and correlation identifier. Restrict mutation,
monitor gaps and protect retention and integrity.
Verification test: ST-11
Residual risk: Logging-service outages require a documented failure and
recovery policy.
T-12 — Unrestricted resource consumption
Component: Export, upload, search and pagination endpoints
Asset: Availability and operational cost
STRIDE category: Denial of Service
Precondition: An authenticated user can repeatedly request expensive work.
Abuse case: The actor creates many exports, uploads oversized objects or
requests unbounded result sets.
Impact: Queue exhaustion, increased cost and degraded availability for
other tenants.
Likelihood: High
Severity: High
Mitigation: Apply per-actor and per-tenant quotas, size limits, pagination
caps, concurrency controls, timeouts and asynchronous job limits.
Verification test: ST-12
Residual risk: Coordinated abuse across many legitimate accounts may
require global adaptive controls.
T-13 — Client-controlled tenant-context override
Component: Gateway and backend request parsing
Asset: Tenant isolation
STRIDE category: Elevation of Privilege
Precondition: Requests accept a tenant identifier in a header, query
parameter or JSON body.
Abuse case: A tenant-A user supplies tenant B as tenant_id or
X-Tenant-ID and the backend uses it as the authorization context.
Impact: Cross-tenant access to multiple APIs.
Likelihood: High
Severity: Critical
Mitigation: Derive tenant membership from trusted identity state. Treat
client tenant values only as object selectors that still require policy
authorization. Use a separate audited support workflow.
Verification test: ST-13
Residual risk: Multi-tenant users require carefully modeled membership
selection.
T-14 — Leaked or replayed object-storage URL
Component: Object-storage download flow
Asset: Stored document files
STRIDE category: Information Disclosure
Precondition: A valid signed URL is copied from browser history, email,
analytics or logs.
Abuse case: Another person reuses the URL outside the original authorized
workflow.
Impact: Document disclosure without a current application session.
Likelihood: Medium
Severity: High
Mitigation: Authorize before URL creation, scope the signature to one
object and method, use a short expiry, avoid logging complete URLs and support
revocation for high-risk downloads.
Verification test: ST-14
Residual risk: The authorized recipient can still copy downloaded content.
