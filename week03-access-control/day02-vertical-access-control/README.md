# Day 2 — Vertical Access Control

## Objective

Study how broken vertical access controls allow unauthorized users to access privileged functionality.

## Activities Completed

- Studied vertical, horizontal, and context-dependent access controls.
- Completed three PortSwigger Web Security Academy access-control labs.
- Completed the TryHackMe Broken Access Control room.
- Inspected HTTP requests, responses, JavaScript, and cookies using Burp Suite.

## Key Lessons

- Authentication identifies a user, session management links requests to that user, and authorization determines what the user may do.
- Hiding an admin link or using an unpredictable URL does not enforce authorization.
- Client-controlled role information must not be trusted.
- Privileged actions require server-side authorization checks on every request.
- Applications should deny access by default and follow the principle of least privilege.

## Safety and Redaction

Testing was performed only in intentionally vulnerable, authorized training environments.

No flags, passwords, credentials, session values, or lab-specific solution values are included.
