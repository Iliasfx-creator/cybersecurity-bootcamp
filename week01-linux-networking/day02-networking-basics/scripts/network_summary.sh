#!/bin/bash

echo "=== Network Summary ==="

echo ""
echo "[+] Hostname:"
hostname

echo ""
echo "[+] IP addresses:"
hostname -I

echo ""
echo "[+] Default route:"
ip route | grep default

echo ""
echo "[+] DNS resolver:"
cat /etc/resolv.conf

echo ""
echo "[+] Listening ports:"
ss -tulpen
