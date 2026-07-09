# Safety Scope

## Allowed targets

- http://127.0.0.1:8003
- http://localhost:8003

## Disallowed targets

No public websites, university systems, company systems, accounts, or third-party applications.

## Lab rule

Stored XSS payloads are used only against my own local intentionally vulnerable application.

I will not test stored XSS payloads on systems I do not own or do not have explicit permission to test.

## Why this matters

Stored XSS can affect other users who view the stored content.

Testing this without permission can create real harm, logs, alerts, and legal problems.

A payload that is local and controlled in this lab would be unacceptable against real third-party systems.
