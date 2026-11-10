# The workspace — shape, lifecycle, gates

A coaching practice run by chatting to Claude. A **record library** (the unit is a
player, one Doc each) with one **pipeline** beside it (booking), split across two
roots: **Structure** (this repo, read-only) and **Data** (the coach's Drive folder).

## Not this?

To route a task, use `CLAUDE.md`. For names and allowed values, use `_system/schema.md`.

## Goal

Every lesson is booked once at a time that works, nobody is double-booked, and what
the coach knows about a player is in that player's one file.

## Shape

| Layer | Where | Who changes it |
|---|---|---|
| Map and contracts | `CLAUDE.md`, every `CONTEXT.md` and `SKILL.md` | the system provider |
| Engine | `_system/` | the system provider |
| Types — the stamps | `_templates/` | the system provider |
| Settings — the shapes | `_templates/settings/` | the system provider |
| Settings — the values | `drive:/_settings/` | the coach, through the agent |
| Players | `drive:/players/<slug>.md` | the coach, through the agent |

The test for any file: does changing it change what the system **does** (Structure,
the system provider's), or only what it **knows** (Data, the coach's)? Settings are
the one split: what can be set is Structure; what it is set to is the coach's.

## Data folder

```
drive:/                     the coaching folder — any name; found by _coaching-workspace.md
├─ _coaching-workspace.md   the marker
├─ _settings/               coach.md · rates.md · levels.md
└─ players/                 <slug>.md — one Doc per player
```

Nothing else belongs in the data folder. The coach owns all of it and shares it with
nobody; the system provider has no access to it.

## A player's life

`trial → active ⇄ paused → archived`, all as a `status:` change in the player's file.
The file never moves; it is binned only when the coach asks
(`_system/conventions.md` § Deleting from Drive).

## Human gates

| Moment | The coach must |
|---|---|
| Any calendar write — create, move, cancel | confirm the slot or pattern in plain words |
| A cancellation that involves money | confirm the policy outcome |
| Any change to a setting | confirm old and new once |
| Archiving or binning a player | confirm once |
| An incident entry | read it back and confirm it is accurate |
