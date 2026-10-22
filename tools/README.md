# tools — Ross only, never attached to a client's project

Python 3 with PyYAML. Every tool takes `--data`: the client's Drive folder as Drive
for Desktop syncs it to this Mac (add a shortcut to their shared folder in My Drive).

| Tool | Job |
|---|---|
| `validate.py` | What state is the book in? Checks Structure (every contract path resolves; data paths written `drive:/…`; placeholders) and Data (layout, record shapes, closed vocabularies, reserved names, release marker). Writes nothing. |
| `build-indexes.py` | Rebuilds `drive:/_index/` and `drive:/FILE-MAP.md` from the records. Writes only those four files, atomically. |
| `release.py` | Ships a structure change: clean tree → selftest → validate both roots → bump `version.md` → commit + push → write `drive:/_release.md`. Never touches a record. `--dry-run`, `--rehearsal`. |
| `selftest.py` | 44 cases against invented fixtures, including every refusal path of `release.py` in a throwaway git repo. `release.py` won't run if it fails. |
| `fixtures/` | A fake structure overlay and a fake Drive folder. No real person, ever. |
