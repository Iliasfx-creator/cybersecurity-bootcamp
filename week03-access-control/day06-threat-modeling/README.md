# Week 3 — Day 6: Product Security Threat Modeling

Status: Complete

## Objective

This project models security risks for AcmeDocs before implementation.

AcmeDocs is a fictional multi-tenant SaaS platform containing documents,
object storage, invitations, billing data, organization exports, browser
sessions, an API gateway, backend services, audit logging, email delivery,
and both deprecated and current API versions.

The primary security invariant is:

> A user, request, object, and action must remain inside the authorized tenant
> unless an explicitly approved and audited support workflow permits otherwise.

## Work completed

- System and actor modeling
- Asset and entry-point inventory
- Trust-boundary identification
- Mermaid data-flow diagram
- STRIDE-based threat identification
- Fourteen concrete threats
- Testable mitigations
- Given/When/Then security requirements
- Negative security-test plan
- Product Security review summary
- TryHackMe Threat Modelling completion notes

## Files

- `source-notes.md` — threat-modeling theory
- `system-model.md` — actors, roles, assets, dependencies and boundaries
- `data-flow-diagram.md` — AcmeDocs data flows
- `threat-register.md` — prioritized threats and mitigations
- `authorization-requirements.md` — testable security requirements
- `security-test-plan.md` — verification plan
- `review-summary.md` — design-review conclusion

## Evidence handling

No flags, challenge answers, target addresses, session values, credentials, or
passwords are stored in this project.
