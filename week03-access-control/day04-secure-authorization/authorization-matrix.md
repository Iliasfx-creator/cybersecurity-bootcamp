# Authorization Matrix

| Actor | Resource or function | Action | Expected | Status | Policy basis |
|---|---|---|---|---|---|
| Anonymous | Document list | Read | Deny | 401 | Authentication required |
| Anonymous | Any document | Read | Deny | 401 | Authentication required |
| Anonymous | Any document | Update | Deny | 401 | Authentication required |
| Anonymous | Role management | Update | Deny | 401 | Authentication required |
| Alice | Alice document | Read | Allow | 200 | Ownership |
| Alice | Alice document | Update | Allow | 200 | Ownership |
| Alice | Bob document | Read | Deny | 404 | Ownership mismatch |
| Alice | Bob document | Update | Deny | 404 | Ownership mismatch |
| Bob | Bob document | Read | Allow | 200 | Ownership |
| Bob | Bob document | Update | Allow | 200 | Ownership |
| Bob | Alice document | Read | Deny | 404 | Ownership mismatch |
| Bob | Alice document | Update | Deny | 404 | Ownership mismatch |
| Administrator | Alice document | Read/update | Allow | 200 | Admin role |
| Administrator | Bob document | Read/update | Allow | 200 | Admin role |
| Alice or Bob | Role management | Update | Deny | 403 | Admin role required |
| Administrator | Role management | Update | Allow | 200 | Admin role |
| Alice with client-supplied admin role | Role management | Update | Deny | 403 | Client role ignored |
| Authenticated actor | Known route using wrong method | Any | Deny | 405 | Method allowlist |
| Authenticated actor | Invalid object ID | Read/update | Deny | 400 | Input validation |
| Authenticated actor | Nonexistent object | Read/update | Deny | 404 | Object not found |
| Any actor | Unknown action | Any | Deny | Varies | Deny-by-default policy |

## Important distinction

RBAC protects privileged functions such as role management.

Ownership authorization protects individual documents belonging to users.

The secure implementation combines both models instead of relying on only one.
