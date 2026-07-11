# XSS Security Review

## Executive summary

This review evaluates a deliberately vulnerable local web application that demonstrates reflected, stored, and DOM-based cross-site scripting. Vulnerable and safer implementations are shown side by side so that the complete data flow can be traced from source to storage and sink. Testing confirmed that untrusted input is interpreted as HTML when it reaches an unsafe rendering location and remains inert when it is handled with context-appropriate output encoding or a safer DOM API. The application is intentionally insecure and suitable only for local training. The principal finding is that XSS is caused by unsafe handling at the sink, not simply by special characters in user input.

## Scope

Testing was restricted to `127.0.0.1:8005` and `localhost:8005`. No external systems, public websites, third-party services, or other hosts were tested. The application used Python's standard-library HTTP server and stored comments only in memory. The reviewed routes were `/`, `/reflected-vuln`, `/reflected-safe`, `/comments`, `/dom`, and an unknown route used to verify the 404 response.

The local payloads were `<b>test-marker</b>` for automated response checks and `<img src=x onerror=alert(1)>` for browser-only DOM verification. The second payload was used only in the local browser because JavaScript execution cannot be validated by a command-line HTTP client.

## Testing methodology

The assessment combined source review, automated regression testing, direct HTTP requests, browser observation, and Burp Repeater comparisons. Source review identified where user-controlled data entered the application, whether it was stored, and which rendering operation consumed it. Automated tests used Python standard-library modules to verify status codes, redirect behavior, vulnerable rendering, escaped rendering, DOM sink presence, and 404 handling.

`curl` preserved complete local HTTP responses for reflected and stored cases. Burp Repeater compared vulnerable and safe requests while changing only the route. Browser testing was required for the DOM case because the browser must parse HTML, construct the DOM, load the invalid image, and execute the event handler before the vulnerable behavior becomes observable.

## Reflected XSS finding

The `/reflected-vuln` route reads the `q` query parameter and inserts it directly into an HTML paragraph. The source is the query-string value. There is no storage stage. The sink is the server-generated HTML response body. Because the value is concatenated into an HTML text context without encoding, the browser interprets markup rather than displaying it as text.

The marker `<b>test-marker</b>` appeared as a real bold element in the vulnerable response. The `/reflected-safe` route applies `html.escape()` before inserting the same value. The safe response contained `&lt;b&gt;test-marker&lt;/b&gt;`, so the browser displayed the original characters instead of constructing an element.

The appropriate fix for this context is HTML text encoding through a maintained template engine with automatic escaping or an equivalent context-aware encoder. A generic input filter would be weaker because it could miss alternate encodings or fail when the output context changes.

## Stored XSS finding

The `/comments` POST handler accepts the `comment` form field and stores it in an in-memory list. The source is POST form data. The storage component is the server-side comments list. The comments page then renders every stored value twice.

The vulnerable section inserts each stored comment directly inside an `<li>` element. The safe section applies `html.escape()` at render time. Testing confirmed that the raw marker became an HTML element in the vulnerable section and appeared as escaped text in the safe section. The 303 redirect after submission confirmed the expected POST/redirect/GET flow.

Stored XSS can have greater impact than a single reflected response because the payload may be rendered repeatedly to other users. The correct fix remains output handling at every sink. Encoding at render time is preferable to permanently transforming the stored value because another output context may require a different defense.

## DOM XSS finding

The `/dom` route returns JavaScript that reads the `name` parameter from `window.location.search` through `URLSearchParams`. The vulnerable branch assigns `"Hello " + name` to `innerHTML`. The safe branch assigns the same string to `textContent`.

The source is a browser-controlled URL value. There is no server-side storage. The vulnerable sink is `innerHTML`, which parses the string as markup. The local image payload created an image element and its invalid source triggered the `onerror` handler. The safe sink, `textContent`, created only a text node, so the payload was visible but not executed.

This demonstrates why the server response alone is insufficient for DOM XSS analysis. The vulnerable transformation occurs after the response reaches the browser. The preferred fix is `textContent` when the requirement is plain text. When HTML is genuinely required, the application should construct approved elements with safe DOM methods or use a maintained allow-list sanitizer.

