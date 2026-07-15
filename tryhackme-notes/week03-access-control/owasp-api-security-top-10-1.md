# OWASP API Security Top 10 — 1

Status: Started

## Concepts

### Broken Object Level Authorization

BOLA occurs when an API accepts an object identifier from the client but does
not verify whether the authenticated actor is authorized to access that
specific object.

Authentication alone is insufficient. The API must evaluate the relationship
between the actor, action, and requested object on every request.

Identifiers may be sequential, encoded, hashed, or random. Their format does
not replace object-level authorization.

### Broken Function Level Authorization

Broken Function Level Authorization occurs when a user can invoke a function
that should be restricted to a different role.

Examples include administrative user management, configuration changes, or
privileged write and delete operations.

Hiding the function from the interface does not protect the backend endpoint.

## Testing methodology

1. Establish the normal authorized request.
2. Identify the acting user, requested action, and target object.
3. Replay the request without authentication.
4. Replay it with a lower-privileged identity.
5. Modify one identifier, function, or method at a time.
6. Compare status codes, response bodies, and application side effects.
7. Verify that denied writes leave application state unchanged.
8. Record the missing server-side authorization decision.

## Mistakes to avoid

- Treating possession of an object ID as proof of authorization.
- Assuming an unguessable identifier prevents unauthorized access.
- Testing only successful requests.
- Relying only on the HTTP status without checking side effects.
- Assuming that a function is protected because it is hidden from the UI.
- Changing multiple request components at the same time.

## Lessons learned

BOLA is primarily an object-level authorization failure, while BFLA is a
function or role-level authorization failure.

A secure API commonly needs both ownership checks and role checks.

Authorization must be evaluated server-side on every request and immediately
before the protected read or mutation.

## Remediation

- Deny access by default.
- Derive the actor and role from trusted server-side session data.
- Enforce object ownership or relationship checks.
- Enforce role checks for privileged functions.
- Centralize authorization decisions.
- Allow only required HTTP methods.
- Add positive and negative authorization tests.
- Verify that denied operations do not modify state.

## Evidence handling

Challenge answers, flags, target addresses, session values, and credentials are
intentionally omitted.

## Day 5 — API Security completion update

Completion: 100%

### Broken Authentication

Broken authentication occurs when an API incorrectly validates credentials, sessions, or tokens. Testing should include missing, invalid, expired, reused, and logged-out authentication material.

### Excessive Data Exposure

An API should return only properties required by the caller. Returning a complete internal object and relying on the frontend to hide sensitive properties is unsafe.

### Resource Consumption and Rate Limiting

APIs should limit request frequency, payload size, pagination size, execution time, and expensive operations. These controls protect availability and operational cost.

### Broken Function Level Authorization

Every privileged operation requires a server-side authorization decision. Hiding administrative functionality in the frontend does not protect the corresponding API endpoint.

### OWASP 2019 to 2023 terminology

- API1:2019 BOLA remains API1:2023 BOLA.
- API2:2019 Broken User Authentication became API2:2023 Broken Authentication.
- API3:2019 Excessive Data Exposure and API6:2019 Mass Assignment were combined into API3:2023 BOPLA.
- API4:2019 Lack of Resources and Rate Limiting became API4:2023 Unrestricted Resource Consumption.
- API5:2019 BFLA remains API5:2023 BFLA.

### Testing methodology

- Establish a legitimate baseline.
- Identify objects, properties, and functions separately.
- Repeat requests without authentication or with lower privileges.
- Change one component at a time.
- Compare responses and server-side side effects.
- Verify that denied requests do not modify state.

### Mistakes

I initially focused mainly on whether an endpoint was visible. The exercises showed that endpoint visibility and authorization are separate concerns. A hidden or unused endpoint is still vulnerable if its server-side policy is missing.

### Lessons learned

API testing requires comparing the same operation across identities, objects, properties, methods, and content types. A successful response alone is not enough; the tester must also verify the resulting server-side state.

### Remediation

Use centralized authentication, object-level authorization, property allowlists, minimal response schemas, function-level role checks, accurate API inventory, and resource-consumption limits.
