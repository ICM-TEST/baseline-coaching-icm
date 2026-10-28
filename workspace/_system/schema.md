# Schema — record shapes and allowed values

Every record's shape and every allowed value. Ross's `validate.py` checks the whole
data folder against this file. **A value not listed here is an error**, not a new
option — a new value in a fixed list here is a structure change (`CLAUDE.md`
rule 6). Levels and courts are the exception: their lists are Kyle's, in
`drive:/_settings/`, and he adds to them through `_settings/CONTEXT.md`.

## Reserved names

`CLAUDE.md` · `CONTEXT.md` · `SKILL.md` exist only in Structure. Any of them in
`drive:/` is a violation.

## Placeholder marker

`{{FILL: question}}` — an answer Ross supplies when he sets up an instance
(`_system/policies.md`, his setup files). Allowed in the template repo; never in a
released instance. Kyle's own answers never use it: an unanswered setting in
`drive:/_settings/` reads `(not set)`.

## Folder marker — `drive:/_coaching-workspace.md`

Template: `_templates/coaching-workspace.md`. Exactly one in Kyle's Drive, at the top
of his coaching folder; every chat finds `drive:/` by it. Frontmatter `created:` and
`structure-version:` (the version at first-run setup).

## Settings — `drive:/_settings/<name>.md`

Exactly four files, each a Doc made from its template in `_templates/settings/`:
`coach.md`, `rates.md`, `voice.md`, `levels.md`. Frontmatter `setting:` names the
file. Their sections and columns are fixed by the template; every value is Kyle's.
A value not given yet reads `(not set)`.

## Client — `drive:/clients/<slug>/client.md`

Template: `_templates/client/client.md`. Derived values — last lesson, next lesson,
balance, lessons owed — are **never** stored here; the generated `drive:/_index/`
holds them.

| Field | Allowed |
|---|---|
| `status` | `trial` · `active` · `paused` · `dormant` · `archived` |
| `level` | a level listed in `drive:/_settings/levels.md` |
| `cadence` | `weekly` · `fortnightly` · `block` · `ad-hoc` |
| `duration` | `30` · `45` · `60` · `90` |
| `rate-unit` | `per-hour` · `per-session` · `package` |
| `court` | a court slug from `drive:/_settings/coach.md` |
| `media-consent` | `yes` · `no` · `unknown` — **unknown means no** |
| `may-collect`, `may-not-collect` | lists of names, may be empty |

A record folder holds `client.md`, `log.md`, `programme.md` and the folders
`sessions/`, `agreements/`, `incidents/`, `output/` — nothing else.

## Incident — `drive:/clients/<slug>/incidents/YYYY-MM-DD-HHMM.md`

Template: `_templates/incident.md`. **Append-only**: a correction is a dated addendum
at the bottom, never an edit above it. Never archived; binned only when Kyle asks,
after the warning in `_system/conventions.md` § Deleting from Drive.

| Field | Allowed |
|---|---|
| `type` | `injury` · `illness` · `distress` · `behaviour` · `altercation` · `collection` · `other` |
| `severity` | `minor` · `first-aid` · `medical` · `emergency-services` |
| `guardian-told` | `yes` · `no` · `not-yet` |

## Coaching agreement — `drive:/clients/<slug>/agreements/YYYY-MM-DD.md`

Template: `_templates/agreement.md`. One file per signed agreement; a new agreement
supersedes, never edits. The signed document lives in the vault (`policies.md`);
this file holds a `vault://` pointer. **Never call an agreement a "contract"** — in
this workspace a contract is a `CONTEXT.md`.

## Brief — `drive:/01_schedule/briefs/YYYY-MM-DD-<slug>.md`

Template: `_templates/brief.md`.

## Message draft — `drive:/01_schedule/messages/YYYY-MM-DD-<slug>.md`

Templates: `_templates/messages/reminder.md`, `_templates/messages/reschedule.md`.
`status`: `draft` · `sent`.

## Court sheet — `drive:/01_schedule/court-sheets/YYYY-MM-DD.md`

No template; the shape is in `01_schedule/SKILL.md` § 8.

## Session note — `drive:/clients/<slug>/sessions/YYYY-MM-DD.md`

Template: `_templates/session-note.md`. Module `02_sessions` is dormant; in Phase 1
a note is written only as the stub for a **charged cancellation** (`01_schedule`).

| Field | Allowed |
|---|---|
| `type` | `private` · `semi-private` · `group` · `match-play` · `assessment` |
| `attended` | `yes` · `no-show` · `cancelled-late` · `cancelled-notice` · `rain` |
| `charged` | `yes` · `no` |
| `source` | `live` · `backfill` |

## Programme assignment — `drive:/clients/<slug>/programme.md`

Dormant until Phase 3. `status`: `active` · `paused` · `completed` · `abandoned`.

## Programme design — `drive:/library/programmes/<slug>.md`

`status`: `active` · `draft` · `retired`.

## Request — `drive:/_requests/YYYY-MM-DD-<slug>.md`

No template file; the shape is fixed here:

```
---
date: YYYY-MM-DD
kind: request       # request · note
status: open        # open · answered · done · declined
---
## Kyle asked for
## Example
## How urgent, and meanwhile
## What the system did instead
## Ross's answer
```

A note (`kind: note`, file `YYYY-MM-DD-note-<slug>.md`) has only `## Note` and
`## Ross's answer`.

Kyle's agent writes every section except `## Ross's answer`, asking first as in
`_system/conventions.md` § Requests. Ross writes the answer and the status. An older
request with `## What he was trying to do` and no `kind:` is still valid; `kind`
defaults to `request`.

## Release marker — `drive:/_release.md`

Written only by Ross's `release.py`. Frontmatter `version:` and `released:`, then one
line on what changed. Compared with `_system/version.md` for the version check.

## Calendar linkage

Every event the system creates ends its `description` with one machine line:

```
icm-client: <slug>
```

The agent maps events to clients by that line only — never by guessing from the title.
