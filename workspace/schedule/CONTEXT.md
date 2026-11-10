# schedule — lessons in time

Getting every lesson into the calendar once, at a time that works: booking, recurring
series, rescheduling and cancelling, and working out whether a lesson is worth
taking. Its only output outside the calendar is a dated note in the player's file.

## Not this?

- Creating or changing a player's file → `players/CONTEXT.md` (come back here to book).
- Changing the cancellation policy, rates, availability or courts → `_settings/CONTEXT.md`.
- Reminders, messages to parents, group lessons, a second calendar → `CLAUDE.md` rule 4.

## Goal

No missed or double-booked lesson, and every booking, move and cancellation written
once in the player's file.

## Inputs

- **Working:** what the coach says; Google Calendar (`calendar-id` in
  `drive:/_settings/coach.md`); the player's file `drive:/players/<slug>.md`;
  `drive:/_settings/coach.md` (availability, courts, travel);
  `drive:/_settings/rates.md` (prices, cancellation policy).
  A setting the task needs reads `(not set)` → `_settings/CONTEXT.md`.
- **Reference:** `_system/schema.md` (calendar linkage).

## Outputs

| What | Where |
|---|---|
| Calendar events, player or guardian as attendee, `icm-player:` line last | Google Calendar |
| `series-event:`, `cadence:`, `default-slot:` | the player's file, details block |
| A dated note per booking, move or cancellation | the end of the player's file |

## Process

Every workflow — book, "is it worth it?", recur, reschedule, cancel — is in `SKILL.md`.

Phone budget: three Drive reads per task (the player's file, `coach.md`, and
`rates.md` only when money is involved). Calendar reads are free.

## Human check

**Reading the calendar is free; writing to it is not.** The coach confirms every slot,
pattern, move and cancellation in plain words before the event changes, and confirms
the policy outcome whenever money is involved.
