# API Risk Map

| Risk | Object/function/property | Test | Expected secure result | Root cause | Remediation |
|---|---|---|---|---|---|
| BOLA | Object selected through an ID | Replace an owned object ID with another valid-format ID | 403 or 404 with no data disclosure or side effect | Missing object-level authorization | Validate caller, action, and object relationship on every request |
| BOPLA — read | Sensitive response property | Compare response properties between roles | Unauthorized property omitted | Full internal object serialized to the client | Use role-aware response schemas and property allowlists |
| BOPLA — write | Protected object property | Add a non-user-writable property to a valid request | Property rejected or ignored with no state change | Automatic binding or missing property authorization | Allowlist writable fields and authorize sensitive changes |
| BFLA | Administrative or privileged function | Replay a privileged operation using a normal-user session | 403 or 404 with no side effect | Missing function-level role check | Enforce server-side authorization on every function |
| Hidden endpoint | Unused or deprecated API route | Test the discovered route under different privilege levels | Endpoint removed or protected identically to current routes | Incomplete API inventory | Remove obsolete routes and protect every deployed version |
| Method exposure | Alternative HTTP method | Test accepted methods against the same resource | Only explicitly permitted methods accepted | Missing method allowlist | Allowlist methods and apply consistent authorization |
| Broken authentication | Session or token processing | Test missing, invalid, expired, and logged-out authentication | Consistent 401 response | Weak token validation or lifecycle management | Centralize authentication and invalidate expired sessions |
| Resource consumption | Expensive or repeated API operation | Perform controlled repeated requests inside lab scope | Rate limit or quota applied | Missing consumption limits | Use rate limits, quotas, pagination limits, timeouts, and size limits |
