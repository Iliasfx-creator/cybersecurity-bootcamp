# OWASP Juice Shop — XSS Notes

## Status

Not completed.

I joined the room, launched the authorized lab environment, and logged into OWASP Juice Shop.

I have not yet completed and verified the XSS-specific task.

## XSS type observed

No room-specific XSS type has been confirmed yet.

I will classify the finding only after tracing the actual input from its entry point to the final sink.

## Entry point

No XSS entry point has been recorded yet.

The login form was accessed during environment setup, but it is not being documented as an XSS finding.

## Source

No room-specific XSS source has been confirmed yet.

## Sink

No room-specific XSS sink has been confirmed yet.

## Tool workflow

- Joined the OWASP Juice Shop TryHackMe room.
- Started the authorized AttackBox and target machine.
- Opened the Juice Shop application.
- Logged into the application.
- Opened Burp Suite.
- Identified that browser traffic was not initially passing through the Burp proxy.
- Reviewed the difference between the AttackBox, target machine, browser, and Burp proxy.
- Did not record credentials, cookies, tokens, flags, or challenge answers.

## What matched my capstone

The current setup reinforced the importance of confirming that testing tools are connected to the correct target and traffic path.

A source-to-sink comparison will be added only after completing the XSS-specific task.

## What differed from my local app

Juice Shop is a larger application with authentication, application state, framework behavior, and more complex client-side code.

My local capstone has deliberately simple routes where the source and sink are visible directly in the code.

## Remediation

No room-specific remediation is claimed before the exact source, sink, and output context have been confirmed.

In general, remediation must be selected according to the final rendering context rather than through a generic input filter.

## Mistakes

I initially assumed that keeping Burp open was sufficient for interception.

The browser must be configured to send its traffic through the Burp proxy, or the Burp-provided browser must be used.

I also need to avoid documenting a vulnerability type before verifying the complete data flow.

## No flags or answers

I did not publish flags or challenge answers.
