# TryHackMe Corridor

Status: Completed

## Concepts

- Insecure Direct Object Reference
- Predictable identifiers
- Hashed or opaque identifiers
- Object-level authorization
- Security through obscurity

## Recognition

The application exposed resources through URL paths containing fixed-length
hexadecimal identifiers. Comparing several paths showed that the identifiers
were deterministic representations of a small and predictable identifier
space.

Testing an identifier that was not linked by the interface showed that the
server accepted it without verifying whether the location should be accessible.

## Why the identifiers were not authorization

Hashing an identifier changes its appearance but does not establish whether
the current user is authorized to access the referenced object.

If the input space is small or predictable, an attacker can generate candidate
identifiers. Even unpredictable identifiers would only make discovery harder;
the server must still enforce access control for every requested object.

## Difficulty

The main difficulty was recognizing that the hexadecimal paths represented
hashed values rather than random authorization tokens. Comparing multiple
examples helped reveal the predictable relationship.

## Connection with Day 1

This reinforces the Day 1 IDOR model:

1. The client supplies an object reference.
2. The server resolves that reference.
3. The server fails to verify authorization for the resolved object.

The encoding or visual complexity of the reference does not change the missing
server-side ownership or access check.

## Remediation

- Enforce object-level authorization for every request.
- Check ownership or permission after resolving the identifier.
- Deny access by default.
- Use non-predictable identifiers only as defense in depth.
- Do not treat hidden links, encoding, or hashing as an access-control mechanism.

## Evidence handling

The challenge answer, target address, and generated identifier values are
intentionally omitted.
