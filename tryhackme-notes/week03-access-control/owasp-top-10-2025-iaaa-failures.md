
TryHackMe — OWASP Top 10 2025: IAAA Failures
Status

Completed — 100%.

IAAA model
Identification: the identity an actor claims.
Authentication: evidence that validates that identity.
Authorization: the actions and resources allowed for that identity.
Accountability: reliable attribution of actions through logs and audit
evidence.
Failure relationships

An application can authenticate a user correctly and still fail authorization.

A valid session does not permit access to every object, property or function.
Authorization must evaluate the current actor, action, target object, tenant
and context on every protected request.

Accountability also requires more than recording a timestamp. Important actions
need actor, tenant, target, result and correlation information protected
against unauthorized modification.

Testing methodology
Test missing and invalid authentication.
Repeat requests with a lower-privileged identity.
Change object identifiers separately.
Test restricted request and response properties.
Invoke privileged functions directly.
Verify that denied mutations leave state unchanged.
Confirm important decisions produce useful audit evidence.
Connection with Week 3

The room reinforced BOLA, property-level authorization, function-level
authorization, session handling, privilege changes and audit-log requirements.

Evidence handling

No room answers, flags, target addresses, cookies, sessions, passwords or
credentials are included.
