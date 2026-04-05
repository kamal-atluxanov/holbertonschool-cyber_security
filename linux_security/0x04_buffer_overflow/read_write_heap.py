#!/usr/bin/python3
"""
İşləyən prosesin heap sahəsindəki stringi tapan və onu əvəz edən skript.
"""

import sys
import os

def print_usage_and_exit():
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)

def read_write_heap():
    # Arqumentlərin yoxlanılması
    if len(sys.argv) != 4:
        print_usage_and_exit()

    pid = sys.argv
    search_string = sys.argv
    replace_string = sys.argv

    if not pid.isdigit():
        print_usage_and_exit()

    maps_filename = f"/proc/{pid}/maps"
    mem_filename = f"/proc/{pid}/mem"

    # Maps faylını oxuyub heap sahəsini tapmaq
    try:
        with open(maps_filename, 'r') as maps_file:
            for line in maps_file:
                if "[heap]" in line:
                    parts = line.split()
                    addr_range = parts.split('-')
                    start_addr = int(addr_range, 16)
                    end_addr = int(addr_range, 16)
                    break
            else:
                print(f"[*] Heap found no for process {pid}")
                sys.exit(1)
    except Exception as e:
        print(f"[!] Error opening maps file: {e}")
        sys.exit(1)

    print(f"[*] Found heap at: [{hex(start_addr)} - {hex(end_addr)}]")

    # Mem faylını açıb stringi tapmaq və dəyişmək
    try:
        with open(mem_filename, 'rb+') as mem_file:
            # Heap sahəsinə keçid
            mem_file.seek(start_addr)
            heap_data = mem_file.read(end_addr - start_addr)

            # Stringi axtarmaq (ASCII olaraq)
            try:
                index = heap_data.index(search_string.encode('ascii'))
            except ValueError:
                print(f"[!] String '{search_string}' not found in heap.")
                sys.exit(1)

            print(f"[*] Found '{search_string}' at offset {hex(index)}")

            # Yazılacaq ünvanı hesablamaq və dəyişmək
            mem_file.seek(start_addr + index)
            # Yeni stringi və sonuna null byte (\0) əlavə edərək yazırıq
            mem_file.write(replace_string.encode('ascii') + b'\x00')

            print(f"[*] Successfully replaced with '{replace_string}'")

    except Exception as e:
        print(f"[!] Error accessing memory: {e}")
        sys.exit(1)

if __name__ == "__main__":
    read_write_heap()
