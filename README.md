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
| **Structure** | `workspace/` in the instance repo — **public**, attached to the client's Claude project as knowledge | the client's Claude; anyone, since it's public — so it never holds client data or settings | Ross only — the client is not a collaborator |
| **Data** | the client's own Google Drive folder, any name, marked by `_coaching-workspace.md`; their settings in `_settings/` | the client's Claude (Drive + Docs connectors); Ross sees `_requests/` (Viewer), and the rest through rclone only if the whole folder is shared | the client, through their Claude; Ross's tools write only `_index/`, `FILE-MAP.md`, `_release.md` |

The routing that ties them together is one short block in the client's project
instructions (`setup/project-instructions.md`); it names no folder — the first chat
asks the client for theirs and marks it. Storage doesn't matter; routing does.

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
  PRD's Drive-permission lock, `deploy.py` and the manifest are retired; the client
  owns their data.
- **The lock is a public instance repo** (22 Oct 2026). Claude's GitHub link lets
  only an org's owners use its private repos, so read-only private access is
  impossible; a public repo needs none, and only Ross can write it.
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
  one plain reason line (what is fixed, never how to get around it), then an offer
  to log a request to update the system (`workspace/CLAUDE.md`; reason lines in
  `workspace/_system/conventions.md` § Error 500 reasons).
- **The client names their own folder** (28 Oct 2026). First-run setup asks for it
  and leaves `_coaching-workspace.md` in it; every chat finds the folder by that file.
- **Settings are the client's** (28 Oct 2026). Rates and policy, availability, courts,
  travel, clearances, voice and levels live in `drive:/_settings/`, asked for at
  first-run setup and changed by chat (one confirm; a warning before removing a level
  or court in use). The repo keeps only their shapes (`workspace/_templates/settings/`);
  a new *kind* of setting is still Error 500.

## Status

**Phase 0 + Phase 1 core + safeguarding, template v0.2.0.** `selftest.py` passes
75/75; `node tools/request-alerts.test.js tools/request-alerts.gs` 12/12. Every
answer only Ross can supply for an instance is `{{FILL: …}}` (policies, scheduled
tasks); a release refuses while any remain. The client's own settings read
`(not set)` until they answer, and never block a release. Next:
`setup/onboarding.md` for Kyle.
