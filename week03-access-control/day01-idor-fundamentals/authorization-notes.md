# Authorization Notes

## Authentication versus authorization

Authentication answers:

> Who is making this request?

In this lab, a random demo session token maps to either Alice or Bob. Once the server resolves the token, it knows the identity associated with the request.

Authorization answers:

> Is this authenticated user allowed to perform this action on this specific resource?

Knowing that the current user is Alice does not automatically allow Alice to read or modify every document.

For document `201`, the server must separately verify:

```python
document["owner"] == current_user
```

The vulnerable routes perform authentication but omit this ownership check.

## Horizontal versus vertical privilege escalation

Horizontal privilege escalation occurs when one user accesses data or functionality belonging to another user with the same general privilege level.

Example:

```text
Alice -> Bob document 201
```

Alice and Bob are both normal users, but Alice crosses the ownership boundary and accesses Bob's resource.

Vertical privilege escalation occurs when a lower-privileged user gains functionality reserved for a higher-privileged role.

Examples include:

- a normal user accessing an administrator endpoint,
- a user changing their own role to administrator,
- an employee accessing manager-only functionality.

This lab demonstrates horizontal privilege escalation.

## Why an object ID is not authorization proof

A document ID identifies which object the client wants.

It does not prove that the client is allowed to access that object.

For example:

```text
id=201
```

This correctly identifies Bob's document, but it contains no evidence that Alice owns the document or has permission to access it.

The server must retrieve the resource and independently verify the authorization policy:

```python
current_user = get_current_user()
document = DOCUMENTS.get(document_id)

if document is None:
    return not_found()

if document["owner"] != current_user:
    return not_found()
```

The identifier is controlled by the client, so it cannot be trusted as permission evidence.

## UUIDs, encoded IDs, and hashed IDs

Sequential identifiers such as `101`, `102`, `201`, and `202` are easy to guess.

UUIDs, Base64 values, encoded identifiers, or hashed references can make guessing more difficult.

This does not fix IDOR.

A foreign identifier may still be disclosed through:

- API responses,
- browser history,
- shared links,
- application logs,
- frontend JavaScript,
- exported files,
- referrer information,
- accidental disclosure.

Once the identifier is known, an endpoint without an ownership check remains vulnerable.

Unpredictable identifiers are defense in depth, not an authorization control.

## Why hiding a frontend link is insufficient

The frontend is controlled by the client.

A user can:

- change the URL,
- modify query parameters,
- change a POST body,
- call an endpoint directly,
- use `curl`,
- use Burp Repeater,
- modify HTML or JavaScript.

Hiding a link or removing a button changes only the interface.

The server endpoint must enforce authorization independently on every request.

## Difference between 401, 403, and 404

### 401 Unauthorized

HTTP `401` normally means that authentication is missing or invalid.

In this lab, protected endpoints return `401` when there is no valid demo session.

Example:

```text
Anonymous -> GET /documents -> 401
```

### 403 Forbidden

HTTP `403` means that the server understands the request and recognizes the user, but the user is not permitted to perform the action.

Returning `403` may confirm that the requested resource exists.

### 404 Not Found

HTTP `404` normally means that the resource does not exist.

A secure application may also return `404` when a resource exists but is not visible to the current user.

This lab returns `404` for foreign documents so Alice cannot distinguish between:

- a document that does not exist,
- a document that exists but belongs to Bob.

This reduces resource enumeration.

## Why authorization must be checked on every operation

Protecting only the document listing is insufficient.

The `/documents` endpoint correctly shows Alice only documents `101` and `102`, but Alice can still directly request:

```text
GET /vuln/document?id=201
```

Authorization must therefore be checked independently on every protected:

- read,
- update,
- delete,
- download,
- export,
- share,
- metadata request.

Protecting a read endpoint does not automatically protect an update endpoint.

Every operation can contain a separate authorization failure.

## Correct server-side ownership pattern

The correct order is:

```text
1. Resolve the authenticated user.
2. Validate the identifier.
3. Retrieve the selected resource.
4. Verify ownership or another access policy.
5. Perform the requested action.
```

The ownership value must come from trusted server-side state:

```python
document["owner"]
```

The server must not trust a client-controlled field such as:

```text
owner=alice
```

A database-backed application could enforce both identifier and ownership in the same query:

```text
SELECT document
WHERE id = requested_id
AND owner = current_user
```

## Relationship between IDOR and API BOLA

IDOR means Insecure Direct Object Reference.

It commonly describes an endpoint that receives a direct object reference but does not verify whether the current user may access the referenced object.

Example:

```text
GET /document?id=201
```

BOLA means Broken Object Level Authorization.

It is the broader API security term for failing to enforce authorization on a requested object.

Example:

```text
GET /api/documents/201
```

If Alice can access Bob's object by modifying only the identifier, the API is vulnerable to BOLA.

The remediation is the same:

```text
Enforce object-level authorization on every protected request.
```

## Main lesson

Authentication establishes identity.

Authorization must evaluate:

```text
authenticated actor + requested action + selected resource
```

A valid session and a valid object identifier are both necessary, but neither proves that access is allowed.
