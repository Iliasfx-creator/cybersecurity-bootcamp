# PortSwigger MFA Lab Review

No credentials, OTP values, cookies, challenge answers, or full walkthroughs
are included.

## 2FA simple bypass

Status: Solved

### Normal authentication flow

The expected flow required successful primary authentication, completion of a
second-factor challenge, and only then access to the account page.

### Trust boundary that failed

The protected account endpoint trusted a session that had completed only the
primary factor. The verification page existed, but the endpoint performing the
protected action did not enforce the MFA state.

### Root cause

The application treated primary authentication as sufficient session
authentication. MFA enforcement depended on following the intended navigation
flow instead of a server-side authorization check on each protected request.

### Impact

An actor with valid primary credentials could bypass the second factor through
direct navigation to a protected endpoint. This defeats the main protection MFA
is intended to provide after password compromise.

### Secure remediation

Represent authentication as explicit server-side states. Every protected
endpoint must require `fully_authenticated`, while `primary_verified` and
`mfa_pending` sessions must be denied. Rotate the session identifier after
successful MFA.

### Retest criteria

- Direct access before MFA is denied.
- Web, API, mobile, and legacy routes enforce the same state.
- Completing MFA rotates the session.
- The old pre-MFA session remains denied.
- Logout revokes both pending and authenticated sessions.

### Personal mistake or lesson

The important lesson was that the presence of an MFA form does not prove that
MFA protects the application. Testing must target the protected endpoint
directly from each intermediate authentication state.

## 2FA broken logic

Status: Solved

### Normal authentication flow

The expected flow linked primary authentication and second-factor verification
to the same account before granting access to its account page.

### Trust boundary that failed

A client-controlled verification selector was trusted to decide which user's
MFA challenge was created and verified. This separated the identity established
by the primary factor from the identity selected during MFA.

### Root cause

The server did not derive the MFA subject exclusively from server-side pending
session state. The challenge was not securely bound to the authenticated user,
pending session, and purpose.

### Impact

An attacker could interfere with another account's MFA verification flow and
obtain an authenticated session for an unintended account after discovering a
valid code in the controlled lab.

### Secure remediation

Store the pending user identity server-side immediately after primary
authentication. Bind every challenge to that user, the pending session,
purpose, TTL, attempt counter, and one-time status. Ignore client-supplied
identity selectors and rotate the session after successful verification.

### Retest criteria

- Changing any client-controlled user selector cannot change the MFA subject.
- A code issued for one user fails for another.
- A code issued for one session fails in another.
- Invalid attempts and resends are strictly limited.
- Successful verification consumes the code atomically.
- The resulting session belongs only to the server-side pending identity.

### Personal mistake or lesson

During testing, I initially changed the selector in a Repeater request and
expected the browser's later request to inherit that change. The browser and
Repeater maintain independent request data. This reinforced the need to inspect
and control every security-relevant value in the exact request being tested.
