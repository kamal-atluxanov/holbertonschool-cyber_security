#!/bin/bash

# Log faylının adını təyin edirik
LOG_FILE="logs.txt"

# Faylın mövcudluğunu yoxlayırıq
if [ ! -f "$LOG_FILE" ]; then
    exit 1
fi

# 1. Hücumçunun IP ünvanını tapırıq
ATTACKER_IP=$(awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}')

# 2. Həmin IP-yə aid User-Agent sətirlərini çıxarırıq və ən çox istifadə olunanı tapırıq
grep "$ATTACKER_IP" "$LOG_FILE" | awk -F'"' '{print $6}' | sort | uniq -c | sort -nr | head -n 1 | awk '{$1=""; print $0}' | sed 's/^ //'
