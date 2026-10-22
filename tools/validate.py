#!/usr/bin/env python3
"""validate.py — "what state is the book in?"   Ross only.

Checks the two roots of an ICM instance and changes nothing:

  Structure  the repo's workspace/ — every path a contract names must resolve,
             data paths must be written drive:/…, placeholders are flagged.
  Data       the client's Drive folder — layout, record shapes, closed
             vocabularies, reserved names, the release marker. Records are
             Google Docs, so read it with --from-drive (tools/drive.py); --data
             is for a local plain-text copy (the selftest fixtures).

    python3 tools/validate.py                          # structure only
    python3 tools/validate.py --data "<drive folder>"  # both roots, a local copy
    python3 tools/validate.py --from-drive kyle:       # both roots, live from Drive (rclone)
    python3 tools/validate.py --data … --for-release   # {{FILL}} becomes an error
    python3 tools/validate.py --data … --json

Exit 1 on any error. Stdlib + PyYAML only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
STRUCTURE = REPO / "workspace"

RESERVED = {"CLAUDE.md", "CONTEXT.md", "SKILL.md"}
FILL = "{{FILL"

# ── Data layout (must match workspace/CONTEXT.md § Data folder) ──────────────
DATA_DIRS = {"clients", "library", "_requests", "_inbox", "_index"}   # + live module folders
DATA_FILES = {"FILE-MAP.md", "_release.md"}
RECORD_DIRS = {"sessions", "agreements", "incidents", "output"}
RECORD_FILES = {"client.md", "log.md", "programme.md"}
LIBRARY_DIRS = {"drills", "programmes", "courts", "notes"}
MODULE_OUTPUT_DIRS = {"01_schedule": {"briefs", "messages", "court-sheets"}}

# Closed vocabularies — must match workspace/_system/schema.md.
VOCAB = {
    "client": {
        "status": {"trial", "active", "paused", "dormant", "archived"},
        "cadence": {"weekly", "fortnightly", "block", "ad-hoc"},
        "duration": {30, 45, 60, 90},
        "rate-unit": {"per-hour", "per-session", "package"},
        "media-consent": {"yes", "no", "unknown"},
    },
    "incident": {
        "type": {"injury", "illness", "distress", "behaviour", "altercation",
                 "collection", "other"},
        "severity": {"minor", "first-aid", "medical", "emergency-services"},
        "guardian-told": {"yes", "no", "not-yet"},
    },
    "session": {
        "type": {"private", "semi-private", "group", "match-play", "assessment"},
        "attended": {"yes", "no-show", "cancelled-late", "cancelled-notice", "rain"},
        "charged": {"yes", "no"},
        "source": {"live", "backfill"},
    },
    "programme-assignment": {"status": {"active", "paused", "completed", "abandoned"}},
    "programme-design": {"status": {"active", "draft", "retired"}},
    "request": {"status": {"open", "answered", "done", "declined"}, "kind": {"request", "note"}},
    "message": {"status": {"draft", "sent"}},
}
DERIVED_FIELDS = {"last-session", "next-session", "lessons-owed", "balance"}
REQUIRED = {
    "client": ["client", "name", "status"],
    "incident": ["client", "date", "type", "severity"],
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


# ── results ──────────────────────────────────────────────────────────────────
@dataclass
class Finding:
    level: str      # error | warning | info
    code: str
    path: str
    msg: str


@dataclass
class Report:
    structure: Path
    data: Path | None
    findings: list[Finding] = field(default_factory=list)
    clients: list[dict] = field(default_factory=list)
    requests: list[dict] = field(default_factory=list)
    incidents: list[dict] = field(default_factory=list)
    structure_version: str | None = None
    released_version: str | None = None

    def add(self, level, code, path, msg):
        self.findings.append(Finding(level, code, str(path), msg))

    def count(self, level):
        return sum(1 for f in self.findings if f.level == level)

    @property
    def ok(self):
        return self.count("error") == 0


# ── helpers ──────────────────────────────────────────────────────────────────
def visible(p: Path | str) -> bool:
    name = p if isinstance(p, str) else p.name
    return not name.startswith(".")


def rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def walk(root: Path):
    """Every visible file under root (hidden files and folders skipped)."""
    for p in sorted(root.rglob("*")):
        if p.is_file() and all(visible(x) for x in p.relative_to(root).parts):
            yield p


def _plain(v):
    """YAML 1.1 reads bare yes/no as booleans and dates as dates. The schema's
    vocabularies are words — undo both."""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    return v


def read_frontmatter(path: Path):
    """(dict, None) or (None, error). A file with no frontmatter → ({}, None)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, None
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None, "frontmatter is not closed with ---"
    try:
        data = yaml.safe_load(parts[0][3:]) or {}
    except yaml.YAMLError as e:
        return None, f"frontmatter is not valid YAML ({e.__class__.__name__})"
    if not isinstance(data, dict):
        return None, "frontmatter is not a set of fields"
    return {k: _plain(v) for k, v in data.items()}, None


