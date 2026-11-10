# library — what the coach knows

The coaching knowledge: drills, programme designs, notes on courts, and anything
else he wants the system to know. **Nothing here is a rule**, so nothing here can
break anything — it only makes the agent better informed. The coach adds, edits and
retires freely, with no involvement from Ross. The shelves live in
`drive:/library/`; this folder holds only the contract.

## Not this?

- About one specific client → `clients/CONTEXT.md`.
- A rate, a policy, a court's travel time, a level → `_settings/CONTEXT.md`. If
  the coach states one of those as fact ("I'm charging 500 now"), that is a settings
  change to confirm there — never a note here. The system must not act on a rule
  it learned from a note.

## Goal

What the coach knows, written once and findable — so it stops evaporating.

## Inputs

- **Working:** what the coach says; `drive:/library/`.
- **Reference:** `drive:/_settings/levels.md` (to tag drills and designs by level).

## Outputs

| Folder | One file per | Name |
|---|---|---|
| `drive:/library/drills/` | drill | `<slug>.md` — what, why, how to run it, which level |
| `drive:/library/programmes/` | reusable programme design | `<slug>.md` — shape and use arrive with Phase 3; the coach may start writing them now |
| `drive:/library/courts/` | court | `<court-slug>.md` — lights, surface, access, parking, quirks |
| `drive:/library/notes/` | anything else | `YYYY-MM-DD-slug.md` or `<slug>.md` |

## Process

1. Pick the folder from the table. If none fits, use `drive:/library/notes/`.
2. Write it in the coach's words; add a short title. Frontmatter only if he tags it
   (`level:`, `status:`).
3. Retire rather than bin anything other records point to: `status: retired`. If
   the coach still wants it gone, `_system/conventions.md` § Deleting from Drive.
4. Confirm in one line where it went.

Write only inside the four shelves — never directly in `drive:/library/`. A new
shelf is a structure change (`CLAUDE.md` rule 6). Never a file named `CONTEXT.md`, `SKILL.md` or `CLAUDE.md`.
