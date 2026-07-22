# PortSwigger Persistent-Session Study Notes

## Core concept

A persistent or “remember me” cookie becomes an alternate authentication
mechanism. Its value must be unpredictable, independently revocable, scoped,
expired, and verified server-side. Base64 is only encoding; it does not make a
predictable username, timestamp, or password-derived value safe.

## Testing method

1. Establish a normal baseline with the persistent-login option disabled.
2. Enable it and compare response cookies and later unauthenticated requests.
3. Determine which cookie actually restores the identity.
4. Inspect structure without publishing the value.
5. Test invalid, modified, expired, and revoked values.
6. Check whether logout invalidates the persistent credential server-side.
7. Check whether a password or privilege change invalidates older persistent
   credentials.

## Lab 1

Status: Solved

Lab selected: Brute-forcing a stay-logged-in cookie

### Observation

A deterministic persistent cookie could be reconstructed from a username and a fast password hash. A candidate list allowed authentication as another user without knowing a server-issued opaque token.

### Root cause

The application derived the persistent credential from predictable client-visible identity data and an unsalted MD5 password hash instead of issuing a random server-side token.

### Remediation

Issue an opaque CSPRNG token, keep identity and lifecycle state server-side, enforce expiration and revocation, rotate after authentication changes, and rate-limit suspicious persistent-login attempts. Persistent credentials must never contain password-derived material.

### Mistake or difficulty

I initially tested one payload and received only redirects. I corrected the payload count, kept one password per line, and verified the processing order with my own account before testing the victim account.

## Lab 2

Status: Solved

Lab selected: Offline password cracking

### Observation

Stored XSS could read a non-HttpOnly persistent cookie. Decoding the cookie exposed a username and a fast password hash that could be tested offline.

### Root cause

The application combined stored XSS, a script-readable persistent cookie, and password-derived data inside the client-side credential. A fast unsalted hash did not protect a guessable password.

### Remediation

Prevent stored XSS with contextual output encoding and input handling, set HttpOnly on authentication cookies, use opaque random persistent tokens backed by revocable server-side state, and store passwords server-side with a salted adaptive password hashing algorithm.

### Mistake or difficulty

The exploit log initially contained only my own requests. I corrected the callback hostname, placed the payload in the blog comment, and waited for the simulated victim request.

## Reference

- [PortSwigger authentication: other mechanisms](https://portswigger.net/web-security/authentication/other-mechanisms)
