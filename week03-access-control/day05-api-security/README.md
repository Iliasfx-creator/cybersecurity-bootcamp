# Week 3 — Day 5: API Security Testing

Status: Completed

## Objective

Map an API attack surface and manually test object-, property-, and function-level authorization using Burp Suite.

## Topics covered

- API reconnaissance and documentation discovery
- Endpoint and API version identification
- HTTP method and content-type testing
- Hidden parameters and unused API functionality
- Broken Object Level Authorization
- Broken Object Property Level Authorization
- Broken Function Level Authorization
- Mass assignment
- Secure API design and prevention

## Practical work

- Exploiting an API endpoint using documentation — Solved
- Finding and exploiting an unused API endpoint — Solved
- Exploiting a mass assignment vulnerability — Solved
- OWASP API Security Top 10 – 1 — 100%

## Main lessons

An API endpoint is defined by more than its path. Method, content type, parameters, authentication context, object identifiers, and accepted properties can all change its security behavior.

API documentation and hidden endpoints increase attack-surface visibility, but the root security requirement remains server-side authorization on every object, property, and function.

## Security and redaction

Testing was performed only inside authorized PortSwigger and TryHackMe environments.

The repository contains no flags, challenge answers, target IPs, live lab hosts, passwords, credentials, or session values.

## Completion criteria

- [x] Three PortSwigger API labs solved
- [x] TryHackMe room completed to 100%
- [x] BOLA, BOPLA, and BFLA distinguished
- [x] API risk map completed
- [x] Endpoint testing checklist completed
- [x] Root causes and remediations documented
- [x] Evidence sanitized
