# Threat–Control–Test Matrix

| Threat or requirement | Control | Verification tests | Expected secure result |
|---|---|---|---|
| Predictable session ID | 32 bytes from `secrets.token_bytes` | `test_01`, `test_02`, `test_03` | CSPRNG is called for 32 bytes; IDs have 256 pre-encoding bits and are unique |
| Forged or unknown ID | Server-side lookup with deny by default | `test_04`, `test_05` | Unknown and modified values are rejected |
| Client changes trusted identity data | Opaque ID and server-side state | `test_06`, `test_07`, `test_29` | User, tenant, role, and state come from trusted records |
| Session fixation before login | Revoke presented ID and issue new ID | `test_08`, `test_09` | Pre-login and attacker-supplied values never survive login |
| Authenticated token reused across re-login | Rotate on authentication | `test_10` | Earlier authenticated token is rejected |
| Privilege context changes under same ID | Rotate after privilege change | `test_11`, `test_12`, `test_13` | Old token fails; new elevated token succeeds |
| Rotation extends session forever | Preserve original absolute deadline | `test_19` | New session keeps the old absolute expiry |
| Logout only clears browser state | Server-side revoke plus cookie deletion | `test_14`, `test_15`, `test_25` | Replay fails and browser receives `Max-Age=0` |
| Unattended session remains valid | Server-side idle expiration | `test_16`, `test_17` | Idle deadline expires; accepted activity refreshes only idle time |
| Continuously active stolen session | Server-side absolute expiration | `test_18` | Session expires even with repeated activity |
| Token leaks through URL or headers | Cookie-only token extractor | `test_20`, `test_21`, `test_22` | Query, custom header, and Bearer values are ignored |
| Cookie exposed to script or cross-site requests | `HttpOnly`, `SameSite=Lax`, `Path=/`; production `Secure` | `test_23`, `test_24`, `test_26` | Required attributes are emitted in the correct mode |
| Revoked token becomes usable again | Terminal revoked state | `test_27` | Explicitly revoked session remains denied |
| Raw token leaked in logs | Keyed HMAC fingerprint | `test_28` | Correlation fingerprint is present; original token is absent |
| Client supplies role in body/query/header | Trusted user lookup and server-side authorization | `test_29`, `test_30`, `test_31` | Client-controlled role values grant no privilege |
| User triggers privilege transition | Server-side admin check | `test_32`, `test_33` | Only canonical administrator can step up |
| Parser or routing bypass | Fail closed on malformed cookies, bad login, methods, and routes | `test_34`, `test_35`, `test_37`, `test_38` | Request receives 4xx and no session is issued |
| Sensitive response cached | `Cache-Control: no-store` | `test_36` | Responses direct intermediaries not to retain content |
