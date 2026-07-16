# TryHackMe — Threat Modelling

## Status

- Completed — 100%.

## STRIDE

- STRIDE helps identify threat categories across components and data flows:

- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege

- The category is only a starting point. A useful threat still identifies a specific actor, action, precondition, asset and impact.

## DREAD

- DREAD is a qualitative prioritization approach based on:

- Damage potential
- Reproducibility
- Exploitability
- Affected users
- Discoverability

- It can help compare risks, but scoring may be subjective. Scales and assumptions must therefore be documented and reviewed consistently.

## PASTA

- PASTA is a risk-centered process that connects business objectives, technical scope, application decomposition, threat analysis, weakness analysis, attack modeling, and risk or impact analysis.

- Its attack-modeling stage helps examine credible attack paths rather than listing disconnected security issues.

- PASTA is useful when the business impact and attacker perspective require more depth than a lightweight design review.

## MITRE ATT&CK

- MITRE ATT&CK is a knowledge base of adversary tactics and techniques based on observed behavior.

- It can support:

- Threat-informed testing
- Adversary emulation
- Control-coverage reviews
- Detection planning
- Communication between offensive and defensive teams

- ATT&CK does not replace a system-specific threat model. It does not by itself decide whether an AcmeDocs user may access a particular tenant object.

## Framework fit for Product Security

- STRIDE combined with a data-flow diagram fits an ordinary Product Security design review best because it is lightweight, repeatable and closely connected to components and trust boundaries.

- PASTA is appropriate for deeper analysis of high-risk product flows.

- DREAD may help prioritize identified threats but should not be treated as an objective measurement.

- ATT&CK is most useful as a supporting framework for realistic attacker behavior, security testing and detection coverage.

## Mistakes

- I initially treated framework names as alternative answers to the same question.
- The room clarified that the frameworks serve different purposes: discovery, prioritization, risk analysis and adversary-behavior mapping.
- I also needed to avoid treating a generic STRIDE label as a complete threat.

## Lessons learned

- Model the system before identifying threats.
- Mark every trust boundary.
- Describe concrete abuse cases.
- Connect every mitigation to a verification test.
- Revisit the model when architecture or permissions change.
- Use multiple frameworks only when each one adds a clear purpose.

## Evidence handling

- No answers, flags, target addresses, credentials, cookies, passwords or session values are included.
