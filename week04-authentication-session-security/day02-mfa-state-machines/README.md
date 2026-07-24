# Week 4 — Day 2: MFA State Machines and Bypass Testing

Status: Completed

## Objective

This unit examines MFA as a server-side authentication state machine rather
than as a single verification page. It combines secure product requirements,
manual security testing, PortSwigger labs, and a TryHackMe exercise.

No new application or automated test suite was created for this unit.

## Completed work

- Reviewed MFA factors, OTP lifecycle, recovery, replacement, and step-up authentication.
- Solved PortSwigger 2FA simple bypass.
- Solved PortSwigger 2FA broken logic.
- Completed TryHackMe Multi-Factor Authentication to 100%.
- Designed a secure MFA state machine.
- Defined testable MFA security requirements.
- Created a manual security test plan with more than twenty cases.
- Produced two sanitized request/response comparisons.

The optional PortSwigger brute-force stretch lab was not required and was not
included in the completion criteria.

## Core security conclusion

Correct primary credentials prove only that the primary factor succeeded.
They must not create a fully authenticated session when MFA is required.

The server must bind each challenge to the expected user, pending session,
purpose, attempt counter, and expiry time. A successful MFA verification must
atomically consume the challenge and rotate the session identifier.

## Main risks reviewed

- Forced browsing after primary authentication but before MFA.
- Cross-user verification caused by client-controlled identity parameters.
- OTP replay, expiry, resend, and concurrent-submission weaknesses.
- Missing attempt limits and rate limiting.
- Factor replacement without recent re-authentication.
- Inconsistent MFA enforcement across web, API, mobile, and legacy endpoints.
- Fail-open behavior when the MFA service is unavailable.
- Sensitive OTP or session values appearing in logs and responses.

## Deliverables

- `mfa-state-machine.md`: states, transitions, and permitted endpoints.
- `mfa-security-requirements.md`: testable product-security requirements.
- `mfa-test-plan.md`: manual positive and negative test cases.
- `portswigger-lab-review.md`: root-cause analysis without a walkthrough.
- `evidence/`: sanitized request/response comparisons.

## Redaction policy

The repository contains no real OTPs, passwords, cookies, challenge answers,
target IP addresses, or flags.

Examples always use:

- `Password: REDACTED`
- `OTP: REDACTED`
- `Cookie: session=REDACTED`

## References

- OWASP Multifactor Authentication Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
- PortSwigger multifactor authentication material:
  https://portswigger.net/web-security/authentication/multi-factor
