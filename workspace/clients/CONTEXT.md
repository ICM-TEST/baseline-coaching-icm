# clients — the record library

One folder per client: who they are, how to reach the family, what keeps them safe
on court, and a dated log of everything that happened. Kyle creates, updates and
archives records freely; the agent writes every new one from the template. The
records live in `drive:/clients/`; this folder holds only the contract.

## Not this?

- Booking, moving or cancelling a lesson → `01_schedule/CONTEXT.md`.
- A drill or a programme design → `library/CONTEXT.md`.
- A rate, policy, level or court of his own → `_settings/CONTEXT.md`.
- A record-shape change — a new field or kind of record → Error 500 (`CLAUDE.md` rule 6).

## Goal

Any client's record answers "who is this, how do I reach the family, and what do I
need to know to keep them safe today" in one read.

## Inputs

- **Working:** what Kyle says; the client's own folder, `drive:/clients/<slug>/`.
- **Reference:** `_templates/client/`, `_templates/incident.md`,
  `_templates/agreement.md`, `drive:/_settings/levels.md`, `drive:/_settings/coach.md`
  (court slugs), `_system/schema.md`, `drive:/_index/roster.md`.

## A record

```
drive:/clients/<slug>/
├─ client.md          the record card — frontmatter + a few lines of prose
├─ log.md             dated: messages, admin, schedule changes, money, parent conversations
├─ programme.md       dormant until Phase 3
├─ sessions/          one note per lesson — Phase 1 writes only charged-cancellation stubs
├─ agreements/        one file per signed coaching agreement (pointer to the vault)
├─ incidents/         one file per incident, append-only
└─ output/            what has been sent to them
```

No file inside a record is ever named `CONTEXT.md`, `SKILL.md` or `CLAUDE.md`.

## Outputs

The record files above, and one-line confirmations to Kyle.

## Process

| Kyle says something like | Workflow in `SKILL.md` |
|---|---|
| "New client, Sarah Ndlovu, green ball, Tuesdays 4pm, mum's Lerato" | Create a client |
| "Ethan's mum's number changed" / "he's on yellow ball now" | Update a record |
| "Sarah has asthma" / "only her dad can fetch her" / "mum's fine with filming" | Safeguarding details |
| "Ethan took a ball to the eye" / anything that happened to a child | **Incident report — before anything else** |
| "Signed agreement for Ethan" | Add an agreement |
| "Michael's stopped" / "Michael's back" | Archive / reactivate |

Phone budget: every workflow resolves in four Drive reads or fewer.

## Human check

Kyle confirms archiving once, and reads an incident report before it is final.
Everything else he corrects by chat afterwards.
