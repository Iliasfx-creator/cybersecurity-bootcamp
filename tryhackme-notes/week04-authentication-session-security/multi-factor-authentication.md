# TryHackMe — Multi-Factor Authentication

Status: 100% completed

No flags, answers, OTP values, credentials, cookies, or target IP addresses are
stored in these notes.

## Concepts

- MFA requires factors from different categories, such as knowledge and possession.
- Two secrets of the same category do not necessarily provide true multifactor assurance.
- Primary authentication and MFA completion are separate server-side states.
- OTPs require short lifetimes, single use, strict attempt limits, and secure generation.
- A verification challenge must be bound to the intended user, session, and purpose.
- Auto-logout alone does not prevent automation when an attacker can repeatedly create new sessions.
- Client-controlled identity or role values must never decide the authenticated subject.
- Recovery and factor replacement are high-risk authentication flows.
- Sensitive operations may require step-up authentication even in an existing session.

## Testing methodology

1. Map the complete authentication state machine.
2. Record cookies and redirects at each transition without publishing their values.
3. Attempt direct access to protected routes before completing MFA.
4. Test whether user identifiers in requests can change the verification subject.
5. Submit invalid values and observe attempt limits, logout, and lock behavior.
6. Test resend, expiry, replay, and concurrent submissions.
7. Verify whether successful MFA rotates the session.
8. Replay pre-MFA and logged-out sessions.
9. Compare web, API, mobile, and legacy enforcement.
10. Review recovery and factor replacement separately from ordinary login.

## Commands

The following commands use placeholders and contain no real target information:

```bash
echo "TARGET_IP mfa.thm" | sudo tee -a /etc/hosts
getent hosts mfa.thm
python3 exploit.py
```

The controlled exercise used an automation script that recreated a login
session after failed verification attempts. The script and its sensitive output
were used only inside the authorized lab and were not committed.

## Mistakes

- Initially treating an MFA page as proof that protected endpoints enforce MFA.
- Forgetting that a failed attempt may destroy the current pending session.
- Assuming changes made in one HTTP tool automatically modify browser cookies.
- Focusing only on the OTP value instead of its user, session, purpose, and state bindings.
- Using redirects alone as a success signal without checking the resulting identity and state.

## Lessons learned

- MFA security is primarily a state-management and binding problem.
- Every protected endpoint must enforce the required authentication state.
- Attempt limits must apply across recreated sessions and not only per request.
- Re-authentication loops can defeat weak per-session brute-force protections.
- OTP success, challenge consumption, and session elevation must be atomic.
- Factor recovery can be more dangerous than the normal login path.
- Useful security logs contain event IDs, actor information, outcomes, and token
  fingerprints, but never real OTPs or session values.
