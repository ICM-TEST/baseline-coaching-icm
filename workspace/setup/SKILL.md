# SKILL — first run

The how-to under `setup/CONTEXT.md`. Runs only while working in `setup/`.

## When

- No Doc titled `_coaching-workspace.md` turns up when a chat looks for the data
  folder (`CLAUDE.md` § Two roots), or
- Kyle says "set up my workspace", or
- a task finds a top-level data folder or a settings file missing. Then: finish
  nothing else first — say in one line that the workspace needs setting up, and ask
  to do it now. The folder is already marked → start at § 3.

## 1 · Find Kyle's folder

1. Ask: "What did you name your coaching folder in Google Drive?"
2. Search Drive for a **folder** with exactly that title, owned by Kyle.
   - One → step 3.
   - None → "I can't find a folder called *<name>*. Create it now?" On yes, create
     it at the top of his Drive and go to § 2 — that yes was the confirm. Anything
     else → stop; nothing is created.
   - Several → ask once which, using a detail you can see (where it sits, when it
     was last changed). Never a numbered list.
3. Confirm once: "Set up your coaching workspace in *<name>*?" Wait for yes. Never use
   a different folder that "looks right".

Two or more `_coaching-workspace.md` Docs already exist → don't pick. Tell Kyle in one
line which folders hold one, ask which is his coaching folder, and write a
`drive:/_inbox/` note for Ross naming the others. Never bin one yourself.

## 2 · Mark it

Create `drive:/_coaching-workspace.md` in that folder as a Doc from `_templates/coaching-workspace.md`:
today's date, and the version from `_system/version.md`. From now on every chat finds
the folder by this file. If it can't be created, say so in one line and stop — a
folder that can't be found again can't be used.

## 3 · Folders

Create only the folders that are missing, in this order. Never rename, move or delete
anything that already exists.

| Folder | Inside it |
|---|---|
| `drive:/_settings/` | — |
| `drive:/clients/` | — |
| `drive:/library/` | `drills/` · `programmes/` · `courts/` · `notes/` |
| `drive:/01_schedule/` | `briefs/` · `messages/` · `court-sheets/` |
| `drive:/_requests/` | — |
| `drive:/_inbox/` | — |

`drive:/_index/`, `drive:/FILE-MAP.md` and `drive:/_release.md` are **not** created
here — Ross's scripts write them.

## 4 · Settings

For each file in `_templates/settings/` that isn't in `drive:/_settings/` yet, ask
its questions below, then create it as a Doc from that template with Kyle's answers
in place of `(not set)`. Never touch a settings file that already exists — changes
go through `_settings/CONTEXT.md`.

Say once, before the first question: "Nine quick questions to set you up — say
'skip' to any and I'll ask when it comes up." Then one question per message, in this
order. A skip, or "don't know", leaves `(not set)`; never ask it again here.

| # | File | Ask |
|---|---|---|
| 1 | `coach.md` | "Which Google Calendar do your lessons go in — your main one?" (Find its id with the Calendar connector; never ask him for an id.) |
| 2 | `coach.md` | "What hours do you coach — weekdays, Saturday, Sunday?" |
| 3 | `coach.md` | "Where do you coach? For each court: the name, where it is, anything useful — lights, access, parking." (Make each slug from the name.) |
| 4 | `coach.md` | "How many minutes is the drive between those courts? And how much gap do you want between back-to-back lessons on the same court?" (One court → only the second half.) |
| 5 | `coach.md` | "When do your coaching qualification, first aid and police clearance expire?" |
| 6 | `rates.md` | "What do you charge — a private hour, other lengths, semi-private per player? And do you sell packages?" |
| 7 | `rates.md` | "What's your cancellation policy — exactly as you'd tell a parent?" Then work out the outcomes table from it and read it back in three lines or fewer: "So: 24 hours' notice is free, later is charged, rain is free — right?" His yes fills the table; a correction replaces what you guessed. |
| 8 | `levels.md` | "I've got the ball colours as your levels: red, orange, green, yellow and adult. Keep them, change them, or tell me yours?" |
| 9 | `voice.md` | "Paste or forward three to five messages you've sent parents — a reminder, a reschedule, a late cancellation. And is there anything you never say?" Write § The pattern from them in a few lines (greeting, length, sign-off, emoji); put up to five in § Examples with every name taken out. |

Where certificates are kept (`coach.md` § Clearances) is not asked here; it stays
`(not set)` until Kyle mentions it.

Create each file as soon as its last question is answered, so a chat that ends
halfway keeps what was said. The next run asks only for files still missing.

## 5 · Finish

1. Check you can use the **Google Docs** connector as well as Drive (records are
   Docs — `_system/conventions.md` § Writing to Drive). Don't block on it.
2. Write `drive:/_inbox/YYYY-MM-DD-setup.md`: the folder's name, one line per folder
   and settings file created, how many settings are still `(not set)`, the structure
   version from `_system/version.md`, and whether Docs is connected.
3. Read back in one line: "Your workspace is set up in *<name>* — ready for your
   first client." If any settings were skipped, a second line: how many, and that
   you'll ask when they come up. If Docs isn't connected, a last line: "Turn on
   Google Docs for this project — without it I can add records but not update them."

## Something unexpected in the data folder

A folder or file at the top level that isn't in the tables above (or a file named
`CLAUDE.md`, `CONTEXT.md` or `SKILL.md` anywhere in Drive) — leave it alone, and
mention it in the setup note for Ross. Never delete it.
