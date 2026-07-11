## XSS type observed

The completed task demonstrated [reflected / stored / DOM-based] XSS.

## Entry point

The input entered through [search field / form / URL parameter / other observed entry point].

## Source

The source was the user-controlled value submitted through the application.

## Sink

The value reached a browser-rendered HTML or DOM sink without the correct protection.

## Tool workflow

- Used the browser inside the authorized TryHackMe environment.
- Used Burp Proxy to inspect the request.
- Used Burp Repeater to compare controlled request changes where necessary.
- Observed how the application processed and rendered the input.
- Did not record flags, cookies, challenge answers, or private values.

## What matched my capstone

The task matched my source-to-sink analysis.

The input entered through a client-controlled source and reached an unsafe sink.

This connected with my reflected, stored, or DOM XSS local routes depending on the observed task.

## What differed from my local app

Juice Shop was a larger application with framework code, more routes, application state, and more complex client/server behavior.

My local application was deliberately small so the source, storage, sink, and context were easier to identify.

## Remediation

The vulnerable sink should be fixed with context-aware output handling.

For plain DOM text, textContent is safer than innerHTML.

For server-rendered HTML text, context-appropriate encoding or secure templates with automatic escaping should be used.

Sanitization is needed only when controlled HTML must be supported.

## Mistakes

I initially focused on the payload rather than tracing the source and sink.

I also needed to verify that Burp was correctly configured as the browser proxy.

## No flags or answers

I did not publish flags or challenge answers.
