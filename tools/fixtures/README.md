# fixtures — invented data only

`selftest.py` builds two roots from these:

- **structure** = a copy of `workspace/` with any remaining `{{FILL}}` replaced.
- **data** = a copy of `data/`, standing in for a client's Drive folder: marked with
  `_coaching-workspace.md`, settings filled in `_settings/` (invented courts
  `test-court-a` and `-b`, the ball-colour levels).

Every person here is invented (`alex-example`, `sam-sample`, `jo-placeholder`) and
every number is a fake `+27 00 …`. **Never put a real client in here** — this
folder is in git.

| Fixture | Exists to prove |
|---|---|
| `alex-example` | a complete, valid record — with an incident and an agreement |
| `sam-sample` | archived: drops out of the roster, folder stays |
| `jo-placeholder` | no phone: flagged in open-items, not skipped silently |
| `_requests/2026-10-10-group-bookings.md` | an open request shows up for Ross |
| `_requests/2026-10-12-note-court-keys.md` | a note for Ross shows up, marked as a note |

`fake-rclone.py` stands in for rclone (via `ICM_RCLONE`) so the `--from-drive` path
is tested without Google: `selftest.py` turns `data/` into the shape rclone sees —
each record a Doc exported as `<name>.md.txt`, with Docs' export noise.
