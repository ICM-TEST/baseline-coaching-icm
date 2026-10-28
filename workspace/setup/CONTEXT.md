# setup — first run

Finds Kyle's coaching folder in his Google Drive the first time, marks it so every
later chat can find it, creates the data folder layout, and asks Kyle for his
settings. Repairs the folder if a top-level folder or a settings file has gone
missing. After that the data folder only grows through the other contracts.

## Not this?

- Creating a client → `clients/CONTEXT.md`.
- Changing a rate, a court, a level or any other setting → `_settings/CONTEXT.md`.

## Goal

Kyle's coaching folder holds `drive:/_coaching-workspace.md`, exactly the layout in
`CONTEXT.md` § Data folder, and a settings file for each of `_templates/settings/`
— every file owned by Kyle.

## Inputs

- **Working:** what Kyle says; his Google Drive (to find the folder); Google Calendar
  (to find his calendar's id).
- **Reference:** `CONTEXT.md` § Data folder (the layout), `_templates/coaching-workspace.md`,
  `_templates/settings/`, `_system/schema.md`, `_system/version.md`.

## Outputs

`drive:/_coaching-workspace.md`, empty folders under `drive:/`, the settings files in
`drive:/_settings/`, and one `drive:/_inbox/` note saying setup ran. Never a client
record, never a `drive:/_index/` file, never `drive:/_release.md` — those come from
Kyle or Ross.

## Process

`SKILL.md`.

## Human check

Kyle names his folder and confirms it once before anything is created in it. He
answers or skips each settings question; nothing is guessed into a setting except the
cancellation outcomes, which he confirms.
