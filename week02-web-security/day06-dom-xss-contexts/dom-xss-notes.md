# DOM XSS Notes

## What DOM XSS is

DOM XSS happens when browser-side JavaScript reads user-controlled input and writes it into the DOM unsafely.

The vulnerability can exist even when the server returns a static page.

## Source

A source is where user-controlled input enters the client-side code.

In this lab, the source was window.location.search, read through URLSearchParams.

## Sink

A sink is where the input is used.

In this lab, the dangerous sink was innerHTML.

The safer sink for plain text was textContent.

## Dangerous sinks

Dangerous sinks include APIs that parse strings as HTML or code.

Examples include:

- innerHTML
- outerHTML
- document.write
- insertAdjacentHTML
- eval

These are risky when used with untrusted input.

## Safer alternatives

For plain text, safer alternatives include:

- textContent
- innerText
- creating text nodes

These avoid parsing the value as HTML.

## Why server-side logs may miss DOM XSS

Server-side logs may only show that the browser requested the static page.

The dangerous behavior can happen later inside the browser after JavaScript reads the URL and modifies the DOM.

This means defenders also need client-side code review and front-end security testing.

## What I should never do outside a lab

I should never test DOM XSS payloads on public websites, university systems, company systems, accounts, or third-party applications without permission.

DOM XSS testing belongs only in local labs, owned systems, or authorized assessments.
