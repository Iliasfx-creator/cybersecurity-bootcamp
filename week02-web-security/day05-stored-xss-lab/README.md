# Day 5 — Stored XSS Lab

## Goal

The goal of this lab was to understand stored XSS and why persistence makes it more dangerous than reflected XSS.

I built a local comment application where submitted comments were stored in memory and rendered later on the page.

## Safety scope

This lab was limited to:

- http://127.0.0.1:8003
- http://localhost:8003

No public websites, real accounts, third-party applications, university systems, or company systems were tested.

## Tools used

- Python
- BaseHTTPRequestHandler
- curl
- browser
- Burp Suite
- html.escape
- bash

## App behavior

The app implemented:

- GET /
- POST /comment

POST /comment read the comment field from the request body and stored it in a server-side comments list.

GET / rendered the stored comments.

## Vulnerable comments section

The vulnerable section rendered stored comments directly into the HTML response.

This meant a stored value such as:

<script>alert(1)</script>

appeared as raw HTML/script inside the page.

## Safe comments section

The safe section rendered the same stored comments using html.escape.

This changed special characters into safe text entities.

The browser displayed the payload as text instead of interpreting it as JavaScript.

## Burp observations

Burp showed the POST request that submitted the comment and the GET request that rendered the page.

This made it clear that the payload entered through one request and appeared later in a different response.

## Difference from reflected XSS

In reflected XSS, the payload appears immediately in the response to the same request.

In stored XSS, the payload is stored by the application and rendered later.

Stored XSS is usually more dangerous because it can affect future viewers of the page.

## Security relevance

Stored XSS matters because stored user input can become executable browser code if rendered unsafely.

The core issue is unsafe output handling at the sink.

The fix is context-aware output encoding before rendering user-controlled data.

## Mistakes / difficulties

The main difficulty was separating source, storage, and sink.

The source was the POST /comment body.

The storage was the comments list in server memory.

The sink was the HTML response where comments were rendered.
