#!/usr/bin/python3
"""
Finds and replaces a string in the heap of a running process.
Usage: read_write_heap.py pid search_string replace_string
"""

import sys

def solve():
    # 1. Arqumentlərin yoxlanılması
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_str = sys.argv
    replace_str = sys.argv

    if not search_str:
        return

    try:
        # 2. Heap-in yerini /proc/[pid]/maps-dan tapırıq
        maps_path = "/proc/{}/maps".format(pid)
        mem_path = "/proc/{}/mem".format(pid)

        start_addr = None
        end_addr = None

        with open(maps_path, "r") as f:
            for line in f:
                if "[heap]" in line:
                    # Adres hissəsini götür: "00c61000-00c82000"
                    addrs = line.split().split('-')
                    start_addr = int(addrs, 16)
                    end_addr = int(addrs, 16)
                    break

        if start_addr is None:
            return

        # 3. Yaddaşda axtarış və dəyişiklik
        with open(mem_path, "rb+") as f:
            f.seek(start_addr)
            heap_data = f.read(end_addr - start_addr)

            # Stringi ASCII baytlar kimi tapırıq
            try:
                offset = heap_data.index(search_str.encode('ascii'))
            except ValueError:
                return # Tapılmasa heç nə etmə

            # Tam ünvana get və yeni stringi yaz
            f.seek(start_addr + offset)
            # VACİB: Yazarkən replace_str-in sonuna NULL byte (\x00) qoyulmalıdır
            f.write(replace_str.encode('ascii') + b'\x00')

    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    solve()
