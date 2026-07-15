# PortSwigger API Testing Lab Review

## Exploiting an API endpoint using documentation

Status: Solved

### Attack surface discovery

A normal account-management flow generated an API request. Examining the API base path revealed machine-readable documentation describing additional operations.

### Normal baseline

The normal authenticated request operated only on the current user's account resource.

### Request component changed

The API path and documented operation were examined to identify functionality that was not exposed through the normal user interface.

### Evidence or side effect

A normal authenticated user could invoke a destructive account-management function that should have required elevated privileges.

### Root cause

The dangerous API function lacked server-side function-level authorization. Documentation increased visibility but was not the primary authorization failure.

### Correct server-side remediation

Require administrative authorization for destructive user-management operations, independently of whether documentation is public. Protect private documentation and keep the API inventory current.

### Mistake or difficulty

The main difficulty was separating information disclosure through documentation from the actual vulnerability: missing authorization on the API function.

---

## Finding and exploiting an unused API endpoint

Status: Solved

### Attack surface discovery

Normal product browsing exposed a read-only price endpoint. Method discovery showed that the same resource accepted an additional method not used by the frontend.

### Normal baseline

The standard request retrieved a product price without changing server-side state.

### Request component changed

The HTTP method, content type, and required JSON property were tested one at a time while preserving the authenticated session.

### Evidence or side effect

The unused method accepted a state-changing request from a normal user and modified product data that should have required administrative privileges.

### Root cause

An unused API capability remained deployed without function-level authorization. The server trusted authentication alone without checking whether the caller could modify pricing.

### Correct server-side remediation

Remove unused functionality, allowlist required methods, maintain an accurate API inventory, and enforce administrative authorization before any price modification.

### Mistake or difficulty

The main difficulty was constructing a valid request from method and content-type errors while ensuring that the request used the current lab session.

---

## Exploiting a mass assignment vulnerability

Status: Solved

### Attack surface discovery

Comparing checkout response data with the normal checkout request revealed an additional property that was returned by the API but not submitted by the frontend.

### Normal baseline

The normal checkout request contained selected products and was rejected when the account lacked sufficient credit.

### Request component changed

One additional object property was added to the existing JSON body while all product data and authentication context remained unchanged.

### Evidence or side effect

The server accepted and processed the client-supplied property, allowing it to influence a security-sensitive checkout calculation.

### Root cause

The API automatically bound a client-controlled property to an internal checkout object without property-level authorization.

### Correct server-side remediation

Calculate discounts server-side, use a strict allowlist of client-writable properties, reject unexpected properties, and authorize all sensitive property changes.

### Mistake or difficulty

The main difficulty was distinguishing successful JSON parsing from proof that the hidden property was actually processed and affected application state.
