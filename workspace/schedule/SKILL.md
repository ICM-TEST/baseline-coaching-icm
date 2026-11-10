# SKILL — lessons in time

The how-to under `schedule/CONTEXT.md`. Runs only while working on the schedule.

**One calendar:** `calendar-id` in `drive:/_settings/coach.md`, timezone `Africa/Johannesburg`.

## 1. Always ask, never assume

A calendar event puts something in the coach's real day and, through the invite, in a
family's. It is asked about, never inferred.

- **Ask for the slot. Don't invent one.** "Tuesday" is a day, not a time. "Next week"
  is not a slot. Get the day *and* the time before creating anything — "the usual"
  means `default-slot:` in the player's file, read back for confirmation.
- **Never bulk-schedule.** One player, one agreed slot. No "book everyone for next term".
- **Never** move or delete an event as a side effect of doing something else.

## 2. Book a lesson

1. Resolve the player: find `drive:/players/<slug>.md` by title and read it (one read).
   Not a player yet → that is `players/CONTEXT.md`; create the file first, then come back.
2. Check the slot against the calendar **and** against `drive:/_settings/coach.md`: inside
   the coach's availability, and the travel time from the previous lesson's court to this one fits.
3. Conflict, outside the coach's availability, or travel doesn't fit → say which in one line, offer the
   nearest two slots that work, create nothing. If the coach still wants it, or the slot
   only fits by pushing other lessons, do § 2a before anything moves.
4. Read back the slot in plain words — "Ethan, Tue 21 Oct, 16:00, 60 min, Kelvin
   Grove 3?" — and wait for yes.
5. Create the event:

| Field | Value |
|---|---|
| `summary` | `Tennis — <name>` |
| `start` / `end` | ISO 8601, `Africa/Johannesburg`; length = `duration:` in the player's file |
| `attendees` | `calendar-attendee:` from the player's file — never more than that |
| `location` | the court's name from `coach.md` |
| `description` | `icm-player: <slug>` as the **last line**, and nothing about the player above it |

6. Add one dated note at the end of the player's file: booked, slot, court.

## 2a. Is it worth it?

The coach's time is the stock: a lesson that costs a drive, or pushes others later, can
earn less than it loses. When a booking request only fits by moving other lessons,
when it would push the day past the coach's availability, or when the coach asks "should I take
this?", work it out before the coach says yes.

1. **Read** that day's calendar (free), then `drive:/_settings/coach.md` (availability,
   courts, travel) and `drive:/_settings/rates.md` (the price of each lesson). A
   price the coach gives for a request ("R200 for an hour at SACS") wins over the table.
2. **Lay out the day with the request in it:** each lesson where it can start once
   the drive from the last court is done, inside the coach's availability. Note what moves
   and what no longer fits — a booked lesson, or another request the coach mentioned in
   this chat.
3. **Compare** the two days: money in against money lost, and extra driving minutes.
   A price that's `(not set)` → compare by lessons kept, and say so.
4. **Say it in two lines,** then the choice:
   "Taking 3pm at SACS means you can't reach Plumstead for 4 — your 4 and 5 move to
   5 and 6, and the 6pm request no longer fits. +R200, −R300: R100 worse. Skip it, or
   offer them another time?"
   Comes out ahead or even → say so in one line and carry on with § 2 step 4.

Never move or decline anything here. Moving a booked lesson is § 4, one player at a
time, each confirmed; declining is the coach's message to send (rule 4). Nothing is
saved: a request the coach hasn't said yes to lives only in this chat.

## 3. Recurring series

Translate the coach's plain words to an `RRULE`. **Never ask the coach for an RRULE** — plain
words are the coach's side; the translation is yours.

| The coach says | You write |
|---|---|
| every day | `RRULE:FREQ=DAILY` |
| every second day | `RRULE:FREQ=DAILY;INTERVAL=2` |
| every Monday | `RRULE:FREQ=WEEKLY;BYDAY=MO` |
| every Monday and Thursday | `RRULE:FREQ=WEEKLY;BYDAY=MO,TH` |
| every weekday | `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| every second Tuesday | `RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TU` |
| 1st of the month | `RRULE:FREQ=MONTHLY;BYMONTHDAY=1` |
| 15th of the month | `RRULE:FREQ=MONTHLY;BYMONTHDAY=15` |
| 1st and 15th of the month | `RRULE:FREQ=MONTHLY;BYMONTHDAY=1,15` |
| every 3 March | `RRULE:FREQ=YEARLY;BYMONTH=3;BYMONTHDAY=3` |
| …through to December / for 10 weeks | add `;UNTIL=YYYYMMDDT235959Z` / `;COUNT=10` |

Weekday codes: `MO TU WE TH FR SA SU`.

- **Start on the first real occurrence.** A "every Tuesday" series that starts on a
  Wednesday fires on Wednesdays.
- **Ambiguous → ask which weeks.** "Every second week" — starting this week or next?
- Read the pattern back in plain words and wait for yes.
- Then do §2 step 5 with `recurrence` set, and **write the link back**: the series id
  to `series-event:`, plus `cadence:` and `default-slot:` on the player's file. Not
  optional — a series with no link back gets offered a second series next time.

## 4. Reschedule

1. Find the event by the `icm-player:` line, never by title.
2. **Part of a series and the coach hasn't said "just this one" or "all of them" → always
   ask.** Getting this wrong wipes a term.
3. Check the new slot as in §2 steps 2–3; read it back; wait for yes.
4. Move the event. Add a note to the player's file: was → now, and why. The calendar
   invite tells the family; you write no message.
5. Changing a whole series' pattern: update `cadence:` / `default-slot:` on the
   player's file **first**, then regenerate the `RRULE`. If the file and the event
   disagree, the file wins — fix the event and tell the coach you did, because the coach may
   have changed it in the calendar on purpose.

## 5. Cancel

1. Find the event; "this one or all of them?" as in §4.
2. Apply `drive:/_settings/rates.md` to the notice given. State the outcome in one line —
   "Under 24 hours, so it's charged — right?" — and wait for the coach's answer whenever
   money is involved.
3. Delete the event (or the one instance). Cancelling the whole series also clears
   `series-event:` in the player's file — the only time that field is emptied.
4. Add a note to the player's file: what was cancelled, by whom, notice given, and
   the outcome the coach confirmed (`charged` or `not charged`).

## When it doesn't fit

Group lessons, a second calendar, a club booking system, a waiting list, blackout
dates, reminders or messages to parents — none exist. That is `CLAUDE.md` rule 4:
the Error 500 line, the reason, and the system provider line. Then offer the nearest
single-player booking the system does support.
