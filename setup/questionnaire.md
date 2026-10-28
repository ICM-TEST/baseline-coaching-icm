# Setup — one short sitting with the client (Ross only)

Ross works through this with the client before the first release of their instance
repo. It covers only what Ross must decide or write into the instance repo — every
remaining `{{FILL}}` there is answered here. Allow about 30 minutes.

Their own settings — calendar, availability, courts, travel times, clearances, rates,
packages, cancellation policy, levels and voice — are **not** asked here. Their
Claude asks for those at first-run setup, keeps them in their Drive
(`drive:/_settings/`), and lets them change any of them by chat.

## Before the session — Ross

- [ ] Instance repo created from the template, under the GitHub organization, public (`onboarding.md` § 1)
- [ ] The client's Claude plan covers connectors and scheduled tasks
- [ ] Courtside day booked in week 2 or 3 — in the calendar now, before there's anything to watch

## 1 · Accounts and access

1. Which Google account do you use for your calendar and Drive? That's the one to
   connect in Claude.
2. Make a folder in that Google Drive for your coaching — call it anything. Your
   Claude will ask its name the first time.
3. Does a club booking system already own any of your calendar? If yes, which hours
   — that becomes a boundary, not something we write to.
4. You'll share the `_requests` folder with Ross so he sees what you ask for. If you
   also share the whole folder, he can check it's healthy — and he'll be able to
   read your notes. Are you comfortable with that? Your words go in
   `_system/policies.md`.
4a. Signed agreements and consent forms stay out of Drive. Who keeps them, and where?
   (`_system/policies.md`)

## 2 · Minors and safety

5. For a junior, who gets the calendar invite — a parent, the player, or both?
6. What medical details do you actually need on court? (We keep a twelve-word extract;
   signed forms stay out of Drive.)
7. Do you film or photograph players? How do you get consent today?
8. Is there any child you coach where someone must not collect them?
9. If something happens on court today — an injury, a fall — what do you do now, and
   who do you tell?

## 3 · Your first clients

10. Five to ten real clients to load: name, level, usual slot and court, parent's name
    and number, anything medical, consent, collection. The client creates the first
    one from their phone with Ross watching, then the rest.

## After the session — Ross

- [ ] Every `{{FILL}}` answered in the instance repo; `validate.py --for-release` shows none left
- [ ] The rest of `onboarding.md`: release, project, Sync, first run, scheduled tasks, exit tests
