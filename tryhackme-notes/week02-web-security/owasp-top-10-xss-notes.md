# TryHackMe XSS Notes

## Rooms / sections worked on

- Intro to Cross-site Scripting
- XSS
- OWASP Top 10 XSS section, if available

## Concepts learned

## Reflected XSS

## Stored XSS

## DOM-based XSS

## What connected with my local labs

## What was different from my local labs

## Mistakes / unclear points

## No flags / no answers note

I did not publish flags or challenge answers.

## DOM XSS connection to my local lab

### What TryHackMe showed

TryHackMe showed that XSS can happen in different forms, including reflected, stored, and DOM-based XSS.

DOM XSS focuses on browser-side JavaScript and DOM manipulation.

### What matched my local DOM lab

My local DOM lab showed a URL parameter being read by JavaScript and written into the page.

The vulnerable sink used innerHTML.

The safer sink used textContent.

This matched the idea that DOM XSS depends on sources and sinks in client-side code.

### What was different

The local lab was intentionally simple and used one static HTML file.

Real applications may have larger JavaScript codebases, frameworks, routing, templates, and many more sources and sinks.

### What I still find confusing

I still need more practice identifying dangerous DOM sinks in larger JavaScript code.

I also need more practice with context-aware encoding for HTML attributes, JavaScript strings, URLs, and CSS.

### No flags / no answers note

I did not publish flags or challenge answers.
