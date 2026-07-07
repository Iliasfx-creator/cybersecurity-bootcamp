#!/bin/bash

TARGET="${1:-http://127.0.0.1:8000}"

echo "=== HTTP Probe ==="
echo "[+] Target: $TARGET"

echo ""
echo "[+] Response headers:"
curl -I "$TARGET"

echo ""
echo "[+] GET response preview:"
curl -s "$TARGET" | head -20

echo ""
echo "[+] OPTIONS response:"
curl -i -X OPTIONS "$TARGET"
