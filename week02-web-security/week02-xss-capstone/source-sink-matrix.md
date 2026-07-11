# Source-to-Sink Matrix

## XSS data flows

| Type | Source | Storage | Sink | Context | Vulnerable behavior | Correct fix |
|---|---|---|---|---|---|---|
| Reflected | `q` URL query parameter | None | Server-generated HTML response | HTML text inside a paragraph | Raw markup is interpreted by the browser | Apply context-aware HTML encoding or use an auto-escaping template engine |
| Stored | `comment` POST form field | In-memory Python comments list | Server-generated `<li>` content | HTML text rendered during a later GET | Stored markup is repeatedly interpreted as HTML | Preserve original data and encode correctly at every output sink |
| DOM | `name` from `window.location.search` | None | `innerHTML` | Browser-side HTML parsing | The browser creates elements and may execute event handlers | Use `textContent` for plain text or sanitize strictly when HTML is required |

## DOM and JavaScript API review

| API | Classification | Reason | Recommended alternative or validation |
|---|---|---|---|
| `innerHTML` | Potentially dangerous | Parses a string as HTML and may create executable elements or event handlers | Use `textContent`, `createElement()`, or a maintained allow-list sanitizer |
| `outerHTML` | Potentially dangerous | Replaces an element and parses the assigned string as HTML | Update safe properties or build approved DOM nodes explicitly |
| `document.write()` | Potentially dangerous | Writes attacker-controlled strings directly into the document parser | Remove it and use safe DOM construction methods |
| `insertAdjacentHTML()` | Potentially dangerous | Parses the supplied value as HTML at a selected DOM position | Use `insertAdjacentText()` or append explicitly created nodes |
| `eval()` | Potentially dangerous | Interprets a string as JavaScript code | Remove it and use normal functions, structured data, or explicit logic |
| `textContent` | Safer for text | Creates text rather than invoking the HTML parser | Preferred for displaying untrusted plain-text values |
| `setAttribute()` | Conditionally safe | Safety depends on the attribute; event handlers and dangerous URL schemes remain risky | Allow only expected attribute names and validate URL schemes and destinations |
| `location.href` | Conditionally safe | Navigation to attacker-controlled URLs may enable unsafe schemes or open redirects | Allow approved schemes and destinations; use URL parsing and allow lists |

## Key conclusion

A source is not automatically vulnerable.

The vulnerability appears when untrusted data reaches a sink that interprets it in a dangerous context.

The final defense must match the exact output context.
