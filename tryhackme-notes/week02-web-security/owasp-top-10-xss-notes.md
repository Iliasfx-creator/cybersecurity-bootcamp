# OWASP Top 10 — XSS-related Notes

## Date

2026-07-08

## Status

Not started

## Concepts learned

## Commands/tools used

## Mistakes

## What connected with my GitHub labs

## What I still do not fully understand

## No flags / no answers note

I did not publish flags or challenge answers.

## Stored XSS connection to my local lab

### What TryHackMe showed

TryHackMe showed that XSS is about unsafe handling of user-controlled input in web applications.

It helped connect XSS to real application behavior instead of treating it as just a payload.

### What matched my local lab

My local lab showed the same core issue: user input entered the application, was processed by the server, and was later rendered in a browser response.

The stored XSS lab made the source, storage, and sink easier to see.

### What was different

The local lab was intentionally simple and stored comments only in server memory.

A real application might store user input in a database and show it to many different users.

Real applications also have more complex contexts, templates, sessions, cookies, and defenses.

### Mistakes / unclear points

I still need more practice identifying all sinks where stored input can appear.

I also need more practice understanding context-aware encoding for HTML body, HTML attributes, JavaScript, URLs, and CSS.

### No flags / no answers note

I did not publish flags or challenge answers.
