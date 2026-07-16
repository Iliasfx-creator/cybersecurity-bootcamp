# Source Notes

## The four threat-modeling questions

A practical threat-modeling process answers four questions:

1. What are we building?
2. What can go wrong?
3. What controls will we use?
4. Did we design and verify the controls well enough?

The process therefore includes system modeling, threat identification,
mitigation selection, and review or validation.

## Threat, vulnerability, risk and control

A **threat** is a possible event or actor action that could harm an asset.

A **vulnerability** is a weakness that makes a threat possible or easier to
execute.

A **risk** combines the likelihood of a threat succeeding with its expected
business or technical impact.

A **control** is a preventive, detective, corrective, or recovery mechanism
that reduces the likelihood or impact of a risk.

For example, a cross-tenant document request is a threat scenario. A missing
object-level authorization check is the vulnerability. Disclosure of another
company's documents is the impact. A tenant-scoped database query and negative
authorization test are controls.

## Why a system model is necessary

A threat model without an accurate system model is unreliable because the
reviewer cannot identify all actors, assets, data flows, entry points, data
stores, dependencies, or privilege changes.

Missing an old API version or an external storage service from the model can
also remove its threats from the review even though the component still exists
in production.

The model must be updated when architecture, roles, data flows, or dependencies
change.

## Trust boundaries

A trust boundary is a location where data, identity, privilege, ownership, or
security assumptions change.

Crossing a trust boundary requires validation. Examples include:

- browser to API gateway,
- API gateway to backend API,
- backend API to database or object storage,
- internal service to an external email provider,
- normal tenant context to cross-tenant support context.

A network location alone does not make input trusted.

## STRIDE

- **Spoofing:** pretending to be another user, service, or tenant.
- **Tampering:** unauthorized modification of data, requests, or logs.
- **Repudiation:** performing an action that cannot later be reliably attributed.
- **Information Disclosure:** exposing data to an unauthorized actor.
- **Denial of Service:** exhausting resources or making the service unavailable.
- **Elevation of Privilege:** gaining permissions or functions beyond the
  actor's assigned authority.

STRIDE is a discovery aid. A STRIDE label does not replace a concrete abuse
case containing an actor, action, target asset, precondition, and impact.

## Threat responses

A risk may be:

- avoided by removing the unsafe feature or flow,
- mitigated with preventive and detective controls,
- transferred through an appropriate contractual or insurance mechanism,
- accepted explicitly by an authorized risk owner.

Risk acceptance must be recorded rather than silently treating an unresolved
finding as complete.

## Why mitigations must be testable

A statement such as “secure the endpoint” is not verifiable.

A testable mitigation identifies:

- where enforcement occurs,
- which actor, object, action, and tenant are evaluated,
- the secure denial behavior,
- the expected side effect or absence of side effects,
- the evidence that proves the control works.

For example, a denied cross-tenant update must return a concealed denial and
must leave the stored document unchanged.

## Review and validation

Review checks whether the model covers the real architecture, whether threats
are specific, whether controls address root causes, and whether every important
control has a verification test.

Validation must also confirm that:

- deprecated endpoints use the same policy,
- denied mutations leave state unchanged,
- logs contain actor and tenant attribution,
- privilege changes invalidate stale access,
- resource limits work under repeated requests.

## Sources

- OWASP Threat Modeling Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- OWASP Threat Modeling:
  https://owasp.org/www-community/Threat_Modeling
- MITRE ATT&CK:
  https://attack.mitre.org/
