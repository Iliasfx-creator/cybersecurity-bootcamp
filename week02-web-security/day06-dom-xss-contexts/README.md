# Day 6 — DOM XSS and Context-Aware Encoding

## Goal

The goal of this lab was to understand DOM XSS and why context-aware encoding matters.

The lab compared a vulnerable DOM sink using innerHTML with a safer plain-text sink using textContent.

## Safety scope

This lab was limited to:

- http://127.0.0.1:8004
- http://localhost:8004

No public websites, real accounts, university systems, company systems, or third-party applications were tested.

## Tools used

- HTML
- JavaScript
- Browser
- Python http.server
- curl
- URLSearchParams

## App behavior

The page read the name parameter from the URL query string.

The same value was written into two places:

- vulnerable-output using innerHTML
- safe-output using textContent

## Vulnerable sink

The vulnerable sink was innerHTML.

innerHTML parsed the value as HTML.

This means injected markup could be interpreted by the browser.

## Safe sink

The safer sink was textContent.

textContent inserted the value as text instead of parsing it as HTML.

For plain text output, textContent is safer than innerHTML.

## Difference from server-side XSS

In reflected and stored XSS, the server returned unsafe HTML.

In DOM XSS, the server can return a static page, but browser-side JavaScript creates the unsafe DOM behavior.

The source was the URL query string.

The sink was innerHTML in the browser DOM.

## Security relevance

DOM XSS matters because vulnerabilities can exist in front-end JavaScript.

Server-side output encoding alone does not fix unsafe client-side DOM sinks.

Developers need to understand where data enters JavaScript and where it is written in the DOM.

## Mistakes / difficulties

The main difficulty was understanding that curl does not execute JavaScript.

The browser behavior matters more for DOM XSS because the vulnerable processing happens client-side.

Another difficulty was separating HTML body encoding from DOM sink safety.
