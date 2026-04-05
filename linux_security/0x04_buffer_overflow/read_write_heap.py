#!/usr/bin/python3
"""
Holberton WebSec 0x04 - Read/Write Heap
Bu script işləyən prosesin heap-ində string tapır və dəyişdirir.
"""

import sys

def solve():
    # 1. Arqumentlərin yoxlanılması (Dəqiq 3 dənə olmalıdır)
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_string = sys.argv
    replace_string = sys.argv

    # Boş string axtarırıqsa, heç nə etməyək
    if not search_string:
        return

    try:
        # 2. Maps faylını oxuyub heap-in yerini tapırıq
        with open(f"/proc/{pid}/maps", "r") as maps_file:
            for line in maps_file:
                if "[heap]" in line:
                    # Adres hissəsini götürürük (məs: 00400000-00421000)
                    addr_range = line.split()
                    start_addr, end_addr = [int(x, 16) for x in addr_range.split('-')]
                    break
            else:
                # Əgər heap tapılmasa
                return

        # 3. Mem faylını "rb+" (oxumaq və yazmaq) rejimində açırıq
        with open(f"/proc/{pid}/mem", "rb+") as mem_file:
            # Heap-in başladığı yerə gedirik
            mem_file.seek(start_addr)
            heap_data = mem_file.read(end_addr - start_addr)

            # Stringi axtarırıq (bytes formatında)
            try:
                index = heap_data.index(search_string.encode('ascii'))
            except ValueError:
                # String tapılmasa heç nə etmə
                return

            # Stringin tapıldığı tam ünvanı hesablayırıq
            found_at = start_addr + index
            
            # Həmin ünvana gedirik və yeni stringi yazırıq
            mem_file.seek(found_at)
            mem_file.write(replace_string.encode('ascii'))
            
    except Exception:
        # Hər hansı icazə və ya sistem xətası olsa exit(1)
        sys.exit(1)

if __name__ == "__main__":
    solve()
