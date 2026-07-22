# Burp Capture Guide

Capture only against `http://127.0.0.1:8013`. Keep the Python server running in
one terminal and use Burp Repeater for the requests below.

## Before starting

1. Set the Repeater target to host `127.0.0.1`, port `8013`, and disable HTTPS.
2. Use HTTP/1.1 requests and leave one blank line after the headers.
3. Never paste a live cookie into the public evidence file.
4. Record status codes, cookie attributes, and outcome—not the real token.

## Comparison 1 — Login issues a new session

Send:

```http
POST /login HTTP/1.1
Host: 127.0.0.1:8013
Content-Type: application/json
Connection: close

{"username":"alice"}
```

Expected: `200`, `Set-Cookie`, `HttpOnly`, `SameSite=Lax`, and `Path=/`.
Copy only the sanitized structure into `01-login-new-session.txt`.

## Comparison 2 — Supplied pre-login cookie is replaced

Repeat the login with an attacker-chosen cookie:

```http
Cookie: session=REDACTED_OLD
```

Expected: a different new session is issued. Replaying the attacker value on
`GET /me` returns `401`.

## Comparison 3 — Query and header transport are rejected

First confirm a valid cookie produces `200` on `/me`. Then remove the Cookie
header and try the redacted token in `?session=...`, `X-Session-ID`, and
`Authorization: Bearer ...` one at a time.

Expected: each non-cookie version returns `401`.

## Comparison 4 — Logout and replay

Log in as `alice`, send `POST /logout` with the current cookie, and observe
`Max-Age=0`. Then replay the same old cookie on `GET /me`.

Expected: logout returns `200`; replay returns `401`.

## Comparison 5 — Privilege rotation

Log in as `admin`. Send `POST /session/step-up` using its standard session.
Record the new `Set-Cookie`. Test the old and new values separately on `/me`.

Expected: old value returns `401`; new value returns `200` and reports the
server-side elevated authentication level.

## Required public redaction vocabulary

Use these exact placeholders:

```text
Password: REDACTED
Cookie: session=REDACTED_OLD
Set-Cookie: session=REDACTED_NEW
Authorization: Bearer REDACTED
```

The finalized evidence was reviewed with the required redaction vocabulary.
