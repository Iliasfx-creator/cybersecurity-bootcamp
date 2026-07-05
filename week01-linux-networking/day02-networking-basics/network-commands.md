# Network Commands

This document explains basic networking commands used during Day 2.

The goal is not only to run commands, but to understand what question each command answers during system inspection, troubleshooting, and security analysis.

---

## Command: ip a

### What it does

Shows network interfaces and their assigned IP addresses.

It can show loopback interfaces, Ethernet interfaces, IPv4 addresses, IPv6 addresses, MAC addresses, interface state, and subnet prefixes.

### Example

```bash
ip a
```

### Security relevance

This command helps identify the network identity of a system.

A security analyst can use it to answer:

- What IP address does this system have?
- Which interface is active?
- Is the system using IPv4, IPv6, or both?
- Is this a local, private, or public-facing address?

This matters because understanding the system's network position is the first step before investigating traffic, exposure, or connectivity problems.

---

## Command: ip route

### What it does

Shows the routing table of the system.

The routing table tells the system where to send network traffic.

The most important line for beginners is usually the default route.

### Example

```bash
ip route
```

### Security relevance

This command helps identify the default gateway and local subnet.

A security analyst can use it to understand:

- Where traffic goes when the destination is outside the local network
- Which gateway is used to reach other networks
- Which subnet is directly connected

This matters during troubleshooting, network mapping, and incident response because wrong routes can break connectivity or send traffic through unexpected paths.

---

## Command: hostname -I

### What it does

Prints the IP addresses assigned to the host.

It is a quick way to see the system's local IP address without the full detail shown by `ip a`.

### Example

```bash
hostname -I
```

### Security relevance

This command is useful when quickly identifying the IP address of the current machine.

In a lab or investigation, it helps confirm which host is being inspected.

It is less detailed than `ip a`, but faster for a quick check.

---

## Command: cat /etc/resolv.conf

### What it does

Prints the DNS resolver configuration file.

This file usually shows which DNS server the system uses to translate domain names into IP addresses.

### Example

```bash
cat /etc/resolv.conf
```

### Security relevance

DNS is important because most internet activity begins with domain resolution.

A security analyst can use this file to check:

- Which DNS resolver the system uses
- Whether DNS is handled locally, by the router, by the ISP, or by another resolver
- Whether DNS settings look unexpected

Unexpected DNS resolvers can be suspicious because attackers sometimes modify DNS settings to redirect traffic.

---

## Command: ss -tulpen

### What it does

Shows TCP and UDP sockets, especially listening services.

The options mean:

- `-t`: TCP
- `-u`: UDP
- `-l`: listening sockets
- `-p`: process information
- `-e`: extended information
- `-n`: numeric output instead of resolving names

### Example

```bash
ss -tulpen
```

### Security relevance

This is one of the most important basic security commands.

It helps answer:

- What ports are open?
- Which services are listening?
- Are the services listening only locally or on a wider network interface?
- Which processes are responsible for the ports?

Listening ports matter because every exposed service can increase the attack surface of a system.

---

## Command: ping

### What it does

Sends ICMP echo requests to test whether a host is reachable.

It can show packet loss and response time.

### Example

```bash
ping -c 4 google.com
```

### Security relevance

`ping` is useful for basic connectivity testing.

It helps answer:

- Can I reach this host?
- Is there packet loss?
- How long does the response take?
- Does DNS resolution work when using a domain name?

In cybersecurity labs, ping is often used as an early network troubleshooting step.

However, some systems block ICMP, so a failed ping does not always mean the host is down.

---

## Command: traceroute

### What it does

Shows the path packets take from the local system to a destination.

It displays intermediate network hops between the source and destination.

### Example

```bash
traceroute google.com
```

### Security relevance

`traceroute` helps understand network path and routing behavior.

It can help identify:

- Where traffic is being routed
- Where latency appears
- Where traffic stops
- Whether traffic is taking an unexpected path

This is useful for troubleshooting and basic network reconnaissance in legal environments.

Some networks block or limit traceroute, so incomplete output is common.

---

## Command: nslookup

### What it does

Performs DNS lookups.

It asks a DNS resolver to translate a domain name into IP addresses.

### Example

```bash
nslookup github.com
```

### Security relevance

DNS lookups are important because domain names are heavily used in normal activity, phishing, malware, and command-and-control infrastructure.

A security analyst can use DNS tools to investigate:

- Which IP addresses a domain resolves to
- Whether a suspicious domain exists
- Whether a domain has IPv4 or IPv6 records
- Whether DNS responses look unusual

DNS evidence can be useful during incident response and threat analysis.

---

## Command: curl -I

### What it does

Sends an HTTP request and shows only the response headers.

The `-I` option means headers only.

### Example

```bash
curl -I https://github.com
```

### Security relevance

HTTP headers reveal useful information about a web server and its security controls.

A security analyst can inspect headers such as:

- `server`
- `content-type`
- `strict-transport-security`
- `content-security-policy`
- `x-frame-options`
- `set-cookie`

This helps identify web technologies, cookie security flags, HTTPS enforcement, caching behavior, and basic browser-side protections.

Headers alone do not prove whether a site is secure, but they are a useful first layer of web security inspection.
