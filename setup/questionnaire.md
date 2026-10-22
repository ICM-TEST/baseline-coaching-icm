# Setup — one sitting with Kyle (Ross only)

Ross works through this with Kyle before the first release of Kyle's instance repo.
Every `{{FILL}}` in the instance repo is answered here. Allow about 90 minutes, plus Kyle's phone for the
WhatsApp screenshots. Write answers straight into the file named in brackets.

## Before the session — Ross

- [ ] Kyle's instance repo created from the template, under the GitHub organization (`onboarding.md`)
- [ ] Kyle's Claude plan covers connectors and scheduled tasks
- [ ] Courtside day booked in week 2 or 3 — in the calendar now, before there's anything to watch

## 1 · Accounts and access

1. Which Google account do you use for your calendar and Drive? (`_shared/coach.md` → `calendar-id`)
2. What should your coaching folder in Drive be called? You'll own it and share it with Ross. (`setup/project-instructions.md`)
3. Does a club booking system already own any of your calendar? If yes, which hours — that becomes a boundary, not something we write to.
4. Ross will be an editor on your folder so he can maintain it, which means he can read your notes. Are you comfortable with that? Your words go in `_system/policies.md`.
4a. Signed agreements and consent forms stay out of Drive. Who keeps them, and where? (`_system/policies.md`)

## 2 · Where and when you coach (`_shared/coach.md`)

5. Your coaching hours, each day.
6. Every court you use: name, where, and the slug we'll call it. Lights, access, parking quirks go to `drive:/library/courts/` — that part is yours to keep updating.
7. Realistic drive time between each pair of courts at the times you actually drive.
8. How much buffer do you want between back-to-back lessons on the same court?
9. Expiry dates: coaching qualification, first aid, police clearance. Where are the certificates?

## 3 · Money and policy (`_shared/rates.md`)

10. Your rates for each lesson length you offer.
11. Do you sell blocks or packages? How many lessons, what price, how paid, do they expire?
12. **Your cancellation and no-show policy, exactly as you'd say it to a parent.** We write it down word for word.
13. Then the table: how much notice avoids a charge? Late cancel? No-show? Rain?

## 4 · Levels (`_shared/curriculum.md`)

14. Red, orange, green, yellow, adult — is that how you group players? Change, split or rename anything.

## 5 · Your voice (`_shared/voice.md`)

15. Screenshot about twenty messages you've sent parents and players — reminders, reschedules, late cancels, a no-show, some good news. Ross removes names and writes the pattern.
16. Anything you'd never say in a message?

## 6 · Minors and safety

17. For a junior, who gets the calendar invite — a parent, the player, or both?
18. What medical details do you actually need on court? (We keep a twelve-word extract; signed forms stay out of Drive.)
19. Do you film or photograph players? How do you get consent today?
20. Is there any child you coach where someone must not collect them?
21. If something happens on court today — an injury, a fall — what do you do now, and who do you tell?

## 7 · Rule or knowledge?

Walk the list once. Anything you'll want to change monthly should be **knowledge**
(yours, in `drive:/library/`), or Ross becomes your bottleneck. Mark each R or K:

court list · travel times · levels · drill library · programme designs · rates ·
package terms · cancellation policy · message templates · what a brief contains

## 8 · Your first clients

22. Five to ten real clients to load by hand: name, level, usual slot and court,
    parent's name and number, anything medical, consent, collection. Kyle creates
    the first one himself from his phone with Ross watching, then the rest.

## After the session — Ross

- [ ] Every `{{FILL}}` answered in the instance repo; `validate.py --for-release` shows none left
- [ ] `voice.md` written from the screenshots
- [ ] The rest of `onboarding.md`: release, project, Sync, first run, scheduled tasks, exit tests
