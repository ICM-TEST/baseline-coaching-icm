# Onboarding a coach: Ross only

The lock is a public repo that only Ross can write to. The coach is not a
collaborator or an organisation member: not being one is the lock. The coach's data
is in their own Google Drive, shared with nobody. Ross has no access to it and needs
none.

## 1. Before the session
Have [questionnaire.md](questionnaire.md) answered, so first-run setup goes quickly.

## 2. The coach's Claude, at claude.ai on a computer
1. Connect Google Drive, Google Docs and Google Calendar under the coach's **own** Google account.
2. Create a Project.
3. Project knowledge → **Add from GitHub** → this repo → tick **only `workspace`**.
4. Paste the instruction from [project-instructions.md](project-instructions.md) into the **Instructions** panel,
   with the coach's first name and your contact line filled in.
5. **Sync** once.

## 3. First chat, with the coach
1. "Set up my workspace": the coach names a folder, and Claude creates it, marks it and asks the settings questions
   ([../workspace/setup/SKILL.md](../workspace/setup/SKILL.md)).
2. Add one real player and book one real lesson.
3. Check the lock: ask for a movie list, then ask it to add a new field to the player file. Both must answer
   `Error 500 - Sorry, this request cannot be carried out`; the second must add your contact line.
4. Check a setting is theirs: "my private rate is 450 now" must be changed after one confirm, with no Error 500.

## 4. Afterwards
A change to the system reaches you only when the coach contacts you. After a release, tell the coach to press Sync at a
computer.
