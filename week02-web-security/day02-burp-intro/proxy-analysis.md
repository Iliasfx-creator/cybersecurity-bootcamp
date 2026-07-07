# Proxy Analysis

## Captured GET request

### Request line

The captured request line was:

GET / HTTP/1.1

This means the browser requested the root path of the local web server.

### Host header

The Host header was:

Host: 127.0.0.1:8000

This tells the server which host and port the browser intended to reach.

### User-Agent header

The User-Agent header identified the browser making the request.

This header matters because servers can use it to change responses or log client information.

### Accept header

The Accept header told the server what content types the browser could handle.

For example, browsers often accept HTML, XML, images, and other web content.

### What Burp showed me

Burp showed the raw HTTP request before it reached the server.

This made the browser request visible as editable text.

## Captured search request

### Original request

The original search request was:

GET /search?q=test HTTP/1.1

This request included a query parameter named q with the value test.

### Query parameter observed

The query parameter was:

q=test

This showed that the search form placed user input into the URL.

### What happens if q changes?

If q changes, the request sent to the server changes.

In this lab, changing q did not make the route work because the Python static server does not implement /search.

However, in a real web application, changing parameters can affect search results, database queries, filtering, access control, or application behavior.

## Captured POST request

### Form fields observed

The POST request contained form fields:

- username
- password

The password value was redacted in evidence.

### Why sending passwords over HTTP is unsafe

HTTP is not encrypted.

If a password is sent over plain HTTP on a real network, someone who can observe the traffic may be able to read it.

This is why login forms should use HTTPS.

In this lab, the traffic stayed local, but the security lesson still applies.

## Modified request

### What I changed

I changed the search request from:

GET /search?q=test HTTP/1.1

to:

GET /search?q=modified-by-burp HTTP/1.1

### Did the server response change?

The server still returned an error because the Python static server does not have a /search backend route.

The important result was not a successful search response.

The important result was that Burp allowed me to modify the request before it reached the server.

### Why request modification matters in web security

Request modification matters because web applications trust and process client-supplied input.

A tester can modify parameters, paths, headers, cookies, and form fields to check how the server responds.

This is useful for finding input validation issues, authorization problems, insecure assumptions, and unexpected behavior.

## What I learned

I learned that browser requests are plain HTTP messages that can be intercepted and inspected.

I also learned that form data and query parameters can be changed before reaching the server.

Burp makes the request/response process visible, which is important for understanding web security.
