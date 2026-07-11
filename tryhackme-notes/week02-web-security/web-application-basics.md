# Web Application Basics

## Date

2026-07-08

## Status

Completed — 100%.

## Concepts learned

- A web application has client-side and server-side components.
- HTTP requests contain a method, path, headers, and sometimes a body.
- HTTP responses contain a status code, headers, and a body.
- Query parameters and form fields are controlled by the client.
- Front-end validation does not replace server-side validation.
- Cookies and session identifiers must be treated as sensitive values.
- The browser renders the response, while the server decides how requests are processed.

## Commands/tools used

- Browser
- AttackBox
- Burp HTTP history
- Burp Repeater
- `curl` in the related local HTTP labs

## Mistakes

I initially treated the browser page as the complete application behavior.

Inspecting the HTTP request and response separately made the client/server boundary clearer.

## What connected with my GitHub labs

The room connected directly with my local routes, query parameters, POST form handling, redirects, status codes, and response headers.

It also helped explain why the same input can be processed differently by different routes.

## What I still need to practise

I need more practice tracing cookies and session state across multiple requests without recording sensitive values.

I also need more practice distinguishing client-side behavior from server-side behavior in larger applications.

## No flags / no answers note

I did not publish flags or challenge answers.
