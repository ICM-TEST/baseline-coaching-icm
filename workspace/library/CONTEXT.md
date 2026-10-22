# library — what Kyle knows

Kyle's coaching knowledge: drills, programme designs, notes on courts, and anything
else he wants the system to know. **Nothing here is a rule**, so nothing here can
break anything — it only makes the agent better informed. Kyle adds, edits and
retires freely, with no involvement from Ross. The shelves live in
`drive:/library/`; this folder holds only the contract.

## Not this?

- About one specific client → `clients/CONTEXT.md`.
- A rate, a policy, a court's travel time, a level → `_shared/` (rules, Ross's). If
  Kyle states one of those as fact ("I'm charging 500 now"), that is a structure
  change — `CLAUDE.md` rule 6 — never a note here. The system must not act on a rule
  it learned from a note.

## Goal

What Kyle knows, written once and findable — so it stops evaporating.

## Inputs

- **Working:** what Kyle says; `drive:/library/`.
- **Reference:** `_shared/curriculum.md` (to tag drills and designs by level).

## Outputs

| Folder | One file per | Name |
|---|---|---|
| `drive:/library/drills/` | drill | `<slug>.md` — what, why, how to run it, which level |
| `drive:/library/programmes/` | reusable programme design | `<slug>.md` — shape and use arrive with Phase 3; Kyle may start writing them now |
| `drive:/library/courts/` | court | `<court-slug>.md` — lights, surface, access, parking, quirks |
| `drive:/library/notes/` | anything else | `YYYY-MM-DD-slug.md` or `<slug>.md` |

## Process

1. Pick the folder from the table. If none fits, use `drive:/library/notes/`.
2. Write it in Kyle's words; add a short title. Frontmatter only if he tags it
   (`level:`, `status:`).
3. Retire rather than bin anything other records point to: `status: retired`. If
   Kyle still wants it gone, `_system/conventions.md` § Deleting from Drive.
4. Confirm in one line where it went.

Write only inside the four shelves — never directly in `drive:/library/`. A new
shelf is a structure change (`CLAUDE.md` rule 6). Never a file named `CONTEXT.md`, `SKILL.md` or `CLAUDE.md`.