## Source-to-sink analysis

The three findings share the same model: untrusted data enters through a source, may pass through storage or processing, and reaches a sink. Reflected XSS uses a query parameter and a server-rendered HTML sink. Stored XSS uses POST data, server-side storage, and a later HTML sink. DOM XSS uses a URL value and a browser-side DOM sink.

Validation at the source does not automatically make a dangerous sink safe. Validation can enforce business rules, but the final protection must match the parser that consumes the value.

## Context-aware output handling

HTML text, HTML attributes, JavaScript strings, CSS values, and URLs are different contexts. A value safely encoded for HTML text may still be unsafe inside JavaScript or an unquoted attribute. This lab uses an HTML text context, where HTML entity encoding is appropriate.

For DOM operations, `textContent` is safer for plain text because it does not invoke the HTML parser. `setAttribute()` is only conditionally safe because event-handler and URL attributes may still create dangerous behavior. URL values require scheme and destination validation. JavaScript execution sinks such as `eval()` should be removed rather than protected with filtering.

## Root causes

The primary root cause is treating untrusted strings as trusted markup. Direct string concatenation into an HTML response and assignment to `innerHTML` both allow the browser to interpret attacker-controlled syntax. A secondary cause is focusing on input characters rather than the destination context.

Storage does not create the vulnerability by itself. Storage increases persistence and potential impact, but execution occurs only when the stored value reaches an unsafe sink.

## Remediation

Server-rendered pages should use a secure template engine with automatic escaping enabled by default. Manual concatenation should be minimized. Existing direct output should be replaced with context-aware encoding.

Client-side code should use `textContent`, `createElement()`, and explicit property assignment for plain content. Dangerous APIs such as `innerHTML`, `outerHTML`, `document.write()`, `insertAdjacentHTML()`, and `eval()` should be removed unless a documented requirement exists. When limited user-authored HTML is necessary, the value should pass through a maintained sanitizer configured with a strict allow list.

Stored data should remain in its original form, while each output location applies the correct defense for its own context. Regression tests should cover safe rendering so future changes do not silently remove escaping.

## Defense in depth

Secure templating and context-aware encoding are primary controls for server-rendered output. Avoiding dangerous DOM sinks is the primary control for client-side rendering. Sanitization is appropriate only when the product intentionally supports HTML input.

A Content Security Policy can reduce exploitability by restricting scripts, event handlers, and external resources. However, CSP is not a substitute for correcting the sink and may be weakened by broad directives.

Cookies should use `HttpOnly` to reduce direct JavaScript access, `Secure` to restrict transport to HTTPS, and an appropriate `SameSite` policy to reduce cross-site request exposure. These flags protect session handling but do not prevent XSS from changing page content or sending authorized requests through the victim's browser. No defense-in-depth control replaces safe output handling.

## Detection and logging

The application should log route, timestamp, response status, and validation failures without recording passwords, session tokens, or sensitive payload values. Production monitoring could detect unusual volumes of markup-like input or unexpected Content Security Policy violation reports. These signals support investigation but are not prevention controls.

Security tests should run in continuous integration. Review should be triggered when known safe rendering tests fail or when new dangerous DOM APIs are introduced.

## Limitations

The application is intentionally small and does not include authentication, a database, multiple users, a production framework, HTTPS, or a real Content Security Policy. Comments disappear when the process restarts. The automated suite verifies response content and sink presence but does not execute JavaScript in a real browser, so browser behavior was documented manually.

The review covers only the specified local routes and payloads. It does not claim that every encoding context, browser variation, or framework behavior was tested.

## Conclusion

The capstone demonstrates reflected, stored, and DOM-based XSS through clear source-to-sink paths. The vulnerable versions interpret untrusted input as markup, while the safer versions apply HTML escaping or `textContent`. The main lesson is that XSS remediation must be applied at the sink and must match the exact output context. Validation, CSP, cookie flags, monitoring, and sanitization can strengthen the system, but they do not replace secure rendering.
