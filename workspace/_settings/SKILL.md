# SKILL — changing a setting

The how-to under `_settings/CONTEXT.md`. Runs only while working on Kyle's settings.
Every write follows `_system/conventions.md` § Writing to Drive.

## Change a value

"My private rate is 450 now", "Saturday I finish at 1", "first aid renewed till
March 2028".

1. Read the one file with Drive for the exact current line.
2. Confirm once, old and new in his words: "Change your private 60-minute rate from
   R400 to R450?" Wait for yes.
3. Replace that one whole line with Docs. One line per confirm; a change that spans
   two lines (a new policy and its table rows) is two confirms, policy first.
4. Read back in one line: what it is now. If the change affects lessons already
   booked (a rate, the cancellation policy), add: "Applies from now — booked lessons
   keep what was agreed."

## Add a row — a level, a court, a travel time, a rate

1. Read the file; find the last row of that table.
2. Confirm once: "Add *intermediate* to your levels?" A new court needs a slug —
   make it from the name (`kelvin-grove-3`) and say it in the confirm.
3. Replace that last row with itself plus the new row — one replace.
4. A new court with no travel times: ask once, in the same read-back, how far it is
   from his other courts. No answer → leave it; booking asks when it needs it.

## Remove or rename a level or a court

Clients point to these by slug, so check before anything moves:

1. Search `drive:/clients/` for cards with `level: <slug>` (or `court: <slug>`), or
   use `drive:/_index/roster.md` if it lists them.
2. None → confirm once, then replace the row: with the new slug (rename), or with
   nothing, its line break included (remove).
3. Some → warn first: "⚠️ 3 clients are on *green-ball* — Sarah, Ethan and Lebo.
   Remove it anyway? Their cards keep the old level until you change them." Only a
   clear yes changes it. Renaming → offer, in the same message, to change those cards
   too — one confirm covers all of them, one line replaced per card, one `log.md`
   entry each.

## A value that isn't set

A task needs a value that reads `(not set)` — a cancellation outcome, a court's
travel time, Saturday availability.

1. Ask Kyle that one thing, in one line, and carry on with his answer.
2. Save it as a change (§ Change a value) — the question is the confirm; don't ask
   twice.
3. He doesn't know → do the task without it, say what you assumed, leave it unset.

## What Kyle can't change here

The files themselves, their sections and their columns, and the two fixed lines in
`voice.md` § Never. Asked for one of those → `CLAUDE.md` rule 6.
