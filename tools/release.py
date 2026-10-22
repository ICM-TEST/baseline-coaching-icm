#!/usr/bin/env python3
"""release.py — ship a structure change to the client.   Ross only.

    python3 tools/release.py --from-drive kyle: --note "what changed" [--bump minor]
    python3 tools/release.py --from-drive kyle: --note … --dry-run
    (--data "<local plain-text copy>" in place of --from-drive: selftest only)

In order, stopping at the first failure:
  1. the git working tree must be clean (commit your edits first)
  2. selftest.py must pass
  3. validate.py --for-release must be clean on both roots
  4. bump workspace/_system/version.md (version, released, one changelog line)
  5. git commit "Release vX.Y.Z" and push
  6. write drive:/_release.md — the client's next court sheet then says "tap Sync"

It writes exactly two files: version.md in the repo and _release.md in the data
folder. It never reads or writes a client record. `--rehearsal` allows {{FILL}}
placeholders, for a test project attached to the template. Stdlib + PyYAML only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("validate", REPO / "tools" / "validate.py")
validate = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("validate", validate)
_spec.loader.exec_module(validate)


class Refused(Exception):
    pass


class MarkerFailed(Exception):
    """The release is committed (and pushed) but _release.md was not written."""


def git(repo: Path, *args, check=True) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and p.returncode:
        raise Refused(f"git {' '.join(args)} failed: {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout.strip()


def bump(version: str, part: str) -> str:
    v = validate.parse_version(version)
    if not v:
        raise Refused(f"current version '{version}' is not X.Y.Z")
    major, minor, patch = v
    return {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0",
            "patch": f"{major}.{minor}.{patch + 1}"}[part]


def stamp_version_md(text: str, new: str, today: str, note: str) -> str:
    text, n1 = re.subn(r"^version:.*$", f"version: {new}", text, count=1, flags=re.M)
    text, n2 = re.subn(r"^released:.*$", f"released: {today}", text, count=1, flags=re.M)
    if not (n1 and n2):
        raise Refused("version.md has no version:/released: frontmatter")
    line = f"- {new} ({today}) — {note}"
    if "## What changed\n" not in text:
        raise Refused("version.md has no '## What changed' section")
    return text.replace("## What changed\n\n", f"## What changed\n\n{line}\n", 1)


def release_marker(new: str, today: str, note: str) -> str:
    return (f"---\nversion: {new}\nreleased: {today}\n---\n\n"
            f"# Release marker\n\nWritten by Ross's release.py. Do not edit.\n\n"
            f"Structure **{new}** is released: {note}\n\n"
            f"If the project's `workspace/_system/version.md` is older than this, the "
            f"snapshot is behind — see its § The version check.\n")


def write_atomic(path: Path, content: str) -> None:
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def release(repo: Path, data: Path, note: str, part: str = "patch", dry_run: bool = False,
            push: bool = True, run_selftest: bool = True, rehearsal: bool = False,
            today: str | None = None, log=print, pre=(), write_marker=None) -> str:
    """Return the new version. Raises Refused and changes nothing on any failed check.
    `pre`: findings from drive.normalise(); `write_marker(text)`: how _release.md is
    written (default: into `data`; --from-drive uploads it instead)."""
    repo, data = Path(repo).resolve(), Path(data).resolve()
    structure = repo / "workspace"
    today = today or dt.date.today().isoformat()
    note = " ".join(note.split())
    if not note:
        raise Refused("--note is required: one line on what changed")
    if not data.is_dir():
        raise Refused(f"data folder not found: {data}")

    log("1/6 git tree clean …")
    if git(repo, "status", "--porcelain"):
        raise Refused("uncommitted changes — commit or stash them first")

    log("2/6 selftest …")
    if run_selftest:
        st = subprocess.run([sys.executable, "-B", str(repo / "tools" / "selftest.py")],
                            capture_output=True, text=True)
        if st.returncode:
            raise Refused("selftest failed:\n" + st.stdout[-2000:])

    log("3/6 validate both roots …")
    r = validate.run(structure, data, for_release=not rehearsal, pre=pre)
    errors = [f for f in r.findings if f.level == "error"]
    if errors:
        raise Refused("validate failed:\n" + "\n".join(f"  {f.path}: {f.msg}" for f in errors[:20]))

    current = r.structure_version
    if r.released_version and (validate.parse_version(r.released_version) or (0,)) > validate.parse_version(current):
        raise Refused(f"the data folder says {r.released_version} is released, newer than this repo's "
                      f"{current} — git pull first")
    new = bump(current, part)
    vfile = structure / "_system" / "version.md"
    new_text = stamp_version_md(vfile.read_text(encoding="utf-8"), new, today, note)
    marker = release_marker(new, today, note)

    log(f"4/6 version {current} → {new}")
    if dry_run:
        log(f"    WOULD write workspace/_system/version.md, commit 'Release v{new}'"
            + (", push" if push else "") + ", write drive:/_release.md")
        return new
    vfile.write_text(new_text, encoding="utf-8")

    log("5/6 commit" + (" + push" if push else "") + " …")
    try:
        git(repo, "add", "workspace/_system/version.md")
        git(repo, "commit", "-q", "-m", f"Release v{new}\n\n{note}")
    except Refused:
        git(repo, "checkout", "--", "workspace/_system/version.md", check=False)
        raise
    if push:
        git(repo, "push", "-q", "origin", "HEAD")

    log("6/6 release marker …")
    try:
        if write_marker:
            write_marker(marker)
        else:
            write_atomic(data / "_release.md", marker)
    except Exception as e:
        raise MarkerFailed(f"v{new} is committed{' and pushed' if push else ''}, but drive:/_release.md "
                           f"was not written, so the client won't be told to Sync.\n{e}\n"
                           f"Fix the cause, then upload this as drive:/_release.md:\n\n{marker}") from None
    log(f"Released {new}. The client's next court sheet will ask them to Sync.")
    return new


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Release a structure change to the client.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-drive", metavar="REMOTE", help="rclone remote whose root is the data folder, e.g. kyle:")
    src.add_argument("--data", help="a local plain-text copy of the data folder (selftest)")
    ap.add_argument("--note", required=True, help="one line on what changed — the client may read it")
    ap.add_argument("--bump", choices=["patch", "minor", "major"], default="patch")
    ap.add_argument("--dry-run", action="store_true", help="run every check, change nothing")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--rehearsal", action="store_true", help="allow {{FILL}} placeholders (test projects only)")
    a = ap.parse_args(argv)
    kw = dict(push=not a.no_push, rehearsal=a.rehearsal)
    try:
        if a.from_drive:
            drive = validate.load_drive()
            try:
                with drive.mirror(a.from_drive) as (path, pre):
                    release(REPO, path, a.note, a.bump, a.dry_run, pre=pre,
                            write_marker=lambda m: drive.push(a.from_drive, {"_release.md": m}), **kw)
            except drive.DriveError as e:
                raise Refused(f"Drive error: {e}") from None
        else:
            release(REPO, Path(a.data), a.note, a.bump, a.dry_run, **kw)
    except Refused as e:
        print(f"REFUSED — nothing released.\n{e}")
        return 1
    except MarkerFailed as e:
        print(f"HALF RELEASED — {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
