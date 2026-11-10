# _system — the engine

The rules every other folder obeys: names, record shapes, allowed values, policies,
which modules are live, and which structure version this is. The coach's agent reads here
and never writes anywhere in Structure.

## Not this?

- A rate, a court, a level, the coach's voice → `_settings/CONTEXT.md` (The coach's values, in his Drive).
- A client's record → `clients/CONTEXT.md`.

## Goal

Every record in `drive:/` conforms to `schema.md`, and the coach is never silently running
an old version of the structure.

## Inputs

- **Reference:** `conventions.md`, `schema.md`, `policies.md`, `modules.yml`; `version.md` at the top of `workspace/`.
- **Working:** `drive:/_release.md`, for the version check only.

## Outputs

None from the coach's agent. Ross's tools (outside this snapshot) write
`drive:/_index/*`, `drive:/FILE-MAP.md` and `drive:/_release.md`.

## Process

| Job | How |
|---|---|
| Version check | `version.md` (top of `workspace/`) § The version check — once a day, in the morning court sheet |
| Anything else here | Ross's, from his own machine |

## Human check

Ross reads `drive:/_requests/` on the settling-curve cadence: daily in weeks 1–4,
twice weekly to week 12, weekly after that.
