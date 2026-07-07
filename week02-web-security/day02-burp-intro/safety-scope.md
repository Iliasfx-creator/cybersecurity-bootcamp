# Safety Scope

## Allowed targets

- http://127.0.0.1:8000
- http://localhost:8000

## Disallowed targets

I will not intercept, modify, attack, or test public websites, university systems, company systems, or accounts that I do not own.

## Why this matters

Proxy tools can modify real HTTP requests.

Using them against systems without permission can cause legal, ethical, and security problems.

Even simple request modification can change how a server behaves.

A proxy makes it easy to tamper with parameters, headers, methods, and form data, so strict scope is required.

I should treat Burp as a powerful security tool, not as a normal browser extension.

## Lab rule

For this lab, Burp is only used against my local Python HTTP server.

No public websites, real accounts, or third-party systems are in scope.
