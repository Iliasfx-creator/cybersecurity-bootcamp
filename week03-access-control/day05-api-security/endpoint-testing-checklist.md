# API Endpoint Testing Checklist

This is a reusable checklist for future authorized API assessments.

## Reconnaissance

- [ ] Browse the complete normal application flow.
- [ ] Filter Burp history to the authorized host.
- [ ] Record API endpoints and versions.
- [ ] Inspect JavaScript for additional API paths.
- [ ] Search for API documentation.
- [ ] Examine API base paths.
- [ ] Identify unused or deprecated endpoints.
- [ ] Record required and optional parameters.
- [ ] Record authentication and role requirements.

## Baseline

- [ ] Capture a valid legitimate request.
- [ ] Replay it unchanged in Repeater.
- [ ] Record the response and side effect.
- [ ] Keep an unchanged control request.
- [ ] Change one request component at a time.

## Authentication

- [ ] Test without authentication.
- [ ] Test with an invalid session.
- [ ] Test after logout.
- [ ] Test with a lower-privileged session.
- [ ] Confirm denied requests have no side effects.

## Objects — BOLA

- [ ] Identify IDs in paths, queries, headers, and bodies.
- [ ] Substitute another valid-format object ID.
- [ ] Test read, update, and delete independently.
- [ ] Compare status, response body, and response length.
- [ ] Verify denied modifications do not change state.

## Properties — BOPLA

- [ ] Compare response properties with submitted properties.
- [ ] Identify sensitive properties returned but not normally submitted.
- [ ] Add one hidden property using a harmless control value.
- [ ] Test invalid property types.
- [ ] Verify sensitive properties are not exposed.
- [ ] Verify protected properties cannot be modified.

## Functions — BFLA

- [ ] Identify administrative or privileged endpoints.
- [ ] Replay privileged requests using a normal-user session.
- [ ] Test direct access without the frontend.
- [ ] Test each accepted method separately.
- [ ] Confirm denial produces no side effect.

## Methods and content types

- [ ] Test GET, POST, PUT, PATCH, DELETE, and OPTIONS where safe.
- [ ] Review `Allow` headers and error messages.
- [ ] Test only authorized lab objects.
- [ ] Compare accepted content types.
- [ ] Confirm unsupported methods return 405.
- [ ] Confirm unexpected content types are rejected.

## Final review

- [ ] Root cause documented.
- [ ] Correct server-side remediation documented.
- [ ] No full exploit walkthrough stored.
- [ ] Hosts redacted.
- [ ] Cookies redacted.
- [ ] Passwords redacted.
- [ ] Flags and challenge answers excluded.
