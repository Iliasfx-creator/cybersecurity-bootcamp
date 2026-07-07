# Day 1 — HTTP and Web Basics

## Goal

The goal of this lab was to understand basic HTTP request and response behavior using a local website and a local Python HTTP server.

I created a simple HTML page, served it locally, tested it with curl, observed browser DevTools, compared HTTP methods, reviewed server logs, and wrote a small HTTP probing script.

## Lab setup

The lab used a local static website served from:

simple-site/index.html

The server was started with:

python3 -m http.server 8000

The local target was:

http://127.0.0.1:8000

This kept the lab safe and local.

## Tools used

- HTML
- Python http.server
- curl
- Browser DevTools
- bash
- nano

## Local web server

The Python HTTP server listened on port 8000 and served files from the simple-site directory.

When the browser or curl requested the root path /, the server returned index.html.

When the client requested /search?q=test, the server returned 404 because this was a static file server and there was no backend route for /search.

## HTTP requests observed

I observed HEAD and GET requests with curl.

A HEAD request returned response headers without the page body.

A GET request returned the full HTML page.

The browser also sent automatic requests and headers that were not manually typed by the user.

## HTTP methods tested

I tested GET, HEAD, POST, and OPTIONS.

GET returned the local HTML page.

HEAD returned headers for the page.

POST returned 501 because the simple Python static server did not support POST for this resource.

OPTIONS also returned 501 because the server did not support that method in this context.

## Browser DevTools observations

In DevTools, I observed the request URL, method, status code, remote address, request headers, and response headers.

The browser automatically sent headers such as Host, User-Agent, Accept, Accept-Language, Accept-Encoding, and Connection.

This showed that a browser request contains more metadata than just the URL.

## Server logs

The server logs showed incoming requests from 127.0.0.1.

The logs included the HTTP method, requested path, protocol version, and status code.

The logs showed successful requests, missing paths, and unsupported methods.

## Security relevance

Web security starts with understanding what the client sends and what the server returns.

Methods, paths, query parameters, headers, status codes, and logs are all security-relevant.

Attackers often inspect server behavior by changing paths, methods, headers, and parameters.

Defenders use logs and normal request patterns to detect suspicious activity.

## Mistakes / difficulties

The main difficulty was keeping the local server running while collecting curl evidence.

Another issue was understanding why /search?q=test returned 404 even though the HTML form existed.

The explanation is that the form can generate the request, but the static Python server does not implement a /search backend route.
