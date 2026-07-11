# Intro to Cross-site Scripting

## Date

2026-07-08

## Status

Completed — 100%.

## Concepts learned

- XSS occurs when untrusted input reaches a sink that the browser interprets as markup or code.
- Reflected XSS returns input in the immediate response.
- Stored XSS saves input and renders it during a later request.
- DOM-based XSS is caused by unsafe browser-side JavaScript data flow.
- The source and sink must be identified before selecting a remediation.
- The payload alone does not explain the vulnerability.

## Commands/tools used

- Browser in the authorized TryHackMe environment
- Burp Proxy
- HTTP history
- Repeater
- Source-to-sink reasoning

## Mistakes

I initially focused more on finding a working payload than on understanding the complete data flow.

The better process is to identify the entry point, storage or processing stage, sink, and output context.

## Connection with my local capstone

The room concepts map directly to:

- `/reflected-vuln` and `/reflected-safe`,
- the vulnerable and safe `/comments` sections,
- the `/dom` comparison between `innerHTML` and `textContent`.

## What needs more practice

I need more practice identifying sources and sinks in large JavaScript codebases.

I also need more practice with HTML attributes, URLs, JavaScript strings, and CSS contexts.

## No flags or answers

I did not publish flags or challenge answers.
