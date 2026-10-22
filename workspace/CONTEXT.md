# The workspace — shape, lifecycle, gates

Kyle's coaching practice, run by chatting to Claude. A **record library** (the unit is
a client) inside an **umbrella** (a shared factory plus numbered operating modules),
split across two roots: **Structure** (this repo, read-only) and **Data** (Kyle's
Drive folder).

## Not this?

To route a specific task, use `CLAUDE.md`. For names and allowed values, use
`_system/schema.md`.

## Goal

Every lesson is booked once and reminded once, nobody is missed or double-booked, and
anything Kyle knows about a player is written where the next brief will find it.

## Shape

| Layer | Where | Who changes it |
|---|---|---|
| Map and contracts | `CLAUDE.md`, every `CONTEXT.md` and `SKILL.md` | Ross |
| Engine | `_system/` | Ross |
| Types — the stamps | `_templates/` | Ross |
| Rules | `_shared/` | Ross |
| Instances | `drive:/clients/<slug>/` | Kyle, through the agent |
| Knowledge | `drive:/library/` | Kyle |
| Module output | `drive:/01_schedule/` | the agent; Kyle reads and sends |
| Change control | `drive:/_requests/` | Kyle writes, Ross answers in the file |
| Unrouted capture | `drive:/_inbox/` | Kyle |
| Generated | `drive:/_index/`, `drive:/FILE-MAP.md` | Ross's scripts only |
| Release marker | `drive:/_release.md` | Ross's `release.py` only |

The test for any file: does changing it change what the system **does** (Structure,
Ross's), or only what it **knows** (Data, Kyle's)?

## Data folder

```
drive:/
├─ clients/<slug>/     client.md · log.md · programme.md · sessions/ · agreements/ · incidents/ · output/
├─ library/            drills/ · programmes/ · courts/ · notes/
├─ 01_schedule/        briefs/ · messages/ · court-sheets/
├─ _requests/  _inbox/
├─ _index/             roster.md · open-items.md · money.md   [generated]
├─ FILE-MAP.md         [generated]
└─ _release.md         [Ross]
```

Nothing else belongs at the top of the data folder. A dormant module gets its
`drive:/0N_<name>/` folder only when it goes live.

## Modules

| Module | State | Job |
|---|---|---|
| `01_schedule/` | **live** | book, recur, reschedule, cancel, remind, court sheet, skeleton brief |
| `02_sessions/` | dormant — Phase 2 | courtside capture → session note |
| `03_programmes/` | dormant — Phase 3 | programme designs and progression |
| `04_money/` | dormant — Phase 4 | lessons delivered, invoices, payments |
| `05_review/` | dormant — Phase 5 | weekly and term review |

The switch is `_system/modules.yml`. A dormant module's contract says so on its first
line; an agent never does that module's work.

## A client's life

`trial → active ⇄ paused → dormant → archived`, all as a `status:` change in
`client.md`. The folder never moves; it is binned only when Kyle asks
(`_system/conventions.md` § Deleting from Drive). Coming back is a flip back
to `active`.

## Human gates

| Moment | Kyle must |
|---|---|
| Any calendar write — create, move, cancel | confirm the slot or pattern in plain words |
| A cancellation that involves money | confirm the policy outcome |
| Any message to a client or parent | send it himself |
| Archiving a client | confirm once |
| An incident report | read it and confirm it is accurate |
