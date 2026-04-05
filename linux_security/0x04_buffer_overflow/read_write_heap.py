#!/usr/bin/python3
"""
Locates and replaces a string in the heap of a running process.
Usage: read_write_heap.py pid search_string replace_string
"""

import sys

def read_write_heap():
    """Finds and replaces a string in the heap of a process."""

    # 1. Validation: Check if exactly 3 arguments are passed (plus script name)
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv
    search_string = sys.argv
    replace_string = sys.argv

    # Ensure search string isn't empty
    if search_string == "":
        return

    # 2. Find the heap in /proc/[pid]/maps
    try:
        with open(f"/proc/{pid}/maps", "r") as maps_file:
            heap_start = None
            heap_end = None

            for line in maps_file:
                if "[heap]" in line:
                    # Line format: 555e646e0000-555e64701000 rw-p 00000000 00:00 0 [heap]
                    parts = line.split()
                    addr_range = parts.split('-')
                    heap_start = int(addr_range, 16)
                    heap_end = int(addr_range, 16)
                    break

            if heap_start is None or heap_end is None:
                print(f"Error: [heap] not found for PID {pid}")
                sys.exit(1)

        # 3. Read and Write in /proc/[pid]/mem
        with open(f"/proc/{pid}/mem", "rb+") as mem_file:
            # Move pointer to start of heap and read its content
            mem_file.seek(heap_start)
            heap_data = mem_file.read(heap_end - heap_start)

            # Find the string in the bytes data
            try:
                # Convert search string to bytes
                offset = heap_data.index(bytes(search_string, "ascii"))
            except ValueError:
                print(f"Error: String '{search_string}' not found in heap.")
                sys.exit(1)

            # Move pointer to the exact location where the string was found
            mem_file.seek(heap_start + offset)

            # Write the replacement string (as bytes)
            mem_file.write(bytes(replace_string, "ascii"))

    except PermissionError:
        print("Permission denied: Try running with sudo.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    read_write_heap()
