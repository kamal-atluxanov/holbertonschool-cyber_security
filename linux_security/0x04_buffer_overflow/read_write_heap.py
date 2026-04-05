#!/usr/bin/python3
"""
İşləyən prosesin heap sahəsindəki stringi tapan və onu əvəz edən skript.
İstifadə: ./read_write_heap.py pid search_string replace_string
"""

import sys

def find_and_replace_in_heap():
    """
    Prosesin ID-sini (pid) alır, heap sahəsini tapır və
    göstərilən stringi yenisi ilə əvəz edir.
    """
    # 1. Arqument sayını yoxla (Düzgün istifadə xətası üçün status 1)
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_str = sys.argv
    replace_str = sys.argv

    # PID-nin rəqəm olub-olmadığını yoxla
    if not pid.isdigit():
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    try:
        # 2. Maps faylını oxuyub heap sahəsini tapırıq
        with open(maps_path, 'r') as maps_file:
            heap_line = None
            for line in maps_file:
                if "[heap]" in line:
                    heap_line = line
                    break

            if not heap_line:
                # Heap tapılmadısa səssizcə çıxmaq və ya xəta vermək olar
                sys.exit(1)

            # Ünvan hissəsini ayırırıq (məs: 555e646e0000-555e64701000)
            addr_range = heap_line.split().split('-')
            start_addr = int(addr_range, 16)
            end_addr = int(addr_range, 16)

        # 3. Mem faylını ikili formatda (binary) yazıb-oxumaq üçün açırıq
        with open(mem_path, 'rb+') as mem_file:
            mem_file.seek(start_addr)
            heap_data = mem_file.read(end_addr - start_addr)

            # Axtarılan stringi bayt formatına çeviririk
            search_bytes = search_str.encode('ascii')

            # Stringin yerini (offset) tapırıq
            offset = heap_data.find(search_bytes)
            if offset == -1:
                # Əgər string tapılmadısa, sistem bunu xəta sayır
                sys.exit(1)

            # Yazılacaq ünvanı müəyyən edib yeni mətni yazırıq
            mem_file.seek(start_addr + offset)

            # QEYD: Yeni stringi yazırıq. Uzunluq fərqi varsa belə,
            # biz sadəcə verilən mətni yazırıq (ASCII).
            mem_file.write(replace_str.encode('ascii'))

            # Yalnız bir dəfə uğur mesajı çap edirik
            print("SUCCESS!")

    except (PermissionError, FileNotFoundError):
        # İcazə yoxdursa və ya proses tapılmadısa
        sys.exit(1)
    except Exception:
        # Digər gözlənilməz xətalar üçün
        sys.exit(1)

if __name__ == "__main__":
    find_and_replace_in_heap()
