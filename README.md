# baseline-coaching-icm

A booking and player-notes system for a tennis coach, run as an ICM workspace by chatting to Claude. This repo holds the
**structure**. Each coach's **data** lives in their own Google Drive.

> **No player or coach data ever lives in this repo. It's public.** If you see a real name or phone number in a commit,
> treat it as a leak.

**Claude:** start at [workspace/CLAUDE.md](workspace/CLAUDE.md). Everything outside `workspace/` is Ross's.

## What it does

- **Booking:** book, repeat, reschedule and cancel lessons in the coach's Google Calendar, checking availability and
  travel between courts.
- **Player files:** one Google Doc per player, holding details, safeguarding information and dated coaching notes.
- **Settings the coach owns:** rates, cancellation policy, hours, courts and levels, changed by chat.

It does not send or draft messages, run reminders, invoice, or hold training programmes.

## Two roots

| Root | Where | Who reads it | Who changes it |
|---|---|---|---|
| **Structure** | This repo, public. Its `workspace/` folder is attached to the coach's Claude Project as knowledge | The coach's Claude, and anyone else, so it never holds data | Only Ross |
| **Data** | The coach's own Google Drive folder, shared with nobody | The coach's Claude | The coach |

## Layout

| Folder | What | Who uses it |
|---|---|---|
| `workspace/` | Rules, skills and templates, markdown only. **The only folder attached to a Project** | The coach's Claude |
| `setup/` | Onboarding, the Project instruction, the questionnaire | Ross only |
| `tools/` | `release.py`, `scan.py`, the tests | Ross only |

## Changing the live system

1. Edit, commit.
2. `python3 tools/release.py --note "what changed"` scans for personal data, runs the tests, bumps the version, commits,
   tags `vX.Y.Z` and pushes.
3. Tell the coach to press Sync at a computer (claude.ai → the project → settings → Sync). Until then they run the
   previous version.

The coach asks for a change by contacting Ross directly: their Claude answers a system change with Error 500 and Ross's
contact line.

## Tests

`python3 tools/tests/test_structure.py` and `python3 tools/tests/test_release.py`. Python 3.10+ only.
