# _settings — Kyle's settings

The facts that change how the system **behaves** for Kyle: what lessons cost and what
happens when one is cancelled, when clients can book him, where he coaches and how
long it takes to get between courts, which clearances he holds, how he sounds in a
message, and which levels exist. The values are Kyle's and live in his Drive, in `drive:/_settings/`;
he sets them at first-run setup and changes them by chat. Which settings exist — the
files, their sections and columns — is Structure.

## Not this?

- A drill, a programme design, a note about a court's lights → `library/CONTEXT.md`.
- A new *kind* of setting — a new file, section or column ("add holiday pricing") →
  `CLAUDE.md` rule 6.
- The settings files don't exist yet → `setup/CONTEXT.md` (first run asks for them).

## Goal

Every rule the agent applies has exactly one home, in Kyle's own words, and Kyle can
change it himself without breaking a client record.

## Inputs

- **Working:** what Kyle says; the one settings file the task needs.
- **Reference:** `_templates/settings/` (the shape of each file), `_system/schema.md`,
  `drive:/_index/roster.md` (which clients use a level or court).

## Outputs

| File | Holds | Read by |
|---|---|---|
| `drive:/_settings/coach.md` | calendar, availability, courts, travel times, clearances | `01_schedule`, `clients` |
| `drive:/_settings/rates.md` | rates, packages, cancellation and no-show policy | `01_schedule`, `clients` |
| `drive:/_settings/voice.md` | how Kyle writes to parents and players | every message draft |
| `drive:/_settings/levels.md` | the closed list of levels | `clients`, `library` |

## Process

Read the one file the task names — with Drive, as for any data file. Never restate a
setting into another file; point to it. A value still `(not set)` when a task needs
it → `SKILL.md` § A value that isn't set. Kyle changes, adds or removes one →
`SKILL.md`.

A setting Kyle states in passing ("I'm charging 500 now") is a change he hasn't
confirmed: ask once, as in `SKILL.md`, before anything acts on it. Never note it
somewhere else instead.

## Human check

Kyle confirms every change once, and gets a ⚠️ warning first if a level or court he
is removing or renaming is still on a client's card.
