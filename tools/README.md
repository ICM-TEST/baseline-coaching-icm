# tools — Ross only, never attached to a client's project

Python 3 with PyYAML, and rclone. Every tool takes `--from-drive <remote>:` (the
client's Drive folder through rclone — `setup/onboarding.md` § 3) or `--data <folder>`
(a local plain-text copy, e.g. the fixtures).

| Tool | Job |
|---|---|
| `validate.py` | What state is the book in? Checks Structure (every contract path resolves; data paths written `drive:/…`; placeholders) and Data (layout, folder marker, the client's settings, record shapes, closed vocabularies, reserved names, release marker). Writes nothing. |
| `build-indexes.py` | Rebuilds `drive:/_index/` and `drive:/FILE-MAP.md` from the records. Writes only those four files, atomically. |
| `release.py` | Ships a structure change: clean tree → selftest → validate both roots → bump `version.md` → commit + push → write `drive:/_release.md`. Never touches a record. `--dry-run`, `--rehearsal`. |
| `selftest.py` | 75 cases against invented fixtures, including every refusal path of `release.py` in a throwaway git repo. `release.py` won't run if it fails. |
| `fixtures/` | A fake Drive folder — marked, settings filled, three invented clients. No real person, ever. |
| `drive.py` | rclone pull / normalise / push, used by the three tools above. |
| `request-alerts.gs` | Google Apps Script, run in Ross's account: emails him when a request lands (`setup/onboarding.md` § Request alerts). Test: `node tools/request-alerts.test.js tools/request-alerts.gs`. |
