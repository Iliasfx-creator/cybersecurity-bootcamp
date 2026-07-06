# Nmap Notes

## What Nmap does

Nmap is a network discovery and security auditing tool.

It can be used to identify hosts, open ports, running services, service versions, and possible firewall behavior.

Nmap is useful for administrators and security analysts because it helps map what is reachable on a network.

## What a port scan is

A port scan checks whether specific ports on a target are open, closed, or filtered.

In simple terms, a port scan asks:

"Is anything listening on this port?"

This is reconnaissance. It maps exposure. It is not the same as exploiting a vulnerability.

## TCP connect scan

A TCP connect scan attempts to complete a normal TCP connection to a target port.

If the connection succeeds, the port is considered open.

If the target refuses the connection, the port is usually closed.

If there is no clear response or a firewall interferes, the port may appear filtered.

## Version detection

Version detection tries to identify what service is running on an open port.

For example, if port 22 is open, version detection may try to identify the SSH service and version.

This is useful for administrators because it helps inventory systems.

It is also useful for attackers, so it must be used only with permission.

## Common port states

### open

An open port means a service is listening and accepting connections on that port.

This is security-relevant because an open service can be interacted with.

### closed

A closed port means the target responded, but no service is listening on that port.

The host is reachable, but that specific port is not open.

### filtered

A filtered port means Nmap cannot clearly determine whether the port is open or closed.

This often happens because a firewall or packet filter is blocking or dropping traffic.

## Why filtered ports matter

Filtered ports matter because they can show firewall behavior.

A filtered result may mean the target is protected by rules that block scanning traffic or hide service status.

For defenders, filtered ports can be a sign that network controls are working.

For analysts, filtered results require careful interpretation because filtered does not always mean open or closed.

## Why service version detection matters

Service version detection matters because the security risk of an open port depends partly on what service is running and which version it is.

An open port alone says something is listening.

A version scan can provide more context, such as whether the service may be outdated or misconfigured.

## Difference between scanning and exploiting

Scanning means identifying hosts, ports, services, and metadata.

Exploitation means trying to use a vulnerability to gain unauthorized access, execute code, bypass controls, or change the target system.

This lab only uses scanning.

I am not exploiting anything, not brute forcing anything, and not scanning unauthorized targets.
