#!/usr/bin/python3
"""
Holberton WebSec 0x04 - Read/Write Heap
Bu script işləyən prosesin heap-ində string tapır və dəyişdirir.
"""

import sys

def read_write_heap():
    # 1. Arqumentlərin düzgünlüyünü yoxlayırıq
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_str = sys.argv
    replace_str = sys.argv

    # Boş string axtarılırsa, heç nə etmədən çıxırıq
    if not search_str:
        return

    try:
        # 2. Heap-in başladığı və bitdiyi ünvanı /proc/[pid]/maps-dan tapırıq
        with open(f"/proc/{pid}/maps", "r") as maps_file:
            heap_start = None
            heap_end = None
            for line in maps_file:
                if "[heap]" in line:
                    # Nümunə format: 00c61000-00c82000 rw-p ... [heap]
                    addr_range = line.split()
                    start_hex, end_hex = addr_range.split('-')
                    heap_start = int(start_hex, 16)
                    heap_end = int(end_hex, 16)
                    break

            # Əgər heap tapılmasa, çıxırıq
            if heap_start is None:
                return

        # 3. /proc/[pid]/mem faylına daxil olub axtarış və dəyişiklik edirik
        with open(f"/proc/{pid}/mem", "rb+") as mem_file:
            # Heap-in yerləşdiyi hissəni oxuyuruq
            mem_file.seek(heap_start)
            heap_data = mem_file.read(heap_end - heap_start)

            # Stringi tapırıq (ASCII baytlar kimi)
            try:
                index = heap_data.index(search_str.encode('ascii'))
            except ValueError:
                # Əgər string tapılmasa, çıxırıq
                return

            # Yazılacaq tam ünvanı hesablayırıq
            target_addr = heap_start + index

            # Həmin ünvana gedirik və yeni stringi yazırıq
            mem_file.seek(target_addr)
            mem_file.write(replace_str.encode('ascii'))

            # Qeyd: Bəzi hallarda stringin sonuna NULL byte (\0) qoymaq lazımdır:
            # mem_file.write(replace_str.encode('ascii') + b'\x00')

    except (PermissionError, ProcessLookupError):
        # İcazə və ya proses tapılmama xətası zamanı 1 ilə çıxırıq
        sys.exit(1)
    except Exception:
        # Digər gözlənilməz xətalar üçün
        sys.exit(1)

if __name__ == "__main__":
    read_write_heap()
