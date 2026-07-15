
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
