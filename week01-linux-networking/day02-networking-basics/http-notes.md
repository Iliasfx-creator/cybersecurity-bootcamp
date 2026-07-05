# HTTP Notes

## What HTTP headers are

HTTP headers are metadata sent with HTTP requests and responses.

In this lab I used curl with the -I option to request only the response headers from three HTTPS websites:

- https://example.com
- https://github.com
- https://overthewire.org

The -I option means headers only. It does not download the full page body.

Headers help describe the response, the content type, caching behavior, server information, cookies, and security controls.

## Status codes observed

All three tested sites returned HTTP/2 200.

HTTP/2 is the HTTP protocol version used in the response.

200 means OK. The request succeeded and the server returned a successful response.

## Server header

The server header can reveal information about the platform or infrastructure that answered the request.

Observed examples:

- example.com returned server: cloudflare
- github.com returned server: github.com
- overthewire.org returned server: cloudflare

This matters in cybersecurity because server headers can help with fingerprinting.

Fingerprinting means identifying technologies, platforms, or infrastructure based on observable behavior or metadata.

## Content-Type header

The content-type header tells the client what kind of content was returned.

Observed examples:

- content-type: text/html
- content-type: text/html; charset=utf-8

This means the responses were HTML pages.

This matters because security analysts often need to know whether a server is returning HTML, JSON, JavaScript, plain text, images, or another content type.

## Security headers I observed

### Strict-Transport-Security

GitHub returned Strict-Transport-Security with a long max-age value, includeSubdomains, and preload.

This header is also called HSTS.

HSTS tells browsers to use HTTPS for the site for a defined period of time. This helps protect against downgrade attacks and accidental HTTP access.

OverTheWire returned Strict-Transport-Security with max-age=0.

That means long-term HSTS enforcement is not being enabled by that header.

### X-Frame-Options

GitHub returned x-frame-options: deny.

This prevents the site from being loaded inside a frame or iframe.

This helps protect against clickjacking.

Clickjacking is an attack where a user is tricked into clicking something hidden or misleading inside a framed page.

### X-Content-Type-Options

GitHub returned x-content-type-options: nosniff.

This tells browsers not to guess a different content type from the one declared by the server.

This helps reduce some content-sniffing risks.

### Content-Security-Policy

GitHub returned a long Content-Security-Policy header.

Content-Security-Policy is also called CSP.

CSP controls where scripts, images, frames, styles, and other resources are allowed to load from.

CSP is important because it can reduce the impact of cross-site scripting and unwanted resource loading.

The full CSP was redacted in the public evidence file for readability.

### Referrer-Policy

GitHub returned a referrer-policy header.

This controls how much referrer information the browser sends when navigating from one site to another.

This matters because referrer data can sometimes leak URLs, paths, or sensitive context.

### Set-Cookie

GitHub returned several set-cookie headers.

The cookie names and values were redacted because cookies and session values should not be committed to a public repository.

Security-relevant cookie flags observed:

- HttpOnly
- secure
- SameSite=Lax

HttpOnly reduces access to cookies from JavaScript.

secure tells the browser to send the cookie only over HTTPS.

SameSite=Lax helps reduce some cross-site request risks.

## Other headers observed

### Cache headers

I observed cache-related headers such as cache-control, cf-cache-status, x-cache, age, and x-cache-hits.

These describe caching behavior.

Caching improves performance, but it can also matter in security when sensitive content is cached incorrectly.

### Access-Control-Allow-Origin

OverTheWire returned access-control-allow-origin: *.

This is a CORS-related header.

By itself, this is not automatically a vulnerability. It depends on what content is exposed and whether credentials are involved.

CORS controls which origins can read responses from a site in browser-based requests.

## Why HTTP headers matter in cybersecurity

HTTP headers matter because they reveal how a web server behaves and what security controls are present.

Security analysts inspect headers to understand:

- whether HTTPS is enforced
- whether clickjacking protections exist
- whether content sniffing protections exist
- whether CSP is configured
- how cookies are protected
- whether server or infrastructure details are exposed
- whether caching behavior could create risk

Headers do not prove that a site is secure or insecure by themselves, but they are an important first layer of web security analysis.
