#!/usr/bin/python3
"""
Finds and replaces a string in the heap of a running process.
Usage: ./read_write_heap.py pid search_string replace_string
"""

import sys


def usage():
    """Print usage message and exit with status code 1."""
    print("Usage: ./read_write_heap.py pid search_string replace_string")
    sys.exit(1)


def read_write_heap(pid, search_string, replace_string):
    """Find and replace a string in the heap of a process."""
    try:
        pid = int(pid)
    except ValueError:
        usage()

    maps_path = "/proc/{}/maps".format(pid)
    mem_path = "/proc/{}/mem".format(pid)

    try:
        with open(maps_path, "r") as maps_file:
            heap_line = None
            for line in maps_file:
                if "[heap]" in line:
                    heap_line = line
                    break

            if not heap_line:
                sys.exit(1)

            addr = heap_line.split().split("-")
            heap_start = int(addr, 16)
            heap_end = int(addr, 16)

        with open(mem_path, "r+b") as mem_file:
            mem_file.seek(heap_start)
            heap_data = mem_file.read(heap_end - heap_start)

            search_bytes = search_string.encode()
            replace_bytes = replace_string.encode()

            if len(replace_bytes) > len(search_bytes):
                sys.exit(1)

            offset = heap_data.find(search_bytes)
            if offset == -1:
                sys.exit(1)

            mem_file.seek(heap_start + offset)
            # Dəqiq uzunluqda yazırıq, artığını boşluqla (və ya null) doldururuq
            mem_file.write(replace_bytes.ljust(len(search_bytes), b'\x00'))

    except (PermissionError, FileNotFoundError):
        sys.exit(1)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()

    p_id = sys.argv
    s_str = sys.argv
    r_str = sys.argv

    read_write_heap(p_id, s_str, r_str)
