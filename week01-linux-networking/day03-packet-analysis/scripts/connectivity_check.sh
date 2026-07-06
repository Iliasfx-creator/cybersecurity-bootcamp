#!/bin/bash

TARGETS=("8.8.8.8" "1.1.1.1" "github.com" "overthewire.org")

echo "=== Connectivity Check ==="

for target in "${TARGETS[@]}"; do
    echo ""
    echo "[+] Testing: $target"
    ping -c 2 "$target"
done
