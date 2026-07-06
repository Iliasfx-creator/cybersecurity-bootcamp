# Packet Analysis Notes

## ICMP capture

### What command generated the traffic?

The traffic was generated with:

ping -c 3 8.8.8.8

This sent three ICMP echo requests from my WSL system to 8.8.8.8.

### What protocol was captured?

The protocol captured was ICMP.

ICMP is used for network control and diagnostic messages. The ping command uses ICMP echo request and ICMP echo reply messages.

### What does request mean?

An ICMP echo request means my system is asking the remote host if it is reachable.

In this capture, the direction was:

[PRIVATE_WSL_IP] -> 8.8.8.8

In simple terms, my system asked:

"Are you reachable?"

### What does reply mean?

An ICMP echo reply means the remote host answered the request.

In this capture, the direction was:

8.8.8.8 -> [PRIVATE_WSL_IP]

In simple terms, the remote host answered:

"Yes, I am reachable."

### What I observed

The capture showed three request/reply pairs:

- seq 1 request and seq 1 reply
- seq 2 request and seq 2 reply
- seq 3 request and seq 3 reply

This matched the ping command because I sent three pings.

The packet id stayed the same during the ping session, while the sequence number increased for each request.

### Why ICMP matters in cybersecurity

ICMP matters because it helps test network reachability and troubleshoot connectivity.

Security analysts can use ICMP to check whether a host responds, whether packets are being lost, and whether latency looks unusual.

Attackers can also use ICMP during reconnaissance to discover live hosts. Because of that, some networks block or limit ICMP traffic.

A failed ping does not always mean a host is offline. It may mean ICMP is filtered.

## DNS capture

### What command generated the traffic?

The traffic was generated with:

nslookup example.com 8.8.8.8

This asked the DNS server 8.8.8.8 to resolve the domain name `example.com`.

### What port was used?

The capture showed traffic to and from port 53.

Port 53 is the standard DNS port.

### Was it TCP or UDP?

This lookup used DNS traffic on port 53. For normal small DNS lookups, DNS usually uses UDP.

In the capture, my system sent DNS queries from random high source ports to destination port 53 on 8.8.8.8.

The DNS server replied from port 53 back to those temporary source ports.

### What does this show about DNS?

This shows that DNS is a question-and-answer protocol.

My system asked:

- What IPv4 address does example.com have?
- What IPv6 address does example.com have?

The DNS server answered with:

- A records for IPv4 addresses
- AAAA records for IPv6 addresses

The capture showed both `A? example.com` and `AAAA? example.com`.

### Why DNS traffic matters in cybersecurity

DNS traffic matters because many network connections begin with a DNS lookup.

Before a system connects to a domain, it often asks a DNS resolver for the domain's IP address.

Security analysts can inspect DNS traffic to find:

- suspicious domains
- malware command-and-control lookups
- phishing infrastructure
- unusual external communication
- systems contacting domains they should not contact

DNS is useful because even when later traffic is encrypted, the DNS lookup may still reveal what domain the system tried to reach, unless encrypted DNS is being used.

## HTTPS capture

### What command generated the traffic?

The traffic was generated with:

curl -I https://example.com

In this lab, I used a resolved IP address for example.com and captured traffic to TCP port 443.

### Which remote IP was contacted?

The remote IP contacted in the capture was:

104.20.23.154

This is a public IP address returned for example.com during the lab.

### Which port was used?

The connection used TCP port 443.

Port 443 is the standard port for HTTPS.

### What TCP behavior did I observe?

The capture showed a TCP three-way handshake:

- SYN from my system to the remote server
- SYN-ACK from the remote server back to my system
- ACK from my system back to the remote server

After the handshake, the capture showed packets with PSH/ACK flags. These packets carried data inside the TCP connection.

At the end, FIN/ACK packets appeared, which showed that the TCP connection was closing.

### Could I see the HTTP content? Why or why not?

I could not see the HTTP headers or page content clearly inside the packet capture because the request used HTTPS.

HTTPS means HTTP over TLS encryption.

Tcpdump can show metadata such as IP addresses, ports, packet timing, TCP flags, and packet sizes. It cannot show the decrypted HTTP content unless TLS decryption keys are available.

### What can an analyst still learn from encrypted traffic metadata?

Even when traffic is encrypted, an analyst can still learn useful metadata:

- which local system communicated
- which remote IP was contacted
- which port was used
- when the connection happened
- how many packets were exchanged
- how much data was transferred
- whether the TCP handshake completed
- whether the connection closed normally

This matters in cybersecurity because suspicious encrypted traffic can still reveal patterns, destinations, timing, and behavior.
