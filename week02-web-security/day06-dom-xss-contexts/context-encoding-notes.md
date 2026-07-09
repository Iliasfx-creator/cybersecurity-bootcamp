# Context-Aware Encoding Notes

## HTML body context

HTML body context means data is placed between HTML tags.

Example:

<p>USER_INPUT</p>

For this context, characters like <, >, &, and quotes should be encoded so the browser treats them as text.

## HTML attribute context

HTML attribute context means data is placed inside an attribute.

Example:

<input value="USER_INPUT">

This context needs attribute-safe encoding because quotes or special characters can break out of the attribute.

## JavaScript string context

JavaScript string context means data is placed inside JavaScript code.

Example:

const name = "USER_INPUT";

This needs JavaScript string escaping, not just HTML escaping.

## URL context

URL context means data is placed inside a URL.

Example:

<a href="/search?q=USER_INPUT">

This needs URL encoding and careful validation.

## CSS context

CSS context means data is placed inside style rules.

Example:

style="color: USER_INPUT"

CSS has its own parsing rules, so unsafe input here can create different risks.

## Why one encoding method is not enough

Different contexts have different parsing rules.

HTML, attributes, JavaScript, URLs, CSS, and DOM APIs do not interpret characters the same way.

One escaping method cannot automatically protect every context.

## What html.escape protects

html.escape helps when placing text into a basic HTML body context.

It converts characters like < and > into safe entities.

This prevents basic HTML/script tags from being interpreted as markup.

## What html.escape does not automatically solve

html.escape does not automatically make data safe for every context.

It is not enough by itself for JavaScript strings, URLs, CSS, or all HTML attribute situations.

Developers must choose defenses based on where the data is placed.
