#!/usr/bin/python3
"""
Locates and replaces a string in the heap of a running process.
"""

import sys
import os


def print_error_and_exit(msg):
    """Prints error message and exits with status 1."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def read_write_heap():
    """Main function to perform heap manipulation."""
    if len(sys.argv) != 4:
        print_error_and_exit("Usage: read_write_heap.py pid search_string replace_string")

    pid = sys.argv
    search_str = sys.argv
    replace_str = sys.argv

    if not pid.isdigit():
        print_error_and_exit("Error: PID must be a number.")

    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    # 1. Find the heap boundaries
    heap_start = None
    heap_end = None

    try:
        with open(maps_path, 'r') as f_maps:
            for line in f_maps:
                if '[heap]' in line:
                    parts = line.split()
                    addr_range = parts.split('-')
                    heap_start = int(addr_range, 16)
                    heap_end = int(addr_range, 16)
                    break
    except Exception as e:
        print_error_and_exit(f"Error accessing maps for PID {pid}: {e}")

    if heap_start is None:
        print_error_and_exit(f"Error: Could not find heap for PID {pid}")

    print(f"[*] Found heap at: [{hex(heap_start)} - {hex(heap_end)}]")

    # 2. Search and replace in memory
    try:
        with open(mem_path, 'rb+') as f_mem:
            # Move to the start of the heap
            f_mem.seek(heap_start)
            heap_content = f_mem.read(heap_end - heap_start)

            # Find the search string in binary format
            try:
                index = heap_content.index(search_str.encode('ascii'))
            except ValueError:
                print_error_and_exit(f"Error: String '{search_str}' not found in heap.")

            # Calculate absolute offset
            target_addr = heap_start + index
            print(f"[*] Found '{search_str}' at {hex(target_addr)}")

            # 3. Perform the overwrite
            f_mem.seek(target_addr)
            f_mem.write(replace_str.encode('ascii') + b'\0') # Null terminator included
            print(f"[*] Replaced with '{replace_str}'")

    except PermissionError:
        print_error_and_exit("Error: Run as root/sudo to access another process's memory.")
    except Exception as e:
        print_error_and_exit(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    read_write_heap()
