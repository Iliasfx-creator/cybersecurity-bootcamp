# Day 2 — Burp Suite Intro

## Goal

The goal of this lab was to learn the basic role of Burp Suite as an HTTP proxy.

I used Burp to observe browser requests, inspect parameters and headers, and safely modify a local request before it reached my local Python HTTP server.

## Safety scope

This lab was limited to:

- http://127.0.0.1:8000
- http://localhost:8000

I did not intercept, modify, or test public websites, real accounts, university systems, company systems, or systems I do not own.

## Tools used

- Burp Suite Community
- Browser
- Python http.server
- curl
- HTML
- bash

## Local server setup

I created a simple local HTML page with a GET search form and a POST login form.

The local server was started with:

python3 -m http.server 8000

The server listened locally on port 8000.

## Burp proxy setup

Burp Proxy was configured to listen on:

127.0.0.1:8080

The browser was configured to use Burp as its HTTP proxy.

This allowed browser requests to pass through Burp before reaching the local web server.

## Requests captured

I captured:

- GET /
- GET /search?q=test
- GET /search?q=modified-by-burp
- POST /login

The POST request included username and password form fields.

The password was redacted in the evidence file.

## Request modification test

I modified the search request from:

GET /search?q=test HTTP/1.1

to:

GET /search?q=modified-by-burp HTTP/1.1

The server still returned an error because the Python static server does not implement the /search route.

The important lesson was that the request could be changed before reaching the server.

## What I learned about HTTP through Burp

Burp showed that browser requests are structured text messages.

I could see the request line, Host header, User-Agent header, Accept header, query parameters, and form fields.

This made it easier to understand how browsers communicate with servers.

## Security relevance

Burp is important in web security because it lets analysts inspect and modify HTTP traffic.

Many web vulnerabilities depend on how a server handles client-controlled input.

Query parameters, form fields, cookies, headers, and methods can all affect server behavior.

## Mistakes / difficulties

The main difficulty was setting the browser proxy correctly.

Another challenge was remembering that the Python static server does not actually implement /search or /login routes.

This means modified requests can still return 404 or 501, even though Burp successfully changed the request.