def load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def table_first_column(text: str, heading: str | None = None) -> set[str]:
    """Slugs from the first column of a markdown table (optionally under a ## heading)."""
    if heading:
        m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
        text = m.group(1) if m else ""
    out = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cell = line.strip("|").split("|")[0].strip().strip("`").strip()
        if not cell or set(cell) <= set("-: ") or FILL in cell or " " in cell:
            continue
        out.add(cell)
    return out - {"Slug", "Level"}


def modules_of(structure: Path) -> dict:
    return load_yaml(structure / "_system" / "modules.yml").get("modules") or {}


def live_modules(structure: Path) -> set[str]:
    return {m for m, s in modules_of(structure).items() if (s or {}).get("state") == "live"}


def parse_version(v) -> tuple[int, int, int] | None:
    v = str(v or "").strip()
    return tuple(int(x) for x in v.split(".")) if VERSION_RE.match(v) else None


def version_of(path: Path) -> str | None:
    if not path.exists():
        return None
    fm, _ = read_frontmatter(path)
    return str(fm.get("version")) if fm and fm.get("version") is not None else None


# ── Structure ────────────────────────────────────────────────────────────────
TOKEN = re.compile(r"`([^`\n]+)`")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
PLACEHOLDER = re.compile(r"<[^>]+>|YYYY|MM-DD|HHMM|\{\{")


def path_tokens(text: str):
    """Backticked tokens that look like paths, outside fenced code blocks."""
    for tok in TOKEN.findall(FENCE.sub("", text)):
        tok = tok.strip()
        if " " in tok or "://" in tok and not tok.startswith("drive:/"):
            continue
        if tok.startswith("drive:/"):
            yield tok
        elif "/" in tok.rstrip("/") and not tok[0].isupper():
            yield tok          # multi-segment path; a bare `name/` is a sub-folder named in prose


def check_paths(r: Report):
    """Every path a structure file names must resolve in the right root."""
    s = r.structure
    data_tops = DATA_DIRS | DATA_FILES | set(modules_of(s))
    for f in walk(s):
        if f.suffix != ".md":
            continue
        fp = rel(s, f)
        for tok in path_tokens(f.read_text(encoding="utf-8")):
            if tok.startswith("drive:/"):
                rest = tok[len("drive:/"):].lstrip("/")
                top = rest.split("/", 1)[0]
                if not rest or "…" in rest or PLACEHOLDER.search(top) or top in data_tops:
                    continue
                r.add("error", "bad-data-path", fp, f"`{tok}` — '{top}' is not in the data folder layout")
                continue
            path = tok[len("workspace/"):] if tok.startswith("workspace/") else tok
            if not path or path == "/":
                continue
            target = s / path.rstrip("/")
            if target.exists():
                continue
            top = path.split("/", 1)[0]
            if PLACEHOLDER.search(path) or top in (DATA_DIRS - {"clients", "library"}):
                if not (s / top).exists():
                    r.add("error", "missing-drive-prefix", fp, f"`{tok}` looks like a data path — write `drive:/{path}`")
                    continue
            if PLACEHOLDER.search(path):
                r.add("error", "missing-drive-prefix", fp, f"`{tok}` looks like a data path — write `drive:/{path}`")
            else:
                r.add("error", "missing-path", fp, f"`{tok}` does not exist in Structure")


def critical_required(structure: Path) -> set[str]:
    """Every data path whose loss breaks the system. conventions.md § Critical in
    Drive must list each one, or the agent bins it without a warning."""
    tops = {f"drive:/{d}/" for d in DATA_DIRS - {"_index"}} | {f"drive:/{m}/" for m in live_modules(structure)}
    record = {"drive:/clients/<slug>/"} | {f"drive:/clients/<slug>/{f}" for f in RECORD_FILES} \
        | {f"drive:/clients/<slug>/{d}/" for d in RECORD_DIRS}
    return tops | record | {"drive:/_release.md"}


def check_critical(r: Report):
    conv = r.structure / "_system" / "conventions.md"
    listed = table_first_column(conv.read_text(encoding="utf-8"), "Critical in Drive") if conv.exists() else set()
    for path in sorted(critical_required(r.structure) - listed):
        r.add("error", "critical-list", "_system/conventions.md",
              f"`{path}` is not in § Critical in Drive — Kyle's agent would bin it without a warning")


