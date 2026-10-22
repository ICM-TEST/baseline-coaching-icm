# Conventions

Inherited from Ross's workspace (`_system/conventions.md` there). Deliberate
divergences are marked ◆ so they don't read as drift.

## Two roots ◆

- **Structure** is this repo's `workspace/`, read-only, attached to Kyle's Claude
  project as knowledge. Paths in Structure are written plainly: `_templates/client/client.md`.
- **Data** is Kyle's Google Drive folder. Paths in Data are written with the prefix
  `drive:/`: `drive:/clients/ethan-moloi/log.md`.
- A contract names every path it reads or writes in one of those two forms, and
  nothing else. Ross's `validate.py` checks that each one resolves in the right root.

## Naming

- Folders and files: lowercase, hyphenated — `kelvin-grove-3.md`.
- Client slugs: `firstname-lastname`, stable for life — `ethan-moloi`. A second
  person with the same name gets a distinguishing suffix Kyle chooses, never a number.
- Dated files: `YYYY-MM-DD.md` or `YYYY-MM-DD-short-slug.md` — the date is the sort order.
- Underscore prefix (`_system/`, `drive:/_requests/`) means machinery or a channel, not live work.
- Numbered prefix (`01_schedule/`) means an operating module. Its contract lives in
  Structure; its output lives at the same name in Data (`drive:/01_schedule/`).

## Reserved names ◆

`CLAUDE.md`, `CONTEXT.md` and `SKILL.md` are **structure** and exist only in
Structure. One of those names anywhere in `drive:/` is an error, never a working
file. A client's record card is `client.md`.

## Frontmatter

YAML between `---` lines. Each record type's shape is defined once, in
`schema.md`. Notes in `drive:/library/notes/` and `drive:/_inbox/` need none.
Write vocabulary words as words — `media-consent: yes`, never `true`.

## Status

Each record type has its own closed status list in `schema.md`, so
`grep '^status:'` over `drive:/` gives a true picture of the whole book.

## Archiving ◆

A status flip, never a move. `status: archived` on a client; `status: retired` on a
programme design. The generated roster drops archived records; the folder stays.

## Links

Relative markdown links inside one root. Across roots, name the path in the
two-root form above — a markdown link can't cross from GitHub to Drive.

## One home per fact

Written once, linked everywhere else. A copied paragraph is a fact with two homes,
and one of them goes stale. Times live in Google Calendar; policies live in
`_shared/rates.md`; a record points to them and never restates them.

## File formats

Markdown text for anything an agent reads — in Drive, inside a Google Doc (below). A
binary that matters (a photo, a PDF) gets a markdown file beside it saying what it
is, because the agent cannot open it later.

## Writing to Drive ◆

Kyle's phone can edit a Google Doc but not a plain file. So every file you write in
`drive:/` is a **Google Doc**, and you change it with the Google Docs connector.

- **Read with Drive, write with Docs.** Read any file with the Google Drive
  connector — it returns the plain text. Never read with the Docs connector: it
  returns every style as well and costs about 30 times as much. Docs is only for
  changing a Doc.
- **Search** with content previews off: find a client by folder name, a file by
  title. Open the one file you need.
- **Create:** a Doc titled with the full filename, `.md` included — `log.md`,
  `2026-10-23-1700.md`. Upload the text as **plain text**; Drive turns it into a Doc
  word for word. Never upload it as markdown — Drive reformats it and the `---`
  frontmatter is lost.
- **Add an entry** (a log line, an incident addendum): insert it at the end of the
  Doc. No read needed. Nothing above it moves.
- **Change a field:** read the file with Drive for the exact current line, then
  replace that one whole line with Docs — `status: trial` → `status: active`. One
  field per replace.
- **Never** rewrite a whole Doc, and never retitle, move or delete one to change it.
- Ross's tools write `drive:/_index/`, `drive:/FILE-MAP.md` and `drive:/_release.md`
  as plain files. Read them; never write them.
- **A write didn't land** (no Docs connector, an error, a record that is a plain
  file): tell Kyle in one line, then create
  `drive:/_inbox/YYYY-MM-DD-unsaved-<slug>.md` with the exact text and the file it
  belongs in. Never promise to do it later — you won't remember. If that fails too,
  give Kyle the text in the chat.

## Deleting from Drive ◆

