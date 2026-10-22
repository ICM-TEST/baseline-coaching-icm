# SKILL — first run

The how-to under `setup/CONTEXT.md`. Runs only while working in `setup/`.

## When

- Kyle says "set up my workspace", or
- any task finds a top-level data folder missing (e.g. `drive:/clients/` doesn't
  exist). Then: finish nothing else first — say in one line that the workspace
  needs setting up, and ask to do it now.

## Steps

1. Find the data folder by the exact name in the project instructions. Not found →
   tell Kyle in one line and stop. Never create the root folder under another name,
   and never use a different folder that "looks right".
2. Confirm once: "Set up your coaching folders in *<name>*?" Wait for yes.
3. Create only the folders that are missing, in this order. Never rename, move or
   delete anything that already exists.

| Folder | Inside it |
|---|---|
| `drive:/clients/` | — |
| `drive:/library/` | `drills/` · `programmes/` · `courts/` · `notes/` |
| `drive:/01_schedule/` | `briefs/` · `messages/` · `court-sheets/` |
| `drive:/_requests/` | — |
| `drive:/_inbox/` | — |

   `drive:/_index/`, `drive:/FILE-MAP.md` and `drive:/_release.md` are **not** created here — Ross's
   scripts write them.
4. Check you can use the **Google Docs** connector as well as Drive (records are
   Docs — `_system/conventions.md` § Writing to Drive). Don't block on it.
5. Write `drive:/_inbox/YYYY-MM-DD-setup.md`: one line per folder created, the
   structure version from `_system/version.md`, and whether Docs is connected.
6. Read back in one line: how many folders were created, and "ready for your first
   client". If Docs isn't connected, a second line: "Turn on Google Docs for this
   project — without it I can add records but not update them."

## Something unexpected in the data folder

A folder or file at the top level that isn't in the table (or a file named
`CLAUDE.md`, `CONTEXT.md` or `SKILL.md` anywhere in Drive) — leave it alone, and
mention it in the setup note for Ross. Never delete it.
