# SKILL — first run

The how-to under `setup/CONTEXT.md`. Runs only while working in `setup/`.

## When

- No Doc titled `_coaching-workspace.md` turns up when a chat looks for the data
  folder (`CLAUDE.md` § Two roots), or
- the coach says "set up my workspace", or
- a task finds `drive:/_settings/`, `drive:/players/` or a settings file missing.
  Then: finish nothing else first — say in one line that the workspace needs setting
  up, and ask to do it now. The folder is already marked → start at § 3.

## 1 · Find the folder

1. Ask: "What did you name your coaching folder in Google Drive?"
2. Search Drive for a **folder** with exactly that title, owned by the coach.
   - One → step 3.
   - None → "I can't find a folder called *<name>*. Create it now?" On yes, create it
     at the top of the coach's Drive and go to § 2 — that yes was the confirm.
     Anything else → stop; nothing is created.
   - Several → ask once which, using a detail you can see (where it sits, when it was
     last changed). Never a numbered list.
3. Confirm once: "Set up your coaching workspace in *<name>*?" Wait for yes. Never use
   a different folder that "looks right".

Two or more `_coaching-workspace.md` Docs already exist → don't pick. Tell the coach
in one line which folders hold one and ask which is the coaching folder. Never bin
one yourself.

## 2 · Mark it

Create `drive:/_coaching-workspace.md` in that folder as a Doc from
`_templates/coaching-workspace.md`: today's date, and the version from `version.md`.
If it can't be created, say so in one line and stop — a folder that can't be found
again can't be used.

## 3 · Folders

Create only what is missing: `drive:/_settings/`, then `drive:/players/`. Never
rename, move or delete anything that already exists. Never share the folder, or
anything in it, with anyone.

## 4 · Settings

For each file in `_templates/settings/` that isn't in `drive:/_settings/` yet, ask
its questions below, then create it as a Doc from that template with the coach's
answers in place of `(not set)`. Never touch a settings file that already exists —
changes go through `_settings/CONTEXT.md`.

Say once, before the first question: "Seven quick questions to set you up — say
'skip' to any and I'll ask when it comes up." Then one question per message, in this
order. A skip, or "don't know", leaves `(not set)`; never ask it again here.

| # | File | Ask |
|---|---|---|
| 1 | `coach.md` | "Which Google Calendar do your lessons go in — your main one?" (Find its id with the Calendar connector; never ask for an id.) |
| 2 | `coach.md` | "What hours do you want players to be able to book you — weekdays, Saturday, Sunday?" |
| 3 | `coach.md` | "Where do you coach? For each court: the name, where it is, anything useful — lights, access, parking." (Make each slug from the name.) |
| 4 | `coach.md` | "How many minutes is the drive between those courts? And how much gap do you want between back-to-back lessons on the same court?" (One court → only the second half.) |
| 5 | `rates.md` | "What do you charge — a private hour, other lengths, semi-private per player? And do you sell packages?" |
| 6 | `rates.md` | "What's your cancellation policy — exactly as you'd tell a parent?" Then work out the outcomes table from it and read it back in three lines or fewer: "So: 24 hours' notice is free, later is charged, rain is free — right?" A yes fills the table; a correction replaces what you guessed. |
| 7 | `levels.md` | "I've got the ball colours as your levels: red, orange, green, yellow and adult. Keep them, change them, or tell me yours?" |

Create each file as soon as its last question is answered, so a chat that ends
halfway keeps what was said. The next run asks only for files still missing.

## 5 · Finish

1. Check you can use the **Google Docs** connector as well as Drive (files are Docs —
   `_system/conventions.md` § Writing to Drive). Don't block on it.
2. Read back in one line: "Your workspace is set up in *<name>* — ready for your
   first player." If any settings were skipped, a second line: how many, and that
   you'll ask when they come up. If Docs isn't connected, a last line: "Turn on
   Google Docs for this project — without it I can add files but not update them."

## Something unexpected in the data folder

A folder or file that isn't in `CONTEXT.md` § Data folder (or a file named
`CLAUDE.md`, `CONTEXT.md` or `SKILL.md` anywhere in Drive) — leave it alone and tell
the coach in one line that it isn't part of the system. Never delete it.
