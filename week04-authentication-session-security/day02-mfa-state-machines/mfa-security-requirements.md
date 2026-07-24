# MFA Security Requirements

The numeric limits below are an explicit product-security baseline and should
be adjusted only through documented risk review.

## MFA-REQ-01 — Primary verification is not full authentication

Given a user whose primary factor is valid, when the user has not completed the
required MFA challenge, then protected resources must remain unavailable and
the session must not be marked fully authenticated.

## MFA-REQ-02 — Challenge binding

Given an issued MFA challenge, when it is verified, then the server must confirm
that it belongs to the same user, pending session, and authentication purpose.

## MFA-REQ-03 — Secure generation and storage

Given a new OTP, when it is generated and stored, then a CSPRNG must be used and
the real value must not be stored in plaintext or written to logs. A protected
keyed verifier should be preferred for low-entropy codes.

## MFA-REQ-04 — Short lifetime

Given an issued OTP, when five minutes have passed without successful use, then
the code must expire and verification must fail without extending its lifetime.

## MFA-REQ-05 — Single use

Given a successfully verified OTP, when the same value is submitted again, then
the server must reject it because successful verification atomically consumes it.

## MFA-REQ-06 — Strict attempt limit

Given an active challenge, when five invalid attempts have occurred, then the
challenge must be locked or revoked and further submissions must be rejected.

## MFA-REQ-07 — Secure resend

Given an active challenge, when a resend succeeds, then the previous challenge
must be invalidated, a new challenge must be created, and resend frequency must
be rate-limited.

## MFA-REQ-08 — No OTP disclosure

Given any MFA request, response, URL, error, metric, or log event, when it is
recorded or returned, then the real OTP must never appear.

## MFA-REQ-09 — Session rotation

Given successful MFA or step-up verification, when the authentication state is
elevated, then the server must issue a new session identifier and revoke the old
identifier.

## MFA-REQ-10 — Server-side identity and state

Given any MFA request, when it contains a username, role, factor state, or other
identity claim controlled by the client, then the server must ignore it for
security decisions and use server-side session state.

## MFA-REQ-11 — Factor change requires recent verification

Given a fully authenticated user, when the user requests factor removal,
replacement, or recovery-setting changes, then recent re-authentication or
step-up verification must be required.

## MFA-REQ-12 — Replacement response

Given a successfully replaced factor, when the change completes, then the user
must receive an independent notification and existing sessions must be reviewed
or revoked according to policy.

## MFA-REQ-13 — Channel and version parity

Given the same account state, when requests arrive through web, API, mobile, or
legacy endpoints, then all channels must enforce the same MFA state requirements.

## MFA-REQ-14 — Fail-closed dependency behavior

Given that the MFA service or verification dependency is unavailable, when an
MFA-protected operation is requested, then the operation must fail closed and
must not elevate the session.

## MFA-REQ-15 — Secure recovery

Given account recovery, when an identifier is submitted, then the response must
not reveal account existence and successful recovery must require appropriately
strong, independently verified evidence.

## MFA-REQ-16 — Step-up authentication

Given a fully authenticated session that requests a high-risk action, when its
recent-authentication requirement is not satisfied, then the action must be
blocked until step-up verification succeeds.

## MFA-REQ-17 — Logout and revocation

Given a pending or fully authenticated session, when logout or administrative
revocation occurs, then the server must invalidate the session and all pending
challenges associated with it.

## MFA-REQ-18 — Concurrent verification safety

Given two concurrent submissions of the same valid OTP, when they reach the
server, then atomic challenge consumption must allow at most one submission to
succeed.
