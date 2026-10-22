# fixtures — invented data only

`selftest.py` builds two roots from these:

- **structure** = a copy of `workspace/` with `structure/` laid over it (a filled
  `_shared/coach.md`) and any remaining `{{FILL}}` replaced.
- **data** = a copy of `data/`, standing in for a client's Drive folder.

Every person here is invented (`alex-example`, `sam-sample`, `jo-placeholder`) and
every number is a fake `+27 00 …`. **Never put a real client in here** — this
folder is in git.

| Fixture | Exists to prove |
|---|---|
| `alex-example` | a complete, valid record — with an incident and an agreement |
| `sam-sample` | archived: drops out of the roster, folder stays |
| `jo-placeholder` | no phone: flagged in open-items, not skipped silently |
| `_requests/2026-10-10-group-bookings.md` | an open request shows up for Ross |

`fake-rclone.py` stands in for rclone (via `ICM_RCLONE`) so the `--from-drive` path
is tested without Google: `selftest.py` turns `data/` into the shape rclone sees —
each record a Doc exported as `<name>.md.txt`, with Docs' export noise.
