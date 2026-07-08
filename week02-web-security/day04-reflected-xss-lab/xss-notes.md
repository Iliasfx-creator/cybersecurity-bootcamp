# XSS Notes

## What XSS is

XSS stands for Cross-Site Scripting.

XSS happens when a web application allows user-controlled input to be interpreted by the browser as code.

The main issue is not the payload itself. The main issue is unsafe handling of input and output.

## Reflected XSS

Reflected XSS happens when input from the current HTTP request is immediately included in the HTTP response in an unsafe way.

The input is reflected back by the server.

In this lab, the q parameter was reflected into the HTML response.

## Source and sink

A source is where user-controlled input enters the application.

In this lab, the source was the q parameter in the URL query string.

A sink is where that input ends up.

In this lab, the sink was the HTML response body inside the paragraph that displayed the search term.

## Why reflected input can be dangerous

Reflected input can be dangerous when the server places it into HTML without encoding.

If the input contains HTML or JavaScript and the server returns it raw, the browser may interpret it as markup or script.

That can allow JavaScript execution in the user's browser.

## Why output encoding matters

Output encoding changes special characters into safe text representations.

For example:

- < becomes &lt;
- > becomes &gt;

This makes the browser display the input as text instead of interpreting it as HTML or JavaScript.

## Why input filtering alone is not enough

Input filtering tries to block specific characters, words, or patterns.

Filtering alone is fragile because attackers may find alternate encodings, different contexts, or bypasses.

Output encoding is stronger because it protects the point where data is placed into the response.

The correct encoding depends on the output context, such as HTML body, HTML attribute, JavaScript, URL, or CSS.

## Difference between vulnerable route and safe route

The vulnerable route inserted q directly into the HTML response.

The safe route used html.escape(q) before inserting q into the HTML response.

The vulnerable route returned script characters raw.

The safe route encoded the characters so the browser displayed them as text.

## What I should never do outside a lab

I should never test XSS payloads on public websites, university systems, company systems, accounts, or third-party applications without permission.

Even simple payloads can trigger security alerts or create legal and ethical problems.

XSS testing belongs only in authorized labs, owned systems, or approved security assessments.
