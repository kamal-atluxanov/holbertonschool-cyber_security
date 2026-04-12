#!/bin/bash

# Log faylının adını təyin edirik
LOG_FILE="logs.txt"

# Faylın mövcudluğunu yoxlayırıq
if [ ! -f "$LOG_FILE" ]; then
    exit 1
fi

# Ən çox müraciət edən IP-nin neçə dəfə göründüyünü (sayını) çap edir
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 1 | awk '{print $1}'
