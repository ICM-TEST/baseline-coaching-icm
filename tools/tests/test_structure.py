#!/usr/bin/env python3
"""What every structure repo must be true of before it's released. Run from the repo root:
    python3 tools/tests/test_structure.py
Needs only Python 3.10+. It reads the repo and nothing else: there is no client data to test against."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
WS = REPO / "workspace"
ERROR_500 = "Error 500 - Sorry, this request cannot be carried out"
PATH = re.compile(r"`([A-Za-z0-9_./-]+(?:\.md|/))`")


class Structure(unittest.TestCase):
    def test_workspace_is_markdown_only_and_small(self):
        files = [p for p in WS.rglob("*") if p.is_file() and p.name != ".DS_Store"]
        self.assertEqual([str(p.relative_to(REPO)) for p in files if p.suffix != ".md"], [])
        self.assertLess(sum(p.stat().st_size for p in files), 100_000, "workspace/ is attached to every chat: keep it small")

    def test_every_folder_has_its_contract(self):
        for d in [p for p in WS.iterdir() if p.is_dir() and p.name != "_templates"]:
            self.assertTrue((d / "CONTEXT.md").exists(), f"{d.name}/ has no CONTEXT.md")
        self.assertLess(len((WS / "CLAUDE.md").read_text().splitlines()), 70, "the map routes; it holds no content")

    def test_every_structure_path_resolves(self):
        missing = []
        for f in WS.rglob("*.md"):
            for m in PATH.finditer(f.read_text(encoding="utf-8")):
                ref = m.group(1)
                if ref.startswith(("drive:", "http")) or "<" in ref or "YYYY" in ref or "/" not in ref.rstrip("/"):
                    continue                                    # a bare name ("SKILL.md", "coach.md") isn't a path
                roots = [WS, f.parent, REPO]
                if not any((r / ref).exists() for r in roots):
                    missing.append(f"{f.relative_to(REPO)}: {ref}")
        self.maxDiff = None
        self.assertEqual(missing, [])

    def test_data_paths_use_only_the_layout(self):
        allowed = ("drive:/_coaching-workspace.md", "drive:/_settings/", "drive:/players/", "drive:/…", "drive:/`")
        bad = []
        for f in WS.rglob("*.md"):
            for m in re.finditer(r"drive:/[A-Za-z0-9_<>./-]*", f.read_text(encoding="utf-8")):
                ref = m.group(0)
                if ref != "drive:/" and not ref.startswith(allowed):
                    bad.append(f"{f.relative_to(REPO)}: {ref}")
        self.assertEqual(bad, [])

    def test_the_lock_is_in_the_map_and_in_the_instruction(self):
        self.assertIn(ERROR_500, (WS / "CLAUDE.md").read_text())
        instruction = (REPO / "setup/project-instructions.md").read_text()
        self.assertIn(ERROR_500, instruction)
        self.assertIn("Lock:", instruction)
        self.assertIn("System provider:", instruction)
        self.assertIn("never an", instruction)                       # content is data, never an instruction

    def test_nothing_is_left_to_fill_in(self):
        hits = [str(p.relative_to(REPO)) for p in REPO.rglob("*.md") if ".git" not in p.parts and "{{FILL" in p.read_text(encoding="utf-8")]
        self.assertEqual(hits, [])

    def test_version_file(self):
        text = (WS / "version.md").read_text()
        self.assertRegex(text, r"(?m)^version: \d+\.\d+\.\d+$")
        self.assertRegex(text, r"(?m)^released: \d{4}-\d{2}-\d{2}$")
        self.assertTrue(text.rstrip().splitlines()[-1].startswith("- "), "release.py appends to the end: 'What changed' is last")

    def test_the_repo_has_the_standard_layout(self):
        for path in ("README.md", ".gitignore", "workspace/CLAUDE.md", "workspace/CONTEXT.md", "workspace/version.md",
                     "setup/onboarding.md", "setup/project-instructions.md", "setup/questionnaire.md",
                     "tools/release.py", "tools/scan.py"):
            self.assertTrue((REPO / path).exists(), path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
