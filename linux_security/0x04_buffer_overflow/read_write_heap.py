#!/usr/bin/python3
"""
Finds and replaces a string in the heap of a running process.
Usage: ./read_write_heap.py pid search_string replace_string
"""

import sys

def main():
    # 1. Arqument sayını yoxla
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_string = sys.argv
    replace_string = sys.argv

    # Əgər axtarılan string boşdursa, heç nə etmə
    if not search_string:
        return

    try:
        # 2. Maps faylından heap-in koordinatlarını tap
        with open("/proc/{}/maps".format(pid), "r") as maps_file:
            start_addr = None
            end_addr = None
            for line in maps_file:
                if "[heap]" in line:
                    # Format: 00c61000-00c82000 rw-p ... [heap]
                    addr_range = line.split()
                    start_hex, end_hex = addr_range.split('-')
                    start_addr = int(start_hex, 16)
                    end_addr = int(end_hex, 16)
                    break
            
            if start_addr is None:
                return # Heap tapılmasa çıx

        # 3. Mem faylına daxil olub dəyişikliyi et
        with open("/proc/{}/mem".format(pid), "rb+") as mem_file:
            # Heap-i oxu
            mem_file.seek(start_addr)
            heap_content = mem_file.read(end_addr - start_addr)

            # Stringi axtar (ASCII baytlar kimi)
            try:
                index = heap_content.index(search_string.encode('ascii'))
            except ValueError:
                return # Tapılmasa çıx

            # Tapılan yerə qayıt və yeni stringi yaz
            mem_file.seek(start_addr + index)
            mem_file.write(replace_string.encode('ascii'))

    except (PermissionError, ProcessLookupError):
        sys.exit(1)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
