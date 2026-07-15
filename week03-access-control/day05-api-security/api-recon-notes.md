# API Reconnaissance Notes

## API reconnaissance

API reconnaissance identifies the complete API attack surface before security testing begins.

For every endpoint, the tester should record:

- HTTP method
- path and API version
- authentication requirement
- accepted content types
- path, query, header, and body parameters
- returned object properties
- supported actions
- expected authorization level
- observable side effects

The visible frontend is only one API client and may not expose every deployed capability.

## API documentation

API documentation may be human-readable or machine-readable, such as OpenAPI JSON or YAML.

Documentation can reveal:

- endpoints not used by the frontend
- accepted methods
- required and optional parameters
- request and response schemas
- administrative operations
- deprecated API versions

Exposed documentation is not itself an authorization control. Every documented or undocumented operation must enforce its own server-side policy.

## Endpoint identification

Useful discovery sources include:

- normal browser traffic
- Burp HTTP history
- JavaScript files
- error responses
- API documentation
- API base paths
- predictable endpoint naming
- older API versions

An endpoint should be treated as a combination of method, path, content type, parameters, and authentication context.

## HTTP methods

Different methods on the same path may perform different operations.

Relevant methods include:

- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS

A secure API uses an explicit method allowlist and performs authorization on every accepted method.

## Content types

Endpoints may behave differently when processing:

- application/json
- application/x-www-form-urlencoded
- multipart/form-data
- application/xml

Unexpected content types should be rejected. Accepted formats should follow equivalent validation and authorization rules.

## Hidden parameters

Undocumented parameters can sometimes be inferred from:

- response objects
- validation messages
- differences between GET and POST schemas
- JavaScript
- API documentation

A property appearing in a response does not mean the caller should be allowed to submit or modify it.

## BOLA

Broken Object Level Authorization occurs when a caller can access another user's object by changing an object identifier.

Authorization must validate the relationship between the authenticated caller, the requested action, and the specific object.

## BOPLA

Broken Object Property Level Authorization occurs when a caller can read or modify an object property that should not be available to them.

Read-side examples include excessive data exposure. Write-side examples include mass assignment.

## BFLA

Broken Function Level Authorization occurs when a caller can invoke a function reserved for another role, such as an administrative update or deletion.

The endpoint must authorize the function even when the frontend does not expose it.

## Mass assignment

Mass assignment occurs when request properties are automatically bound to internal object fields.

The server should allowlist writable properties, reject unexpected properties, and independently authorize security-sensitive changes.

## Prevention

- Maintain an accurate inventory of endpoints and API versions.
- Remove deprecated and unused functionality.
- Authenticate requests consistently.
- Authorize every object access.
- Apply property-level read and write controls.
- Enforce role checks on privileged functions.
- Allowlist methods and content types.
- Use strict request and response schemas.
- Return generic errors.
- Apply rate limits, quotas, timeouts, and payload limits.
- Verify negative cases and absence of unauthorized side effects.
