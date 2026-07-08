# Day 4 — Reflected XSS Lab

## Goal

The goal of this lab was to understand reflected XSS by comparing a vulnerable route with a fixed route.

I created one route that reflected user input without escaping and another route that used html.escape before returning the input in an HTML response.

## Safety scope

This lab was limited to:

- http://127.0.0.1:8002
- http://localhost:8002

No public websites, university systems, company systems, accounts, or third-party applications were tested.

## Tools used

- Python
- BaseHTTPRequestHandler
- curl
- browser
- Burp Suite
- html.escape
- bash

## Routes implemented

The app implemented:

- GET /
- GET /vuln-search?q=...
- GET /safe-search?q=...

The root route returned a page with two forms.

The vulnerable route reflected q without escaping.

The safe route reflected q after applying html.escape.

## Vulnerable route behavior

The vulnerable route inserted q directly into the HTML response.

When the payload contained script tags, the response included those tags raw.

This created reflected XSS behavior because the browser could interpret the reflected input as code.

## Safe route behavior

The safe route used html.escape before returning q.

This changed characters such as < and > into safe text representations.

As a result, the browser displayed the payload as text instead of executing it as JavaScript.

## Burp observations

Burp showed the exact GET requests sent to both routes.

The vulnerable and safe requests used the same payload.

The difference was not the request. The difference was how the backend handled the input before building the response.

## What I learned about output encoding

I learned that output encoding must happen before user-controlled input is placed into an HTML response.

For HTML body context, escaping characters such as < and > prevents the browser from interpreting input as markup or script.

The source was the q parameter.

The sink was the HTML response body.

## Security relevance

Reflected XSS matters because a crafted URL can cause attacker-controlled input to appear in a response.

If the response treats that input as code, the browser may execute it.

The correct fix is not blocking one specific payload. The correct fix is safe output handling based on context.

## Mistakes / difficulties

The main difficulty was understanding that the payload is not the root cause.

The root cause is unsafe reflection of user-controlled input into an HTML response.

Another important point was comparing the raw vulnerable response with the escaped safe response.
