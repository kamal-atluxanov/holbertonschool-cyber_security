#!/bin/bash
# Bu skript son 1000 sətri analiz edərək ələ keçirilmiş hesabı tapır.

LOG_FILE="auth.log"

# Faylın mövcudluğunu yoxla
if [ -f "$LOG_FILE" ]; then
    # 1. Son 1000 sətri götür
    # 2. Uğurlu girişləri (Accepted) filtrələ
    # 3. İstifadəçi adını çıxar (adətən 'for' sözündən sonrakı sütun)
    # 4. Əgər eyni istifadəçi həm də çoxlu 'Failed' alıbsa, o hədəfdir
    
    tail -n 1000 "$LOG_FILE" | grep "Accepted" | awk '{for(i=1;i<=NF;i++) if($i=="for") print $(i+1)}' | sort | uniq
else
    echo "Log file not found!"
    exit 1
fi
