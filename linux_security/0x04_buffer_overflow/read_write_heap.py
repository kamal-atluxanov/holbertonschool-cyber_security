#!/usr/bin/env python3
"""
A script to find and replace a string in the heap memory of a running process.
"""

import sys


def usage():
    """Print usage message and exit with status code 1."""
    print("Usage: ./read_write_heap.py pid search_string replace_string")
    sys.exit(1)


def read_write_heap(pid, search_string, replace_string):
    """Find and replace a string in the heap of a process."""
    try:
        # Validate PID
        pid = int(pid)
    except ValueError:
        usage()

    # Paths to memory maps and memory
    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    try:
        # Open the memory maps file
        with open(maps_path, "r") as maps_file:
            heap = None
            for line in maps_file:
                if "[heap]" in line:
                    heap = line
                    break

            if not heap:
                sys.exit(1)

            # Extract start and end addresses of the heap
            addr_range = heap.split()
            heap_start, heap_end = [int(x, 16) for x in addr_range.split("-")]

        # Open the memory file for reading and writing
        with open(mem_path, "r+b") as mem_file:
            # Seek to the start of the heap
            mem_file.seek(heap_start)
            # Read heap content
            heap_data = mem_file.read(heap_end - heap_start)

            # Search for the target string
            search_bytes = search_string.encode()
            replace_bytes = replace_string.encode()

            if len(replace_bytes) > len(search_bytes):
                sys.exit(1)

            offset = heap_data.find(search_bytes)
            if offset == -1:
                sys.exit(1)

            # Replace the string
            mem_file.seek(heap_start + offset)
            mem_file.write(replace_bytes.ljust(len(search_bytes), b'\x00'))

    except (PermissionError, FileNotFoundError):
        sys.exit(1)
    except Exception:
        sys.exit(1)


# Main logic
if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()

    p_id = sys.argv
    s_str = sys.argv
    r_str = sys.argv

    read_write_heap(p_id, s_str, r_str)
