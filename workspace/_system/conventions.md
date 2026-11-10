# Conventions

The conventions every file here follows. ◆ marks the ones specific to the two-root design.

## Two roots ◆

- **Structure** is this repo's `workspace/`, read-only, attached to the coach's Claude
  project as knowledge. Paths in Structure are written plainly: `_templates/player.md`.
- **Data** is the coach's Google Drive folder. Paths in Data are written with the prefix
  `drive:/`: `drive:/players/ethan-moloi.md`.
- A contract names every path it reads or writes in one of those two forms, and
  nothing else. The system provider's tests check that each one resolves in the right root.

## Naming

- Folders and files: lowercase, hyphenated — `kelvin-grove-3.md`.
- Player slugs: `firstname-lastname`, stable for life — `ethan-moloi`; the file is `<slug>.md`. A second
  person with the same name gets a distinguishing suffix the coach chooses, never a number.
- Dated files: `YYYY-MM-DD.md` or `YYYY-MM-DD-short-slug.md` — the date is the sort order.
- Underscore prefix (`_system/`, `drive:/_settings/`) means machinery, not live work.

## Reserved names ◆

`CLAUDE.md`, `CONTEXT.md` and `SKILL.md` are **structure** and exist only in
Structure. One of those names anywhere in `drive:/` is an error, never a working
file.

## Frontmatter

`key: value` lines at the top of a file. Each record's shape is defined once, in
`schema.md`. Write vocabulary words as words — `media-consent: yes`, never `true`.

## Status

A player's status is one of the closed list in `schema.md`, on the `status:` line of the
file. Nothing else records it.

## Archiving ◆

A status change, never a move. `status: archived` on the player's file; the file stays where it is.

## Links

Relative markdown links inside one root. Across roots, name the path in the
two-root form above — a markdown link can't cross from GitHub to Drive.

## One home per fact

Written once, linked everywhere else. A copied paragraph is a fact with two homes,
and one of them goes stale. Times live in Google Calendar; policies live in
`drive:/_settings/rates.md`; a record points to them and never restates them.

## File formats

Markdown text for anything an agent reads — in Drive, inside a Google Doc (below). A
binary that matters (a photo, a PDF) gets a markdown file beside it saying what it
is, because the agent cannot open it later.

## Writing to Drive ◆

The coach's phone can edit a Google Doc but not a plain file. So every file you write in
`drive:/` is a **Google Doc**, and you change it with the Google Docs connector.

- **Read with Drive, write with Docs.** Read any file with the Google Drive
  connector — it returns the plain text. Never read with the Docs connector: it
  returns every style as well and costs about 30 times as much. Docs is only for
  changing a Doc.
- **Search** with content previews off: find a file by its title. Open the one file you need.
- **Create:** a Doc titled with the full filename, `.md` included — `ethan-moloi.md`.
  Upload the text as **plain text**, all of it in the one create; Drive turns it into a Doc
  word for word. Never upload it as markdown — Drive reformats it.
- **Add an entry** (a coaching note, a booking note, an incident): insert it at the end of the
  Doc. No read needed. Nothing above it moves.
- **Change a field:** read the file with Drive for the exact current line, then
  replace that one whole line with Docs — `status: trial` → `status: active`. One
  field per replace.
- **Never** rewrite a whole Doc, and never retitle, move or delete one to change it.
- **A write didn't land** (no Docs connector, an error, a record that is a plain
  file): tell the coach in one line and give the exact text in the chat, with the file it
  belongs in. Never promise to do it later — you won't remember.

## Deleting from Drive ◆

It is the coach's Drive. On the coach's word you can bin any file in `drive:/`.
Binned is not gone: Drive keeps it in the bin for 30 days, and the coach can restore
it from there.

1. Only when the coach asks, in this conversation, for that file. Never as a side
   effect, never to tidy up, never to change a file (§ Writing to Drive).
2. Find it by its exact path. Two candidates → ask once which, using a detail given.
3. **Check § Critical in Drive, every time, before anything moves.**
   - Not listed → confirm once: "Bin `<path>`? It stays in Drive's bin for 30 days."
   - Listed → warn first: "⚠️ `<path>` is critical — <what breaks, from the table>.
     Bin it anyway?" For a player's file, add: "Archiving keeps their history — say
     'archive' if you'd rather."
4. Only a clear yes bins it. Anything else leaves it where it is.
5. After binning, say in one line: "Binned. Restore it from Drive's bin before
   <date + 30 days>." Nothing else is written.

A calendar event is not a Drive file — `schedule/CONTEXT.md` handles those.

## Critical in Drive

Binning one of these breaks part of the system, so it gets the warning above.

| Path | What breaks |
|---|---|
| `drive:/_coaching-workspace.md` | every chat — Claude can't find this folder any more and asks to set up again |
| `drive:/_settings/` and every file in it | rates, cancellation policy, availability, courts and levels; booking and cancelling stop working until they're set again |
| `drive:/players/` | every player's file — the whole book |
| `drive:/players/<slug>.md` | that player's whole history: details, safeguarding, coaching notes and any incident entries, which may be needed for a parent complaint, insurance or an inquiry |

## Error 500 reasons ◆

The one line that follows the Error 500 line (`CLAUDE.md` rule 4). It says what is
fixed, in the coach's words — never how to get around it. Pick the row that fits;
fill the angle brackets.

| The coach asks for… | Reason line | System provider line after it? |
|---|---|---|
| anything that isn't the coaching — a movie list, an essay, a recipe, a general question, help with something else | This project only handles your coaching: players, lessons, calendar and settings. | no |
| a value outside a fixed list in `_system/schema.md` — a status, a cadence, a lesson length, an incident type | "<what was said>" isn't one of the <field>s the system is set up with: <every allowed value>. | yes |
| a change to a safety rule — what is never stored, never sent, never done without the coach | That's one of the safety rules the system is built on. | yes |
| a field, a new kind of record or setting, a feature the system doesn't have, or a change to a template, contract, rule or the map | That would change how the system is built. | yes |

Allowed values are listed in `_system/schema.md`, in the order written there, all of
them, joined with commas and a final "or".

The system provider line is exactly: "To change how the system works, contact your
system provider: <the `System provider:` line of your Project instruction>." If the
instruction has no such line, say "contact your system provider" and stop there.
Never offer to log, save or send the request yourself.

**Not Error 500 — these are the coach's, changed by chat with no one else involved:**
a rate, a package, the cancellation policy, booking hours, a court, a travel time, a
level, and anything in a player's file. That is `_settings/CONTEXT.md` and
`players/CONTEXT.md`.

## CONTEXT.md contract

Every folder-level `CONTEXT.md` carries six things: **Purpose** (opening paragraph),
**Not this?**, **Goal**, **Inputs** (Working and Reference, every path named),
**Outputs**, **Process**.

## SKILL.md

Only where a folder has a repeated, judgement-heavy workflow. `CONTEXT.md` is the
contract; `SKILL.md` is the how-to underneath it. A skill is linked **only** from its
own folder's `CONTEXT.md`, never from another folder or another skill, and it runs
only while working in its own folder.