def check_structure(r: Report, for_release: bool):
    s = r.structure
    if not (s / "CLAUDE.md").exists():
        r.add("error", "no-map", "CLAUDE.md", "structure root has no CLAUDE.md — wrong folder?")
        return
    for f in walk(s):
        if f.suffix not in (".md", ".yml", ".yaml"):
            r.add("error", "not-markdown", rel(s, f), "Structure is markdown and YAML only — tools belong in tools/")
    for mod, spec in modules_of(s).items():
        if not (s / mod / "CONTEXT.md").exists():
            r.add("error", "missing-module", mod, "module in modules.yml has no CONTEXT.md")
        if (spec or {}).get("state") == "live" and not (s / mod / "SKILL.md").exists():
            r.add("error", "missing-module", mod, "live module has no SKILL.md")
    r.structure_version = version_of(s / "_system" / "version.md")
    if not parse_version(r.structure_version):
        r.add("error", "version", "_system/version.md", f"version '{r.structure_version}' is not X.Y.Z")
    targets = list((s / "_shared").glob("*.md")) + [s / "_system" / "policies.md"]
    if s == STRUCTURE:   # the Ross-only setup files that carry instance answers
        targets += [REPO / "setup" / "project-instructions.md", REPO / "setup" / "scheduled-tasks.md"]
    for p in targets:
        if p.exists() and FILL in (t := p.read_text(encoding="utf-8")):
            where = rel(s, p) if p.is_relative_to(s) else rel(s.parent, p)
            r.add("error" if for_release else "warning", "fill", where,
                  f"{t.count(FILL)} placeholder(s) still to answer — setup/questionnaire.md")
    check_paths(r)
    check_critical(r)


# ── Data ─────────────────────────────────────────────────────────────────────
def vocab_check(r: Report, kind: str, fm: dict, path: str):
    for key, allowed in VOCAB[kind].items():
        v = fm.get(key)
        if v in (None, ""):
            continue
        if v not in allowed:
            r.add("error", "vocab", path, f"{key}: '{v}' is not one of {sorted(map(str, allowed))}")
    for key in REQUIRED.get(kind, []):
        if fm.get(key) in (None, ""):
            r.add("error", "missing-field", path, f"{key} is required")


def check_layout(r: Report):
    d, live = r.data, live_modules(r.structure)
    tops = DATA_DIRS | live
    for p in sorted(d.iterdir()):
        if not visible(p):
            continue
        if p.is_dir() and p.name not in tops:
            r.add("error", "invented-folder", p.name, "not in the data folder layout — needs a request, not a folder")
        elif p.is_file() and p.name not in DATA_FILES:
            r.add("error", "stray-file", p.name, "loose file at the top of the data folder — route it to _inbox/")
    missing = sorted(t for t in tops - {"_index"} if not (d / t).is_dir())
    if missing:
        r.add("warning", "setup", "/", f"missing {', '.join(missing)} — run first-run setup (workspace/setup/)")

    for p in walk(d):
        if p.name in RESERVED:
            r.add("error", "reserved-name", rel(d, p), "structure filename inside the data folder — remove it")

    lib = d / "library"
    if lib.is_dir():
        for e in sorted(lib.iterdir()):
            if not visible(e):
                continue
            if e.is_dir() and e.name not in LIBRARY_DIRS:
                r.add("error", "invented-folder", rel(d, e), "library has four shelves: drills, programmes, courts, notes")
            elif e.is_file():
                r.add("warning", "stray-file", rel(d, e), "file directly in library/ — put it on a shelf")
            else:
                for sub in e.iterdir():
                    if sub.is_dir() and visible(sub):
                        r.add("warning", "invented-folder", rel(d, sub), "nested folder on a library shelf")

    for mod in live:
        mdir = d / mod
        if not mdir.is_dir():
            continue
        ok = MODULE_OUTPUT_DIRS.get(mod, set())
        for e in mdir.iterdir():
            if not visible(e):
                continue
            if e.is_dir() and e.name not in ok:
                r.add("error", "invented-folder", rel(d, e), "not an output folder of this module")
            elif e.is_file():
                r.add("warning", "stray-file", rel(d, e), f"file directly in {mod}/ — it belongs in one of {sorted(ok)}")
        msgs = mdir / "messages"
        for m in sorted(msgs.glob("*.md")) if msgs.is_dir() else []:
            fm, err = read_frontmatter(m)
            if err:
                r.add("error", "frontmatter", rel(d, m), err)
            elif fm:
                vocab_check(r, "message", fm, rel(d, m))


