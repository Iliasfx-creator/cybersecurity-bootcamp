# Scan Analysis

## Localhost scan

### What target did I scan?

I scanned:

127.0.0.1

This is the loopback address. It points back to my own local system.

### What ports were open?

The basic Nmap scan showed no open ports on 127.0.0.1 among the default 1000 scanned TCP ports.

The output showed that all scanned TCP ports were closed or in ignored closed states.

### What services did Nmap identify?

Nmap did not identify open services on 127.0.0.1.

The version scan also did not identify services because there were no open TCP ports found on that exact target.

### Did the results match ss -tulpen?

The results mostly made sense, but they showed an important difference between tools.

Nmap scanned the exact target 127.0.0.1.

The ss -tulpen output showed local DNS-related listeners on addresses such as 127.0.0.53, 127.0.0.54, and a local DNS resolver address.

Those are local addresses, but they are not the same exact target as 127.0.0.1.

Also, ss showed UDP listeners, while the basic Nmap scan checked TCP ports.

So this was not a contradiction. It showed that target address, protocol, and scan type matter.

### What surprised me?

The surprising part was that localhost did not show open TCP ports in the Nmap scan, even though ss showed local listening sockets.

This taught me that I must be precise about the exact IP address, protocol, and scan type being checked.

## scanme.nmap.org scan

### Why this target is allowed

scanme.nmap.org is an official Nmap test target intended for learning and testing light scans.

I only used light scans against this host and avoided aggressive or high-volume scanning.

### What ports did I scan?

I used:

- a top 20 ports scan with -T2
- a version scan only on ports 22, 80, and 9929

The version scan was intentionally limited to a small number of ports.

### What ports were open?

The top ports scan showed these open ports:

- 22/tcp open ssh
- 80/tcp open http

The version scan showed these open ports:

- 22/tcp open ssh
- 80/tcp open http
- 9929/tcp open nping-echo

### What services were detected?

Nmap detected:

- OpenSSH on port 22
- Apache httpd on port 80
- Nping echo on port 9929

The version scan provided more detail than the basic scan because it tried to identify the services behind the open ports.

### Why I avoided aggressive scans

I avoided aggressive scans because the lab scope only allows light scanning.

Aggressive scans can create more traffic, trigger alerts, stress systems, or look hostile.

Even when a target is intended for testing, scanning should stay controlled and respectful.

## Nmap traffic capture

### What did tcpdump show?

tcpdump showed packets between my WSL system and scanme.nmap.org.

The capture showed Nmap sending TCP SYN packets to several ports on the target.

The capture also showed different responses from the target depending on whether the port was open or closed.

### What packets did Nmap generate?

Nmap generated TCP SYN packets to multiple ports.

For open ports such as 80 and 22, the target replied with SYN-ACK.

After that, my system acknowledged the connection and then reset it with RST. This showed that Nmap only needed enough interaction to determine that the port was open.

For closed ports such as 23, 25, 443, 21, 139, 445, 110, and 3389, the target replied with RST.

This showed that the host was reachable but those ports were not accepting connections.

### What does this reveal about scanning?

This reveals that port scanning creates visible network traffic.

A scan is not invisible. It sends packets to target ports and waits for responses.

The response pattern helps Nmap decide whether a port is open, closed, or filtered.

An open port often responds differently from a closed port.

### Why defenders can detect scans in logs/traffic?

Defenders can detect scans because scanning creates repeated connection attempts to multiple ports.

These attempts can appear in packet captures, firewall logs, intrusion detection systems, and service logs.

A defender may notice one source trying many ports in a short period of time.

This is why port scanning is security-relevant behavior, even when it is not exploitation.
