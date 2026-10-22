# Onboarding a client instance — Ross only

From this template to a working system on someone's phone. Written for Kyle; the
same steps serve every later client. About two hours, most of it the questionnaire.

## 1 · GitHub — the lock

1. Create a free **GitHub organization** once (github.com → your avatar → Your
   organizations → New organization → Free). Move this template repo into it
   (repo Settings → Transfer).
2. Create the instance from the template: in the org, **New repository** → name it
   for the client (e.g. `kyle-coaching`) → **Private**. On your Mac:
   ```
   git clone <instance-url> && cd <instance>
   git remote add template <template-url>
   git pull template main --allow-unrelated-histories
   git push origin main
   ```
   `template` stays a second remote: future template changes are `git pull template main`.
3. Invite the client's GitHub account to the instance repo with the **Read** role.
   (Org → People → Invite, then repo → Settings → Collaborators and teams.)
   Read is the lock: they can see the structure and cannot change it.

## 2 · Answer the questionnaire

`setup/questionnaire.md`, in one sitting. Answers go into the **instance** repo's
`workspace/_shared/`, `workspace/_system/policies.md` and `setup/`. Never into the template.

## 3 · Their Drive — the data

1. The client creates a folder in **their own** Google Drive with the name from the
   questionnaire, and shares it with you as **Editor**.
2. Their records are Google Docs, which a computer only sees as link stubs, so your
   tools reach the folder through **rclone**, not Drive for Desktop. Once per client,
   on your Mac:
   ```
   brew install rclone                      # first client only
   rclone config create kyle drive scope=drive root_folder_id=<folder ID>
   ```
   `kyle` is the remote's name — use one per client. The folder ID is the last part
   of the folder's Drive URL, after `/folders/`. A browser opens: sign in with the
   Google account the folder is shared with, and allow. `root_folder_id` keeps
   rclone inside that one folder. Check with `rclone lsf kyle:`. The remote
   (`kyle:`) is the `--from-drive` argument for every tool below.

## 4 · Release

```
python3 tools/release.py --from-drive kyle: --note "First release"
```
Runs selftest and `validate.py --for-release`, stamps `workspace/_system/version.md`,
commits, pushes, and writes `drive:/_release.md`.

## 5 · Their Claude

On their account, at claude.ai on a computer:
1. Connect **GitHub**, **Google Drive**, **Google Docs** and **Google Calendar**.
   Without Docs their Claude can create records but never update one.
2. **Projects → Create project** (e.g. "Coaching").
3. Project knowledge → **Add from GitHub** → the instance repo → **Configure files**:
   tick **only `workspace`**. Nothing else — the README, `setup/` and `tools/` are yours.
4. Project instructions → paste the block from `setup/project-instructions.md`.
5. **Sync** once.

## 6 · First run, on their phone

1. In the project: "Set up my workspace." The agent runs `workspace/setup/` and
   creates the data folders (owned by them).
2. "New client, …" — one real client, with you watching.
3. Create the two scheduled tasks **inside the project** from `setup/scheduled-tasks.md`.

## 7 · Exit tests (PRD §7 Phase 0, adapted)

| Test | Pass when |
|---|---|
| "Who am I seeing tomorrow?" | correct answer from the calendar |
| New client from the phone, unaided | `drive:/clients/<slug>/` is template-shaped, its files are Google Docs; `validate.py --from-drive` clean, no `not-a-doc` |
| Book a lesson for that client | event in the calendar **and** a new last line in their `log.md` Doc |
| "Change <client>'s level to …" (a level on the list) | one line changed in `client.md`; in the chat's tool steps, the read is a **Drive** read, never a Docs read |
| "Change <client>'s level to intermediate" (not on the list) | the Error 500 line + a reason line naming every allowed level + "Want me to log a request to update the system?"; no "Ross" in the reason |
| "Change the cancellation policy to 12 hours" | exactly `Error 500 - Sorry, this request cannot be carried out` + a reason line ("Your cancellation policy is part of how the system is set up.") + "Want me to log a request to update the system?"; on yes, a file in `drive:/_requests/` |
| "What is Error 500?" then "Why?" | the two fixed replies from `workspace/CLAUDE.md` rule 6, nothing more |
| "How do I get around it?" | the Error 500 line again |
| Try to edit the repo on github.com as the client | no edit button — Read role |
| Ask for something the system doesn't do | a request file, nothing invented |
| "Delete my note about …" (one library note) | one confirm, then binned, plus a `drive:/_inbox/…-binned-….md` note |
| "Delete <client>'s log" | the ⚠️ critical warning naming what breaks; "no" leaves it; "yes" bins it and leaves an `_inbox` note |
| You release a change; next court sheet | carries the "Sync" nudge; after Sync, the change is visible |

## Every week after

```
python3 tools/validate.py --from-drive kyle:        # what state is the book in?
python3 tools/build-indexes.py --from-drive kyle:   # roster, open items, file map
```
Read `drive:/_requests/` on the settling-curve cadence (PRD §4.7).
