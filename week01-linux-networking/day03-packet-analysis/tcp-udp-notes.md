# TCP vs UDP Notes

## TCP

### What TCP is

TCP stands for Transmission Control Protocol.

TCP is connection-based. Before real data is exchanged, the client and server first establish a connection.

The basic TCP opening sequence is called the three-way handshake:

- SYN
- SYN-ACK
- ACK

In simple terms:

- client says: I want to start a connection
- server says: I accept and acknowledge
- client says: confirmed, connection is open

### Why reliability matters

TCP is designed for reliable communication.

Reliability means that data should arrive completely, in order, and without missing parts.

This matters for services like SSH and HTTPS. If data is missing or arrives in the wrong order, the session can break or become corrupted.

TCP uses sequence numbers, acknowledgements, and retransmissions to handle this.

### Examples of TCP services

Common TCP services include:

- SSH on port 22
- HTTP on port 80
- HTTPS on port 443

### Security relevance

TCP matters in cybersecurity because many exposed services use TCP.

If a TCP port is open, a service may be reachable.

Security analysts inspect TCP traffic to understand:

- whether a service is listening
- whether a connection is established
- whether a TCP handshake completed
- which ports are exposed
- whether traffic patterns look normal or suspicious

Attackers also scan TCP ports to find possible attack surfaces.

## UDP

### What UDP is

UDP stands for User Datagram Protocol.

UDP is connectionless. It does not use a three-way handshake before sending data.

A UDP client can send a packet directly to a destination without first establishing a session.

In simple terms:

- TCP is like starting a confirmed phone call
- UDP is like sending a quick message and not waiting for a full connection setup

### Why speed matters

UDP has less overhead than TCP.

It is useful when speed matters more than built-in reliability.

Some applications prefer speed because small delays are worse than small packet loss.

Examples include voice, video, gaming, DNS, and some modern web traffic using QUIC.

### Examples of UDP services

Common UDP examples include:

- DNS on port 53
- NTP on port 123
- QUIC on port 443
- gaming traffic
- voice and video traffic

### Security relevance

UDP matters in cybersecurity because important network services use it.

Security analysts inspect UDP traffic to understand:

- DNS lookups
- time synchronization
- unusual outbound communication
- possible tunneling
- scanning behavior
- denial-of-service abuse

UDP can be abused in amplification attacks when small requests cause larger replies from exposed servers.

## Main difference

The main difference is that TCP creates and manages a connection, while UDP sends packets without a full connection setup.

TCP focuses on reliability.

UDP focuses on speed and low overhead.

In my own words:

TCP is better when the communication must arrive correctly and in order.

UDP is better when fast communication matters and the application can handle loss or missing reliability itself.
