# TryHackMe — IDOR Notes

## Status

Completed — 100%.

## Concepts learned

IDOR occurs when an application uses a client-controlled object reference but does not verify whether the authenticated user is authorized to access the selected object.

Authentication answers who the current user is.

Authorization answers whether that user may perform a particular action on a particular object.

A valid session does not automatically allow access to every object in the application.

IDOR commonly causes horizontal privilege escalation, where one normal user accesses data belonging to another normal user.

## Plaintext identifiers

Plaintext identifiers expose the object reference directly.

Examples include `?id=201`, `/user/15`, and `/document/102`.

Sequential identifiers are often easy to guess or enumerate.

However, predictability is not the root cause. The root cause is the missing server-side authorization check after the object has been selected.

## Encoded identifiers

Encoded identifiers change the representation of a value but do not provide authorization.

An encoded identifier may be reversible and may still represent a simple internal object ID.

Encoding is not encryption and does not prove that the current user may access the referenced object.

The server must still authorize access after decoding and resolving the identifier.

## Hashed and unpredictable identifiers

Hashed values and UUIDs can make identifiers harder to guess.

They do not fix IDOR.

A foreign identifier may still be exposed through:

- another API response,
- shared links,
- browser history,
- frontend JavaScript,
- application logs,
- exported data,
- accidental disclosure.

Once a valid foreign identifier becomes known, an endpoint without object-level authorization remains vulnerable.

Unpredictable identifiers are defense in depth, not a replacement for access control.

## Tools and workflow

Tools used:

- TryHackMe AttackBox
- Browser
- Burp Proxy
- Burp HTTP history
- Burp Repeater
- Controlled modification of object identifiers

Workflow followed:

1. Logged in as an authorized lab user.
2. Observed a legitimate request for an accessible object.
3. Identified the client-controlled object reference.
4. Sent the request to Burp Repeater.
5. Changed only the object identifier.
6. Compared the new response with the original response.
7. Determined whether another user's object became accessible.
8. Identified the missing server-side authorization check.

## Practical observation

The practical task demonstrated that changing an object reference could cause the application to return a different object's data.

The server accepted the client-controlled identifier but did not sufficiently verify whether the selected object belonged to the authenticated user.

This demonstrated that successful authentication and a valid identifier are not enough to prove authorization.

## Connection with my local lab

My local lab used two demo users: Alice and Bob.

Alice owned documents `101` and `102`.

Bob owned documents `201` and `202`.

The vulnerable read route authenticated Alice but returned Bob's document when the identifier changed from `101` to `201`.

The vulnerable update route also allowed Alice to modify Bob's document.

The safe routes repeated a server-side ownership check before every read or update.

The required rule was equivalent to `document["owner"] == current_user`.

The local lab therefore reproduced both read and write IDOR behavior.

## Authentication versus authorization

Authentication established which user owned the session.

Authorization had to evaluate the authenticated user, the requested action, and the selected object.

The vulnerable endpoints performed authentication but omitted the ownership decision.

The safe endpoints performed both authentication and authorization.

## Relationship with API BOLA

IDOR and Broken Object Level Authorization describe closely related access-control failures.

BOLA is commonly used in API security when an endpoint receives an object identifier but fails to enforce permissions on the selected object.

For example, an endpoint such as `GET /api/documents/201` is vulnerable when Alice can retrieve Bob's document by changing only the identifier.

The remediation is object-level authorization on every protected request.

## Remediation

A secure server-side flow is:

1. Authenticate the user.
2. Validate the object identifier.
3. Retrieve the selected object.
4. Verify ownership or another access-control policy.
5. Perform the requested action only when authorization succeeds.

For an ownership-based application, access must be denied when `document["owner"] != current_user`.

Where possible, database queries should include the authorization condition directly, selecting the object by both its identifier and its authorized owner.

Authorization must be checked separately for:

- reads,
- updates,
- deletes,
- downloads,
- exports,
- sharing operations,
- metadata requests.

Frontend restrictions, hidden buttons, UUIDs, hashes, and encoded references do not replace server-side authorization.

## Status-code handling

HTTP `401` is appropriate when authentication is missing or invalid.

HTTP `403` may be used when the user is authenticated but forbidden from accessing the resource.

HTTP `404` may be used for both nonexistent and foreign objects to reduce resource enumeration.

The selected status code is secondary to correctly enforcing the authorization decision.

## Mistakes

Initially, I focused too much on whether an identifier was sequential, encoded, or hashed.

The more important question was whether the server verified authorization after resolving the identifier.

I also needed to separate authentication from authorization. A request can contain a valid session and still be unauthorized for the selected object.

## Points needing more practice

I need more practice with:

- locating indirect object references in larger applications,
- tracing identifiers across multiple requests,
- recognizing BOLA in JSON APIs,
- testing shared-resource permission models,
- identifying authorization failures involving roles and organizations,
- reviewing delete, export, and download endpoints.

## No flags or answers

I did not publish flags or challenge answers.
