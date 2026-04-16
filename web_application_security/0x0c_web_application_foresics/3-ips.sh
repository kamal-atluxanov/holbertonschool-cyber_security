#!/bin/bash
# Bu skript sistemə uğurla daxil olan unikal IP ünvanlarının sayını hesablayır.

LOG_FILE="auth.log"

# Faylın mövcudluğunu yoxla
if [ -f "$LOG_FILE" ]; then
    # 1. "Accepted" (uğurlu giriş) olan sətirləri tap
    # 2. Sətirlərdəki IP ünvanlarını çıxar (adətən "from" sözündən sonra gəlir)
    # 3. IP-ləri sırala və təkrarları sil (unikal et)
    # 4. Unikal sətirləri say (wc -l)
    
    grep "Accepted" "$LOG_FILE" | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' | sort | uniq | wc -l
else
    echo "Log file not found!"
    exit 1
fi
