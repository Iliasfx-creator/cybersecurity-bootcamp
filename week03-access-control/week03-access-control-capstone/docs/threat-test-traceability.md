# Day 6 Threat-to-Test Traceability

This table connects the capstone to the AcmeDocs Day 6 threat register and
testable security requirements. It references the exact Day 6 IDs rather than
creating a second threat taxonomy.

| Day 6 threat | Requirement | Capstone control or demonstration | Automated verification | Burp/report evidence | Status |
| --- | --- | --- | --- | --- | --- |
| T-01 — Cross-tenant document disclosure | SR-01 | v2 checks tenant and ownership and conceals denial | Tests 33–36 and 46 | Evidence 01; F-01 | Covered |
| T-02 — Cross-tenant document or storage mutation | SR-02 | v2 authorizes before update and preserves denied state | Test 37 | Evidence 02; F-01 | Document mutation covered; storage outside scope |
| T-03 — Mass assignment of tenant, owner or role | SR-04 | Server-side identity plus v2 write allowlist and atomic rejection | Tests 12, 38–40 | Evidence 03; F-02 | Covered |
| T-04 — Unauthorized property disclosure | SR-05 | v2 response serializer uses an explicit allowlist | Test 32 | Evidence 04; F-02 | Covered |
| T-05 — Unauthorized organization export | SR-06 | Matching `tenant_admin` and tenant required | Tests 19, 27, 41–42 | Evidence 05; F-03 | Covered |
| T-06 — Unauthorized support-administrator function | SR-07 | Only `support_admin` may run support unlock | Tests 7–8, 20, 28, 43 | F-03 | Covered |
| T-07 — Stolen or replayed browser session | SR-08 | Logout removes the server-side session mapping | Test 13 | Architecture session model | Logout replay covered; theft detection outside scope |
| T-10 — Deprecated `/api/v1` authorization bypass | SR-11 | Six comparisons prove v1/v2 discrepancy; v2 uses central policy | Tests 14–21 and 22–45 | Evidence 01–06; F-04 | Demonstrated; remains open until v1 retirement/parity |
| T-11 — Audit tampering or missing attribution | SR-12 | v2 records server-derived attribution and outcome for privileged attempts | Tests 29–30, 41, 43 | F-03; remediation review | Attribution covered; durable integrity outside scope |
| T-13 — Client-controlled tenant-context override | SR-14 | Actor tenant and role come from canonical server state | Tests 12, 38–40 | Evidence 03; authorization matrix | Covered |

## Additional capstone checks

| Control objective | Tests |
| --- | --- |
| Deny missing actor and unknown action | 1, 2, 9, 10 |
| Allow legitimate owner and administrator operations | 3, 5, 22–28 |
| Scope collection results per object | 21 and 31 |
| Reject alternate HTTP method | 45 |
| Handle nonexistent object safely | 46 |
| Reject invalid JSON without mutation | 47 |
| Deny unknown route | 48 |

## Coverage interpretation

The capstone directly implements and tests ten Day 6 threat/requirement pairs.
Invitation abuse, immediate role-downgrade propagation, unrestricted resource
consumption, and signed object-storage access require components not present in
this small in-memory API. They remain explicit future security-test work rather
than being marked as falsely covered.
