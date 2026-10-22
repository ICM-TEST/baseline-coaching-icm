"""drive.py — reach the client's Drive folder through rclone.   Ross only.

Kyle's records are Google Docs (his phone can edit a Doc, not a plain file). On a
computer a Doc is only a link stub, so the tools never read the Drive-for-Desktop
copy of a record. Instead:

    pull     rclone copies the folder, Docs exported as plain text, into a
             temporary mirror; normalise() turns the export back into the
             markdown the agent wrote. The tools read the mirror.
    push     generated files (_index/, FILE-MAP.md, _release.md) go back up as
             plain .md files — the agent only reads those, never edits them.

Set up once (setup/onboarding.md § 1b): an rclone remote whose root is the data
folder, e.g. `kyle:`. Then pass `--from-drive kyle:` to validate, build-indexes or
release. ICM_RCLONE overrides the rclone command (the selftest uses a fake).
Stdlib only.
"""
from __future__ import annotations

import contextlib
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

# Files Kyle's agent edits in place. They must be Docs, or the phone can't change them.
EDITED = re.compile(r"^clients/[^/]+/(client\.md|log\.md|programme\.md|incidents/[^/]+\.md)$")


class DriveError(Exception):
    pass


def _rclone() -> list[str]:
    return shlex.split(os.environ.get("ICM_RCLONE", "rclone"))


def _run(*args: str) -> None:
    try:
        p = subprocess.run([*_rclone(), *args], capture_output=True, text=True)
    except FileNotFoundError:
        raise DriveError("rclone is not installed — see setup/onboarding.md § 1b") from None
    if p.returncode:
        tail = (p.stderr or p.stdout).strip().splitlines()[-5:]
        raise DriveError(f"rclone {args[0]} failed:\n  " + "\n  ".join(tail))


def join(remote: str, relpath: str) -> str:
    return remote + ("" if remote.endswith((":", "/")) else "/") + relpath


def clean(text: str) -> str:
    """A Google Docs plain-text export → the text the agent wrote.
    Drops the byte-order mark, Windows line ends and non-breaking spaces, and the
    extra blank line Docs adds between paragraphs."""
    text = text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n").replace(" ", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"


def normalise(root: Path) -> list[tuple[str, str, str, str]]:
    """Rename each exported Doc `<name>.md.txt` → `<name>.md` with clean() text.
    Returns findings as (level, code, path, message)."""
    root = Path(root)
    found: list[tuple[str, str, str, str]] = []
    docs: set[str] = set()
    for p in sorted(root.rglob("*.txt")):
        rel = p.relative_to(root).as_posix()
        if not p.name.endswith(".md.txt"):
            found.append(("warning", "doc-title", rel,
                          "a .txt file, or a Doc whose title doesn't end in .md — records are Docs titled <name>.md"))
            continue
        target = p.with_name(p.name[:-4])
        trel = target.relative_to(root).as_posix()
        if target.exists():
            found.append(("error", "duplicate-file", trel,
                          "a Doc and a plain file share this name — keep the Doc, delete the plain file"))
        target.write_text(clean(p.read_text(encoding="utf-8-sig")), encoding="utf-8")
        p.unlink()
        docs.add(trel)
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if EDITED.match(rel) and rel not in docs:
            found.append(("warning", "not-a-doc", rel,
                          "plain file, not a Google Doc — Kyle's phone can't edit it; open it in Drive → Open with Google Docs, keep the Doc"))
    return found


def pull(remote: str, dest: Path) -> list[tuple[str, str, str, str]]:
    _run("copy", remote, str(dest), "--drive-export-formats", "txt", "--drive-skip-shortcuts")
    return normalise(dest)


@contextlib.contextmanager
def mirror(remote: str):
    """Yield (mirror folder, findings). The mirror is deleted afterwards."""
    tmp = Path(tempfile.mkdtemp(prefix="icm-drive-"))
    try:
        yield tmp, pull(remote, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def push(remote: str, files: dict[str, str]) -> None:
    """Upload {path relative to the data root: content} as plain files (no Doc conversion)."""
    tmp = Path(tempfile.mkdtemp(prefix="icm-push-"))
    try:
        for relpath, content in files.items():
            src = tmp / relpath
            src.parent.mkdir(parents=True, exist_ok=True)
            src.write_text(content, encoding="utf-8")
        for relpath in files:
            _run("copyto", str(tmp / relpath), join(remote, relpath))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
