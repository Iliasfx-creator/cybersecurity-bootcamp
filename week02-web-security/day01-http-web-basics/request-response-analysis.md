# Request / Response Analysis

## Local page request

### Request URL

The browser requested:

http://127.0.0.1:8000/

### Request method

The request method was GET.

GET asks the server to return a resource.

### Status code

The expected status code for the local index page was 200 OK.

This means the server found the requested page and returned it successfully.

### Remote address

The remote address was:

127.0.0.1:8000

This means the browser connected to a local web server running on my own machine.

### Important request headers

The browser automatically sent request headers.

Important examples include:

- Host
- User-Agent
- Accept
- Accept-Language
- Accept-Encoding
- Connection

These headers tell the server what host is being requested, what client is making the request, and what types of content the browser can accept.

### Important response headers

The Python HTTP server returned response headers.

Important examples include:

- Server
- Date
- Content-type
- Content-Length
- Last-Modified

These headers describe the server response and the returned file.

## What the browser sends automatically

The browser sends more information than a simple user might expect.

It automatically sends headers such as User-Agent, Accept, language preferences, encoding support, and connection behavior.

This matters because HTTP requests contain metadata even when the user only types a URL.

## What the server returns

The server returns a status code, response headers, and usually a response body.

For the index page, the body was the HTML file.

For missing paths such as /search?q=test, the server may return a 404 error because the simple static server does not implement that route.

## Why this matters in web security

Web security starts by understanding exactly what the client sends and what the server returns.

Headers, methods, status codes, paths, and query parameters can all affect security.

Attackers often look for unusual behavior in routes, methods, headers, parameters, and error responses.

Defenders need to understand normal request and response behavior so they can recognize suspicious activity.

## Server logs

### What appeared in the server logs?

The Python HTTP server logged incoming requests from 127.0.0.1.

The logs showed the requested path, HTTP method, HTTP version, status code, and timestamp.

### Which requests returned 200?

Requests for the root page, such as GET /, returned 200 OK.

HEAD / may also return 200 because the resource exists and the server can return headers for it.

### Which requests returned 404 or 501?

The /search?q=test request may return 404 because the static server does not have a /search route.

POST and OPTIONS may return 501 if the Python HTTP server does not support those methods in this context.

### Why logs matter in web security

Logs matter because they show what clients requested and how the server responded.

In web security, logs can help detect scanning, brute force attempts, broken links, suspicious parameters, unusual methods, and repeated errors.

Server logs are often one of the first places analysts check during investigation.
