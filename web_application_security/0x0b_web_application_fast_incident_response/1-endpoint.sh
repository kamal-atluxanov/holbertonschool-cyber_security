#!/bin/bash

# Log faylının adını təyin edirik
LOG_FILE="logs.txt"

# Faylın mövcudluğunu yoxlayırıq
if [ ! -f "$LOG_FILE" ]; then
    exit 1
fi

# URL-ləri çıxarır (adətən 7-ci sütun), sayır və ən çox müraciət olunanı çap edir
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