It is Kyle's Drive. On his word you can bin any file or folder in `drive:/`,
incident reports included. Binned is not gone: Drive keeps it in the bin for 30
days, and Kyle or Ross can restore it from there.

1. Only when Kyle asks, in this conversation, for that file or folder. Never as a
   side effect, never to tidy up, never to change a file (§ Writing to Drive).
2. Find it by its exact path. Two candidates → ask once which, using a detail he gave.
3. **Check § Critical in Drive, every time, before anything moves.**
   - Not listed → confirm once: "Bin `<path>`? It stays in Drive's bin for 30 days."
   - Listed → warn first: "⚠️ `<path>` is critical — <what breaks, from the table>.
     Bin it anyway?" For a folder, say how many files are inside. For a client
     folder, add: "Archiving keeps their history — say 'archive' if you'd rather."
4. Only a clear yes bins it. Anything else leaves it where it is.
5. After binning, create `drive:/_inbox/YYYY-MM-DD-binned-<slug>.md`: what was
   binned, Kyle's reason in his words, and "restore from Drive's bin before
   <date + 30 days>". It is Ross's only sign the file existed.

A calendar event is not a Drive file — `01_schedule/CONTEXT.md` handles those.

## Critical in Drive

Binning one of these breaks part of the system, so it gets the warning in
§ Deleting from Drive. A folder row covers the folder itself; rows marked
**everything in it** also cover each file inside. Ross's `validate.py` checks that
this list covers the whole data folder layout.

| Path | What breaks |
|---|---|
| `drive:/clients/` | every client record — the whole book |
| `drive:/clients/<slug>/` | that client's whole history: card, log, programme, lessons, agreements, incidents |
| `drive:/clients/<slug>/client.md` | the client drops out of the roster; the rest of the record is orphaned |
| `drive:/clients/<slug>/log.md` | the dated history — what was agreed, who said what |
| `drive:/clients/<slug>/programme.md` | where they are in their programme |
| `drive:/clients/<slug>/sessions/` | **everything in it** — the lesson notes; nothing is billable without one |
| `drive:/clients/<slug>/agreements/` | **everything in it** — the record of what the family signed |
| `drive:/clients/<slug>/incidents/` | **everything in it** — safeguarding records about a child; may be needed for a parent complaint, insurance or an inquiry |
| `drive:/clients/<slug>/output/` | **everything in it** — what has been sent to the family |
| `drive:/library/` | every drill, programme design, court and note |
| `drive:/01_schedule/` | briefs, message drafts and court sheets |
| `drive:/_requests/` | requests Ross hasn't answered yet |
| `drive:/_inbox/` | notes waiting for Ross, including unsaved writes and bin notes |
| `drive:/_release.md` | the version check — Kyle stops being told to Sync |

Not critical: `drive:/_index/` and `drive:/FILE-MAP.md` (Ross's tools rebuild them),
a single library file, a court sheet, a brief or a draft.

## Error 500 reasons ◆

The one line that follows the Error 500 line (`CLAUDE.md` rule 6). It says what is
fixed, in Kyle's words — never who fixed it, never how to get around it. Pick the
row that fits; fill the angle brackets.

| Kyle tries to… | Reason line |
|---|---|
| set a field to a value that isn't allowed — a level, a court, a status | "<what he said>" isn't one of the <field>s the system is set up with: <every allowed value>. |
| change a rate, the cancellation policy, his hours, a court's details or his voice | Your <thing> is part of how the system is set up. |
| add a field or a new kind of record, or change a template, contract, rule or this map | That would change how the system is built. |

Allowed values come from where `_system/schema.md` says the field's list lives
(levels: `_shared/curriculum.md`; courts: `_shared/coach.md`). List them all, in the
order written there, joined with commas and a final "or".

## CONTEXT.md contract

Every folder-level `CONTEXT.md` carries six things: **Purpose** (opening paragraph),
**Not this?**, **Goal**, **Inputs** (Working and Reference, every path named),
**Outputs**, **Process**.

## SKILL.md

Only where a folder has a repeated, judgement-heavy workflow. `CONTEXT.md` is the
contract; `SKILL.md` is the how-to underneath it. A skill is linked **only** from its
own folder's `CONTEXT.md`, never from another folder or another skill, and it runs
only while working in its own folder.
