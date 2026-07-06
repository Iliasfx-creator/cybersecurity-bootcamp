#!/bin/bash

TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    echo "Allowed targets: 127.0.0.1, localhost, scanme.nmap.org"
    exit 1
fi

case "$TARGET" in
    127.0.0.1|localhost|scanme.nmap.org)
        echo "[+] Target allowed: $TARGET"
        echo "[+] Running safe basic scan..."
        nmap -T2 --top-ports 20 "$TARGET"
        ;;
    *)
        echo "[-] Target not allowed for this lab."
        echo "Allowed targets: 127.0.0.1, localhost, scanme.nmap.org"
        exit 1
        ;;
esac
