# 01_schedule — lessons in time · LIVE

Getting every lesson into the calendar once, at a time that works, and making sure
everyone turns up knowing what it's for: booking, recurring series, rescheduling and
cancelling, the client reminder, Kyle's morning court sheet, and the skeleton
pre-lesson brief. Its output lives in `drive:/01_schedule/`.

## Not this?

- Creating or changing a client record → `clients/CONTEXT.md` (come back here to book).
- What happened in a lesson → `02_sessions` is dormant; that is a request.
- Changing the cancellation policy, rates, availability or courts → `_settings/CONTEXT.md`.

## Goal

No missed or double-booked lesson, every client reminded without Kyle starting it,
and Kyle reading three lines per lesson each morning.

## Inputs

- **Working:** what Kyle says; Google Calendar (`calendar-id` in `drive:/_settings/coach.md`);
  `drive:/clients/<slug>/client.md` and the last entry of `drive:/clients/<slug>/log.md`;
  `drive:/_release.md` (court sheet only, for the version check); Kyle's settings —
  `drive:/_settings/coach.md` (availability, courts, travel, clearances),
  `drive:/_settings/rates.md` (cancellation policy), `drive:/_settings/voice.md`.
  A setting the task needs reads `(not set)` → `_settings/CONTEXT.md`.
- **Reference:** `_templates/brief.md`, `_templates/messages/`,
  `_templates/session-note.md`, `_system/schema.md` (calendar linkage),
  `_system/version.md` (version check), `drive:/_index/money.md` (empty until Phase 4).

## Outputs

| What | Where |
|---|---|
| Calendar events, client or guardian as attendee, `icm-client:` line last | Google Calendar |
| `series-event:`, `cadence:`, `default-slot:` | `drive:/clients/<slug>/client.md` |
| A line per booking, move or cancellation | `drive:/clients/<slug>/log.md` |
| Charged-cancellation stub | `drive:/clients/<slug>/sessions/YYYY-MM-DD.md` |
| Reminder and reschedule drafts | `drive:/01_schedule/messages/YYYY-MM-DD-<slug>.md` |
| Skeleton briefs | `drive:/01_schedule/briefs/YYYY-MM-DD-<slug>.md` |
| Morning court sheet | `drive:/01_schedule/court-sheets/YYYY-MM-DD.md` |

## Process

Every workflow — book (and whether a lesson is worth taking), recur, reschedule/cancel, remind, court sheet, brief — is in
`SKILL.md`. Two of them run on a timer, as scheduled tasks inside Kyle's coaching
project: the 06:00 court sheet and the evening reminder drafts.

Phone budget: four Drive reads per task. Calendar reads don't count; they're free.

## Human check

**Reading the calendar is free; writing to it is not.** Kyle confirms every slot,
pattern, move and cancellation in plain words before the event changes, and confirms
the policy outcome whenever money is involved. Every message is a draft he sends.
