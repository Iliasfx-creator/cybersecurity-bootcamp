# Week 1 Capstone Report — Linux & Networking Security Baseline

## Executive Summary

This capstone report summarizes a local Linux and networking security baseline audit performed in my WSL lab environment. The purpose was to combine the Week 1 topics into one analyst-style report: Linux identity, network interfaces, routes, DNS behavior, listening ports, local scanning, HTTP headers, and defensive interpretation.

The audit did not attempt exploitation. It focused only on observation, evidence collection, and risk interpretation. The target was my own local environment, especially 127.0.0.1 and local system configuration. The main result was that the local Nmap scan of 127.0.0.1 did not show open TCP ports in the default scan, while ss showed local listening sockets on specific local addresses and protocols. This was an important distinction because tools can appear to disagree when they are checking different addresses or protocols.

Overall, the system did not show obvious exposed TCP services on 127.0.0.1 from the basic Nmap scan. However, local DNS-related listeners and local UDP services were visible through ss. This means the environment still has network-relevant components that should be understood and monitored.

## Scope

The scope of this audit was limited to my local WSL environment and basic external checks to GitHub and OverTheWire using DNS and HTTPS headers.

The local scan target was:

- 127.0.0.1

The DNS and HTTP checks were limited to:

- github.com
- overthewire.org

No random public IPs, university networks, company systems, neighbor networks, or unauthorized targets were scanned.

## Tools Used

The tools used in this capstone were:

- whoami
- hostname
- uname
- ip
- ss
- ps
- nmap
- nslookup
- curl
- bash
- grep
- sed

These tools provided identity, operating system, network, DNS, process, port, and HTTP header evidence.

## Findings

### Finding 1 — Local network identity

The system and network snapshot collected user, host, kernel, IP address, route, DNS resolver, listening socket, and process information.

Sensitive local details such as the local username, hostname, private WSL IP addresses, MAC addresses, and local resolver address were redacted before committing evidence to the public repository.

This finding matters because system identity and network identity are the starting point of any defensive audit. A security analyst needs to know what system is being reviewed, what network interfaces exist, what routes are present, and which resolver is being used.

### Finding 2 — Listening ports and services

The ss evidence showed listening sockets on local addresses. The visible services were mainly DNS-related local listeners and local UDP time synchronization related sockets.

This is important because a listening socket means a process is waiting for network communication. Not every listener is dangerous, but every listener is security-relevant. A service listening only on a local address has a different risk level from a service listening on all interfaces or exposed to the internet.

The main defensive action is to review listening ports regularly and confirm that each one has a legitimate purpose.

### Finding 3 — Localhost Nmap scan

The Nmap scan of 127.0.0.1 showed that all default scanned TCP ports were closed or ignored closed states. Nmap did not identify open TCP services on that exact target.

This result mostly makes sense when compared with ss, but the comparison requires precision. Nmap scanned 127.0.0.1 over TCP. The ss output showed sockets on multiple local addresses, including local DNS resolver addresses, and included UDP sockets as well as TCP sockets.

Therefore, the results are not a contradiction. They show that target IP, listening address, and protocol matter. A scan of 127.0.0.1 is not the same as checking every local address. A TCP scan is not the same as checking UDP listeners.

### Finding 4 — DNS behavior

The DNS checks showed that the system could resolve github.com and overthewire.org. The public evidence redacted the local DNS resolver.

DNS is important in security because many network connections begin with name resolution. Even when later traffic is encrypted, DNS behavior can still reveal which domains a system is trying to contact, unless encrypted DNS is used.

From a defensive perspective, DNS logs can help identify suspicious domains, malware command-and-control behavior, phishing infrastructure, or unusual outbound activity.

### Finding 5 — HTTP headers

The HTTP header checks showed successful HTTPS responses from GitHub and OverTheWire.

GitHub returned several security-related headers, including strict transport security, frame protection, content type protection, referrer policy, and content security policy. These headers help control browser behavior and reduce certain classes of web risk.

OverTheWire returned headers through Cloudflare and caching/proxy infrastructure. This showed that modern web services often sit behind reverse proxies, CDNs, or caching layers.

HTTP headers are useful signals, but they are not full proof of security. They show configuration details and defensive controls, but they do not prove whether the application itself is secure.

## Risk Assessment

The observed local risk appears low from the limited evidence collected. The basic Nmap scan did not find open TCP ports on 127.0.0.1. However, local listening sockets were still present in ss output.

The main risk is not a confirmed vulnerability. The main risk is misunderstanding exposure. A system owner could incorrectly assume that no services exist because one scan found no open ports, while another tool shows listeners on different addresses or protocols.

This is why multiple tools and careful interpretation are necessary.

## Recommendations

First, continue reviewing listening ports with ss and Nmap. Check exact IP addresses and protocols instead of assuming all local addresses behave the same.

Second, keep the system updated. Updates reduce exposure to known vulnerabilities.

Third, avoid unnecessary services. If a service is not needed, it should not be listening.

Fourth, protect secrets and private keys. Nothing sensitive should be committed to GitHub.

Fifth, monitor authentication logs, DNS behavior, and unexpected outbound connections.

Sixth, document evidence clearly and sanitize private information before publishing.

## Lessons Learned

The biggest lesson from Week 1 is that network visibility depends on the tool, target, protocol, and context.

I learned that ping, DNS, HTTP, tcpdump, ss, logs, SSH, and Nmap all show different parts of the same system. No single command tells the whole story.

I also learned that encrypted traffic still exposes useful metadata, that logs are essential for investigation, and that services listening on ports are part of attack surface.

Finally, I learned that safe security work requires strict scope. Scanning is not the same as exploitation, but it is still security-relevant and must only be done on authorized targets.

## Evidence Files

- evidence/system_network_snapshot.txt
- evidence/local_nmap_scan.txt
- evidence/local_ss_ports.txt
- evidence/dns_checks.txt
- evidence/http_header_checks.txt
- evidence/system_network_snapshot_from_script.txt
- evidence/local_nmap_scan_from_script.txt
