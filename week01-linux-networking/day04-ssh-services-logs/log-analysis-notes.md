# Log Analysis Notes

## What authentication logs are

Authentication logs record login-related and privilege-related events on a system.

They can include successful logins, failed logins, sudo usage, SSH authentication attempts, session openings, and session closings.

## What kind of events can appear there

Authentication logs may show events such as:

- successful user login
- failed password attempts
- sudo command usage
- SSH login attempts
- user sessions opening or closing
- authentication errors
- permission-related messages

## What failed login attempts might look like

Failed login attempts often include words like:

- Failed password
- authentication failure
- invalid user
- failed login
- denied

For SSH specifically, failed login logs may show the username attempted, the source IP address, and the authentication method that failed.

## Why logs matter in incident response

Logs matter because they help reconstruct what happened on a system.

During incident response, logs can help answer questions such as:

- who tried to log in
- when the attempt happened
- whether authentication succeeded or failed
- whether sudo was used
- whether there were repeated failed attempts
- whether activity looks normal or suspicious

Without logs, an analyst has much less evidence.

## What I observed in my system

I checked authentication logs using /var/log/auth.log and journalctl.

In my sample, /var/log/auth.log existed and contained authentication-related events.

I observed sudo activity, including commands being run as root. This matters because sudo logs can show when a user performed privileged actions.

I also observed session open and session close events. These show when user or root sessions started and ended.

I observed CRON session entries. These show scheduled system activity.

In the journalctl output, I observed system service messages and WSL-related service warnings.

I did not observe clear SSH failed login attempts in this sample.

I should not invent failed logins if they are not present in the evidence. The correct conclusion is based only on what the logs actually show.
