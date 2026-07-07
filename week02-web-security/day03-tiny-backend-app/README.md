# Day 3 — Tiny Backend App

## Goal

The goal of this lab was to build a tiny backend web application and observe real GET and POST handling.

In previous labs, the Python static server returned 404 for /search and 501 for POST /login because it had no backend logic.

In this lab, the server implemented routes for /, /search, and /login.

## Tools used

- Python
- BaseHTTPRequestHandler
- curl
- Burp Suite
- browser
- bash

## Backend routes

The backend implemented these routes:

- GET /
- GET /search?q=value
- POST /login

The root route returned an HTML page with a search form and a login form.

The search route read a query parameter.

The login route read POST form data and returned success or failure.

## GET request handling

The /search route used the q query parameter from the URL.

When q was test, the response displayed test.

When q was hello, the response displayed hello.

This showed that the backend was reading client input and using it in the response.

## POST request handling

The /login route read username and password from the POST request body.

A valid login returned 200 OK and Login successful.

An invalid login returned 401 Unauthorized and Login failed.

The password was redacted in committed evidence.

## Burp observations

Burp showed the raw HTTP requests sent by the browser.

I captured GET /, GET /search?q=test, a modified search request, and POST /login requests.

I modified the search parameter from q=test to q=modified-by-burp.

The server processed the modified value, which showed that client-controlled input can affect backend behavior.

## Security relevance

Web security depends on how the backend reads, validates, transforms, and returns user input.

The search route used html.escape to reduce XSS risk by encoding special HTML characters before placing user input in the response.

The login route showed basic authentication logic, but it is not production-ready.

Hardcoded credentials, plain HTTP, and missing session management would all need to be fixed before production.

## Mistakes / difficulties

The main difficulty was understanding the difference between a static server and a backend server.

A static server only serves files.

A backend server can define routes and make decisions based on request paths, query parameters, and form data.

Another difficulty was keeping password values redacted in evidence while still proving that valid and invalid login behavior worked.
