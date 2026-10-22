# SKILL — running a client record

The how-to under `clients/CONTEXT.md`. Runs only while working on client records.

## Finding the client

1. Read `drive:/_index/roster.md`. It is generated and **may lag** behind a client Kyle
   created today.
2. Not there → search Drive for a folder titled with the slug inside `drive:/clients/`.
3. Two possible matches → ask **once**, using a detail Kyle already gave ("Sarah on
   Tuesdays, or Sarah the adult?"). Never a numbered list.

## Create a client

1. Slugify the name: `firstname-lastname`, lowercase, hyphens. Check for a collision
   (above). A collision gets a suffix **Kyle** chooses.
2. Create `drive:/clients/<slug>/` and create in it, as Docs, from
   `_templates/client/`: `client.md`, `log.md`, `programme.md` (the template text,
   frontmatter filled in steps 3–5). Then create the four empty folders `sessions/`, `agreements/`,
   `incidents/`, `output/`. Nothing else goes in a record folder.
3. Fill `client.md` frontmatter **only** from what Kyle said. Unknowns stay blank;
   never guess a phone number, a level or a rate. `status: trial` unless he says
   they're already a regular.
4. `level:` must be in `_shared/curriculum.md`; `court:` must be a slug in
   `_shared/coach.md`. Not there → leave blank, mention it in the read-back.
5. First `log.md` entry: today's date, how they came in, what was agreed.
6. Read back **three lines**: name and level · slot and court · what's still missing
   (phone, medical, consent). Then: "Want me to book the first lesson?" — booking is
   `01_schedule`'s job.

## Update a record

Change only the field Kyle named — replace its one line. Add a one-line `log.md` entry for anything a future
reader would want to know changed (level, guardian, phone, rate). Confirm in one line.

## Safeguarding details

- **Medical:** write a twelve-word operational extract to `medical:` — the condition,
  where the medication is, who to call. A full history is not stored
  (`_system/policies.md`). If Kyle has a signed form, `medical-source:` gets the
  `vault://` pointer; the form itself never goes in Drive.
- **Media consent:** `yes` or `no` plus `media-consent-date:`. Until it is set,
  `unknown` — and unknown means no filming and no photos.
- **Collection:** names into `may-collect` or `may-not-collect`. If `may-not-collect`
  is ever non-empty, add a `log.md` entry saying who told Kyle and when.
- None of these fields is ever copied into an invite, a brief's client-visible
  section, or a message draft.

## Incident report

Comes **before** any other task in the same message.

1. Write `_templates/incident.md` to `drive:/clients/<slug>/incidents/YYYY-MM-DD-HHMM.md`
   (date and time it happened). One file per child involved.
2. Fill it from what Kyle said, in his order, in plain words. Facts, not conclusions.
   Anything he didn't say stays blank — never fill a gap with a likely story.
3. `written:` is now. Ask **one** question only if `guardian-told` is unknown.
4. Read it back short: type, severity, who's been told. Ask him to confirm it's
   accurate. A correction after confirmation goes under **Addenda**, dated —
   never an edit above it.
5. Add one `log.md` line pointing to the incident file.

## Add an agreement

Write `_templates/agreement.md` to `drive:/clients/<slug>/agreements/YYYY-MM-DD.md` (the
signing date). `document:` is a `vault://` pointer; the signed copy never goes in
Drive. A new agreement sets `supersedes:` — the old file is never edited.

## Archive / reactivate

- **Archive:** confirm once. Then `status: archived` and a closing `log.md` entry
  saying why they stopped, in Kyle's words. Never move the folder. Archiving keeps
  it; if Kyle wants it gone, that is `_system/conventions.md` § Deleting from Drive.
  If they have a recurring series, ask whether to end it — that is `01_schedule`.
- **Reactivate:** `status: active`, a `log.md` entry, and a three-line read-back from
  the record: where they got to, why they stopped, what to check first.

## When it doesn't fit

Kyle wants a field, a folder or a kind of record the template doesn't have → that
changes the structure: `CLAUDE.md` rule 6 (Error 500, then offer the request). If he
gave you information along with it, put it in `client.md` under `## Notes` so
nothing is lost.
