---
status: placeholder        # becomes active once every {{FILL}} is answered
calendar-id: "{{FILL: Kyle's Google Calendar id — usually his Gmail address}}"
timezone: Africa/Johannesburg
---

# Coach

## Hours

| Day | From | To |
|---|---|---|
| Mon–Fri | {{FILL: first lesson}} | {{FILL: last lesson ends}} |
| Sat | {{FILL}} | {{FILL}} |
| Sun | {{FILL: or "off"}} | |

## Courts

The `court:` field on a client must be a slug from this table.

| Slug | Name | Where | Notes |
|---|---|---|---|
| {{FILL: e.g. kelvin-grove-3}} | {{FILL}} | {{FILL}} | {{FILL: lights, access, parking}} |

## Travel time between courts

Minutes, door to door at the times Kyle actually drives. Booking refuses a slot that
doesn't leave this gap.

| From → To | Minutes |
|---|---|
| {{FILL}} → {{FILL}} | {{FILL}} |

Same court, back-to-back: {{FILL: minutes of buffer Kyle wants, 0 if none}}.

## Clearances

Each one is checked by the morning court sheet. **Sixty days before expiry**, the
sheet carries one line saying what expires and when. An expired one is a line every
day until it is renewed.

| Clearance | Expires | Where the certificate is |
|---|---|---|
| Coaching qualification | {{FILL: YYYY-MM-DD or "none"}} | {{FILL: vault:// pointer}} |
| First aid | {{FILL}} | {{FILL}} |
| Police clearance / working with children | {{FILL}} | {{FILL}} |
