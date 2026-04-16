#!/bin/bash
# Bu skript loq faylını analiz edərək hansı xidmətin hədəf alındığını müəyyən edir.

# Analiz ediləcək loq faylının yolu (adətən auth.log və ya secure log olur)
LOG_FILE="auth.log"

# Əgər loq faylı mövcuddursa, analizə başla
if [ -f "$LOG_FILE" ]; then
    # 1. 'sshd' olan sətirləri tap
    # 2. Lazımsız hissələri kəs (məsələn, vaxt və host adı)
    # 3. Sözləri say və azalan sıra ilə düz
    cat "$LOG_FILE" | grep "sshd" | awk '{for(i=5;i<=NF;i++) print $i}' | sort | uniq -c | sort -nr
else
    echo "Log file not found!"
    exit 1
fi
