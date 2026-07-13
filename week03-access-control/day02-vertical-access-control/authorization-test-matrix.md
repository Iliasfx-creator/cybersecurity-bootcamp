# Authorization Test Matrix

| Actor | Function | Expected | Observed vulnerable result | Missing control |
|---|---|---|---|---|
| Anonymous | Admin function | Deny | Allowed | Authentication and authorization |
| Normal user | Admin function | Deny | Allowed | Server-side role enforcement |
| Administrator | Admin function | Allow | Allowed | None |

## Testing Principle

Access-control testing should compare the same function across different actors and privilege levels.

A hidden interface element is not evidence that access is denied. The underlying request must be tested directly, and authorization must be enforced by the server.
