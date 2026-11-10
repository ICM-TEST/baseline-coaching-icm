# SKILL — a player's file

The how-to under `players/CONTEXT.md`. Runs only while working on a player's file.
Every write follows `_system/conventions.md` § Writing to Drive.

## Finding the player

1. Search Drive for a Doc titled `<slug>.md` inside `drive:/players/` (by title,
   previews off). A first name only → search the folder for titles starting with it.
2. Two possible matches → ask **once**, using a detail the coach already gave ("Sarah
   on Tuesdays, or Sarah the adult?"). Never a numbered list.

## Create a player

1. Slugify the name: `firstname-lastname`, lowercase, hyphens. A collision gets a
   suffix **the coach** chooses, never a number.
2. Create `drive:/players/<slug>.md` as a Doc from `_templates/player.md`, in one
   create, with the details already filled.
3. Fill details **only** from what the coach said. Unknowns stay blank; never guess a
   phone number, a level or a rate. `status: trial` unless they're already a regular.
4. `level:` must be in `drive:/_settings/levels.md`; `court:` must be a slug in
   `drive:/_settings/coach.md`. Not there → leave it blank and offer to add it:
   "*intermediate* isn't one of your levels — add it?" (`_settings/CONTEXT.md`).
5. First note: today's date, how they came in, what was agreed.
6. Read back **three lines**: name and level · slot and court · what's still missing
   (phone, medical, consent). Then: "Want me to book the first lesson?"

## Update a detail

Change only the field named — read the file for the exact line, replace that one
line. Confirm in one line. No note unless the coach adds one.

## Add a coaching note

Insert at the **end** of the Doc, no read needed:

```
### YYYY-MM-DD
<what the coach said, in the coach's words, as short as it was said>
```

Never tidy, summarise or merge earlier notes. Two notes on one day are two entries.

## Read back — "where are we with Ethan?"

One read. Three lines: level and usual slot · the last two notes · anything in
Safeguarding worth saying today. Nothing else unless asked.

## Safeguarding

- **Medical:** a twelve-word operational note in `medical:` — the condition, where the
  medication is, who to call. Never a full history (`_system/policies.md`).
- **Media consent:** `yes` or `no` plus `media-consent-date:`. Until set, `unknown` —
  and unknown means no filming and no photos.
- **Collection:** names into `may-collect` or `may-not-collect`. When
  `may-not-collect` gains a name, add a note saying who told the coach and when.
- None of these is ever copied into a calendar invite.

## Incident

Comes **before** any other task in the same message. It is a note with a fixed
shape, inserted at the end of the player's file (one entry per child involved):

```
### YYYY-MM-DD HH:MM — INCIDENT
type: <injury · illness · distress · behaviour · altercation · collection · other>
severity: <minor · first-aid · medical · emergency-services>
guardian-told: <yes · no · not-yet>
What happened:
Who was there:
What was done:
Who was told, and when:
```

1. Fill it from what the coach said, in that order, in plain words. Facts, not
   conclusions. Anything not said stays blank — never fill a gap with a likely story.
2. Ask **one** question only if `guardian-told` is unknown.
3. Read it back short — type, severity, who's been told — and ask the coach to confirm
   it is accurate.
4. **An incident entry is never edited.** A correction is a new entry below it:
   `### YYYY-MM-DD HH:MM — INCIDENT ADDENDUM`, saying what is corrected and why.

## Archive / reactivate

- **Archive:** confirm once. Then `status: archived` and a closing note saying why
  they stopped, in the coach's words. If they have a recurring series, ask whether
  to end it — that is `schedule/CONTEXT.md`.
- **Reactivate:** `status: active`, a note, and a three-line read-back.

## When it doesn't fit

A field, section or kind of record the template doesn't have → `CLAUDE.md` rule 4.
If the coach gave information along with it, put it in a coaching note so nothing is
lost, and say so.
