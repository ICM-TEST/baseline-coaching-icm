---
client:              # slug, e.g. ethan-moloi — same as the folder name
name:
status: trial        # trial | active | paused | dormant | archived
dob:                 # YYYY-MM-DD
level:               # from drive:/_settings/levels.md
started:             # YYYY-MM-DD
cadence:             # weekly | fortnightly | block | ad-hoc
default-slot:        # the usual slot in words, e.g. "Tue 16:00". The calendar owns real times.
series-event:        # Google Calendar id of the recurring series — written back at booking
duration: 60         # 30 | 45 | 60 | 90
court:               # court slug from drive:/_settings/coach.md
rate:
rate-unit:           # per-hour | per-session | package
package:             # e.g. "10-lesson block, started 2026-08-01"
guardian:
guardian-phone:
guardian-email:
calendar-attendee:   # who receives the invite — usually the guardian
# ── Safeguarding · Kyle's eyes only · never in an invite or a message draft ──
medical:             # operational extract, 12 words max: "asthma — inhaler in his bag"
medical-source:      # vault:// pointer to the signed intake form, if any
emergency-contact:   # only if different from the guardian
emergency-phone:
media-consent: unknown   # yes | no | unknown — unknown means no filming, no photos
media-consent-date:
may-collect: []      # people allowed to collect the child
may-not-collect: []  # people who must NOT collect the child — surfaced on every court sheet
---

# <name>

## Who they are
<!-- A few lines in Kyle's words: age, school, temperament, why they play. -->

## What they're working towards
<!-- The goal, and whose goal it is — the player's, the parent's, or Kyle's. -->

## Notes
<!-- Anything else worth knowing that isn't a dated event. Dated things go in log.md. -->
