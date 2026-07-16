# AcmeDocs System Model

## Security invariant

Every request must be authorized using the authenticated actor, trusted tenant
membership, requested action, target object, and current role.

Client-provided tenant identifiers, roles, ownership fields, object identifiers,
headers, paths, and workflow state are untrusted inputs.

## Actors

| Actor | Description | Primary risk |
|---|---|---|
| Anonymous visitor | Has no valid session | Authentication bypass |
| Tenant user | Works inside one tenant | Cross-tenant object access |
| Tenant administrator | Manages one tenant | Cross-tenant or excessive administration |
| Support administrator | Performs approved support operations | High-impact cross-tenant misuse |
| External attacker | Controls requests but has no legitimate authority | Session theft and resource abuse |
| Internal operator | Maintains services and infrastructure | Excessive data or log access |
| Email recipient | Receives invitation links | Invitation forwarding or replay |

## Roles and intended permissions

### user

- Read and update permitted documents inside the user's tenant.
- Download permitted tenant objects.
- Use ordinary account functions.
- Cannot manage roles, billing, invitations, or organization exports.

### tenant_admin

- Includes normal tenant-user permissions.
- Manages users and invitations only inside the administrator's tenant.
- Views permitted billing information for that tenant.
- Starts organization exports only for that tenant.
- Cannot perform cross-tenant support operations.

### support_admin

- Uses a separate support workflow.
- May access another tenant only for an approved support reason.
- Every cross-tenant action requires explicit target selection, current
  permission, step-up authentication, and audit attribution.
- Support access must not be inferred only from a hidden interface or URL.

## Assets

- Document contents and metadata
- Object-storage files and storage keys
- Tenant identifiers and membership relationships
- User identities, roles and invitation state
- Browser sessions and session-revocation state
- Billing records
- Organization exports
- Audit events and actor attribution
- API schemas and endpoint inventory
- Availability and processing capacity
- Email invitation tokens

## Entry points

- Browser application
- Authentication and logout endpoints
- `/api/v1` deprecated endpoints
- `/api/v2` current endpoints
- Document read, update, delete and download endpoints
- Invitation creation and acceptance endpoints
- Role-management endpoints
- Billing endpoints
- Organization-export endpoints
- Support-administration endpoints
- Object-storage signed URLs
- API headers, query parameters and JSON properties

## Data stores

- Primary relational database
- Object storage
- Session or revocation store
- Organization-export storage
- Append-oriented audit-log service

## External dependencies

- Email-delivery service
- Identity or authentication provider
- Object-storage provider
- Billing provider
- Monitoring and alerting platform

## Main data flows

### Document request

1. The browser sends a session-authenticated request to the API gateway.
2. The gateway applies transport, routing, and coarse resource controls.
3. The backend authenticates the session.
4. The backend resolves current tenant membership and role.
5. Authorization is evaluated before retrieving or mutating the object.
6. The database query includes the authorized tenant relationship.
7. The action and result are sent to the audit service when required.

### Document download

1. The backend authorizes the actor and document.
2. The backend resolves the storage object.
3. A short-lived, narrowly scoped download authorization is created.
4. The download event is attributed in the audit log.

### Invitation flow

1. A tenant administrator creates an invitation.
2. The backend binds the token to tenant, intended role, recipient and expiry.
3. The email service delivers the link.
4. Acceptance validates the complete binding.
5. Successful acceptance consumes the token once.

### Organization export

1. The backend validates current tenant-administrator permission.
2. An asynchronous export job is created with quotas.
3. The job reads only records belonging to the authorized tenant.
4. Output is stored with limited retention and download authorization.
5. Creation and download are recorded in audit logs.

## Trust boundaries

### TB-1 — User-controlled client to public edge

The browser, URL, headers, methods, parameters, cookies and JSON bodies are
untrusted. TLS protects transport but does not make client input trustworthy.

### TB-2 — API gateway to backend API

The gateway may authenticate or route requests, but endpoint-level
authorization remains mandatory in the backend that performs the operation.

### TB-3 — Backend API to data services

The backend crosses into databases, storage and audit services. Queries and
storage operations must remain tenant-scoped.

### TB-4 — Internal system to external email provider

Only necessary invitation data should leave the trusted application. Tokens
must be short-lived, single-use and safe if an email is forwarded.

### TB-5 — Tenant context to support context

Cross-tenant support access is a privilege boundary. It requires explicit
authorization, step-up authentication, justification and audit attribution.

### TB-6 — Current `/api/v2` to deprecated `/api/v1`

Both versions expose the same assets through different entry points. The old
version must not retain weaker authorization or validation.

## Security assumptions requiring validation

| Assumption | Validation |
|---|---|
| Tenant identity comes from trusted session state | Attempt query, body and header tenant overrides |
| Role changes apply immediately | Reuse a session after role downgrade |
| API gateway and backend agree on routing | Test path normalization and both API versions |
| Object storage cannot bypass backend policy | Test leaked, expired and cross-tenant object URLs |
| Audit events cannot be silently modified | Verify append-only permissions and integrity monitoring |
| Invitation tokens are single-use | Replay an accepted invitation |
| Export jobs are tenant-scoped | Inspect an export using mixed-tenant fixture data |
