# _shared — the rules

The facts that change how the system **behaves**: what lessons cost and what happens
when one is cancelled, where Kyle coaches and how long it takes to get between courts,
how he sounds in a message, and which levels exist. Every module reads from here;
nothing writes to it except Ross, through a release.

## Not this?

- A drill, a programme design, a note about a court's lights → `library/CONTEXT.md`.
  That is knowledge, and Kyle adds it freely.
- Kyle wants a rate, policy, court or level changed → `CLAUDE.md` rule 6
  (Error 500, then offer the request). Carry on under the current rule.

## Goal

Every rule the agent applies has exactly one home, in Kyle's own words, here.

## Inputs

- **Reference:** none. This folder is the reference everything else reads.

## Outputs

| File | Holds | Read by |
|---|---|---|
| `coach.md` | calendar, hours, courts, travel times, clearances | `01_schedule`, `clients` |
| `rates.md` | rates, packages, cancellation and no-show policy | `01_schedule`, `clients` |
| `voice.md` | how Kyle writes to parents and players | every message draft |
| `curriculum.md` | the closed list of levels | `clients` |

## Process

Read the one file the task names. Never restate a rule into another file — link it.
