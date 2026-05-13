import sys
import json

def required_height(stream):
    """
    Parse an asciinema recording (JSON lines format) and simulate a terminal
    to determine the total number of lines needed to display all content without scrolling.
    """
    # Read header
    first_line = stream.readline().strip()
    header = json.loads(first_line)
    width = header["width"]

    col = 0          # current cursor column (0-based)
    row = 0          # current cursor row
    max_row = 0      # highest row ever reached

    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Only process output events ("o")
        if not isinstance(entry, list) or len(entry) < 3 or entry[1] != "o":
            continue

        data = entry[2]
        i = 0
        while i < len(data):
            ch = data[i]

            if ch == '\x1b':          # ESC – skip ANSI escape sequences
                i += 1
                # Skip until the terminating letter (a–z or A–Z)
                while i < len(data) and not data[i].isalpha():
                    i += 1
                if i < len(data):
                    i += 1            # skip the terminator letter
                continue

            elif ch == '\n':          # newline
                row += 1
                col = 0
                max_row = max(max_row, row)
                i += 1

            elif ch == '\r':          # carriage return
                col = 0
                i += 1

            elif ch == '\b':          # backspace
                if col > 0:
                    col -= 1
                i += 1

            elif ch == '\t':          # tab – advance to next tab stop (every 8 columns)
                # A tab always advances at least one column, then to a multiple of 8
                while True:
                    col += 1
                    if col == width:          # wrap on reaching right margin
                        col = 0
                        row += 1
                        max_row = max(max_row, row)
                    if col % 8 == 0:
                        break
                i += 1

            else:                     # printable character (including space)
                col += 1
                if col == width:      # line wrap
                    col = 0
                    row += 1
                    max_row = max(max_row, row)
                i += 1

    # Total lines needed = highest row index + 1
    return max_row + 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            h = required_height(f)
    else:
        h = required_height(sys.stdin)
    print(h)