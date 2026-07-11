# TryHackMe XSS Notes

## Status

Completed learning sections:

- Intro to Cross-site Scripting — 100%
- XSS Introduction — 100%

The OWASP Juice Shop XSS-specific task is documented separately and remains not completed.

## Reflected XSS

User-controlled input is returned in the immediate HTTP response and reaches an HTML sink.

The correct defense depends on the output context. In an HTML-text context, context-aware HTML encoding prevents markup from being interpreted.

## Stored XSS

User-controlled input is stored and later rendered.

Storage increases persistence and possible impact, but execution occurs only when the stored value reaches an unsafe sink.

Stored values should generally remain in their original form, while every output location applies the correct context-specific defense.

## DOM-based XSS

Browser-side JavaScript reads a value from a source such as `window.location.search` and passes it to a dangerous sink such as `innerHTML`.

For untrusted plain text, `textContent` avoids invoking the HTML parser.

## Source-to-sink workflow

1. Identify the user-controlled source.
2. Determine whether the value is transformed or stored.
3. Identify the final sink.
4. Determine the parser and output context.
5. Compare vulnerable and safe behavior.
6. Select a remediation for that exact context.

## What connected with my local labs

My capstone reproduced:

- reflected raw and escaped HTML rendering,
- stored raw and escaped rendering,
- DOM behavior using `innerHTML` and `textContent`,
- Burp request and response comparison,
- browser-only validation of DOM execution.

## What was different from my local labs

The TryHackMe applications contained more routes, client-side logic, application state, and framework behavior.

My local app was deliberately small so each source, storage stage, sink, and context could be traced directly.

## Mistakes and unclear points

I initially concentrated on payloads instead of data flow.

I also initially assumed that opening Burp automatically configured browser interception.

I still need more practice with attribute, JavaScript, URL, and CSS output contexts.

## No flags / no answers note

I did not publish flags or challenge answers.
