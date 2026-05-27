import os
import glob
import json
from io import StringIO

from castc import required_height

workdir = os.path.dirname(os.path.abspath(__file__))
cast_files = glob.glob(os.path.join(workdir, "*.cast"))

for cast_path in cast_files:
    with open(cast_path, "r", encoding="utf-8") as f:
        content = f.read()

    height = required_height(StringIO(content))

    lines = content.splitlines(True)
    header = json.loads(lines[0])
    header["height"] = height
    lines[0] = json.dumps(header) + "\n"

    with open(cast_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"{os.path.basename(cast_path)}: height={height}")
