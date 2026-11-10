# Schema — record shapes and allowed values

Every record's shape and every allowed value. **A value not listed here is an
error**, not a new option — a new value in a fixed list is a structure change
(`CLAUDE.md` rule 4). Levels and courts are the exception: their lists are the
coach's, in `drive:/_settings/`, changed through `_settings/CONTEXT.md`.

## Reserved names

`CLAUDE.md` · `CONTEXT.md` · `SKILL.md` exist only in Structure. Any of them in
`drive:/` is a violation.

## Folder marker — `drive:/_coaching-workspace.md`

Template: `_templates/coaching-workspace.md`. Exactly one in the coach's Drive, at the
top of the coaching folder; every chat finds `drive:/` by it. `created:` and
`structure-version:` (the version at first-run setup).

## Settings — `drive:/_settings/<name>.md`

Exactly three files, each a Doc made from its template in `_templates/settings/`:
`coach.md`, `rates.md`, `levels.md`. Their sections and columns are fixed by the
template; every value is the coach's. A value not given yet reads `(not set)`.

## Player — `drive:/players/<slug>.md`

Template: `_templates/player.md`. One Doc per player and nothing else in
`drive:/players/`: no folders, no second file for a player.

| Field | Allowed |
|---|---|
| `status` | `trial` · `active` · `paused` · `archived` |
| `level` | a level listed in `drive:/_settings/levels.md` |
| `cadence` | `weekly` · `fortnightly` · `block` · `ad-hoc` |
| `duration` | `30` · `45` · `60` · `90` |
| `court` | a court slug from `drive:/_settings/coach.md` |
| `media-consent` | `yes` · `no` · `unknown` — **unknown means no** |
| `may-collect`, `may-not-collect` | names, may be empty |

The file's four parts, in this order, are fixed: the details block, `## Safeguarding`,
`## Important`, `## Notes`.

## Note — an entry under `## Notes`

`### YYYY-MM-DD` then the coach's words. Added at the end; never edited or merged.

## Incident — an entry under `## Notes`

`### YYYY-MM-DD HH:MM — INCIDENT`, in the shape in `players/SKILL.md` § Incident.
**Never edited**: a correction is a later `— INCIDENT ADDENDUM` entry.

| Field | Allowed |
|---|---|
| `type` | `injury` · `illness` · `distress` · `behaviour` · `altercation` · `collection` · `other` |
| `severity` | `minor` · `first-aid` · `medical` · `emergency-services` |
| `guardian-told` | `yes` · `no` · `not-yet` |

## Calendar linkage

Every event the system creates ends its `description` with one machine line:

```
icm-player: <slug>
```

The agent maps events to players by that line only — never by guessing from the title.
