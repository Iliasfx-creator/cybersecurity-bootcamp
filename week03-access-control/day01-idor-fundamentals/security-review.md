# IDOR Security Review

## Executive summary

This review evaluates a deliberately vulnerable local document application that demonstrates read and write Insecure Direct Object Reference vulnerabilities. The application contains two fictional users, Alice and Bob, and documents owned independently by each user. Every protected endpoint requires a valid demo session, but the vulnerable endpoints fail to verify that the selected document belongs to the authenticated user.

Testing confirmed that Alice could read and modify Bob's document by changing only the client-controlled document identifier. Equivalent safe endpoints repeated a server-side ownership check and rejected access with HTTP 404. The principal root cause is missing object-level authorization, not missing authentication or weak identifier validation.

## Scope

Testing was restricted to `127.0.0.1:8010`.

The reviewed functionality included:

- demo login and logout,
- current-user document listing,
- vulnerable document reads,
- safe document reads,
- vulnerable document updates,
- safe document updates,
- invalid identifiers,
- nonexistent resources,
- unauthenticated access,
- unknown routes.

No public systems, external IP addresses, third-party applications, or unrelated local services were tested.

## Application model

The lab contains two users:

- Alice, who owns documents 101 and 102.
- Bob, who owns documents 201 and 202.

The demo login endpoint creates a random session token that maps to one of the two usernames. This mechanism is intentionally simplified and exists only to isolate authorization behavior.

The application stores users, sessions, and documents in memory. Restarting the server resets all sessions and restores the original document contents.

## Authentication behavior

Protected routes call a helper that resolves the session cookie and returns the current username.

Requests without a valid session receive HTTP 401.

This behavior establishes the identity of the caller but does not determine which resources the caller may access.

The vulnerable routes therefore demonstrate an important security distinction: an endpoint can authenticate a user successfully while still being vulnerable to Broken Access Control.

## Read IDOR finding

The vulnerable read endpoint accepts a client-controlled `id` query parameter.

Alice can request her own document:

```text
GET /vuln/document?id=101
```

The endpoint returns HTTP 200 and the Alice-owned document.

Changing only the identifier to:

```text
GET /vuln/document?id=201
```

also returns HTTP 200, but the returned object belongs to Bob.

The endpoint validates that the caller has a session, verifies that the identifier is syntactically valid, and confirms that the document exists. It does not compare the document owner with the authenticated username.

This is horizontal privilege escalation because Alice gains access to another normal user's resource.

## Write IDOR finding

The vulnerable update endpoint accepts a document ID and new content through POST form data.

Using an Alice session, the following request successfully modified Bob's document:

```text
id=201&content=changed-by-alice
```

The response returned HTTP 200 and included a document whose owner remained Bob while its content had been changed by Alice.

A subsequent read confirmed that the unauthorized change had been stored.

Write IDOR can have greater impact than read-only exposure because it can affect data integrity, business operations, audit records, and other users' trust in the application.

## Safe endpoint behavior

The safe endpoints repeat the object-level authorization check after retrieving the document.

The effective rule is:

```python
document["owner"] == current_user
```

Alice can read or update documents 101 and 102.

Alice receives HTTP 404 when requesting or updating Bob's documents.

The rejected safe update leaves Bob's document unchanged, as confirmed through a later Bob-authenticated safe read.

## Root cause

The root cause is selecting a resource from a client-controlled identifier without enforcing authorization for that selected object.

The vulnerable logic effectively performs:

```text
Authenticate user.
Parse ID.
Find object.
Return or update object.
```

The required authorization step is absent.

The secure flow performs:

```text
Authenticate user.
Validate ID.
Find object.
Verify ownership.
Perform action.
```

The document identifier specifies the target object but does not prove permission.

## Identifier validation

The application returns HTTP 400 for values such as:

- an empty ID,
- alphabetic input,
- decimal input,
- negative values.

It returns HTTP 404 for syntactically valid but nonexistent identifiers.

This validation improves request handling but does not fix IDOR. The value `201` is a perfectly valid identifier, yet Alice must still be denied because the selected object belongs to Bob.

Validation and authorization solve different problems.

