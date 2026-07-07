# HTTP Notes

## What HTTP is

HTTP stands for HyperText Transfer Protocol. It is the protocol used by browsers and web servers to exchange requests and responses.

In web security, HTTP is important because most web attacks happen by manipulating requests, parameters, headers, methods, cookies, or paths.

## Request

An HTTP request is sent by a client, such as a browser or curl, to ask a server for something.

A request usually includes:

- method
- path
- headers
- optional body

Example:

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: curl
Response

An HTTP response is sent by the server back to the client.

A response usually includes:

status code
response headers
optional body

Example:

HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.14.4
Content-type: text/html
GET

GET requests a resource from the server.

In this lab, GET / returned the local HTML page with status 200 OK.

GET is important in web security because query parameters can expose input handling issues, such as injection, reflected XSS, or information disclosure.

HEAD

HEAD requests only the response headers, without the body.

In this lab, HEAD / returned 200 OK with headers such as Server, Date, Content-type, Content-Length, and Last-Modified.

HEAD is useful for quickly checking server behavior without downloading the full response body.

POST

POST usually sends data to the server.

In this lab, POST / returned 501 Unsupported method because Python's simple static HTTP server did not support POST for this resource.

POST is important in web security because login forms, uploads, API requests, and state-changing actions often use POST.

OPTIONS

OPTIONS asks the server which HTTP methods are supported.

In this lab, OPTIONS returned 501 Unsupported method.

OPTIONS matters because exposed or misconfigured methods can reveal server behavior or allow risky actions if improperly enabled.

Status codes observed

I observed:

200 OK: the request succeeded
404 File not found: the requested path did not exist
501 Unsupported method: the server did not support the requested method
Headers observed

I observed headers such as:

Server
Date
Content-type
Content-Length
Last-Modified
Connection

These headers describe how the server responded and what kind of content was returned.

Why HTTP methods matter in cybersecurity

HTTP methods matter because they define what action the client is asking the server to perform.

Attackers may test different methods to find unexpected behavior. Defenders need to understand normal method usage so they can detect suspicious requests, unsupported methods, scanning, and abuse attempts.
