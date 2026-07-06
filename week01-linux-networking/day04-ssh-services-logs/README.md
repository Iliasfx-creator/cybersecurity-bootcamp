# Day 4 — SSH, Services, Logs, Basic Hardening

## Goal

The goal of this lab was to understand SSH basics, service inventory, authentication logs, and basic Linux hardening.

This lab focused on how a security analyst or system administrator can inspect access methods, running services, listening ports, logs, and possible attack surface.

## What I practiced

I practiced:

- checking the SSH client version
- generating an SSH keypair safely
- distinguishing public keys from private keys
- collecting service inventory
- checking running processes
- checking listening ports
- reviewing authentication logs and journal logs
- writing a basic service and log audit script
- checking the repository for accidental secret files

## SSH summary

SSH is an encrypted remote shell protocol.

It is commonly used to manage Linux servers remotely. SSH usually uses TCP port 22.

SSH is security-relevant because successful SSH access can give a user direct command-line access to a system.

Password authentication is simple, but it can be attacked with brute force, password spraying, reused passwords, or stolen credentials.

Key authentication is usually stronger when the private key is protected correctly.

The private key must never be committed to GitHub.

## Services summary

A service is a background program that provides a function.

Some services only run locally. Other services listen on network ports.

Services are related to attack surface because each running service can become a possible point of interaction or attack.

A service listening on a network port is especially important because another system may be able to communicate with it.

## Logs summary

Authentication logs help show login-related and privilege-related activity.

They can show sudo usage, session opens and closes, failed logins, SSH attempts, and other authentication events.

Logs matter because they help analysts reconstruct what happened during troubleshooting or incident response.

## Basic Linux hardening checklist

### Keep system updated

Updates fix bugs and security vulnerabilities.

An outdated system may contain known weaknesses that attackers already know how to exploit.

### Use strong passwords

Strong passwords reduce the chance of successful guessing, brute force, or password spraying.

Weak or reused passwords make account compromise easier.

### Prefer SSH keys over passwords

SSH keys are usually harder to brute force than passwords.

They are safer when the private key is protected and not shared.

### Disable unused services

Unused services create unnecessary attack surface.

If a service is not needed, disabling it reduces the number of things an attacker can target.

### Check listening ports

Listening ports show which services may be reachable.

Reviewing listening ports helps identify unexpected or unnecessary network exposure.

### Use least privilege

Least privilege means users and processes should only have the permissions they need.

This limits damage if an account or process is compromised.

### Review authentication logs

Authentication logs can reveal failed login attempts, sudo usage, suspicious sessions, or unexpected access.

Regular log review helps detect problems earlier.

### Avoid exposing services to the internet unnecessarily

A service exposed to the public internet can be scanned and attacked by anyone.

Services should only be exposed when needed and should be protected with strong authentication and firewall rules.

### Never commit secrets or private keys

Secrets and private keys must not be stored in public repositories.

If a private key is committed, it may remain in Git history even after deletion and should be considered compromised.
