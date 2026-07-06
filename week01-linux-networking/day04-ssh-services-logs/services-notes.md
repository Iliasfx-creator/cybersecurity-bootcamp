# Services Notes

## What a service is

A service is a program that runs in the background to provide a function for the system or for users.

Some services only run locally. Other services listen on network ports and accept connections from other machines.

Examples of services include SSH servers, web servers, database servers, logging services, scheduled jobs, and update services.

## What systemctl shows

systemctl is used on Linux systems that use systemd.

It can show which services are running, stopped, failed, enabled, or disabled.

In a normal Linux server, systemctl is one of the main tools for managing services.

In WSL, systemctl may not always behave exactly like it does on a full Linux installation because WSL may not run a complete traditional systemd environment.

## What service --status-all shows

service --status-all shows services known through older service management scripts.

It can show which services appear to be running and which are stopped.

This is useful as a fallback when systemctl is limited or unavailable.

## What ps aux shows

ps aux shows running processes.

A process is a currently running program.

This command helps me see what is executing, which user owns the process, and how much CPU or memory it is using.

This matters because suspicious processes can indicate malware, persistence, misconfiguration, or unexpected software running on a system.

## What ss -tulpen shows

ss -tulpen shows listening network sockets.

It can show:

- TCP listeners
- UDP listeners
- local addresses
- ports
- users
- process information when available

This is security-relevant because a listening port means something may be reachable through the network.

## How services relate to attack surface

Attack surface means the places where an attacker can interact with a system.

Every running service can increase attack surface, especially if it listens on a network port.

An unnecessary service creates unnecessary risk.

A vulnerable or misconfigured service can become an entry point for an attacker.

Reducing attack surface means disabling unused services, limiting exposed ports, keeping software updated, and using least privilege.

## Which services/ports did I observe?

I collected service information using systemctl, service --status-all, ps aux, and ss -tulpen.

The most important observation is that services and listening ports must be reviewed together.

A running process is important, but a process that listens on a network port is even more security-relevant because other systems may be able to communicate with it.

In this lab environment, I used the evidence file services_inventory.txt to document what was running and what ports were listening.
