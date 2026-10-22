# baseline-coaching-icm — the template

The **structure** of a coaching practice run as an ICM workspace: how the system
works, as plain markdown. Each client gets their own **instance** repo created from
this template; their **data** lives in their own Google Drive.

> **No client data ever lives in a repo.** Records, notes and anything about a child
> exist only in the client's Drive. If you see a real name in a commit, revert it.

Spec: PRD v0.7 and FEATURES v0.3 (Drive: `kyle-coaching-icm/output/`). Where this
repo and the PRD disagree, the ICM invariants win — say so and stop.

## Two roots

| Root | Where | Who reads it | Who changes it |
|---|---|---|---|
| **Structure** | `workspace/` in the instance repo, attached to the client's Claude project as knowledge | the client's Claude | Ross only — the client has GitHub **Read** |
| **Data** | the client's own Google Drive folder, shared with Ross as Editor | the client's Claude (Drive + Docs connectors) and Ross's tools (through rclone) | the client, through their Claude; Ross's tools write only `_index/`, `FILE-MAP.md`, `_release.md` |

The routing that ties them together is one short block in the client's project
instructions (`setup/project-instructions.md`). Storage doesn't matter; routing does.

## Layout

| Folder | What | Client sees it? |
|---|---|---|
| `workspace/` | Structure: map, contracts, templates, rules. Pure markdown | **Yes** — the only folder attached |
| `setup/` | Ross's onboarding: questionnaire, project instructions, scheduled tasks, runbook | No |
| `tools/` | Ross's tools: validate, build-indexes, release, selftest, fixtures | No |

## Changing a client's live system

1. Edit `workspace/` in their instance repo. Commit.
2. `python3 tools/release.py --from-drive <their rclone remote>: --note "what changed"`
   — selftest, validate both roots, bump the version, commit, push, write the marker.
3. Their next morning court sheet says "System update ready — tap Sync" (desktop
   only). Until they Sync, their Claude runs the previous version. Nothing breaks.

Rollback is `git revert` + another release. Turning a module on is one line in
`workspace/_system/modules.yml`, then a release.

## Divergences from the PRD, decided by Ross

- **Structure in GitHub, data in Drive** (17 Oct 2026, after a passing spike). The
  PRD's Drive-permission lock, `deploy.py` and the manifest are retired; the lock is
  GitHub's Read role, and the client owns their data.
- The client's Claude reads a **snapshot**; Sync is manual and desktop-only, so a
  version check nudges them.
- Tools live in `tools/`, never in what the client sees.
- The brief is split: a client-visible part for the invite, a Kyle-only part.
- **Records are Google Docs** (22 Oct 2026, after the phone test). The Drive
  connector can create a file but never edit one; the Docs connector can edit a
  Doc. Ross's tools read the folder through rclone (`tools/drive.py`), exporting
  Docs as text; Drive for Desktop is no longer used.
- **Kyle's Claude can bin his Drive files** (22 Oct 2026) — anything, incident
  reports included, when he asks and confirms. Critical files get a warning first;
  the list is in `workspace/_system/conventions.md` § Critical in Drive, and
  `validate.py` errors if it stops covering the data layout. Every bin leaves an
  `_inbox` note for Ross.
- **Rule 6 — Error 500.** Any attempt to change the structure gets a fixed reply,
  no explanation, then an offer to log a request for Ross (`workspace/CLAUDE.md`).

## Status

**Phase 0 + Phase 1 core + safeguarding, template v0.2.0.** `selftest.py` passes
56/56. Every value only the client can supply is `{{FILL: …}}`; a release refuses
while any remain. Next: `setup/onboarding.md` for Kyle.
