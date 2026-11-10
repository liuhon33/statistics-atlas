---
id: system-claude-readme
title: Claude's working notes
layer: auxiliary
created: '2026-11-08'
updated: '2026-11-08'
tags:
- atlas/auxiliary
- claude
---

# Claude's working notes

Documentation of maintenance work done by Claude (Anthropic) in this vault, kept apart from Codex's records. These are auxiliary pages: they appear only in the atlas's **Everything** view. [[AGENTS]] remains the authoritative SOP; every SOP change made by Claude is signed in [[_system/SOP/Amendments]] (AGENTS §13) and logged in [[_system/Log]].

| Note | What it covers | SOP amendment |
|---|---|---|
| [[_system/Claude/Review fixes 2026-11-08\|Review fixes, 2026-11-08]] | What each forked chat fixed after the review of Codex's build, with commits, and what is still open | A1–A4, A7 |
| [[_system/Claude/Refresh\|Atlas refresh]] | Incremental refresh: properties from Obsidian's cache, rebuild only when the map changes; `test-refresh.cjs` | A5 |
| [[_system/Claude/Validator\|Vault validator]] | Rule-based `validate.py`, its 23 rules, the before/after test, the regression test, and the plugin model test split into frozen-fixture and live checks | A3, A4 |

Earlier Claude changes are recorded in the amendment ledger and the log: typed backbone links (A1), the live page block (A2), the canvas-smear fix, direction chevrons, and the layer fallback.
