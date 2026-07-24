# MFA Security Test Plan

These tests are intended for authorized environments. Values captured during
execution must be sanitized before publication.

| ID | Preconditions | Request/action | Expected HTTP result | Expected session state | Expected state mutation | Security reason |
|---|---|---|---|---|---|---|
| TC-01 | No session | Request a protected account endpoint | `401` or concealed denial | `anonymous` | None | Anonymous forced browsing must fail |
| TC-02 | Primary factor accepted but MFA incomplete | Request a protected account endpoint directly | `403` or concealed denial | `mfa_pending` | None | Primary verification is not full authentication |
| TC-03 | Active bound challenge | Request the MFA verification form | `200` | `mfa_pending` | None | Only MFA-flow endpoints are allowed while pending |
| TC-04 | Active challenge with correct bound OTP | Submit the valid OTP | `200` or `302` | `fully_authenticated` | Challenge consumed and session rotated | Valid completion must elevate exactly once |
| TC-05 | OTP belongs to user A | Submit it while authenticating user B | `401` | `mfa_pending` | Failed-attempt counter increases | Prevent cross-user code use |
| TC-06 | OTP belongs to pending session A | Submit it from pending session B | `401` | Session B remains `mfa_pending` | Failed-attempt counter increases | Prevent cross-session code use |
| TC-07 | OTP issued for login | Submit it for factor replacement or recovery | `401` | Existing state unchanged | Attempt recorded | OTPs must be purpose-bound |
| TC-08 | OTP already used successfully | Replay the same OTP | `401` | Existing authenticated session unchanged | No new elevation | Enforce single use |
| TC-09 | OTP is older than its TTL | Submit the expired OTP | `401` | `expired/revoked` or new `mfa_pending` flow required | Expired challenge revoked | Limit exposure window |
| TC-10 | Active challenge below attempt limit | Submit an invalid OTP | Generic `401` | `mfa_pending` | Attempt counter increases | Invalid values must not reveal useful details |
| TC-11 | One attempt remains | Submit another invalid OTP | `429` or generic lock response | `locked` | Challenge revoked or locked | Enforce strict attempt limit |
| TC-12 | Challenge is locked | Submit any further OTP | `429` | `locked` | No verification processing | Prevent continued brute force |
| TC-13 | Active challenge exists | Request a permitted resend | `200` or `204` | `mfa_pending` | Old challenge revoked; new challenge created | Resend must invalidate the old code |
| TC-14 | Resend limit exceeded | Request another resend | `429` | `mfa_pending` or `locked` | No new challenge | Prevent resend abuse and message flooding |
| TC-15 | MFA operations completed | Inspect URLs, bodies, responses, logs and metrics | No secret returned | State unchanged | Only fingerprints or event IDs logged | Prevent OTP disclosure |
| TC-16 | Session is pending MFA | Complete MFA successfully | `200` or `302` with new cookie | `fully_authenticated` | New session issued | Prevent session fixation |
| TC-17 | MFA caused rotation | Replay the old pre-MFA session | `401` | `expired/revoked` | None | Old tokens must be unusable |
| TC-18 | Pending or authenticated session exists | Perform logout and replay its cookie | Logout `200/204`; replay `401` | `expired/revoked` | Session and challenges revoked | Logout must work server-side |
| TC-19 | Recovery requested for valid and invalid identifiers | Compare both responses | Same generic `200/202` response | `recovery_pending` only when valid internally | No public account disclosure | Prevent account enumeration |
| TC-20 | Fully authenticated session lacks recent step-up | Request factor replacement | `403` | `step_up_required` | No factor change | Protect factor-management operations |
| TC-21 | Step-up succeeds for factor replacement | Replace the factor | `200/204` | `fully_authenticated` with rotated session | Factor changed, notification sent, sessions reviewed | Detect and contain account takeover |
| TC-22 | MFA is pending | Test equivalent web, API, mobile and legacy protected endpoints | All deny consistently | `mfa_pending` | None | Prevent enforcement gaps across channels |
| TC-23 | MFA verification service is unavailable | Submit verification or request protected operation | `503` and no protected data | State remains non-authenticated | No elevation | Dependency failure must fail closed |
| TC-24 | Same valid OTP submitted concurrently twice | Send synchronized verification requests | Exactly one success; other request rejected | One `fully_authenticated` session | Challenge consumed once | Prevent race-condition replay |
| TC-25 | Fully authenticated session requests high-risk export | Attempt without current step-up, then complete step-up | First `403`; second authorized according to policy | `step_up_required` then `fully_authenticated` | Session rotates after step-up | Require fresh assurance for sensitive actions |
