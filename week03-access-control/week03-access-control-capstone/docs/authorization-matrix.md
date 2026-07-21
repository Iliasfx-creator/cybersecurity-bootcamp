# AcmeDocs Authorization Matrix

## Actors

| Actor | Tenant | Role | Intended scope |
| --- | --- | --- | --- |
| Unauthenticated | None | None | No API access |
| `alice` | `alpha` | `user` | Alice-owned Alpha documents |
| `bob` | `beta` | `user` | Bob-owned Beta documents |
| `admin_alpha` | `alpha` | `tenant_admin` | All Alpha documents and Alpha export |
| `support_admin` | Platform | `support_admin` | Support operations and audit events |

## Function and object policy

`Allow` below means the v2 central policy explicitly grants the action.
`Deny (404)` conceals document existence. `Deny (403)` is used for an
authenticated actor who lacks permission for a known privileged function.

| Actor | List documents | Own document read/update | Other document in same tenant | Cross-tenant document | Own-tenant export | Other-tenant export | Support unlock | Read audit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unauthenticated | Deny (401) | Deny (401) | Deny (401) | Deny (401) | Deny (401) | Deny (401) | Deny (401) | Deny (401) |
| `alice` / `bob` | Allow, object-filtered | Allow | Deny (404) | Deny (404) | Deny (403) | Deny (403) | Deny (403) | Deny (403) |
| `admin_alpha` | Allow, tenant-filtered | Allow | Allow within Alpha | Deny (404) | Allow for Alpha | Deny (403) | Deny (403) | Deny (403) |
| `support_admin` | Deny (403) | Deny (404) | Deny (404) | Deny (404) | Deny (403) | Deny (403) | Allow for known tenant | Allow |

## Document property policy

| Property | Client may write in v2 | Returned in v2 | Authority/source |
| --- | ---: | ---: | --- |
| `id` | No | Yes | Server-created object identity |
| `tenant_id` | No | No | Server-side object relationship |
| `owner_id` | No | Yes | Server-side ownership relationship |
| `title` | Yes | Yes | Allowlisted business field |
| `content` | Yes | Yes | Allowlisted business field |
| `internal_label` | No | No | Internal-only metadata |
| `role` | No | No | Canonical server-side user record |

## Decision rules

- Invalid or missing actors are denied.
- Unknown actions are denied.
- A normal user must match both the document tenant and `owner_id`.
- A tenant administrator must match the document or export tenant.
- The support administrator has no implicit document access.
- Query, header, or body values cannot replace the canonical actor tenant or
  role.
- Collection endpoints apply object authorization to every returned item.
- Unsupported methods return `405` with the allowed methods.
- Denied or invalid updates do not partially mutate state.