def check_clients(r: Report):
    s, d = r.structure, r.data
    curriculum, coach = s / "_shared" / "curriculum.md", s / "_shared" / "coach.md"
    levels = table_first_column(curriculum.read_text(encoding="utf-8")) if curriculum.exists() else set()
    courts = table_first_column(coach.read_text(encoding="utf-8"), "Courts") if coach.exists() else set()
    clients = d / "clients"
    if not clients.is_dir():
        return
    for rec in sorted(clients.iterdir()):
        if not visible(rec):
            continue
        if rec.is_file():
            r.add("error", "stray-file", rel(d, rec), "loose file in clients/ — every client is a folder")
            continue
        for e in sorted(rec.iterdir()):
            if not visible(e) or e.name in RESERVED:
                continue
            if e.is_dir() and e.name not in RECORD_DIRS:
                r.add("error", "invented-folder", rel(d, e), "folder not in the client record shape")
            elif e.is_dir():
                for sub in e.iterdir():
                    if sub.is_dir() and visible(sub):
                        r.add("error", "invented-folder", rel(d, sub), "nested folder inside a record")
            elif e.name not in RECORD_FILES:
                r.add("warning", "stray-file", rel(d, e), "file not in the client record shape — move it into output/ or the log")

        card, cp = rec / "client.md", rel(d, rec / "client.md")
        if not card.exists():
            r.add("error", "missing-card", rel(d, rec), "client folder has no client.md")
            continue
        fm, err = read_frontmatter(card)
        if err:
            r.add("error", "frontmatter", cp, err)
            continue
        vocab_check(r, "client", fm, cp)
        if fm.get("client") and fm["client"] != rec.name:
            r.add("error", "slug-mismatch", cp, f"client: '{fm['client']}' but the folder is '{rec.name}'")
        if fm.get("level") and levels and fm["level"] not in levels:
            r.add("error", "vocab", cp, f"level: '{fm['level']}' is not in _shared/curriculum.md")
        if fm.get("court") and courts and fm["court"] not in courts:
            r.add("error", "vocab", cp, f"court: '{fm['court']}' is not a court in _shared/coach.md")
        for key in ("dob", "started", "media-consent-date"):
            if fm.get(key) and not DATE_RE.match(str(fm[key])):
                r.add("error", "date", cp, f"{key}: '{fm[key]}' is not YYYY-MM-DD")
        for key in ("may-collect", "may-not-collect"):
            if fm.get(key) is not None and not isinstance(fm[key], list):
                r.add("error", "shape", cp, f"{key} must be a list, e.g. [Thandi Moloi]")
        for key in sorted(DERIVED_FIELDS & set(fm)):
            r.add("error", "derived-field", cp, f"{key} is derived — it lives in _index/, never on the card")
        live = fm.get("status") != "archived"
        if live and not fm.get("guardian-phone"):
            r.add("warning", "no-phone", cp, "no phone number — reminders can't be drafted")
        if live and fm.get("media-consent", "unknown") in ("unknown", None, ""):
            r.add("info", "consent-unknown", cp, "media consent unknown — no filming or photos")
        fm["_slug"] = rec.name
        r.clients.append(fm)

        for inc in sorted((rec / "incidents").glob("*.md")) if (rec / "incidents").is_dir() else []:
            ip = rel(d, inc)
            ifm, err = read_frontmatter(inc)
            if err:
                r.add("error", "frontmatter", ip, err)
                continue
            vocab_check(r, "incident", ifm, ip)
            if ifm.get("guardian-told") in ("not-yet", "no"):
                r.add("warning", "guardian-not-told", ip, "incident recorded; guardian not told yet")
            ifm["_path"] = ip
            r.incidents.append(ifm)

        for note in sorted((rec / "sessions").glob("*.md")) if (rec / "sessions").is_dir() else []:
            sp = rel(d, note)
            sfm, err = read_frontmatter(note)
            if err:
                r.add("error", "frontmatter", sp, err)
                continue
            vocab_check(r, "session", sfm, sp)
            if sfm.get("date") and not note.stem.startswith(str(sfm["date"])):
                r.add("warning", "date", sp, "file name and date: field disagree")

        for ag in sorted((rec / "agreements").glob("*.md")) if (rec / "agreements").is_dir() else []:
            afm, err = read_frontmatter(ag)
            if err:
                r.add("error", "frontmatter", rel(d, ag), err)
            elif afm.get("document") and not str(afm["document"]).startswith("vault://"):
                r.add("warning", "vault", rel(d, ag), "signed agreements live in the vault — document: should be a vault:// pointer")

        prog = rec / "programme.md"
        if prog.exists():
            pfm, err = read_frontmatter(prog)
            if err:
                r.add("error", "frontmatter", rel(d, prog), err)
            else:
                vocab_check(r, "programme-assignment", pfm, rel(d, prog))


