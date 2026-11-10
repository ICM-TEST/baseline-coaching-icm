# players — one file per player

One Google Doc per player: who they are, how to reach the family, what keeps them
safe on court, and the dated coaching notes. The files live in `drive:/players/`;
this folder holds only the contract.

## Not this?

- Booking, moving or cancelling a lesson → `schedule/CONTEXT.md`.
- A rate, policy, level or court → `_settings/CONTEXT.md`.
- A new field, section or kind of record → Error 500 (`CLAUDE.md` rule 4).

## Goal

One read of a player's file answers "who is this, how do I reach the family, what do
I need to know to keep them safe today, and where did we get to".

## Inputs

- **Working:** what the coach says; the one file `drive:/players/<slug>.md`.
- **Reference:** `_templates/player.md`, `_system/schema.md`,
  `drive:/_settings/levels.md` and `drive:/_settings/coach.md` (only when a level or
  court is being set).

## The file

`drive:/players/<slug>.md`, made from `_templates/player.md`:

1. **Details** — the `key: value` block at the top: status, level, usual slot, guardian.
2. **Safeguarding** — medical, emergency contact, media consent, who may and may not collect.
3. **Important** — a few lines in the coach's words.
4. **Notes** — dated entries, newest last: coaching notes, bookings, incidents.

## Outputs

The player's file, and one-line confirmations to the coach.

## Process

| The coach says something like | Workflow in `SKILL.md` |
|---|---|
| "New player, Sarah Ndlovu, green ball, Tuesdays 4pm, mum's Lerato" | Create a player |
| "Ethan's mum's number changed" / "he's on yellow ball now" | Update a detail |
| "Ethan — backhand's much better, keep working on the split step" | Add a coaching note |
| "Sarah has asthma" / "only her dad can fetch her" / "mum's fine with filming" | Safeguarding |
| "Ethan took a ball to the eye" / anything that happened to a child | **Incident — before anything else** |
| "Where are we with Ethan?" | Read back |
| "Michael's stopped" / "Michael's back" | Archive / reactivate |

## Human check

The coach confirms archiving once, and confirms an incident entry is accurate.
Everything else is corrected by chat afterwards.
