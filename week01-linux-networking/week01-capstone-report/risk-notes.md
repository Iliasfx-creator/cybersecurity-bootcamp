# Risk Notes

## Exposed services

The local Nmap scan of 127.0.0.1 did not show open TCP ports among the default scanned ports.

This suggests that, on that exact loopback address, there were no obvious TCP services exposed in the default Nmap scan.

## Listening ports

The ss output showed local listening sockets, mainly DNS-related listeners and local time synchronization related UDP sockets.

This does not directly contradict the Nmap result because Nmap scanned 127.0.0.1 TCP ports, while ss showed multiple local addresses and both TCP and UDP sockets.

The main lesson is that listening address and protocol matter.

## DNS observations

DNS resolution worked for github.com and overthewire.org.

The system used a local DNS resolver, which was redacted in the public evidence.

DNS is security-relevant because it shows which domains a system is resolving before making network connections.

## HTTP header observations

The HTTP header checks showed that HTTPS connections completed successfully.

GitHub returned several security-related headers, including strict transport security, frame protection, content type protection, referrer policy, and content security policy.

OverTheWire returned headers through Cloudflare and other caching/proxy infrastructure.

I should not treat headers alone as proof that a site is secure or insecure. Headers are signals that need context.

## Logs and monitoring

Authentication logs and service logs are important because they help reconstruct activity.

For a real system, I would monitor failed logins, sudo usage, unexpected sessions, new listening ports, and unusual DNS or outbound traffic.

## What I would harden first

I would first review listening services and disable anything unnecessary.

Then I would keep the system updated, prefer SSH keys over passwords, protect private keys, and avoid exposing services to the internet unless needed.

## What I would monitor first

I would monitor authentication logs, listening ports, DNS queries, and repeated connection attempts.

These areas give early signals about suspicious access attempts, misconfiguration, or unexpected network behavior.
