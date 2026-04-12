#!/bin/bash

# Faylın mövcudluğunu yoxlayırıq
LOG_FILE="logs.txt"

if [ ! -f "$LOG_FILE" ]; then
    echo "Fayl tapılmadı: $LOG_FILE"
    exit 1
fi

# IP ünvanlarını çıxarır, sayır və ən çox müraciət edəni çap edir
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
