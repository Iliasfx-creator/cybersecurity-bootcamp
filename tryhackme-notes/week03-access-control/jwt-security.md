# TryHackMe — JWT Security

Status: Completed 100%

## Core concepts

A JSON Web Token contains three Base64URL-encoded parts:

- Header: identifies the token type and signing algorithm.
- Payload: contains claims about the subject.
- Signature: protects the integrity of the header and payload.

Decoding a JWT does not verify that it is authentic. The payload is readable and
must not contain passwords, secrets, flags, or other sensitive information.

## Claims

Important claims include:

- `sub`: subject represented by the token.
- `iss`: service that issued the token.
- `aud`: service that should accept the token.
- `iat`: time at which the token was issued.
- `nbf`: time before which the token must not be accepted.
- `exp`: time after which the token must be rejected.

Claims must only be trusted after cryptographic and semantic validation.

## Signature validation mistakes

The room demonstrated these implementation risks:

- Disabling signature verification.
- Accepting the `none` algorithm.
- Trusting the algorithm supplied by the token without an allowlist.
- Using a predictable symmetric signing secret.
- Mixing symmetric and asymmetric algorithms.
- Treating an asymmetric public key as an HMAC secret.

The server must explicitly allow the expected algorithm and use the correct key
type for that algorithm.

## Token lifetimes

Tokens require short and appropriate lifetimes. A token without `exp`, or with
an excessive lifetime, increases the impact of theft and replay.

Applications should validate `exp`, `nbf`, `iat`, `iss`, and `aud` as required.
Refresh and revocation mechanisms should be designed for the application's risk.

## Cross-service relay attacks

A valid token issued for one service must not automatically work on another
service. Each receiving service must verify that the `aud` claim identifies
that specific service and that the `iss` claim identifies a trusted issuer.

Signature validation alone is not sufficient if audience validation is missing.

## Testing methodology

- Establish a valid-token baseline.
- Decode the header and payload without treating them as trusted.
- Check for sensitive information in claims.
- Verify that modified payloads are rejected.
- Test missing or invalid signatures.
- Test unexpected algorithms.
- Test expired, not-yet-valid, and missing-lifetime claims.
- Test tokens issued for a different audience.
- Confirm that server-side authorization still applies after token validation.

## Mistakes and difficulties

A JWT library was unavailable during one exercise, so the token was generated
using Python's standard Base64URL and HMAC functionality. This reinforced that
token structure and signature validation should be understood independently of
a specific library.

## Remediation lessons

- Never place sensitive information inside JWT claims.
- Verify signatures on every authenticated request.
- Use an explicit algorithm allowlist.
- Use strong, randomly generated signing keys.
- Keep asymmetric and symmetric verification paths separate.
- Validate issuer, audience, lifetime, and required claims.
- Apply authorization after successful token validation.
- Plan token rotation and revocation.

## Redaction

Authorization: Bearer REDACTED  
Cookie: session=REDACTED  
Password: REDACTED
