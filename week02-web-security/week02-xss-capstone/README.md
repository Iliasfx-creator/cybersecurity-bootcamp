# Week 2 XSS Capstone

## Goal

This capstone combines reflected, stored, and DOM-based cross-site scripting into one local application.

The objective is to trace untrusted input from its source to storage and finally to the sink that interprets or displays it.

Each vulnerable implementation is paired with a safer implementation so the behavior can be compared directly.

## Safety scope

Testing is restricted to:

- `http://127.0.0.1:8005`
- `http://localhost:8005`

No external hosts, public websites, third-party systems, or unrelated services are authorized.

## Application

The application uses Python's standard-library HTTP server.

Start it with:

```bash
cd week02-web-security/week02-xss-capstone/app
python3 -u server.py

The application listens only on 127.0.0.1:8005.

Routes
Route	Purpose
/	Home page with links and forms for all labs
/reflected-vuln?q=	Renders query input without HTML escaping
/reflected-safe?q=	Renders query input with HTML escaping
/comments GET	Displays vulnerable and escaped stored comments
/comments POST	Stores a comment and returns a 303 redirect
/dom?name=	Compares innerHTML with textContent
Unknown route	Returns HTTP 404
Test payloads

Automated response marker:

<b>test-marker</b>

Local browser-only DOM payload:

<img src=x onerror=alert(1)>

The browser payload must never be used outside the authorized local lab.

Automated tests

Run:

python3 week02-web-security/week02-xss-capstone/tests/xss_regression_tests.py

The suite verifies:

home route status,
vulnerable reflected rendering,
safe reflected rendering,
comment redirect behavior,
comments page status,
vulnerable stored rendering,
safe stored rendering,
DOM source and sink presence,
unknown-route 404 handling.

Each stored rendering test creates the state that it requires.

A failed check produces a non-zero process exit status.

Evidence

The evidence/ directory contains:

direct reflected HTTP responses,
direct stored HTTP responses,
browser-based DOM verification notes,
Burp Repeater reflected comparisons,
Burp Repeater stored-flow evidence,
automated regression-test output.

Sensitive values, credentials, cookies, tokens, and challenge answers are not stored.

Source-to-sink model

Reflected XSS:

Query parameter -> server rendering -> HTML response

Stored XSS:

POST form data -> in-memory storage -> later HTML rendering

DOM XSS:

window.location.search -> URLSearchParams -> innerHTML or textContent
Main lessons

XSS is not fixed by applying one generic input filter.

The required defense depends on the output context and the parser that receives the value.

For HTML text, context-aware HTML encoding is appropriate.

For plain DOM text, textContent is safer than innerHTML.

Storage increases persistence and impact, but execution occurs only when data reaches an unsafe sink.

curl can verify response content but cannot execute JavaScript or validate browser DOM behavior.

Limitations

The server is intentionally small and vulnerable.

Comments exist only in memory and disappear after the server restarts.

The application has no authentication, database, HTTPS, or production framework.

It must not be exposed beyond the defined local scope.
