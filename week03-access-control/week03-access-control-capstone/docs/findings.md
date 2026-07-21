# AcmeDocs Security Findings

All findings were reproduced only against the intentionally vulnerable local
`/api/v1` implementation on `127.0.0.1`. The corresponding `/api/v2` requests
are the remediation retests.

## F-01 — Broken Object Level Authorization in document operations

- **Category:** OWASP API1:2023 Broken Object Level Authorization (BOLA)
- **Severity:** Critical
- **Affected component:** `/api/v1/documents/{document_id}` read and update
- **Precondition:** The attacker has any valid fictional application session
  and knows or guesses another tenant's document identifier.
- **Impact:** A tenant user can disclose or alter another tenant's document,
  causing a direct confidentiality and integrity breach.

### Root cause

The v1 handler checks only whether a session is authenticated. It retrieves the
client-selected document by identifier and never verifies the actor's tenant,
ownership, role, or permission for the requested action.

### Controlled reproduction

Using Alice's Alpha-tenant session, a read for the Beta document
`beta-2001` returned `200`. A v1 update of the same object also returned `200`
and changed its content. Session values were redacted from evidence.

Evidence:

- `evidence/burp/01-bola-read-comparison.txt`
- `evidence/burp/02-bola-update-comparison.txt`

### Remediation

Resolve the actor from trusted session state and authorize actor, action,
object, tenant, and ownership immediately before every read or mutation. Use
the same policy for item and collection endpoints. Conceal unauthorized object
existence with the same response used for a nonexistent document.

### Retest

The same v2 read and update returned `404`. Test 33 verifies cross-tenant read
denial, and test 37 verifies that the denied update leaves the document
unchanged. Tests 34 through 36 cover additional ownership, tenant, and
administrator boundary cases.

## F-02 — Broken Object Property Level Authorization and mass assignment

- **Category:** OWASP API3:2023 Broken Object Property Level Authorization
  (BOPLA)
- **Severity:** Critical
- **Affected component:** v1 document update and response serialization
- **Precondition:** An authenticated user can update a document or read an
  otherwise authorized object.
- **Impact:** A client can transfer ownership, change tenant association, or
  receive internal metadata. Changing security properties can enable later
  tenant-boundary bypasses.

### Root cause

The v1 update copies every client property except `id` into the stored object,
and the v1 serializer returns the complete internal object. It has neither an
operation-specific write schema nor a response allowlist.

### Controlled reproduction

A v1 update included `owner_id` and `tenant_id` beside an ordinary `content`
change. The response showed that all three properties were stored. A normal v1
read also disclosed `tenant_id` and `internal_label`.

Evidence:

- `evidence/burp/03-mass-assignment-comparison.txt`
- `evidence/burp/04-response-property-comparison.txt`

### Remediation

Use explicit request and response schemas per operation. Derive tenant,
ownership, and role from trusted server-side state. Reject unknown sensitive
properties before changing any field, and serialize only the properties needed
for the authorized use case.

### Retest

The v2 mass-assignment request returned `400` and made no partial change. Its
normal read omitted the internal properties. Tests 32, 38, and 39 verify the
response allowlist, atomic request rejection, and rejection of a supplied role.

## F-03 — Broken Function Level Authorization in privileged operations

- **Category:** OWASP API5:2023 Broken Function Level Authorization (BFLA)
- **Severity:** Critical
- **Affected component:** v1 organization export and support unlock functions
- **Precondition:** The actor has any valid fictional session and discovers a
  privileged endpoint.
- **Impact:** A normal tenant user can perform bulk export or platform support
  functions that should require an administrative role.

### Root cause

The v1 privileged handlers treat authentication as authorization. They do not
check current role, target tenant, actor-target relationship, or function-level
permission, and the support action has no audit attribution.

### Controlled reproduction

Alice invoked the Alpha organization export through v1 and received `200` with
both Alpha documents. The automated suite separately confirms that a normal
user can invoke the v1 support operation.

Evidence:

- `evidence/burp/05-organization-export-comparison.txt`
- automated tests 19 and 20

### Remediation

Require the current server-side permission at the endpoint performing the
operation. Restrict exports to a tenant administrator whose tenant matches the
target. Restrict support operations to the support-administrator role and
record attributable audit events for both allowed and denied attempts.

### Retest

The same v2 export request returned `403`. Tests 27, 28, 41, 42, and 43 verify
allowed administrative paths and denied lower-privilege or cross-tenant paths.
Tests 29 and 30 validate audit attribution and authorized audit access.

## F-04 — Legacy API policy discrepancy bypasses secure v2 controls

- **Category:** Legacy authorization-policy discrepancy
- **Severity:** Critical
- **Affected component:** Reachable `/api/v1` routes
- **Precondition:** A user can select the legacy API version after an equivalent
  v2 operation is denied or filtered.
- **Impact:** v2 controls can be bypassed by repeating the operation through v1,
  reintroducing BOLA, BOPLA, BFLA, and excessive data exposure.

### Root cause

The API versions do not share one authorization enforcement point. v2 invokes
the central policy and property allowlists, while v1 implements weaker,
route-local authentication checks.

### Controlled reproduction

Alice's v1 collection request returned all four documents from both tenants and
included internal properties. The v2 collection returned only Alice's
authorized `alpha-1001` object and filtered its properties.

Evidence:

- `evidence/burp/06-legacy-listing-comparison.txt`
- all six v1/v2 comparison files

### Remediation

Retire v1 or route every version through the same central authorization and
serialization policy. Maintain an endpoint inventory, add version-parity
security tests, monitor v1 use, publish a deprecation deadline, and remove the
legacy routes after migration.

### Retest

Test 31 confirms the secure v2 collection is object-filtered. Tests 14 through
21 intentionally preserve proof that v1 is vulnerable. Therefore the finding
is remediated in v2 but remains open as a production release blocker until v1
is unavailable or reaches policy parity.
