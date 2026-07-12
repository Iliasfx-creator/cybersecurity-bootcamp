# Week 3 Day 1 — IDOR Fundamentals

## Goal

This lab demonstrates Broken Access Control through read and write IDOR vulnerabilities.

The central distinction is:

- Authentication determines who the current user is.
- Authorization determines whether that user may access a specific resource.

The vulnerable endpoints authenticate the user but select documents only through a client-controlled ID.

The safe endpoints repeat a server-side ownership check before every protected action.

## Safety scope

Testing is restricted to:

```text
http://127.0.0.1:8010
```

The server binds exclusively to `127.0.0.1`.

No external hosts, public applications, third-party services, or unrelated local systems are authorized.

## Demo users

| Username | Description |
|---|---|
| `alice` | Demo user who owns documents 101 and 102 |
| `bob` | Demo user who owns documents 201 and 202 |

The `/demo-login` endpoint is not real authentication. It exists only to create isolated lab sessions for studying authorization.

## Demo documents

| ID | Owner |
|---|---|
| `101` | Alice |
| `102` | Alice |
| `201` | Bob |
| `202` | Bob |

## Routes

| Route | Method | Behavior |
|---|---|---|
| `/demo-login` | POST | Creates a demo session for Alice or Bob |
| `/logout` | POST | Removes the current session |
| `/documents` | GET | Lists only documents owned by the current user |
| `/vuln/document?id=` | GET | Finds a document only from its ID |
| `/safe/document?id=` | GET | Checks document existence and ownership |
| `/vuln/document/update` | POST | Updates a document only from its ID |
| `/safe/document/update` | POST | Checks ownership before updating |
| Unknown route | GET/POST | Returns HTTP 404 |

## Running the application

```bash
cd week03-access-control/day01-idor-fundamentals/app
python3 -u server.py
```

The expected startup message is:

```text
Serving IDOR lab on http://127.0.0.1:8010
```

## Running the tests

With the server running in another terminal:

```bash
python3 week03-access-control/day01-idor-fundamentals/tests/access_control_tests.py
```

Expected result:

```text
Passed: 17
Failed: 0
```

The test process exits with a non-zero code when any check fails.

## Demonstrated vulnerable read

Alice first requests her own document:

```text
GET /vuln/document?id=101
```

The request returns HTTP 200.

Changing only the identifier:

```text
GET /vuln/document?id=201
```

also returns HTTP 200 and exposes Bob's document.

The server authenticated Alice but failed to verify resource ownership.

## Demonstrated safe read

The equivalent safe request:

```text
GET /safe/document?id=201
```

returns HTTP 404.

The server checks that:

```python
document["owner"] == current_user
```

before returning the resource.

## Demonstrated vulnerable update

Alice sends:

```text
POST /vuln/document/update
id=201&content=changed-by-alice
```

The server updates Bob's document because the vulnerable endpoint selects the object only from the ID.

## Demonstrated safe update

The same Alice session sends an update to:

```text
POST /safe/document/update
```

The request returns HTTP 404 and Bob's document remains unchanged.

## HTTP status policy

- `401` for missing or invalid authentication.
- `400` for malformed document identifiers.
- `404` for nonexistent documents.
- `404` for foreign documents on safe routes.

Foreign and nonexistent documents use the same response to reduce resource enumeration.

## Evidence

The `evidence/` directory contains:

- automated test output,
- Burp read IDOR comparison,
- Burp write IDOR comparison,
- vulnerable and safe behavior summary.

All committed cookie values are written as:

```text
session=REDACTED
```

No real cookies, credentials, tokens, flags, or challenge answers are stored.

## Main lessons

A valid object ID is not proof of authorization.

Authentication alone does not prevent horizontal privilege escalation.

Frontend restrictions do not protect server endpoints.

UUIDs and encoded identifiers can reduce guessing but do not replace server-side access control.

Ownership must be checked on every read, update, delete, download, and other protected operation.

## Limitations

The application is intentionally vulnerable.

Sessions and documents are stored only in memory.

The demo login has no password and must not be treated as production authentication.

The application has no database, HTTPS, persistent storage, roles, or multi-process support.

It must never be exposed outside the defined local scope.