## Why UUIDs do not fix the vulnerability

Replacing sequential IDs with UUIDs, encoded values, or hashes could make resource discovery harder.

This may reduce basic guessing but does not enforce access control.

Identifiers can be exposed through legitimate API responses, shared URLs, logs, frontend code, browser history, exported data, or accidental disclosure.

Once a foreign identifier becomes known, an endpoint without an ownership check remains vulnerable.

Unpredictable identifiers are therefore defense in depth, not a remediation for IDOR.

## Frontend restrictions

Hiding Bob's documents from Alice's `/documents` listing is useful but insufficient.

Alice can still manually request `id=201`.

The client can modify URLs, request bodies, browser code, and Burp Repeater requests. For this reason, frontend controls cannot be treated as security boundaries.

Every protected server endpoint must enforce its own authorization policy.

## Status-code decision

The application returns HTTP 401 when authentication is missing.

It returns HTTP 400 when the identifier is malformed.

The safe routes return HTTP 404 for both nonexistent and foreign documents.

HTTP 403 could also represent an authenticated but forbidden request. However, using 404 for foreign resources avoids confirming to Alice that a Bob-owned document exists at a particular identifier.

This decision reduces object enumeration but does not replace the ownership check.

## IDOR and BOLA

IDOR is commonly used to describe direct references such as query parameters, path IDs, or form fields that allow unauthorized access to objects.

Broken Object Level Authorization, or BOLA, is the broader API security term for failing to enforce permissions on a requested object.

An API endpoint such as `/api/documents/201` has the same security requirement as this lab. The server must authorize the authenticated actor against document 201 before returning, updating, or deleting it.

## Remediation

The primary remediation is centralized server-side object authorization.

Each protected action should:

1. Resolve the authenticated user.
2. Validate the identifier format.
3. retrieve the selected object.
4. Apply the access-control rule.
5. Perform the requested action only after authorization succeeds.

Where possible, database queries should include the ownership condition directly.

For example, conceptually:

```text
SELECT document
WHERE id = requested_id
AND owner = current_user
```

This reduces the chance that developers retrieve a foreign object and forget a separate permission check.

Authorization helpers should be reused across read, update, delete, download, and export operations.

## Defense in depth

Unpredictable IDs can reduce guessing.

Rate limiting can reduce automated enumeration.

Audit logs can record denied object-access attempts without storing sensitive session values.

Automated tests can detect regressions in ownership checks.

Secure cookie attributes should be used in production. The lab uses `HttpOnly` and `SameSite=Lax`. A production HTTPS application should also use `Secure`.

These measures strengthen the application but do not replace object-level authorization.

## Detection and logging

Production monitoring should record:

- authenticated user identifier,
- requested action,
- requested resource identifier,
- authorization decision,
- route,
- timestamp,
- response status.

Logs should not contain raw session cookies, passwords, or authentication tokens.

Repeated requests for many foreign identifiers may indicate enumeration or access-control testing.

Denied access patterns should support alerting and investigation while avoiding excessive disclosure in responses.

## Testing methodology

The application was tested through:

- direct HTTP requests,
- Burp Repeater comparisons,
- automated Python standard-library tests,
- independent Alice and Bob sessions,
- state restoration before mutable tests.

The suite contains 17 checks and exits with a non-zero status if a check fails.

The mutable Bob document is restored before relevant tests, and vulnerable update cleanup runs inside a `finally` block.

This prevents test success from depending on execution order.

## Limitations

The application is deliberately simplified.

It uses in-memory state, a fake login mechanism, no database, no real passwords, no HTTPS, and only one ownership policy.

The lab does not model shared documents, organization membership, administrators, role-based access control, or complex permission inheritance.

The findings apply to the demonstrated routes and should not be interpreted as a complete review of a production application.

## Conclusion

The lab successfully demonstrates read and write IDOR as failures of object-level authorization.

Alice is authenticated correctly but can access Bob's resource through vulnerable endpoints because the server trusts the client-controlled document ID without checking ownership.

The safe endpoints enforce the authorization rule on every request and deny foreign-object access.

The core lesson is that authentication identifies the actor, while authorization must evaluate that actor against the requested action and resource.
