#!/usr/bin/env python3
"""selftest.py — prove the tools work before any release.   Ross only.

    python3 tools/selftest.py

Builds two temporary roots from tools/fixtures/ — a filled copy of workspace/ as
Structure and a fake Drive folder as Data — and runs validate.py,
build-indexes.py and release.py against deliberate good and bad states.
Exit 0 only if every case passes. release.py refuses to run if this fails.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import os
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
WS = REPO / "workspace"
TOOLS = REPO / "tools"
FIX = TOOLS / "fixtures"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


validate = load("validate", "validate.py")
indexes = load("build_indexes", "build-indexes.py")
release = load("release", "release.py")

RESULTS: list[tuple[bool, str, str]] = []
CASES = []


def case(name):
    def wrap(fn):
        def run():
            try:
                fn()
                RESULTS.append((True, name, ""))
            except AssertionError as e:
                RESULTS.append((False, name, str(e)))
            except Exception as e:  # a crash is a failure, not a pass
                RESULTS.append((False, name, f"{e.__class__.__name__}: {e}"))
        CASES.append(run)
        return run
    return wrap


def roots() -> tuple[Path, Path]:
    """Fresh (structure, data) in a temp folder: structure filled, data from fixtures
    (a marked folder with Kyle's settings filled in)."""
    tmp = Path(tempfile.mkdtemp(prefix="icm-selftest-"))
    s, d = tmp / "workspace", tmp / "data"
    shutil.copytree(WS, s)
    for p in list(s.rglob("*.md")):
        p.write_text(re.sub(r"\{\{FILL[^}]*\}\}", "fixture", p.read_text()), encoding="utf-8")
    shutil.copytree(FIX / "data", d)
    return s, d


def run(s, d=None, **kw):
    return validate.run(s, d, **kw)


def codes(report, level="error"):
    return [f.code for f in report.findings if f.level == level]


def errors(report):
    return [(f.code, f.path, f.msg) for f in report.findings if f.level == "error"]


def set_field(path: Path, key: str, value: str):
    text = path.read_text()
    new, n = re.subn(rf"^{re.escape(key)}:.*$", f"{key}: {value}", text, count=1, flags=re.M)
    assert n == 1, f"field {key} not found in {path}"
    path.write_text(new)


def stamp_client(d: Path, s: Path, slug: str, name: str) -> Path:
    """Do what clients/SKILL.md says: write the template files, make the four folders."""
    rec = d / "clients" / slug
    rec.mkdir(parents=True)
    for f in ("client.md", "log.md", "programme.md"):
        shutil.copy(s / "_templates" / "client" / f, rec / f)
    for sub in ("sessions", "agreements", "incidents", "output"):
        (rec / sub).mkdir()
    set_field(rec / "client.md", "client", slug)
    set_field(rec / "client.md", "name", name)
    return rec


def tree_hash(root: Path, skip=()) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name not in skip:
            h.update(str(p.relative_to(root)).encode() + p.read_bytes())
    return h.hexdigest()


# ── the repo itself ──────────────────────────────────────────────────────────
@case("repo structure validates with 0 errors (every contract path resolves)")
def _():
    r = run(WS)
    assert r.ok, errors(r)


@case("repo structure is NOT releasable while {{FILL}} remains")
def _():
    assert "fill" in codes(run(WS, for_release=True))


@case("structure is pure markdown/YAML — no scripts in what the client sees")
def _():
    bad = [p for p in validate.walk(WS) if p.suffix not in (".md", ".yml", ".yaml")]
    assert not bad, bad


@case("every module has a contract; the live one has a skill")
def _():
    for mod, spec in validate.modules_of(WS).items():
        assert (WS / mod / "CONTEXT.md").exists(), mod
        if spec.get("state") == "live":
            assert (WS / mod / "SKILL.md").exists(), mod


@case("structure version is X.Y.Z")
def _():
    assert validate.parse_version(validate.version_of(WS / "_system" / "version.md"))


ERROR_500 = (
    "Error 500 - Sorry, this request cannot be carried out",
    "Structure / system files cannot be changed or edited",
    "Structure is safe guarded from breaking or corrupting",
)


@case("rule 6: the three Error 500 replies are in the map, word for word")
def _():
    text = (WS / "CLAUDE.md").read_text()
    for line in ERROR_500:
        assert f"`{line}`" in text, f"missing or reworded in CLAUDE.md: {line}"
    assert "Want me to log a request to update the system?" in text
    assert "§ Error 500 reasons" in text, "rule 6 must point to the reason lines"


@case("rule 6: reason lines live in conventions, one row per kind, never name Ross")
def _():
    text = (WS / "_system" / "conventions.md").read_text()
    assert "## Error 500 reasons" in text, "conventions.md has no § Error 500 reasons"
    section = text.split("## Error 500 reasons", 1)[1].split("\n## ", 1)[0]
    rows = [l for l in section.splitlines() if l.startswith("| ") and not l.startswith("| Kyle")]
    assert len(rows) >= 3, f"expected a reason row per kind, found {len(rows)}"
    assert "Ross" not in section, "a reason line must not say who set it"


@case("rule 6: the replies have one home — no other structure file restates them")
def _():
    for p in validate.walk(WS):
        if p.name == "CLAUDE.md" and p.parent == WS:
            continue
        text = p.read_text()
        for line in ERROR_500:
            assert line not in text, f"{validate.rel(WS, p)} restates: {line}"


@case("rule 6: structure-change routes point to rule 6, feature gaps to rule 5")
def _():
    for f in ("_settings/CONTEXT.md", "_settings/SKILL.md", "clients/CONTEXT.md", "_system/schema.md"):
        assert "rule 6" in (WS / f).read_text(), f
    for f in ("02_sessions/CONTEXT.md", "01_schedule/SKILL.md"):
        assert "rule 5" in (WS / f).read_text(), f


# ── path discipline in contracts ─────────────────────────────────────────────
@case("path check: a contract naming a missing structure file is an error")
def _():
    s, _ = roots()
    p = s / "library" / "CONTEXT.md"
    p.write_text(p.read_text() + "\nSee `_templates/nope.md`.\n")
    assert "missing-path" in codes(run(s))


@case("path check: a data path written without drive:/ is an error")
def _():
    s, _ = roots()
    p = s / "library" / "CONTEXT.md"
    p.write_text(p.read_text() + "\nWrite to `clients/<slug>/log.md`.\n")
    assert "missing-drive-prefix" in codes(run(s))


@case("path check: a drive:/ path outside the data layout is an error")
def _():
    s, _ = roots()
    p = s / "library" / "CONTEXT.md"
    p.write_text(p.read_text() + "\nWrite to `drive:/outputs/x.md`.\n")
    assert "bad-data-path" in codes(run(s))


# ── a filled instance ────────────────────────────────────────────────────────
@case("filled instance is releasable (0 errors with --for-release)")
def _():
    s, d = roots()
    r = run(s, d, for_release=True)
    assert r.ok, errors(r)


@case("instance test: a client written per clients/SKILL.md validates")
def _():
    s, d = roots()
    stamp_client(d, s, "new-player", "New Player")
    r = run(s, d, for_release=True)
    assert r.ok, errors(r)


@case("instance test: an incident written from the template validates")
def _():
    s, d = roots()
    inc = d / "clients" / "alex-example" / "incidents" / "2026-10-02-1700.md"
    shutil.copy(s / "_templates" / "incident.md", inc)
    for k, v in (("client", "alex-example"), ("date", "2026-10-02"), ("type", "illness"),
                 ("severity", "minor"), ("guardian-told", "not-yet")):
        set_field(inc, k, v)
    r = run(s, d)
    assert r.ok, errors(r)
    assert "guardian-not-told" in codes(r, "warning")


@case("first run: an empty data folder is a setup warning, not an error")
def _():
    s, _ = roots()
    empty = s.parent / "empty"
    empty.mkdir()
    r = run(s, empty)
    assert r.ok and "setup" in codes(r, "warning"), errors(r)


@case("archive test: archived client leaves the roster, folder stays")
def _():
    s, d = roots()
    roster = indexes.build(d, s)["_index/roster.md"]
    assert "alex-example" in roster and "jo-placeholder" in roster
    assert "sam-sample" not in roster
    assert (d / "clients" / "sam-sample" / "client.md").exists()


@case("no phone → flagged in open-items, never skipped silently")
def _():
    s, d = roots()
    assert "jo-placeholder" in indexes.build(d, s)["_index/open-items.md"]


@case("open request appears in open-items")
def _():
    s, d = roots()
    assert "2026-10-10-group-bookings" in indexes.build(d, s)["_index/open-items.md"]


@case("a note for Ross appears in open-items, marked as a note")
def _():
    s, d = roots()
    items = indexes.build(d, s)["_index/open-items.md"]
    assert "2026-10-12-note-court-keys](" in items and "— note, open" in items, items


@case("request without kind: (older shape) is still valid and counts as a request")
def _():
    s, d = roots()
    r = run(s, d)
    old = next(q for q in r.requests if "group-bookings" in q["_path"])
    assert old["kind"] == "request" and r.ok, errors(r)


@case("vocab: request kind outside request/note is an error")
def _():
    s, d = roots()
    set_field(d / "_requests" / "2026-10-12-note-court-keys.md", "kind", "memo")
    assert "vocab" in codes(run(s, d))


@case("rule 5: asks the three questions from conventions, word for word, before logging")
def _():
    rule5 = next(l for l in (WS / "CLAUDE.md").read_text().splitlines() if l.startswith("5. "))
    assert "§ Requests" in rule5 and "Send Ross a note" in rule5
    text = (WS / "_system" / "conventions.md").read_text()
    section = text.split("## Requests", 1)[1].split("\n## ", 1)[0]
    for q in ("1. What should the system do?",
              "2. Give me one real example — who, when, what happened.",
              "3. How urgent is it, and what will you do until then?"):
        assert q in section, f"missing or reworded: {q}"
    assert "Ask once" in section and "kind: note" in section


@case("roster never carries phone numbers or medical details")
def _():
    s, d = roots()
    roster = indexes.build(d, s)["_index/roster.md"]
    assert "+27" not in roster and "inhaler" not in roster


@case("indexes land in the data root, atomically, and never touch structure")
def _():
    s, d = roots()
    before = tree_hash(s)
    indexes.write_all(d, indexes.build(d, s))
    assert (d / "_index" / "roster.md").read_text().startswith("# Roster [G]")
    assert (d / "FILE-MAP.md").exists() and not list(d.rglob(".*.tmp"))
    assert tree_hash(s) == before
    assert run(s, d).ok, "data with indexes written must still validate"


# ── deliberate violations in the data folder ─────────────────────────────────
@case("reserved name in a client record is an error")
def _():
    s, d = roots()
    (d / "clients" / "alex-example" / "CONTEXT.md").write_text("# sneaky\n")
    assert "reserved-name" in codes(run(s, d))


@case("reserved name on a library shelf is an error")
def _():
    s, d = roots()
    (d / "library" / "drills" / "SKILL.md").write_text("# sneaky\n")
    assert "reserved-name" in codes(run(s, d))


@case("a copied structure folder at the data root is an error")
def _():
    s, d = roots()
    shutil.copytree(s / "_templates", d / "_templates")
    r = run(s, d)
    assert "invented-folder" in codes(r)


@case("invented folder at the data root is an error")
def _():
    s, d = roots()
    (d / "group-bookings").mkdir()
    assert "invented-folder" in codes(run(s, d))


@case("invented folder inside a record is an error")
def _():
    s, d = roots()
    (d / "clients" / "alex-example" / "videos").mkdir()
    assert "invented-folder" in codes(run(s, d))


@case("invented shelf in the library is an error")
def _():
    s, d = roots()
    (d / "library" / "videos").mkdir()
    assert "invented-folder" in codes(run(s, d))


@case("invented folder in a module's output is an error")
def _():
    s, d = roots()
    (d / "01_schedule" / "invoices").mkdir(parents=True)
    assert "invented-folder" in codes(run(s, d))


@case("a dormant module's folder in Drive is an error")
def _():
    s, d = roots()
    (d / "04_money").mkdir()
    assert "invented-folder" in codes(run(s, d))


@case("vocab: unknown status is an error")
def _():
    s, d = roots()
    set_field(d / "clients" / "alex-example" / "client.md", "status", "superstar")
    assert "vocab" in codes(run(s, d))


@case("vocab: level not in Kyle's levels (drive:/_settings/levels.md) is an error")
def _():
    s, d = roots()
    set_field(d / "clients" / "alex-example" / "client.md", "level", "purple-ball")
    assert "vocab" in codes(run(s, d))


@case("vocab: court not in Kyle's _settings/coach.md is an error")
def _():
    s, d = roots()
    set_field(d / "clients" / "alex-example" / "client.md", "court", "wimbledon")
    assert "vocab" in codes(run(s, d))


@case("vocab: incident severity outside the list is an error")
def _():
    s, d = roots()
    set_field(d / "clients" / "alex-example" / "incidents" / "2026-10-01-1600.md", "severity", "bad")
    assert "vocab" in codes(run(s, d))


@case("vocab: bare yes/no in YAML is read as the word, not a boolean")
def _():
    s, d = roots()
    r = run(s, d)
    alex = next(c for c in r.clients if c["_slug"] == "alex-example")
    assert alex["media-consent"] == "yes" and r.ok, errors(r)


@case("derived field stored on a card is an error")
def _():
    s, d = roots()
    card = d / "clients" / "alex-example" / "client.md"
    card.write_text(card.read_text().replace("status: active", "status: active\nnext-session: 2026-10-20", 1))
    assert "derived-field" in codes(run(s, d))


@case("folder and slug disagree is an error")
def _():
    s, d = roots()
    set_field(d / "clients" / "alex-example" / "client.md", "client", "alex-other")
    assert "slug-mismatch" in codes(run(s, d))


# ── the version check ────────────────────────────────────────────────────────
def marker(d: Path, version: str):
    (d / "_release.md").write_text(release.release_marker(version, "2026-10-17", "fixture"))


@case("version: same version released → no version finding")
def _():
    s, d = roots()
    marker(d, validate.version_of(s / "_system" / "version.md"))
    r = run(s, d)
    assert not {"unreleased", "repo-behind"} & set(codes(r, "warning")), r.findings


@case("version: repo newer than released → 'unreleased' warning")
def _():
    s, d = roots()
    marker(d, "0.0.1")
    assert "unreleased" in codes(run(s, d), "warning")


@case("version: released newer than repo → 'repo-behind' warning")
def _():
    s, d = roots()
    marker(d, "99.0.0")
    assert "repo-behind" in codes(run(s, d), "warning")


# ── release.py, in a throwaway git repo ──────────────────────────────────────
def git_repo() -> tuple[Path, Path]:
    """A throwaway repo whose workspace/ is a filled structure, plus a data folder."""
    s, d = roots()
    repo = s.parent / "repo"
    repo.mkdir()
    shutil.move(str(s), repo / "workspace")
    shutil.copytree(TOOLS, repo / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@example.com"],
                ["config", "user.name", "selftest"], ["add", "-A"], ["commit", "-q", "-m", "init"]):
        subprocess.run(["git", "-C", str(repo), *cmd], check=True, capture_output=True)
    return repo, d


def do_release(repo, d, **kw):
    kw.setdefault("push", False)
    kw.setdefault("run_selftest", False)
    kw.setdefault("today", "2026-10-18")
    return release.release(repo, d, kw.pop("note", "selftest release"), log=lambda *_: None, **kw)


@case("release dry-run changes nothing anywhere")
def _():
    repo, d = git_repo()
    before = (tree_hash(repo, skip={"index"}), tree_hash(d))
    do_release(repo, d, dry_run=True)
    assert (tree_hash(repo, skip={"index"}), tree_hash(d)) == before


@case("release bumps version.md, commits, writes the marker — and then validates clean")
def _():
    repo, d = git_repo()
    old = validate.version_of(repo / "workspace" / "_system" / "version.md")
    new = do_release(repo, d, part="minor", note="Adds blackout dates")
    assert new == release.bump(old, "minor")
    assert validate.version_of(repo / "workspace" / "_system" / "version.md") == new
    assert validate.version_of(d / "_release.md") == new
    assert "Adds blackout dates" in (repo / "workspace" / "_system" / "version.md").read_text()
    log = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%s"], capture_output=True, text=True).stdout
    assert log.strip() == f"Release v{new}", log
    r = run(repo / "workspace", d, for_release=True)
    assert r.ok and not {"unreleased", "repo-behind"} & set(codes(r, "warning")), errors(r)


@case("release never touches a client record")
def _():
    repo, d = git_repo()
    before = tree_hash(d / "clients"), tree_hash(d / "library"), tree_hash(d / "_requests")
    do_release(repo, d)
    assert (tree_hash(d / "clients"), tree_hash(d / "library"), tree_hash(d / "_requests")) == before


@case("release refuses with uncommitted changes, and changes nothing")
def _():
    repo, d = git_repo()
    (repo / "workspace" / "CLAUDE.md").write_text("# edited, not committed\n")
    before = tree_hash(d)
    try:
        do_release(repo, d)
        raise AssertionError("released a dirty tree")
    except release.Refused:
        pass
    assert tree_hash(d) == before


@case("release refuses {{FILL}} placeholders unless --rehearsal")
def _():
    repo, d = git_repo()
    p = repo / "workspace" / "_system" / "policies.md"
    p.write_text(p.read_text() + "\n{{FILL: a question}}\n")
    subprocess.run(["git", "-C", str(repo), "commit", "-qam", "fill"], check=True)
    try:
        do_release(repo, d)
        raise AssertionError("released with placeholders")
    except release.Refused:
        pass
    assert do_release(repo, d, rehearsal=True)


@case("release refuses when the data folder has errors")
def _():
    repo, d = git_repo()
    (d / "clients" / "alex-example" / "CONTEXT.md").write_text("x")
    try:
        do_release(repo, d)
        raise AssertionError("released over a broken data folder")
    except release.Refused:
        pass
    assert not (d / "_release.md").exists()


# ── Kyle's folder and settings: found by a marker, values in his Drive ───────
@case("folder: the map finds drive:/ by the marker, and the project instructions name no folder")
def _():
    claude = (WS / "CLAUDE.md").read_text()
    assert "`_coaching-workspace.md`" in claude and "setup/CONTEXT.md" in claude
    block = (REPO / "setup" / "project-instructions.md").read_text().split("```")[1]
    assert "FILL" not in block and "named" not in block, block
    assert "workspace/CLAUDE.md" in block


@case("folder: the map stays within 60 lines")
def _():
    n = len((WS / "CLAUDE.md").read_text().splitlines())
    assert n <= 60, f"CLAUDE.md is {n} lines"


@case("folder: first run asks Kyle for his folder's name and writes the marker")
def _():
    skill = (WS / "setup" / "SKILL.md").read_text()
    assert "What did you name your coaching folder in Google Drive?" in skill
    assert "`_templates/coaching-workspace.md`" in skill and (WS / "_templates" / "coaching-workspace.md").exists()


@case("folder: no marker is a setup warning that names it")
def _():
    s, d = roots()
    (d / "_coaching-workspace.md").unlink()
    r = run(s, d)
    assert r.ok and any(f.code == "setup" and "_coaching-workspace.md" in f.msg for f in r.findings), errors(r)


@case("settings: the fixture's filled settings give no settings findings")
def _():
    s, d = roots()
    r = run(s, d)
    assert not [f for f in r.findings if f.code.startswith("settings")], [(f.code, f.msg) for f in r.findings]


@case("settings: a file fresh from its template warns (not set), never errors")
def _():
    s, d = roots()
    shutil.copy(WS / "_templates" / "settings" / "rates.md", d / "_settings" / "rates.md")
    r = run(s, d, for_release=True)
    assert r.ok and "settings-unset" in codes(r, "warning"), errors(r)


@case("settings: a missing file is a setup warning")
def _():
    s, d = roots()
    (d / "_settings" / "voice.md").unlink()
    r = run(s, d)
    assert r.ok and any(f.code == "setup" and "voice.md" in f.path for f in r.findings), errors(r)


@case("settings: a fifth file in _settings/ is an error")
def _():
    s, d = roots()
    (d / "_settings" / "holidays.md").write_text("---\nsetting: holidays\n---\n")
    assert "stray-file" in codes(run(s, d))


@case("settings: a file whose setting: doesn't match its name is an error")
def _():
    s, d = roots()
    set_field(d / "_settings" / "levels.md", "setting", "rates")
    assert "settings-shape" in codes(run(s, d))


@case("settings: the templates are exactly the four files validate expects")
def _():
    s, _ = roots()
    (s / "_templates" / "settings" / "holidays.md").write_text("x")
    assert "settings-shape" in codes(run(s))


@case("settings: a template carrying {{FILL}} is an error — it gets copied into Drive")
def _():
    s, _ = roots()
    p = s / "_templates" / "settings" / "voice.md"
    p.write_text(p.read_text() + "\n{{FILL: a question}}\n")
    assert "fill" in codes(run(s))


@case("settings: a level Kyle adds becomes valid on a client card")
def _():
    s, d = roots()
    lv = d / "_settings" / "levels.md"
    lv.write_text(lv.read_text().rstrip("\n") + "\n| `intermediate` | Kyle's own |\n")
    set_field(d / "clients" / "alex-example" / "client.md", "level", "intermediate")
    r = run(s, d)
    assert r.ok, errors(r)


@case("settings: changing a level or rate is Kyle's, not Error 500")
def _():
    conv = (WS / "_system" / "conventions.md").read_text()
    section = conv.split("## Error 500 reasons", 1)[1].split("\n## ", 1)[0]
    assert "a level, a court" not in section and "change a rate" not in section
    assert "`_settings/CONTEXT.md`" in section
    rule6 = next(l for l in (WS / "CLAUDE.md").read_text().splitlines() if l.startswith("6. "))
    assert "rate" not in rule6 and "level" not in rule6, rule6


@case("critical list: the marker and _settings/ are on it")
def _():
    s, _ = roots()
    for path in ("drive:/_coaching-workspace.md", "drive:/_settings/"):
        s2, _ = roots()
        drop_critical_row(s2, path)
        r = run(s2)
        assert any(f.code == "critical-list" and path in f.msg for f in r.findings), (path, errors(r))


# ── Deleting: the critical-file list must cover the data layout ─────────────
def drop_critical_row(s: Path, path: str):
    conv = s / "_system" / "conventions.md"
    text = conv.read_text()
    new = re.sub(rf"^\| `{re.escape(path)}` \|.*\n", "", text, count=1, flags=re.M)
    assert new != text, f"no row for {path}"
    conv.write_text(new)


@case("critical list: the workspace's list covers the whole data layout")
def _():
    s, d = roots()
    assert "critical-list" not in codes(run(s)), errors(run(s))


@case("critical list: incidents missing from it is an error")
def _():
    s, d = roots()
    drop_critical_row(s, "drive:/clients/<slug>/incidents/")
    r = run(s)
    assert any(f.code == "critical-list" and "incidents" in f.msg for f in r.findings), errors(r)


@case("critical list: a live module missing from it is an error")
def _():
    s, d = roots()
    drop_critical_row(s, "drive:/01_schedule/")
    assert "critical-list" in codes(run(s)), errors(run(s))


# ── Drive through rclone (tools/drive.py) ────────────────────────────────────
drive = validate.load_drive()
GENERATED = {"_release.md", "FILE-MAP.md"}


def export_noise(text: str) -> str:
    """What a Google Docs plain-text export does to the agent's text."""
    return "﻿" + text.replace("\n\n", "\n\n\n").replace("\n", "\r\n").rstrip("\r\n")


def as_drive(d: Path) -> Path:
    """The data folder as rclone sees Drive: every record a Doc (`x.md.txt`),
    generated files plain. Returns the fake Drive root."""
    fake = d.parent / "fake-drive"
    shutil.copytree(d, fake)
    for p in sorted(fake.rglob("*.md")):
        relp = p.relative_to(fake).as_posix()
        if relp in GENERATED or relp.startswith("_index/"):
            continue
        p.with_name(p.name + ".txt").write_text(export_noise(p.read_text()), encoding="utf-8")
        p.unlink()
    return fake


@contextlib.contextmanager
def fake_rclone(fake: Path, fail=False):
    env = {"ICM_RCLONE": f"{sys.executable} {TOOLS / 'fixtures' / 'fake-rclone.py'}",
           "FAKE_DRIVE": str(fake), **({"FAKE_RCLONE_FAIL": "1"} if fail else {})}
    old = {k: os.environ.get(k) for k in (*env, "FAKE_RCLONE_FAIL")}
    os.environ.update(env)
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = fn(*a, **kw)
    return code, out.getvalue()


@case("drive: a Docs export is cleaned back to the text the agent wrote")
def _():
    s, d = roots()
    src = d / "clients" / "alex-example" / "log.md"
    fake = as_drive(d)
    assert (fake / "clients" / "alex-example" / "log.md.txt").exists()
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(fake, tmp, dirs_exist_ok=True)
        found = drive.normalise(Path(tmp))
        got = (Path(tmp) / "clients" / "alex-example" / "log.md").read_text()
        assert not list(Path(tmp).rglob("*.txt")), "exported .txt names left behind"
    assert got == src.read_text().rstrip("\n") + "\n", "export not cleaned back to the original"
    assert not [f for f in found if f[0] == "error"], found


@case("drive: validate --from-drive on the fixture Drive is clean, like --data")
def _():
    s, d = roots()
    want = errors(run(s, d))
    with fake_rclone(as_drive(d)):
        with drive.mirror("fake:") as (path, pre):
            r = run(s, path, pre=pre)
    assert errors(r) == want, errors(r)
    assert len(r.clients) == 3, len(r.clients)
    assert "not-a-doc" not in codes(r, "warning")


@case("drive: a record left as a plain file (not a Doc) is a warning")
def _():
    s, d = roots()
    fake = as_drive(d)
    doc = fake / "clients" / "alex-example" / "log.md.txt"
    (doc.with_name("log.md")).write_text((d / "clients" / "alex-example" / "log.md").read_text())
    doc.unlink()
    with fake_rclone(fake), drive.mirror("fake:") as (path, pre):
        r = run(s, path, pre=pre)
    assert ("not-a-doc", "clients/alex-example/log.md") in [(f.code, f.path) for f in r.findings], r.findings


@case("drive: a Doc and a plain file with the same name is an error")
def _():
    s, d = roots()
    fake = as_drive(d)
    shutil.copy(d / "clients" / "alex-example" / "log.md", fake / "clients" / "alex-example" / "log.md")
    with fake_rclone(fake), drive.mirror("fake:") as (path, pre):
        r = run(s, path, pre=pre)
    assert "duplicate-file" in codes(r), errors(r)


@case("drive: a Doc titled without .md is a warning, not silently dropped")
def _():
    s, d = roots()
    fake = as_drive(d)
    (fake / "_inbox").mkdir(exist_ok=True)
    (fake / "_inbox" / "Untitled document.txt").write_text("hello")
    with fake_rclone(fake), drive.mirror("fake:") as (path, pre):
        r = run(s, path, pre=pre)
    assert "doc-title" in codes(r, "warning"), r.findings


@case("drive: rclone missing or failing → a plain message, exit 1, no traceback")
def _():
    s, d = roots()
    os.environ["ICM_RCLONE"] = "no-such-rclone-binary"
    try:
        code, out = quiet(validate.main, ["--structure", str(s), "--from-drive", "fake:"])
    finally:
        os.environ.pop("ICM_RCLONE")
    assert code == 1 and "rclone is not installed" in out, out
    with fake_rclone(as_drive(d), fail=True):
        code, out = quiet(validate.main, ["--structure", str(s), "--from-drive", "fake:"])
    assert code == 1 and "couldn't connect" in out, out


@case("drive: build-indexes --from-drive uploads the indexes as plain .md, touches nothing else")
def _():
    s, d = roots()
    fake = as_drive(d)
    before = tree_hash(fake)
    with fake_rclone(fake):
        code, out = quiet(indexes.main, ["--from-drive", "fake:", "--structure", str(s)])
    assert code == 0, out
    for f in ("_index/roster.md", "_index/open-items.md", "_index/money.md", "FILE-MAP.md"):
        assert (fake / f).is_file(), f"{f} not uploaded"
    assert "alex-example" in (fake / "_index" / "roster.md").read_text()
    for f in ("_index", "FILE-MAP.md"):
        p = fake / f
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    assert tree_hash(fake) == before, "a record changed"


@case("drive: release --from-drive uploads _release.md")
def _():
    repo, d = git_repo()
    fake = as_drive(d)
    with fake_rclone(fake), drive.mirror("fake:") as (path, pre):
        new = do_release(repo, path, pre=pre,
                         write_marker=lambda m: drive.push("fake:", {"_release.md": m}))
    assert validate.version_of(fake / "_release.md") == new


@case("drive: release whose marker upload fails says so — HALF RELEASED, not 'nothing released'")
def _():
    repo, d = git_repo()

    def broken(_):
        raise drive.DriveError("upload refused")
    try:
        do_release(repo, d, write_marker=broken)
        raise AssertionError("a failed marker upload passed silently")
    except release.MarkerFailed as e:
        assert "committed" in str(e) and "version:" in str(e), e
    assert not (d / "_release.md").exists()


def main() -> int:
    for fn in CASES:
        fn()
    for ok, name, why in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"\n      → {why}" if why else ""))
    failed = sum(1 for ok, *_ in RESULTS if not ok)
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
