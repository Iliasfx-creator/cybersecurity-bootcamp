# Day 5 — Safe Port Scanning with Nmap

## Goal

The goal of this lab was to learn safe and controlled port scanning with Nmap.

I practiced scanning only approved targets, analyzing open and closed ports, comparing Nmap results with local listening sockets, capturing scan traffic, and writing a script that refuses unauthorized targets.

## Safety scope

Allowed targets for this lab:

- 127.0.0.1
- localhost
- scanme.nmap.org

I did not scan random public IPs, university networks, company systems, neighbor networks, or systems where I do not have permission.

Port scanning is not exploitation, but it is still security-relevant behavior and can be interpreted as suspicious when done without authorization.

## Tools used

- nmap
- dig
- ss
- tcpdump
- bash

## Localhost scan summary

I scanned 127.0.0.1 with a basic Nmap scan and a version detection scan.

Nmap did not find open TCP ports on 127.0.0.1 among the default scanned ports.

I also compared the result with ss -tulpen.

The ss output showed local listening sockets on other local addresses and UDP ports, which taught me that exact target address and protocol matter.

## scanme.nmap.org scan summary

I scanned scanme.nmap.org using light scans.

The top ports scan showed open SSH and HTTP services.

The version scan on selected ports showed:

- OpenSSH on port 22
- Apache httpd on port 80
- Nping echo on port 9929

This showed how version detection gives more detail than a basic port scan.

## What I learned about open ports

An open port means a service is listening and accepting connections.

Open ports matter because they expose services that can be interacted with.

From a defender's point of view, every open port should have a reason to exist.

## What I learned about filtered ports

A filtered port means Nmap cannot clearly determine whether the port is open or closed.

This often happens because a firewall or packet filter blocks or drops traffic.

Filtered does not automatically mean safe. It means the scanner did not receive a clear answer.

## What I learned about service version detection

Service version detection tries to identify the software behind an open port.

This is useful for inventory and security review.

It can also be useful to attackers, so it should only be used on systems where scanning is authorized.

## What defenders can observe

Defenders can observe port scanning through network traffic, firewall logs, IDS alerts, and service logs.

A scan may appear as one source contacting many ports in a short period of time.

The tcpdump capture showed that Nmap generated visible TCP packets, including SYN packets and responses such as SYN-ACK or RST.

## Mistakes / difficulties

The localhost scan initially seemed confusing because Nmap showed no open TCP ports on 127.0.0.1, while ss showed local listening sockets.

The reason was that ss showed sockets on multiple local addresses and protocols, while Nmap scanned one exact IP address and TCP ports.

Another important point was keeping the scan scope strict and avoiding unauthorized targets.
