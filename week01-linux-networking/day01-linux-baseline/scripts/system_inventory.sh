#!/bin/bash

echo "=== System Inventory ==="

echo ""
echo "[+] Current user:"
whoami

echo ""
echo "[+] Hostname:"
hostname

echo ""
echo "[+] Kernel:"
uname -a

echo ""
echo "[+] IP addresses:"
ip a

echo ""
echo "[+] Listening ports:"
ss -tulpen

echo ""
echo "[+] Top processes:"
ps aux --sort=-%mem | head

echo ""
echo "[+] Disk usage:"
df -h

echo ""
echo "[+] Memory usage:"
free -h
