#!/bin/bash
# Bu skript dmesg faylından əməliyyat sistemi versiyasını çıxarır.

# Analiz ediləcək faylın yolu
LOG_FILE="dmesg"

# Faylın mövcudluğunu yoxla
if [ -f "$LOG_FILE" ]; then
    # "Linux version" ifadəsini axtar və həmin sətri çap et
    grep "Linux version" "$LOG_FILE"
else
    echo "dmesg file not found!"
    exit 1
fi
