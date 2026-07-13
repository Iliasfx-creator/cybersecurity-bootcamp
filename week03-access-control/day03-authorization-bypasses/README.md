# Week 3 — Day 3: Authorization Bypass Techniques

## Objective

Study how authorization can fail when an application protects only a URL,
HTTP method, workflow step, or client-controlled header instead of the
privileged operation itself.

## Completed exercises

- URL-based access control can be circumvented — Solved
- Method-based access control can be circumvented — Solved
- Multi-step process with no access control on one step — Solved
- Referer-based access control — Solved
- TryHackMe Corridor — Completed

## Key lessons

- Authorization must be enforced server-side for every sensitive operation.
- Frontend and backend routing disagreements can create authorization gaps.
- Authorization must remain consistent across all accepted HTTP methods.
- Every state-changing workflow step requires its own authorization check.
- Client-controlled headers cannot prove identity or privilege.
- Hidden, encoded, or hashed identifiers do not replace object-level authorization.

## Testing approach

For each exercise, I established the normal application flow, captured the
privileged request, replayed it with a lower-privileged identity, and changed
one request component at a time.

## Evidence handling

This directory contains conceptual summaries rather than walkthroughs.
Challenge answers, target addresses, credentials, and active session values
have been intentionally omitted.
