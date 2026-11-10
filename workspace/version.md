---
version: 0.2.0
released: 2026-10-17
---

# Structure version

The version of the structure this snapshot holds. Written only by the system provider's
release tool; never by hand, never by the agent.

## Updates

The system provider releases a new version and tells the coach. The coach then
presses Sync at a computer: claude.ai → the coaching project → settings → Sync. There
is no version check to run, and nothing about versions is ever written to Drive.
Asked "what version is this?" → say the `version:` above.

## What changed

- 0.2.0 (2026-10-17) — Structure and data split: structure in this repo, data in the coach's Drive.
