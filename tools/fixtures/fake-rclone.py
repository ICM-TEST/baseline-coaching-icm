#!/usr/bin/env python3
"""A stand-in for rclone, for selftest.py only. The remote `fake:` is the folder in
$FAKE_DRIVE, which holds files the way rclone sees Drive: a Google Doc titled
`log.md` arrives as `log.md.txt` (with --drive-export-formats txt).

    copy   fake:[path] DEST   — needs --drive-export-formats txt, like the real tools pass
    copyto SRC fake:path      — upload one file
$FAKE_RCLONE_FAIL=1 makes every call fail, like a lost connection.
"""
import os
import shutil
import sys
from pathlib import Path


def remote(arg: str) -> Path:
    assert arg.startswith("fake:"), f"not a fake remote: {arg}"
    return Path(os.environ["FAKE_DRIVE"]) / arg[len("fake:"):].lstrip("/")


def main(argv):
    if os.environ.get("FAKE_RCLONE_FAIL"):
        print("ERROR : Failed to create file system: couldn't connect", file=sys.stderr)
        return 1
    cmd, src, dest, *flags = argv
    if cmd == "copy":
        if "--drive-export-formats" not in flags or flags[flags.index("--drive-export-formats") + 1] != "txt":
            print("Docs would not be exported as text", file=sys.stderr)
            return 2
        shutil.copytree(remote(src), dest, dirs_exist_ok=True)
    elif cmd == "copyto":
        out = remote(dest)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, out)
    else:
        print(f"fake rclone: unknown command {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
