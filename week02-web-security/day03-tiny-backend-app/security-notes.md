# Security Notes

## Input handling

Input handling means reading and processing data that comes from the client.

In this lab, input came from:

- the q query parameter in GET /search
- username and password fields in POST /login

Client input should never be blindly trusted.

## Output encoding

Output encoding means converting special characters before placing user input into a response.

This prevents the browser from interpreting user input as HTML or JavaScript.

## Why html.escape was used

html.escape(q) was used before placing the search value into the HTML response.

This reduces XSS risk because characters such as <, >, and & are escaped.

Without escaping, user input containing HTML tags or scripts could be interpreted by the browser as real HTML or JavaScript.

With escaping, the input is displayed as text instead of executed or rendered as markup.

## Authentication logic

The login route checked whether the submitted username and password matched the server-side USERS dictionary.

If the values matched, the server returned Login successful.

If they did not match, the server returned Login failed with status 401.

This is simple authentication logic for a lab, not production-grade authentication.

## Why hardcoded credentials are bad

Hardcoded credentials are bad because they can be exposed in source code, commits, logs, backups, or screenshots.

In real applications, credentials should not be stored directly in source code.

They should be stored securely, hashed when appropriate, and managed through safer configuration or secret management systems.

## Why HTTP is unsafe for login forms

HTTP is not encrypted.

If credentials are sent over plain HTTP on a real network, someone who can observe the traffic may be able to read them.

Login forms should use HTTPS so credentials are protected in transit.

## What would need to improve before production

Before production, this app would need:

- HTTPS
- no hardcoded credentials
- password hashing
- secure session management
- CSRF protection
- stronger input validation
- better logging
- better error handling
- separation between code and secrets
