# Burp Suite Notes

## What Burp Suite is

Burp Suite is a web security testing tool.

It is commonly used to inspect, intercept, modify, and replay HTTP requests and responses.

In this lab, I used Burp only against my own local test site.

## What a proxy is

A proxy sits between the browser and the web server.

Instead of the browser sending the request directly to the server, the browser sends the request to the proxy first.

Then the proxy forwards the request to the server.

The response can also pass back through the proxy.

In simple terms:

Browser -> Burp Proxy -> Web Server

## What interception means

Interception means Burp can pause a request before it reaches the server.

While the request is paused, I can inspect it and modify it.

After that, I can forward it to the server.

This shows that HTTP requests are not magic. They are structured text messages that can be inspected and changed.

## Why Burp is useful in web security

Burp is useful because it makes HTTP traffic visible.

It helps analysts understand:

- request methods
- paths
- query parameters
- headers
- cookies
- form data
- server responses
- status codes

This matters because many web vulnerabilities depend on how the server handles input from requests.

## Community vs Professional

Burp Suite Community is the free version.

It includes important manual testing tools such as Proxy, Repeater, and basic request inspection.

Burp Suite Professional includes more advanced features such as automated scanning and more powerful testing tools.

For this lab, Community is enough because the goal is manual request observation and safe local modification.

## Safety note

Burp can modify real HTTP requests.

Because of that, it must only be used on systems I own or systems where I have explicit permission to test.

For this lab, Burp is only used against my local Python HTTP server on 127.0.0.1:8000.
