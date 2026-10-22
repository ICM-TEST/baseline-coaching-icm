# SKILL — lessons in time

The how-to under `01_schedule/CONTEXT.md`. Runs only while working on the schedule.
§1, §3, §4 and §5 are taken from the schedule skill in Ross's own second brain and adapted
from Notion to client records; they were already right.

**One calendar:** `calendar-id` in `_shared/coach.md`, timezone `Africa/Johannesburg`.

## 1. Always ask, never assume

A calendar event puts something in Kyle's real day and, through the invite, in a
family's. It is asked about, never inferred.

- **Ask for the slot. Don't invent one.** "Tuesday" is a day, not a time. "Next week"
  is not a slot. Get the day *and* the time before creating anything — "the usual"
  means `default-slot:` on the record, read back for confirmation.
- **Never bulk-schedule.** One client, one agreed slot. No "book everyone for next term".
- **Never** move or delete an event as a side effect of doing something else.

## 2. Book a lesson

1. Resolve the client: `drive:/_index/roster.md` first; it may lag, so if the name isn't
   there, search for the slug folder inside `drive:/clients/`. Not a client yet → that is
   `clients/CONTEXT.md`; create the record first, then come back.
2. Check the slot against the calendar **and** against `_shared/coach.md`: inside
   hours, and the travel time from the previous lesson's court to this one fits.
3. Conflict, outside hours, or travel doesn't fit → say which in one line, offer the
   nearest two slots that work, create nothing.
4. Read back the slot in plain words — "Ethan, Tue 21 Oct, 16:00, 60 min, Kelvin
   Grove 3?" — and wait for yes.
5. Create the event:

| Field | Value |
|---|---|
| `summary` | `Tennis — <name>` |
| `start` / `end` | ISO 8601, `Africa/Johannesburg`; length = `duration:` on the record |
| `attendees` | `calendar-attendee:` from the record — never more than that |
| `location` | the court's name from `coach.md` |
| `description` | the client-visible brief bullets if one exists, then a blank line, then `icm-client: <slug>` as the **last line** |

6. Append one line to `drive:/clients/<slug>/log.md`: date booked, slot, court.

## 3. Recurring series

Translate Kyle's plain words to an `RRULE`. **Never ask Kyle for an RRULE** — plain
words are his side; the translation is yours.

| Kyle says | You write |
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
  to `series-event:`, plus `cadence:` and `default-slot:` on `drive:/clients/<slug>/client.md`. Not
  optional — a series with no link back gets offered a second series next time.

## 4. Reschedule

1. Find the event by the `icm-client:` line, never by title.
2. **Part of a series and Kyle hasn't said "just this one" or "all of them" → always
   ask.** Getting this wrong wipes a term.
3. Check the new slot as in §2 steps 2–3; read it back; wait for yes.
4. Move the event. `log.md`: was → now, and why.
5. Draft the message from `_templates/messages/reschedule.md` into
   `drive:/01_schedule/messages/YYYY-MM-DD-<slug>.md`. Kyle sends it.
6. Changing a whole series' pattern: update `cadence:` / `default-slot:` on the
   record **first**, then regenerate the `RRULE`. If the record and the event
   disagree, the record wins — fix the event and tell Kyle you did, because he may
   have changed it in the calendar on purpose.

## 5. Cancel

1. Find the event; "this one or all of them?" as in §4.
2. Apply `_shared/rates.md` to the notice given. State the outcome in one line —
   "Under 24 hours, so it's charged — right?" — and wait for Kyle's answer whenever
   money is involved.
3. Delete the event (or the one instance). Cancelling the whole series also clears
   `series-event:` on the record — the only time that field is emptied.
4. `log.md`: what was cancelled, by whom, notice given, the outcome Kyle confirmed.
5. **Charged** → write a session-note stub from `_templates/session-note.md` to
   `drive:/clients/<slug>/sessions/YYYY-MM-DD.md` with `attended: cancelled-late` or
   `no-show`, `charged: yes`, and nothing in the body. (Rule 1: money reads notes.)
6. Draft the message as in §4 step 5.

## 6. Client reminder — evening before

Run by the scheduled task. For each lesson tomorrow:

1. Phone missing on the record → no draft; add the client to the run's summary as
   "no number" so Kyle sees it.
2. Otherwise draft from `_templates/messages/reminder.md` in Kyle's voice
   (`_shared/voice.md`): day, time, court, and what they'll work on from the
   client-visible bullets. Nothing from "For Kyle only" or "Flags".
3. Write to `drive:/01_schedule/messages/YYYY-MM-DD-<slug>.md`.
4. Tell Kyle in one line: how many drafts are ready, and who has no number.

The calendar invite itself is the other reminder channel — Google sends it, free.

## 7. Skeleton brief — morning of

Run by the 06:00 task, for each lesson today.

1. Read `client.md` and the **last** `log.md` entry. That is all Phase 1 reads.
2. Fill `_templates/brief.md` into `drive:/01_schedule/briefs/YYYY-MM-DD-<slug>.md`.
   `thin: true` — say plainly it's a thin brief.
3. Copy the client-visible bullets into the event description, **above** the
   `icm-client:` line. Never change the event's time, attendees or anything else.
4. Flags = medical extract, any `may-not-collect` name, anything open in the log.

## 8. Morning court sheet — 06:00

Into `drive:/01_schedule/court-sheets/YYYY-MM-DD.md`, and the same text as the task's reply to Kyle.

- Nothing on today → "Nothing on today." Four words, not an empty report.
- Otherwise, in order: **three lines per lesson, maximum** —
  1. time · name · court (· "new" if `status: trial`)
  2. today, from the brief
  3. flags: medical extract, `may-not-collect`, "no consent to film" if relevant, owed money once Phase 4 is live
- Travel: one line between lessons only where the gap is tight.
- Clearances: one line for anything in `_shared/coach.md` expiring within 60 days or expired.
- Version: read `drive:/_release.md`; if it is newer than `_system/version.md`, add the
  one-line update nudge from `_system/version.md`. Last line of the sheet.

## When it doesn't fit

Group lessons, a second calendar, a club booking system, a waiting list, blackout
dates — none exist yet. Write the request (`CLAUDE.md` rule 5) and do the nearest
single-client booking Kyle agrees to.
