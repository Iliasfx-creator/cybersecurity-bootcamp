#!/bin/bash

echo "=== Service and Log Quick Audit ==="

echo ""
echo "[+] Current user:"
whoami

echo ""
echo "[+] Hostname:"
hostname

echo ""
echo "[+] Listening ports:"
ss -tulpen

echo ""
echo "[+] Top processes:"
ps aux --sort=-%mem | head -15

echo ""
echo "[+] Recent auth logs:"
if [ -f /var/log/auth.log ]; then
    sudo tail -20 /var/log/auth.log
else
    echo "/var/log/auth.log not found. Trying journalctl..."
    sudo journalctl -n 20 2>&1
fi
