#!/usr/bin/env python3
"""build-indexes.py — regenerate drive:/_index/ and drive:/FILE-MAP.md   Ross only.

    python3 tools/build-indexes.py --from-drive kyle:   # live from Drive (rclone)
    python3 tools/build-indexes.py --data "<local plain-text copy>"

Writes only generated files into the DATA root: _index/roster.md,
_index/open-items.md, _index/money.md and FILE-MAP.md. Reads the structure
(this repo's workspace/) for vocabularies; never writes to it.
Every file is built in memory first and written only if all of them built — an
index is never left half-written. With --from-drive the files go up as plain .md
(the agent reads them; it never edits them).

On Drive, these files are the navigation layer: one read instead of six. Keep
them current. Stdlib + PyYAML only.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("validate", HERE / "validate.py")
validate = importlib.util.module_from_spec(_spec)
sys.modules["validate"] = validate
_spec.loader.exec_module(validate)

STATUS_ORDER = {"trial": 0, "active": 1, "paused": 2, "dormant": 3}


def stamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def header(title: str, what: str) -> str:
    return (f"# {title} [G]\n\nGenerated {stamp()} by Ross's build-indexes.py. "
            f"Do not edit — change the records, then rebuild.\n\n{what}\n\n")


def cell(v) -> str:
    return str(v).replace("|", "/").replace("\n", " ") if v not in (None, "") else "—"


# ── roster ───────────────────────────────────────────────────────────────────
def build_roster(r) -> str:
    live = [c for c in r.clients if c.get("status") != "archived"]
    archived = len(r.clients) - len(live)
    live.sort(key=lambda c: (STATUS_ORDER.get(c.get("status"), 9), str(c.get("name") or c["_slug"])))
    out = header("Roster", f"{len(live)} current clients · {archived} archived (not listed — their "
                 "folders are still in `clients/`). For resolving names: if a client isn't here, "
                 "it may be newer than this file — search `clients/` for the slug.")
    out += ("No phone numbers, medical or collection details here — they have one home, "
            "the client's own `client.md`.\n\n")
    if not live:
        return out + "_No clients yet._\n"
    out += "| Client | Slug | Status | Level | Usual slot | Court | Guardian | Phone on file |\n"
    out += "|---|---|---|---|---|---|---|---|\n"
    for c in live:
        s = c["_slug"]
        out += (f"| [{cell(c.get('name') or s)}](../clients/{s}/client.md) | `{s}` | {cell(c.get('status'))} "
                f"| {cell(c.get('level'))} | {cell(c.get('default-slot'))} | {cell(c.get('court'))} "
                f"| {cell(c.get('guardian'))} | {'yes' if c.get('guardian-phone') else '**missing**'} |\n")
    return out


# ── open items ───────────────────────────────────────────────────────────────
def build_open_items(r) -> str:
    out = header("Open items", "What needs Kyle or Ross. Rebuilt from the records every run — "
                 "fix the record and the line disappears.")
    sections = []

    errors = [f for f in r.findings if f.level == "error" and f.code != "fill"]
    if errors:
        body = "".join(f"- `{f.path}` — {f.msg}\n" for f in errors)
        sections.append(("Needs fixing — for Ross", body))

    gnt = [f for f in r.findings if f.code == "guardian-not-told"]
    if gnt:
        body = "".join(f"- [{Path(f.path).parent.parent.name}]({'../' + f.path}) — guardian not told yet\n" for f in gnt)
        sections.append(("Incidents waiting on the guardian", body))

    nophone = [f for f in r.findings if f.code == "no-phone"]
    if nophone:
        body = "".join(f"- {Path(f.path).parent.name} — no phone number, so no reminder draft\n" for f in nophone)
        sections.append(("Missing details", body))

    open_req = [q for q in r.requests if q.get("status") in ("open", "answered")]
    if open_req:
        body = "".join(f"- [{Path(q['_path']).stem}](../{q['_path']}) — {'note, ' if q.get('kind') == 'note' else ''}{q['status']}\n" for q in open_req)
        sections.append(("Requests to Ross", body))

    setup = [f for f in r.findings if f.code == "setup"]
    if setup:
        body = "".join(f"- {f.msg}\n" for f in setup)
        sections.append(("Setup still to finish", body))

    if not sections:
        return out + "Nothing open.\n"
    return out + "\n".join(f"## {t}\n\n{b}" for t, b in sections)


# ── money ────────────────────────────────────────────────────────────────────
def build_money(r, modules: dict) -> str:
    state = (modules.get("04_money") or {}).get("state", "dormant")
    if state != "live":
        return header("Money", "Module 04_money is dormant until Phase 4. Nothing is tracked here "
                      "yet — the court sheet shows no money line until it is live.") + "_Not tracking yet._\n"
    return header("Money", "Lessons delivered vs paid, derived from session notes only (rule 1).") + \
        "_Ledger arrives with the Phase 4 build._\n"


# ── file map ─────────────────────────────────────────────────────────────────
def count_md(d: Path) -> int:
    return sum(1 for p in d.glob("*.md")) if d.is_dir() else 0


def build_file_map(r, modules: dict) -> str:
    root = r.data
    out = header("FILE-MAP", "What is in this data folder, in one read. Drive has no cheap "
                 "tree walk — use this, then open the one file you need. How the system works "
                 "is in the project's knowledge, not here.")
    out += (f"Structure version **{r.structure_version or '—'}** · released "
            f"**{r.released_version or '—'}**\n\n")

    clients = sorted(r.clients, key=lambda c: c["_slug"])
    live = sum(1 for c in clients if c.get("status") != "archived")
    out += f"\n## Clients — {live} current, {len(clients) - live} archived\n\n"
    if clients:
        out += "| Slug | Status | Sessions | Agreements | Incidents |\n|---|---|---|---|---|\n"
        for c in clients:
            d = root / "clients" / c["_slug"]
            out += (f"| [`{c['_slug']}`](clients/{c['_slug']}/client.md) | {cell(c.get('status'))} "
                    f"| {count_md(d / 'sessions')} | {count_md(d / 'agreements')} | {count_md(d / 'incidents')} |\n")
    else:
        out += "_No clients yet._\n"

    out += "\n## Library\n\n"
    lib = root / "library"
    for shelf in sorted(validate.LIBRARY_DIRS):
        files = sorted(p.name for p in (lib / shelf).glob("*.md")) if (lib / shelf).is_dir() else []
        shown = ", ".join(f"`{f}`" for f in files[:200]) or "_empty_"
        more = f" … and {len(files) - 200} more" if len(files) > 200 else ""
        out += f"- **{shelf}/** ({len(files)}): {shown}{more}\n"

    out += "\n## Module outputs\n\n"
    for mod, spec in sorted(modules.items()):
        if (spec or {}).get("state") != "live":
            continue
        odir = root / mod
        for sub in sorted(validate.MODULE_OUTPUT_DIRS.get(mod, set())):
            files = sorted(p.stem for p in (odir / sub).glob("*.md")) if (odir / sub).is_dir() else []
            latest = files[-1] if files else "—"
            out += f"- `{mod}/{sub}/` — {len(files)} files, latest `{latest}`\n"

    open_req = sum(1 for q in r.requests if q.get("status") == "open")
    out += f"\n## Requests and inbox\n\n- `_requests/` — {len(r.requests)} total, {open_req} open\n"
    out += f"- `_inbox/` — {count_md(root / '_inbox')} unrouted captures\n"
    return out


# ── write ────────────────────────────────────────────────────────────────────
def build(data: Path | str, structure: Path | str = validate.STRUCTURE) -> dict[str, str]:
    """{path relative to the data root: content} for every generated file. Writes nothing."""
    r = validate.run(structure, data)
    if r.data is None or not r.data.is_dir():
        raise SystemExit(f"data folder not found: {data}")
    modules = validate.modules_of(r.structure)
    return {
        "_index/roster.md": build_roster(r),
        "_index/open-items.md": build_open_items(r),
        "_index/money.md": build_money(r, modules),
        "FILE-MAP.md": build_file_map(r, modules),
    }


def write_all(root: Path | str, files: dict[str, str]) -> None:
    root = Path(root).resolve()
    tmps = []
    try:
        for relpath, content in files.items():
            dest = root / relpath
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_name(f".{dest.name}.tmp")
            tmp.write_text(content, encoding="utf-8")
            tmps.append((tmp, dest))
        for tmp, dest in tmps:
            os.replace(tmp, dest)
    finally:
        for tmp, _ in tmps:
            if tmp.exists():
                tmp.unlink()


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Regenerate the data folder's indexes.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-drive", metavar="REMOTE", help="rclone remote whose root is the data folder, e.g. kyle:")
    src.add_argument("--data", help="a local plain-text copy of the data folder")
    ap.add_argument("--structure", default=str(validate.STRUCTURE))
    a = ap.parse_args(argv)
    if a.from_drive:
        drive = validate.load_drive()
        try:
            with drive.mirror(a.from_drive) as (path, _):
                files = build(path, a.structure)
            drive.push(a.from_drive, files)
        except drive.DriveError as e:
            print(f"Drive error — indexes not updated.\n{e}")
            return 1
    else:
        files = build(a.data, a.structure)
        write_all(a.data, files)
    for p in files:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
