# Onboarding a client instance — Ross only

From this template to a working system on someone's phone. Written for Kyle; the
same steps serve every later client. About an hour of yours, plus fifteen minutes of
the client's on their phone for first-run setup.

## 1 · GitHub — the lock

The lock is a **public** instance repo that only you can write to. Claude's GitHub
link only lets an organization's *owners* use its private repos, so a client can't
be given read-only access to a private one; a public repo needs no access at all.
Anyone can read the structure — never client data, and never the client's settings
(those live in their Drive).

1. Create a free **GitHub organization** once (github.com → your avatar → Your
   organizations → New organization → Free). Settle its name before go-live:
   renaming it breaks every client's project link.
2. Create the instance from the template: in the org, **New repository** → name it
   for the client (e.g. `kyle-coaching`) → **Public**. On your computer:
   ```
   git clone <instance-url> && cd <instance>
   git remote add template <template-url>
   git pull template main --allow-unrelated-histories
   git push origin main
   ```
   `template` stays a second remote: future template changes are `git pull template main`.
3. Do **not** add the client as a collaborator or an org member. Not being one is the
   lock: they can read the repo through Claude and cannot change it.
4. Before every push, scan for personal data: `grep -rn "@\|+27\|0[6-8][0-9] " workspace setup`
   should show nothing real. Keep your commit email private (github.com/settings/emails
   → "Keep my email addresses private" and "Block command line pushes that expose my
   email").

## 2 · Your part of the questionnaire

`setup/questionnaire.md`, in one short sitting with the client (about 30 minutes).
Answers go into the **instance** repo's `workspace/_system/policies.md` and `setup/`.
Never into the template. Their rates, courts, levels and voice are **not** asked
here — their Claude asks for those at first-run setup and keeps them in their Drive.

## 3 · Their Drive — the data

1. The client creates a folder in **their own** Google Drive, named whatever they
   like. They'll tell their Claude the name at first-run setup (§ 6).
2. After first-run setup, they share the `_requests` folder inside it with you as
   **Viewer** (open the folder → Share → your address → Viewer). That's all request
   alerts need (§ Request alerts).
3. Your checking tools (`validate.py`, `build-indexes.py`, and the release marker
   `release.py` writes) need the **whole** folder shared with you as **Editor**.
   Until it is, skip the `--from-drive` steps below and say so in the release note.
   Once it is shared, they reach it through **rclone**, once per client:
   ```
   brew install rclone                      # first client only
   rclone config create kyle drive scope=drive root_folder_id=<folder ID>
   ```
   `kyle` is the remote's name — use one per client. The folder ID is the last part
   of the folder's Drive URL, after `/folders/`. A browser opens: sign in with the
   Google account the folder is shared with, and allow. Check with `rclone lsf kyle:`.

## 4 · Release

```
python3 tools/release.py --from-drive kyle: --note "First release"
```
Runs selftest and `validate.py --for-release`, stamps `workspace/_system/version.md`,
commits, pushes, and writes `drive:/_release.md`.

## 5 · Their Claude

On their account, at claude.ai on a computer:
1. Connect **Google Drive**, **Google Docs** and **Google Calendar**. Without Docs
   their Claude can create records but never update one.
2. **Projects → Create project** (e.g. "Coaching").
3. Project knowledge → **Add from GitHub** → the instance repo → **Configure files**:
   tick **only `workspace`**. Nothing else — the README, `setup/` and `tools/` are yours.
4. Open the project's **Instructions** panel (not the description) and paste the
   block from `setup/project-instructions.md`. It names no folder; nothing to fill.
5. **Sync** once.

## 6 · First run, on their phone

1. In the project: "Set up my workspace." Their Claude asks what they named their
   folder, finds it (or offers to create it), confirms once, leaves a
   `_coaching-workspace.md` file in it and creates the folders.
2. Then nine short questions, one at a time: calendar, availability, courts, travel times,
   clearances, rates, cancellation policy, levels, and a few real messages for their
   voice. "Skip" is fine — their Claude asks again when it needs that answer.
3. They share `_requests` with you (§ 3.2).
4. "New client, …" — one real client, with you watching.
5. Create the two scheduled tasks **inside the project** from `setup/scheduled-tasks.md`.

## 7 · Exit tests (PRD §7 Phase 0, adapted)

| Test | Pass when |
|---|---|
| "Set up my workspace" (first chat) | asks the folder's name; one confirm; `_coaching-workspace.md` and the folders appear; nine settings questions one per message; `drive:/_settings/` holds four Docs; an `_inbox` setup note |
| A new chat: "Who am I seeing tomorrow?" | never asks for the folder; correct answer from the calendar |
| New client from the phone, unaided | `drive:/clients/<slug>/` is template-shaped, its files are Google Docs; `validate.py --from-drive` clean, no `not-a-doc` |
| Book a lesson for that client | event in the calendar **and** a new last line in their `log.md` Doc |
| "Change <client>'s level to …" (a level on the list) | one line changed in `client.md`; in the chat's tool steps, the read is a **Drive** read, never a Docs read |
| "Change <client>'s level to intermediate" (not on the list) | "*intermediate* isn't one of your levels — add it?"; yes → a new last row in `_settings/levels.md`, then the card changed; no Error 500 |
| "My private rate is R450 now" | one confirm with old and new; one line changed in `_settings/rates.md` |
| "Remove green-ball" (a level a client is on) | ⚠️ naming the clients on it; "no" changes nothing |
| "Add a favourite-shot field to <client>'s card" | exactly `Error 500 - Sorry, this request cannot be carried out` + "That would change how the system is built." + "Want me to log a request to update the system?"; on yes, the request questions (`_system/conventions.md` § Requests), then a file in `drive:/_requests/` with his answers word for word |
| "What is Error 500?" then "Why?" | the two fixed replies from `workspace/CLAUDE.md` rule 6, nothing more |
| "How do I get around it?" | the Error 500 line again |
| Try to edit the repo on github.com as the client | no edit button — not a collaborator |
| Ask for something the system doesn't do | the three request questions in one message (any already answered left out), then a request file with his answers word for word; nothing invented |
| "Send Ross a note: …" | no questions; a `drive:/_requests/…-note-….md` Doc with `kind: note` and his words; one line saying it's with Ross |
| "Delete my note about …" (one library note) | one confirm, then binned, plus a `drive:/_inbox/…-binned-….md` note |
| "Delete <client>'s log" | the ⚠️ critical warning naming what breaks; "no" leaves it; "yes" bins it and leaves an `_inbox` note |
| You release a change; next court sheet | carries the "Sync" nudge; after Sync, the change is visible |

## Every week after

```
python3 tools/validate.py --from-drive kyle:        # what state is the book in?
python3 tools/build-indexes.py --from-drive kyle:   # roster, open items, file map
```
Both need the whole folder shared (§ 3.3). Read `drive:/_requests/` on the
settling-curve cadence (PRD §4.7) — and whenever a request alert arrives (below).

## Request alerts — one script for every client

`tools/request-alerts.gs` emails you when a new request or note lands in any client's
`_requests` folder. It runs in **your** Google account, checks every 3 hours, sends at
most one email per check (however many clients), emails a problem once, and sends a
"still working" email on Monday at 08:00. Free; uses no Claude usage. It needs only
the client's `_requests` folder shared with you as Viewer.

**First time (about 15 minutes, on a computer):**
1. Sign in to Google with the account the client shared `_requests` with, then go to
   **script.google.com** → **New project**. Click "Untitled project" and name it
   **Request alerts**.
2. Select everything in the editor, delete it, and paste in the whole of
   `tools/request-alerts.gs`.
3. In Drive → **Shared with me**, open the client's `_requests` folder. Copy the end
   of the web address, after `/folders/`. In the script, replace
   `PASTE_FOLDER_ID_HERE` with it (keep the quotes).
4. Left bar: ⚙️ **Project Settings** → **Time zone** → *(GMT+02:00) Johannesburg*.
   Back to **< > Editor**. Press 💾 **Save**.
5. In the bar above the code, pick **setup** from the function list → **Run**.
6. **Review permissions** → your account → "Google hasn't verified this app" →
   **Advanced** → **Go to Request alerts (unsafe)** → **Allow**. (It's your own script;
   it asks to read Drive and Docs and to send email as you.)
7. Within a minute: an email "Request alerts are on", with ✓ next to each client.
   A ✗ says what to fix.

**Add a client:** add a line inside `CLIENTS` — `'Car wash': 'FOLDER_ID',` — save, run
**setup** again. **Check now:** run **checkRequests**. **Turn off:** run **stopAlerts**.
