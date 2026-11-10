# _settings — the coach's settings

The facts that change how the system **behaves** for this coach: what lessons cost
and what happens when one is cancelled, when players can book, where the coach works
and how long it takes to get between courts, and which levels exist. **The values are
the coach's.** They live in the coach's own Drive, in `drive:/_settings/`, are set at
first-run setup, and are changed by chat whenever the coach likes — nobody else is
asked. Which settings exist — the files, their sections and columns — is Structure.

## Not this?

- A new *kind* of setting — a new file, section or column ("add holiday pricing") →
  `CLAUDE.md` rule 4.
- The settings files don't exist yet → `setup/CONTEXT.md`.

## Goal

Every rule the agent applies has exactly one home, in the coach's own words, and the
coach can change it without help and without breaking a player's file.

## Inputs

- **Working:** what the coach says; the one settings file the task needs.
- **Reference:** `_templates/settings/` (the shape of each file), `_system/schema.md`.

## Outputs

| File | Holds | Read by |
|---|---|---|
| `drive:/_settings/coach.md` | calendar, availability, courts, travel times | `schedule`, `players` |
| `drive:/_settings/rates.md` | rates, packages, cancellation and no-show policy | `schedule` |
| `drive:/_settings/levels.md` | the list of levels | `players` |

## Process

Read the one file the task names, with Drive. Never restate a setting into another
file; point to it. A value still `(not set)` when a task needs it → `SKILL.md` § A
value that isn't set. The coach changes, adds or removes one → `SKILL.md`.

A setting stated in passing ("I'm charging 500 now") is a change not yet confirmed:
ask once, as in `SKILL.md`, before anything acts on it.

## Human check

The coach confirms every change once, and gets a ⚠️ warning first if a level or court
being removed or renamed is still on a player's file.
