# Day 2 — Networking Basics

## Goal

The goal of this lab is to understand basic network identity, ports, DNS, HTTP headers, and how these concepts matter in cybersecurity.

## Network identity

### My local IP address

My WSL system received a private IP address on the `eth0` interface. The real value was redacted from the public evidence file because this repository is public.

The address used a `/20` prefix. The prefix shows which part of the address belongs to the network. A `/20` network is larger than a `/24` network.

### My default gateway

The default gateway was a private WSL gateway address. This is where traffic is sent when the destination is outside the local WSL network.

In simple terms, the gateway is the next hop used to reach other networks or the internet.

### My DNS resolver

The DNS resolver was also a private WSL-generated address from `/etc/resolv.conf`.

The DNS resolver is used to translate domain names like `github.com` into IP addresses.

### What this means

My WSL machine is behind a private virtual network. It has its own private IP, default route, and DNS resolver. These values are useful for troubleshooting, but they should be redacted before uploading public evidence to GitHub.

## Listening ports

### What `ss -tulpen` shows

The `ss -tulpen` command shows network sockets that are currently listening for traffic.

In this lab, I observed mainly DNS-related services on port 53 and time synchronization services on port 323.

The important fields are:

- `Netid`: the protocol, such as TCP or UDP
- `State`: whether the socket is listening or unconnected
- `Local Address:Port`: the local IP address and port used by the service
- `Peer Address:Port`: the remote address, if there is an active connection
- `Process`: the service or process related to the socket

### TCP vs UDP

TCP is connection-based. It is used when reliable communication is needed, such as SSH or HTTPS.

UDP is connectionless. It is often used for DNS, time synchronization, voice, video, and gaming traffic.

In the output, TCP services can appear as `LISTEN`, while UDP sockets often appear as `UNCONN` because UDP does not work like a TCP connection.

### Local address vs peer address

The local address is the address and port on my system.

The peer address is the remote system connected to it. For listening services, the peer is often shown as `0.0.0.0:*` or `[::]:*` because no specific remote client is connected yet.

### Why listening ports matter in cybersecurity

Listening ports matter because each open service can increase the attack surface of a system.

If a service is listening and reachable by other machines, an attacker may try to identify the service, find its version, test default credentials, exploit a known vulnerability, or abuse a misconfiguration.

In this lab, most observed services were local or WSL-internal DNS/time services. They are still useful to understand because security analysts must know how to identify what is listening on a system and whether it should be exposed.
