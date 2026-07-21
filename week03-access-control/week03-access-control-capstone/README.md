# Week 3 Access-Control Capstone — AcmeDocs

AcmeDocs is a local, multi-tenant authorization lab that compares an
intentionally vulnerable legacy API with a secure implementation of the same
core functions.

The project demonstrates the difference between authentication and
authorization, and between object-, property-, and function-level controls.

## Safety scope

- The server binds only to `127.0.0.1:8012`.
- `/api/v1` is intentionally vulnerable and must never be exposed externally.
- `/api/v2` is the secure comparison implementation.
- The actors and data are fictional and stored only in memory.
- Evidence uses `Cookie: session=REDACTED` and contains no passwords or real
  credentials.

## Scenario

The application contains two tenants, `alpha` and `beta`, and four actors:

| Actor | Tenant | Server-side role |
| --- | --- | --- |
| `alice` | `alpha` | `user` |
| `bob` | `beta` | `user` |
| `admin_alpha` | `alpha` | `tenant_admin` |
| `support_admin` | Platform scope | `support_admin` |

Each tenant has two documents. Normal users can read and update only their own
documents. A tenant administrator can operate on documents and exports inside
that administrator's tenant. The support administrator can run the explicit
support function and read audit events, but cannot read tenant documents.

## Version comparison

| Area | `/api/v1` | `/api/v2` |
| --- | --- | --- |
| Object authorization | Authentication only | Tenant and ownership policy |
| Writable properties | Arbitrary fields except `id` | `title` and `content` allowlist |
| Response properties | Internal object returned | Response allowlist |
| Organization export | Any authenticated actor | Matching `tenant_admin` only |
| Support operation | Any authenticated actor | `support_admin` only |
| Audit attribution | Missing | Recorded for privileged attempts |
| Unknown actions/methods | Route-specific behavior | Deny by default and `405` |

## Project layout

```text
week03-access-control-capstone/
├── README.md
├── app/
│   ├── authorization.py
│   ├── data.py
│   └── server.py
├── tests/
│   └── test_authorization.py
├── docs/
│   ├── architecture.md
│   ├── authorization-matrix.md
│   ├── findings.md
│   ├── remediation-review.md
│   └── threat-test-traceability.md
└── evidence/
    ├── automated-test-results.txt
    └── burp/
        ├── 01-bola-read-comparison.txt
        ├── 02-bola-update-comparison.txt
        ├── 03-mass-assignment-comparison.txt
        ├── 04-response-property-comparison.txt
        ├── 05-organization-export-comparison.txt
        └── 06-legacy-listing-comparison.txt
```

## Run locally

From the capstone directory:

```bash
python3 app/server.py
```

The server prints its local URL. A demo session can be created without a
password because authentication itself is not the subject of this local lab:

```bash
curl -sS -c /tmp/acme-alice.cookies \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice"}' \
  http://127.0.0.1:8012/demo-login
```

The cookie value must never be copied into evidence or documentation.

## Run the automated tests

```bash
python3 tests/test_authorization.py 2>&1 \
  | tee evidence/automated-test-results.txt
```

The completed run contains 48 tests, including 23 explicitly named negative
tests. The suite covers central policy behavior, authentication boundaries,
v1 vulnerability proofs, v2 positive cases, v2 negative cases, mutation
atomicity, property allowlists, method rejection, and audit attribution.

## Evidence and findings

Six Burp comparisons show the same actor and operation against both API
versions. Four formal findings cover:

- BOLA in document reads and updates;
- BOPLA and mass assignment;
- BFLA in privileged functions;
- legacy-policy discrepancy between v1 and v2.

The findings describe controlled local reproduction, remediation, and retest
results without publishing a usable session value.

## Security conclusion

The v2 implementation demonstrates central, deny-by-default authorization,
server-side identity attributes, object and property checks, atomic denial,
and auditable privileged operations. The v1 routes remain deliberately unsafe
for training. A production release would require v1 removal or policy parity,
real authentication, durable transactional storage, rate limiting, CSRF
protection, TLS, and production-grade audit retention.
