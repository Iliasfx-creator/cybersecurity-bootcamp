#!/bin/bash

set -euo pipefail

OUTPUT_DIR="../evidence"
RAW_DIR="$HOME/private-bootcamp-evidence/week01-capstone/script-output"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$RAW_DIR"

sanitize_file() {
    local input_file="$1"
    local output_file="$2"

    sed -E \
    -e "s/$USER/[LOCAL_USER]/g" \
    -e "s/$(hostname)/[LOCAL_HOST]/g" \
    -e 's/[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}/[MAC_REDACTED]/g' \
    -e 's/172\.(1[6-9]|2[0-9]|3[0-1])\.[0-9]+\.[0-9]+/[PRIVATE_WSL_IP]/g' \
    -e 's/10\.255\.255\.254/[LOCAL_DNS_RESOLVER]/g' \
    -e 's#/mnt/c/Users/[^/ ]+#/mnt/c/Users/[WINDOWS_USER]#g' \
    "$input_file" > "$output_file"
}

echo "[+] Collecting system and network snapshot..."
{
  echo "=== User / Host ==="
  whoami
  hostname

  echo ""
  echo "=== Kernel ==="
  uname -a

  echo ""
  echo "=== IP addresses ==="
  ip a

  echo ""
  echo "=== Routes ==="
  ip route

  echo ""
  echo "=== DNS resolver ==="
  cat /etc/resolv.conf

  echo ""
  echo "=== Listening ports ==="
  ss -tulpen

  echo ""
  echo "=== Top processes ==="
  ps aux --sort=-%mem | head -15
} > "$RAW_DIR/system_network_snapshot_from_script_raw.txt"

sanitize_file \
"$RAW_DIR/system_network_snapshot_from_script_raw.txt" \
"$OUTPUT_DIR/system_network_snapshot_from_script.txt"

echo "[+] Running localhost Nmap scan..."
nmap 127.0.0.1 > "$RAW_DIR/local_nmap_scan_from_script_raw.txt"

sanitize_file \
"$RAW_DIR/local_nmap_scan_from_script_raw.txt" \
"$OUTPUT_DIR/local_nmap_scan_from_script.txt"

echo "[+] Done."
