---
id: system-claude-review-fixes
title: Review fixes, 2026-11-08
layer: auxiliary
created: '2026-11-08'
updated: '2026-11-08'
tags:
- atlas/auxiliary
- claude
---

# Review fixes, 2026-11-08

On 2026-11-08 Claude reviewed Codex's initial build (the statistics-atlas plugin and the 756-page backbone). The review found 15 items, split into "must fix", back end and front end. The user then worked through several of them in separate forked chats. This page records what each chat did, so the forks could be deleted afterwards. Per-change detail is in each commit message, in [[AGENTS]] §13 (amendments A1–A4) and in [[_system/Log]].

## Done

| Review item | Commit | What changed |
|---|---|---|
| 1. 156 broken source links | `c2c8995` | `_system/Sources/Bayesian Data Analysis.md` renamed back to `bda.md`. Content unchanged (hash matches the build manifest). All 4,745 vault links resolve. |
| 2. Link types only in the frozen JSON | `a95921f` (A1) | Backbone cross-links moved from untyped `connections` to typed properties on the page where the arrow starts: `prerequisite_for` (24), `applied_in` (30), `related` (36). The plugin reads types from notes and node order from `layout.json`, and no longer reads the baseline JSON. Added `build_plugin.py`. |
| 3. Hand-copied lists go stale | `5aa56f6` (A2) | Removed the generated `## Topics` (180 pages) and `## Connected from` (63 pages) sections. All 756 pages get an empty `atlas` code block that the plugin fills live: Topics, Connected from (type and reason) and My notes here. The block writes nothing back, and Ctrl-click opens a new tab. |
| (found while testing) Map smears when dragged | `b5737ff` | Each redraw now re-syncs canvas size and pixel ratio and clears the whole bitmap, so a reset canvas no longer draws into a corner. Redraws are limited to one per animation frame (partly covers item 14), the map redraws on `contextrestored`, and the canvas tooltip is fixed. |
| (follow-up) Arrowheads crowd at the target | `b2a1839` | Prerequisite and application links carry small chevrons along the whole dashed line, pointing source → target, instead of one arrowhead at the end. Related links stay dotted without chevrons. |
| 5. Notes without `layer` vanish | `cd151d8` | An explicit `layer:` wins; otherwise the folder decides (`Learning/` → learning, `Backbone/` → backbone, else auxiliary). Map checks warns about a missing value, an unknown value, or a value that disagrees with the folder. Six new model tests. |
| 7. Validator fails on first digest | `6430dae` (A3) | `validate.py` rewritten as 21 error rules, 2 warnings, and a non-failing change report against the baseline. 15-case regression test `test_validate.py`. PyYAML is now optional. See [[_system/Claude/Validator]]. |
| (follow-up to 7) Model test pinned to snapshot | `d566e83` (A4) | `test-model.cjs` asserts the exact 756/843 counts only on a vault rebuilt from the baseline JSON. On the live vault it checks only rules that always hold. |
| 8. Refresh efficiency | (A5) | The atlas refreshes incrementally. Properties come from Obsidian's metadata cache, and only reason lines are kept from note text (23,671 instead of 520,772 characters). It rebuilds and redraws only when a property or reason line changed, and reads `layout.json` once. New `test-refresh.cjs`. Done in this session, not a fork. See [[_system/Claude/Refresh]]. |
| 11. Learning notes would crowd the outer ring | (A7) | Notes no longer spiral 65–110 units around their home, where they would cover neighbouring level-5 dots (about 18 units apart) or point inward. They sit on a halo 60 units beyond the outermost backbone dot, inside the home's slice: one column for a level-5 home, spread across the subtree arc for a broader home. Slots are fixed and filled in `created` order, then id, so a newer note never moves older ones. Halo checks added to `test-model.cjs`. Done in this session. Not yet seen in the app, because there are no learning notes yet. |
| 14. Map redraws too much | (this session) | Two tiers in `ui.js`. Tier 1: the map repaints only when the hovered dot changes (moving within a dot or over empty space just moves the tooltip), and theme colours and wrapped label sizes are cached until Obsidian's theme changes. Tier 2: while a dot is hovered or selected, the faded web is drawn once into an off-screen canvas, rebuilt when the camera, view, size or theme changes, and each frame copies it and draws only the highlighted neighbourhood and labels on top. Measured in headless Chrome on vault data, 400 mouse moves: backbone 963 → 268 ms of drawing, Everything with 200 synthetic notes 3,836 → 471 ms (400 → about 90 redraws). With nothing highlighted the output is pixel-identical; while hovering, about 0.1% of pixels differ, where a highlighted line now sits on top of a faded dot. Each paint also sets line width and text alignment itself; previously the admin label and box inherited them from the previous frame. Dragging and zooming are unchanged (about 9 ms per frame with 200 notes). A rejected first attempt, batching all lines of one style into one path, made frames slower. |
| 15. Controls take a lot of room | (this session) | One toolbar row (view switch, search, levels, icon buttons for whole web / fit / zoom / side panel). Search results are a dropdown (Enter picks the first, Escape clears). Legend and status float in the map's empty bottom corners. Topic browser and Map checks moved into the side panel, which can be hidden; the choice is saved with the workspace, and a dot on the panel button flags open map checks. The map fills the rest of the tab (it used to get the window height minus about 270 px) and keeps its centre when the panel or pane changes size. Narrow pane: panel under the map. The Everything view's administration cluster moved from x≈2400 into the empty top-right corner, so Fit no longer shrinks the web by about a fifth. Checked in a browser page built from the vault export; not yet in the app. |
| (housekeeping) App state | `be643bc` | Committed working-tree app changes the user made in Obsidian: the obsidian-git plugin, enabled plugins, graph zoom, `Untitled.base`. |

## Discussed, no change

- **Item 4, nested vs flat folders.** Comparison only. Link length doesn't depend on the layout: links currently spell out the full folder path (about 144 characters on average, 1,686 of them in backbone pages), and short `[[Title]]` links would work with any layout because titles are unique. The recommendation was a middle option: three subject folders with flat notes inside, so the hierarchy lives only in `parent:`. Nested currently uses 234 of the 260-character Windows path limit. **Open decision for the user.**

## Still open from the review

- 4: short links, plus the folder decision above
- 6: a "Recompute and save layout" command for new backbone nodes
- 9: native-graph clutter from `sources` links
- 10: highlight the full path from the centre to the selected dot on the map
- 12: choose the colours (blue/yellow/pink from the original web, or the plugin's blue/orange/green)
- 13: open notes in the same tab by default; make auto-open on launch a setting

None of these changes have been checked live in the running Obsidian app unless the commit says so. Reload the Statistics atlas plugin to pick them up.
