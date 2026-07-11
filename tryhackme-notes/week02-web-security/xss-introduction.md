# XSS Introduction

## Date

2026-07-08

## Status

Completed — 100%.

## Concepts learned

- Browser execution must be distinguished from raw HTTP response content.
- HTML encoding is appropriate for an HTML-text output context.
- `textContent` is safer than `innerHTML` when the requirement is plain text.
- Input validation and output encoding solve different problems.
- Sanitization is required only when controlled HTML must intentionally be supported.
- Content Security Policy is defense in depth and does not replace fixing the sink.
- Cookie flags can limit some consequences but do not remove the XSS vulnerability.

## Commands/tools used

- Browser
- Burp Proxy
- Burp Repeater
- HTTP request and response comparison
- Local browser verification
- `curl` for non-executing response inspection

## Mistakes

I initially expected `curl` to demonstrate DOM execution.

`curl` retrieves the response but does not construct a DOM or execute JavaScript, so browser verification is required.

## Connection with my local capstone

The local capstone provided separate vulnerable and safe sinks for reflected, stored, and DOM behavior.

The automated marker verified response transformation, while the browser-only marker verified DOM execution.

## What needs more practice

I need more practice selecting the correct encoder or safe API for each output context.

I also need more practice reviewing framework-generated client-side code.

## No flags or answers

I did not publish flags or challenge answers.
