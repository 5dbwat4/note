import sys
import json

def _skip_escape(data, i):
    while i < len(data) and not data[i].isalpha():
        i += 1
    if i < len(data):
        i += 1
    return i


def required_height(stream):
    first_line = stream.readline().strip()
    header = json.loads(first_line)
    width = header["width"]

    col = 0
    row = 0
    max_row = 0
    in_escape = False

    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(entry, list) or len(entry) < 3 or entry[1] != "o":
            continue

        data = entry[2]
        i = 0
        n = len(data)

        if in_escape:
            i = _skip_escape(data, 0)
            if i < n and data[i - 1].isalpha():
                in_escape = False

        while i < n:
            ch = data[i]

            if ch == '\x1b':
                i = _skip_escape(data, i + 1)
                if i >= n or not data[i - 1].isalpha():
                    in_escape = True
                continue

            elif ch == '\n':
                row += 1
                col = 0
                max_row = max(max_row, row)
                i += 1

            elif ch == '\r':
                col = 0
                i += 1

            elif ch == '\b':
                if col > 0:
                    col -= 1
                i += 1

            elif ch == '\t':
                while True:
                    col += 1
                    if col == width:
                        col = 0
                        row += 1
                        max_row = max(max_row, row)
                    if col % 8 == 0:
                        break
                i += 1

            else:
                col += 1
                if col == width:
                    col = 0
                    row += 1
                    max_row = max(max_row, row)
                i += 1

    return max_row + 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            h = required_height(f)
    else:
        h = required_height(sys.stdin)
    print(h)