# _system — the engine

The rules every other folder obeys: names, record shapes, allowed values and
policies. The agent reads here and never writes anywhere in Structure.

## Not this?

- A rate, a court, a level → `_settings/CONTEXT.md` (the coach's values, in the coach's Drive).
- A player's file → `players/CONTEXT.md`.

## Goal

Every file in `drive:/` conforms to `schema.md`.

## Inputs

- **Reference:** `conventions.md`, `schema.md`, `policies.md`; `version.md` at the top of `workspace/`.

## Outputs

None. Nothing in this folder is ever written by the agent, and the system provider
writes nothing in `drive:/`.

## Process

| Job | How |
|---|---|
| "What version is this?" | read `version.md` and say it |
| A change to anything here | the system provider's — `CLAUDE.md` rule 4 |

## Human check

The system provider changes Structure and tells the coach when to press Sync.
