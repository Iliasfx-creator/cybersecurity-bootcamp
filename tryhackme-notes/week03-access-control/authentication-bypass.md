# TryHackMe — Authentication Bypass

## Status

- Completed: 100%
- Scope: authorized TryHackMe training environment
- Redaction: no answers, flags, target addresses, cookies, usernames,
  credentials, or reset links are recorded here

## Enumeration

- Authentication flows can disclose whether an account exists through
  different messages, response lengths, status codes, or timing.
- Enumeration reduces the search space for later password attacks and can also
  expose private account membership.
- Registration, login, recovery, invitation, and support flows should use
  consistent external responses.
- Internal logs can retain diagnostic detail without returning that detail to
  an untrusted client.

## Rate limiting

- A weak password policy becomes more dangerous when login and recovery
  endpoints allow unlimited attempts.
- Limits should consider account, source, device, tenant, and global patterns;
  a single IP-only rule is easy to distribute around and can create denial of
  service against shared users.
- Backoff, monitoring, alerting, breached-password defenses, and strong
  multi-factor authentication complement rate limiting.
- The server should rate-limit both failed authentication and abuse of account
  discovery or reset workflows.

## Logic flaws

- A secure-looking multi-step flow can fail when later processing trusts a
  different parameter source than the earlier validation step.
- Duplicate parameter names across query strings and request bodies can create
  ambiguous precedence and allow an attacker to replace a previously checked
  value.
- Security decisions must bind the account, destination, purpose, expiry, and
  one-time reset state together on the server.
- The final action must revalidate the complete workflow rather than assuming
  earlier pages were followed correctly.

## Cookie tampering

- Plain-text client cookies such as login or administrator booleans are not
  proof of identity or privilege.
- Base64 changes representation but provides no confidentiality, integrity, or
  authenticity. A client can decode, modify, and re-encode it.
- Unsalted MD5 is deterministic and unsuitable for password storage. Common
  values can often be recovered through precomputed or dictionary lookup.
- Privileges should be resolved from trusted server-side session state, or from
  a cryptographically protected token that is fully validated and revocable as
  required by the application.

## Remediation

- Use generic external responses for account discovery-sensitive operations.
- Apply layered rate limits, monitoring, lockout safeguards, and MFA.
- Use one canonical input source and reject conflicting security parameters.
- Bind reset tokens to one account, destination, purpose, short expiry, and
  one-time state; invalidate them after use or account changes.
- Store passwords with a modern password-hashing function and unique salts.
- Keep roles and authorization state server-side; never trust an unsigned or
  unauthenticated privilege cookie.
- Apply `Secure`, `HttpOnly`, and appropriate `SameSite` cookie attributes, but
  remember that attributes do not make client-supplied authorization values
  trustworthy.

## Mistakes and lessons learned

- I initially focused on individual fields instead of tracing which input
  source the application used at each workflow step.
- I reinforced the difference between hashing and encoding: hashing is designed
  to be one-way, while encoding is reversible.
- A successful login state does not prove that authorization is correct; the
  server must still authorize every protected action.
- The most useful testing habit is to establish a normal baseline, change one
  client-controlled value at a time, observe the side effect, and identify the
  missing server-side control.
