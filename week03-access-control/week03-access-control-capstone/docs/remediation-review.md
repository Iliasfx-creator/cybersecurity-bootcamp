# AcmeDocs Remediation Review

## Review outcome

The secure v2 path correctly addresses the authorization failure classes
demonstrated by v1. The review result is suitable for a local educational
comparison, but not for production while the intentionally vulnerable v1
routes remain reachable.

## Control comparison

| Security concern | Vulnerable v1 behavior | Secure v2 control | Verification |
| --- | --- | --- | --- |
| Cross-tenant read | Any authenticated actor can select any document | Central tenant and ownership policy with concealed denial | Tests 33–36; evidence 01 |
| Cross-tenant update | Foreign object is mutated | Authorization before mutation; denied state unchanged | Test 37; evidence 02 |
| Mass assignment | Arbitrary properties are persisted | `title`/`content` write allowlist; atomic rejection | Tests 38–39; evidence 03 |
| Property disclosure | Internal object is serialized | Explicit response allowlist | Test 32; evidence 04 |
| Organization export | Authentication is sufficient | Matching `tenant_admin` required | Tests 27, 41–42; evidence 05 |
| Support function | Authentication is sufficient | `support_admin` required | Tests 28 and 43 |
| Collection listing | All tenants and properties returned | Per-object policy and response filtering | Test 31; evidence 06 |
| Client role/tenant | Extra values may reach weak handlers | Canonical server-side actor; client values ignored or rejected | Tests 12, 39–40 |
| Methods/routes | Risk of alternate access path | Explicit route methods and deny-by-default dispatch | Tests 45 and 48 |
| Privileged attribution | Missing | Allowed and denied attempts recorded server-side | Tests 29–30, 41, 43 |

## Why the v2 placement is effective

The request handler resolves the actor from server-side session state and calls
one policy using an explicit action. Object authorization happens after the
target is loaded but before response or mutation. Full property validation
happens before any allowed update field is written. These placements protect
the action itself rather than a frontend route or normal navigation path.

## Denial behavior

- Missing or invalid authentication returns `401`.
- Unauthorized or nonexistent documents return the same `404` response to
  reduce identifier disclosure.
- Known privileged functions return `403` when the actor is authenticated but
  lacks permission.
- Unsupported methods return `405` and an `Allow` header.
- Invalid input returns `400` or the relevant content/body error without
  changing state.

## Audit review

The v2 export, support, and audit-log functions create events using the
server-resolved actor. Events contain timestamp, actor, actor role, action,
target, and outcome. Denied privileged attempts are also recorded.

For production, events should additionally include a correlation identifier,
approved reason where required, source context, integrity protection, durable
retention, access monitoring, and an explicit policy for logging-service
failure.

## Residual risk and production work

- Remove v1 or give it complete policy parity before any deployment.
- Replace demo login with real authentication and secure session expiry,
  rotation, revocation, and reauthentication.
- Add CSRF protection for cookie-authenticated state-changing requests.
- Enforce tenant-scoped queries and mutations transactionally in the database;
  consider defense-in-depth row-level controls.
- Add rate limits, quotas, pagination caps, request timeouts, and concurrency
  limits.
- Protect transport with TLS and apply production cookie attributes.
- Store audit events in a durable, append-oriented service with restricted
  mutation and monitored delivery.
- Test race conditions, role downgrade, invitation flows, object storage, and
  distributed authorization-cache invalidation in the full product.

## Release decision

The v2 authorization design passes the capstone's defined local tests. A
production release remains blocked until the legacy policy discrepancy is
closed and the intentionally simplified authentication, persistence, audit,
and availability controls are replaced with production implementations.
