# DNS Notes

## What DNS does

DNS stands for Domain Name System.

DNS translates human-readable domain names into IP addresses. For example, when I type `github.com`, my system needs an IP address before it can communicate with GitHub.

In simple terms:

```text
domain name -> DNS lookup -> IP address
```

A domain name is easier for humans to remember. An IP address is what computers use to route traffic.

## What a DNS resolver is

A DNS resolver is the server my system asks when it needs to translate a domain name into an IP address.

In this lab, WSL used a private internal DNS resolver. I redacted the resolver address in the public evidence file because the repository is public.

## What an A record is

An A record maps a domain name to an IPv4 address.

Example from this lab:

```text
github.com -> 140.82.121.3
```

IPv4 addresses look like this:

```text
140.82.121.3
172.217.16.142
```

## What an AAAA record is

An AAAA record maps a domain name to an IPv6 address.

Example from this lab:

```text
google.com -> 2a00:1450:4017:816::200e
```

IPv6 addresses are longer than IPv4 addresses and use hexadecimal notation.

## What "non-authoritative answer" means

A non-authoritative answer means the response came from a DNS resolver or cache, not directly from the authoritative DNS server responsible for that domain.

This is normal for everyday DNS lookups.

## Why DNS matters in cybersecurity

DNS matters in cybersecurity because many network activities begin with DNS.

Security analysts can use DNS information to investigate:

- suspicious domain lookups
- phishing domains
- malware command-and-control domains
- unusual traffic patterns
- domain reputation
- systems contacting unknown infrastructure

If a compromised machine keeps resolving strange domains, DNS logs can help identify malicious activity.

## Example lookups

### google.com

Result:

```text
A record:    172.217.16.142
AAAA record: 2a00:1450:4017:816::200e
```

This means `google.com` resolved to both IPv4 and IPv6 addresses.

### github.com

Result:

```text
A record: 140.82.121.3
```

This means `github.com` resolved to an IPv4 address in this lookup.

### overthewire.org

Result:

```text
A records:
104.21.46.149
172.67.140.53

AAAA records:
2606:4700:3033::6815:2e95
2606:4700:3035::ac43:8c35
```

This means `overthewire.org` resolved to multiple IPv4 and IPv6 addresses.
