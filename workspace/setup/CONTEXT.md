# setup — first run

Creates Kyle's data folder layout in his Google Drive the first time, and repairs it
if a top-level folder has gone missing. Runs once; after that the data folder only
grows through the other contracts.

## Not this?

- Creating a client → `clients/CONTEXT.md`.
- Changing rates, courts or anything in `_shared/` → `CLAUDE.md` rule 6.

## Goal

The data folder named in the project instructions holds exactly the layout in
`CONTEXT.md` § Data folder, every folder owned by Kyle.

## Inputs

- **Working:** the Drive folder named in the project instructions.
- **Reference:** `CONTEXT.md` § Data folder (the layout), `_system/schema.md`.

## Outputs

Empty folders under `drive:/` and one `drive:/_inbox/` note saying setup ran.
Never a client record, never a `drive:/_index/` file, never `drive:/_release.md` — those come from
Kyle or Ross.

## Process

`SKILL.md`.

## Human check

Kyle confirms once that the folder named in the project instructions is the right
one before anything is created in it.
