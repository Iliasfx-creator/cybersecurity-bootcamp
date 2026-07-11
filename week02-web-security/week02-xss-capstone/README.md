# Week 2 XSS Capstone

## Goal

This capstone combines reflected, stored, and DOM-based cross-site scripting in one intentionally vulnerable local application.

The objective is to trace untrusted input from its source, through any storage or processing stage, to the sink that finally interprets or displays it.

Each vulnerable implementation is paired with a safer implementation for direct comparison.

## Safety scope

Testing is restricted to:

- `http://127.0.0.1:8005`
- `http://localhost:8005`

No public websites, external systems, third-party services, or unrelated local services are authorized.

## Application

The application uses Python's standard-library HTTP server.

Start it with:

```bash
cd week02-web-security/week02-xss-capstone/app
python3 -u server.py
```

The application listens only on `127.0.0.1:8005`.

## Routes

| Route | Purpose |
|---|---|
| `/` | Home page with links and forms for the labs |
| `/reflected-vuln?q=` | Renders query input without HTML escaping |
| `/reflected-safe?q=` | Renders query input with HTML escaping |
| `/comments` GET | Displays stored comments in vulnerable and safe sections |
| `/comments` POST | Stores a comment and returns a `303` redirect |
| `/dom?name=` | Compares `innerHTML` and `textContent` |
| Unknown route | Returns HTTP `404` |

## Test payloads

Automated response marker:

```html
<b>test-marker</b>
```

Browser-only local DOM payload:

```html
<img src=x onerror=alert(1)>
```

The executable browser payload is restricted to this local lab.

## Automated tests

Run:

```bash
python3 week02-web-security/week02-xss-capstone/tests/xss_regression_tests.py
```

The suite verifies:

- the home route,
- reflected vulnerable rendering,
- reflected safe rendering,
- comment redirect behavior,
- comments-page availability,
- vulnerable stored rendering,
- safe stored rendering,
- DOM source and sink presence,
- unknown-route `404` handling.

Each stored rendering test creates the state it requires by submitting its own marker.

A failed check produces a non-zero process exit code.

## Evidence

The `evidence/` directory contains:

- direct reflected HTTP responses,
- direct stored HTTP responses,
- browser-based DOM verification notes,
- Burp Repeater reflected comparisons,
- Burp Repeater stored-flow evidence,
- automated regression-test output.

Credentials, passwords, cookies, tokens, TryHackMe flags, and challenge answers are not stored.

## Source-to-sink model

Reflected XSS:

```text
Query parameter -> server rendering -> HTML response
```

Stored XSS:

```text
POST form data -> in-memory storage -> later HTML rendering
```

DOM XSS:

```text
window.location.search -> URLSearchParams -> innerHTML or textContent
```

## Lessons learned

XSS is not fixed by applying one generic input filter.

The required defense depends on the output context and the parser that receives the value.

For HTML text, context-aware HTML encoding is appropriate.

For plain DOM text, `textContent` is safer than `innerHTML`.

Storage increases persistence and potential impact, but execution occurs only when the stored value reaches an unsafe sink.

`curl` can verify response content but cannot execute JavaScript or validate browser-side DOM behavior.

## Limitations

The server is intentionally small and vulnerable.

Comments are stored only in memory and disappear when the server restarts.

The application has no authentication, database, HTTPS, production framework, or real multi-user behavior.

It must not be exposed beyond the defined local scope.
