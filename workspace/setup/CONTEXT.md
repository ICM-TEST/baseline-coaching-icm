# setup — first run

Finds the coaching folder in the coach's Google Drive the first time, marks it so
every later chat can find it, creates the two data folders, and asks the coach for
the settings. Repairs the folder if a folder or a settings file has gone missing.

## Not this?

- Creating a player → `players/CONTEXT.md`.
- Changing a rate, a court, a level or any other setting → `_settings/CONTEXT.md`.

## Goal

The coaching folder holds `drive:/_coaching-workspace.md`, exactly the layout in
`CONTEXT.md` § Data folder, and a settings file for each of `_templates/settings/` —
every file owned by the coach and shared with nobody.

## Inputs

- **Working:** what the coach says; Google Drive (to find the folder); Google Calendar
  (to find the calendar's id).
- **Reference:** `CONTEXT.md` § Data folder, `_templates/coaching-workspace.md`,
  `_templates/settings/`, `_system/schema.md`, `version.md`.

## Outputs

`drive:/_coaching-workspace.md`, the folders `drive:/_settings/` and `drive:/players/`,
and the settings files. Never a player's file.

## Process

`SKILL.md`.

## Human check

The coach names the folder and confirms it once before anything is created in it, and
answers or skips each settings question. Nothing is guessed into a setting except the
cancellation outcomes, which the coach confirms.
