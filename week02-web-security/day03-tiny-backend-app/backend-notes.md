# Backend Notes

## What a backend is

A backend is the server-side part of a web application.

It receives requests, reads input, applies logic, and returns responses.

Unlike a static file server, a backend can decide what to do based on paths, parameters, form data, authentication state, or other application logic.

## Difference between static server and backend server

A static server mainly serves files.

If the file or path does not exist, it usually returns 404.

A backend server can define routes such as /search or /login and handle them with code.

In the previous labs, /search returned 404 and POST /login returned 501 because the Python static server did not implement those actions.

In this lab, the backend implemented /search and /login directly.

## What routing means

Routing means matching a request path to server-side logic.

For example:

- GET / returns the main page
- GET /search reads the query parameter
- POST /login reads form data and checks credentials

Routing is important because different paths can trigger different backend behavior.

## What query parameters are

Query parameters are values placed in the URL after a question mark.

Example:

/search?q=test

In this example, q is the parameter name and test is the value.

The backend can read q and use it to build a response.

## What form data is

Form data is data submitted from an HTML form.

For POST requests, form data is usually sent in the request body.

In this lab, the login form sent username and password fields to /login.

## What status codes appeared

The backend returned:

- 200 OK for the main page
- 200 OK for search requests
- 200 OK for valid login
- 401 Unauthorized for invalid login
- 404 Not Found for unknown paths

## Why backend behavior matters in web security

Web security depends on how the backend handles input.

The backend decides whether to trust, reject, transform, encode, or store user-controlled data.

If backend logic is weak, attackers may be able to abuse parameters, form fields, authentication checks, or output rendering.
