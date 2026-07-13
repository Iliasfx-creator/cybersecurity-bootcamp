# Authorization Testing Checklist

Use only on systems for which testing is explicitly authorized.

## Establish the baseline

- [ ] Identify the actor, action, resource, and expected authorization result.
- [ ] Capture the normal application flow.
- [ ] Identify the request that actually performs the privileged operation.
- [ ] Record both the HTTP response and the resulting application state.

## Identity and session checks

- [ ] Test without authentication.
- [ ] Test after logout.
- [ ] Replay the same request with a lower-privileged session.
- [ ] Test access as another user at the same privilege level.
- [ ] Confirm that disabling a UI control does not replace server-side enforcement.

## HTTP method checks

- [ ] Test every method accepted by the endpoint.
- [ ] Try an alternative method while keeping the action and parameters equivalent.
- [ ] Confirm that unsupported methods are rejected.
- [ ] Confirm that read-only methods cannot perform state changes.

## Workflow checks

- [ ] Access the final workflow step directly.
- [ ] Skip review or confirmation steps.
- [ ] Repeat a previously completed final request.
- [ ] Change parameters between the review and confirmation steps.
- [ ] Verify that final authorization is evaluated immediately before the change.

## Header and routing checks

- [ ] Modify client-controlled routing headers.
- [ ] Modify or remove the Referer header.
- [ ] Test path capitalization.
- [ ] Test a trailing slash.
- [ ] Test alternative URL encoding.
- [ ] Compare frontend routing with backend routing.
- [ ] Verify consistent normalization across every application layer.

## Resource and action checks

- [ ] Test each read action independently.
- [ ] Test each create action independently.
- [ ] Test each update action independently.
- [ ] Test each delete action independently.
- [ ] Confirm object ownership is checked server-side.
- [ ] Confirm opaque, encoded, or hashed identifiers are not treated as authorization.

## Result validation

- [ ] Change only one request element at a time.
- [ ] Compare expected and observed results.
- [ ] Check for side effects instead of relying only on status codes.
- [ ] Document the trusted layer and the client-controlled input.
- [ ] Record the root cause and server-side remediation.
- [ ] Remove sensitive values before saving evidence.
