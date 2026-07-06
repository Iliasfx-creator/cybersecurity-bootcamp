# Nmap Safety Rules

## Allowed targets for this lab

- 127.0.0.1
- localhost
- scanme.nmap.org

## Disallowed targets

I will not scan public IPs, university networks, company systems, neighbor networks, random websites, or any system I do not own or have permission to test.

## Why permission matters

Port scanning can be interpreted as suspicious or hostile when done without authorization.

Scanning creates visible network behavior. Even if it is not exploitation, it can still trigger logs, alerts, firewall rules, or abuse complaints.

Permission matters because security testing must be done only on systems I own or systems where I have explicit authorization.

Without permission, scanning can create legal, ethical, and operational problems.

## Scan intensity rule

I will use light scans only and avoid aggressive/high-volume scanning.

For this lab, I will avoid hammering targets, avoid wide scans, avoid random targets, and only use the specific approved lab targets.

The purpose is learning how scanning works, not stressing or attacking systems.
