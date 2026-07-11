# Burp Suite: The Basics

## Date

2026-07-08

## Status

Completed — 100%.

## Concepts learned

- Burp Proxy operates between the browser and the target application.
- Intercept pauses requests before they reach the server.
- HTTP history records requests even when interception is disabled.
- Repeater allows one request to be modified and sent repeatedly.
- Request method, path, headers, parameters, and body must be examined separately.
- Burp being open does not automatically mean that browser traffic is using its proxy.

## Commands/tools used

- Burp browser
- Proxy
- Intercept
- HTTP history
- Repeater
- Forward
- AttackBox browser

## Mistakes

I initially expected Burp to intercept traffic simply because the application was open.

The browser must use the Burp proxy, or the Burp-provided browser must be used.

## What connected with my GitHub labs

I used the same workflow in my local XSS capstone to compare vulnerable and safe reflected responses and to document the stored POST/redirect/GET flow.

## What I still need to practise

I need more practice identifying which request is responsible for a specific application action when many requests appear in HTTP history.

I also need more practice using scope and filtering to reduce unrelated traffic.

## No flags / no answers note

I did not publish flags or challenge answers.