def check_requests(r: Report):
    req = r.data / "_requests"
    for p in sorted(req.glob("*.md")) if req.is_dir() else []:
        rp = rel(r.data, p)
        fm, err = read_frontmatter(p)
        if err:
            r.add("error", "frontmatter", rp, err)
            continue
        vocab_check(r, "request", fm, rp)
        fm["_path"] = rp
        fm.setdefault("status", "open")
        fm.setdefault("kind", "request")
        r.requests.append(fm)


def check_library(r: Report):
    prog = r.data / "library" / "programmes"
    for p in sorted(prog.glob("*.md")) if prog.is_dir() else []:
        fm, err = read_frontmatter(p)
        if err:
            r.add("error", "frontmatter", rel(r.data, p), err)
        elif fm:
            vocab_check(r, "programme-design", fm, rel(r.data, p))


def check_release(r: Report):
    marker = r.data / "_release.md"
    r.released_version = version_of(marker)
    if r.released_version is None:
        r.add("info", "no-release", "_release.md", "no release marker yet — release.py writes it")
        return
    have, rel_v = parse_version(r.structure_version), parse_version(r.released_version)
    if not rel_v:
        r.add("error", "version", "_release.md", f"version '{r.released_version}' is not X.Y.Z")
    elif have and have > rel_v:
        r.add("warning", "unreleased", "_release.md",
              f"structure is {r.structure_version}, released is {r.released_version} — run release.py")
    elif have and have < rel_v:
        r.add("warning", "repo-behind", "_release.md",
              f"released {r.released_version} is newer than this repo's {r.structure_version} — git pull")


# ── entry points ─────────────────────────────────────────────────────────────
def load_drive():
    """tools/drive.py, loaded by path so this works from any folder."""
    import importlib.util
    if "drive" not in sys.modules:
        spec = importlib.util.spec_from_file_location("drive", Path(__file__).resolve().parent / "drive.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["drive"] = mod
        spec.loader.exec_module(mod)
    return sys.modules["drive"]


def run(structure: Path | str = STRUCTURE, data: Path | str | None = None,
        for_release: bool = False, pre=()) -> Report:
    """`pre`: findings already made about the data, e.g. by drive.normalise()."""
    r = Report(Path(structure).resolve(), Path(data).resolve() if data else None)
    for f in pre:
        r.add(*f)
    check_structure(r, for_release)
    if r.data:
        if not r.data.is_dir():
            r.add("error", "no-data", str(r.data), "data folder not found")
            return r
        check_layout(r)
        check_clients(r)
        check_requests(r)
        check_library(r)
        check_release(r)
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check the structure and data roots of an ICM instance.")
    ap.add_argument("--structure", default=str(STRUCTURE), help="structure root (default: this repo's workspace/)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--from-drive", metavar="REMOTE", help="rclone remote whose root is the data folder, e.g. kyle:")
    src.add_argument("--data", help="a local plain-text copy of the data folder")
    ap.add_argument("--for-release", action="store_true", help="placeholders are errors")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.from_drive:
        drive = load_drive()
        try:
            with drive.mirror(a.from_drive) as (path, pre):
                r = run(a.structure, path, a.for_release, pre)
        except drive.DriveError as e:
            print(f"Could not read Drive — nothing checked.\n{e}")
            return 1
    else:
        r = run(a.structure, a.data, a.for_release)
    return report(r, a.json)


def report(r: Report, as_json: bool) -> int:
    if as_json:
        print(json.dumps({"ok": r.ok, "findings": [f.__dict__ for f in r.findings],
                          "clients": len(r.clients), "structure_version": r.structure_version,
                          "released_version": r.released_version,
                          "open_requests": sum(1 for q in r.requests if q["status"] == "open")}, indent=2))
    else:
        for lvl in ("error", "warning", "info"):
            for f in (x for x in r.findings if x.level == lvl):
                print(f"{lvl.upper():7} {f.code:20} {f.path}: {f.msg}")
        data_line = (f"{len(r.clients)} clients · "
                     f"{sum(1 for q in r.requests if q['status'] == 'open')} open requests · "
                     f"released {r.released_version or '—'}") if r.data else "structure only"
        print(f"\n{r.count('error')} errors · {r.count('warning')} warnings · "
              f"structure {r.structure_version} · {data_line}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())
