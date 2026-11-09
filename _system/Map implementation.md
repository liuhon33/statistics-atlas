---
id: system-implementation
title: Map implementation
layer: auxiliary
connections:
- '[[AGENTS]]'
---

# Map implementation

Plugin: `statistics-atlas`, local, no external dependencies or network requests. The plugin reads Markdown properties and shows a custom ItemView using the documented Obsidian API. It does not rewrite notes.

Live authority: note properties. `_system/baseline/statistics-backbone.json` is the frozen original; `_system/layout.json` preserves original ordering, coordinates, colors and the baseline edge metadata. *[Claude · A1, 2026-11-08]* Backbone cross-links are declared in typed properties on the page where the arrow starts: `prerequisite_for`, `applied_in` and `related`. Learning and auxiliary notes declare untyped extra edges in `connections`. One-line body reasons explain every link, and the plugin reads reasons only from the body. The plugin no longer reads the baseline JSON; it reads the notes plus `_system/layout.json`. `sources` creates separate provenance edges visible only in Everything. Plain-text paths, body links, and tags create no conceptual edges. *[Claude · fix 5, 2026-11-08]* Layer: an explicit `layer` property wins. When it is missing, the folder decides (`Learning/` → learning, `Backbone/` → backbone, otherwise auxiliary; `_system/`, `raw/`, `assets/` and root admin files are always auxiliary), and Map checks lists a hint. Unknown values fall back to the folder, and declared values that disagree with the folder are flagged. Covered by the layer-fallback block in `test-model.cjs`.

The original all-level radial layout is retained. Depth filters hide nodes without moving their saved positions. Branch focus zooms the same fixed geometry. A new backbone ID without a saved position is shown as a provisional placement with a warning; approving and recording a new layout is a separate maintenance decision.

The native Obsidian graph remains available and follows its own wikilink behavior. This plugin does not modify graph.json.

Source: `_system/plugin-src/`. Checks: `_system/tools/validate.py`, `_system/tools/test-model.cjs` and `_system/tools/test-refresh.cjs`. Rebuild the plugin by concatenating core.js, ui.js, plugin.js in that order into `.obsidian/plugins/statistics-atlas/main.js`, then reload the plugin. Preserve changes to notes; do not rerun the initial page generator over an edited vault.

References: [Obsidian custom views](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/User%20interface/Views.md), [plugin installation](https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin).

Live page block (Claude, 2026-11-08, AGENTS A2): the plugin registers a ```atlas``` code-block renderer. Each backbone page ends with an empty block that shows Topics, Connected from and My notes here, computed by `AtlasCore.pageLinks` from the current model and re-rendered on every model refresh. It replaces the generated Topics/Connected-from text; see `_system/tools/migrate_live_block.py`.

Incremental refresh (Claude, 2026-11-08, AGENTS A5): the plugin keeps an `AtlasCore.RecordStore` of each note's properties (from Obsidian's metadata cache) and its `- [[target]] — reason` lines; other note text is not kept. Edit events mark only the affected file. A refresh rebuilds the model and redraws views and page blocks only when a stored signature changed. The first `resolved` event after startup triggers one full rescan; folder renames and the **Refresh statistics atlas** command do too. `layout.json` is cached and re-read when it is modified. Covered by `_system/tools/test-refresh.cjs`; details in `_system/Claude/Refresh.md`.

Direction chevrons (Claude, 2026-11-08): prerequisite and application links are dashed lines with filled chevrons spaced along them, pointing source → target (`AtlasUI.chevrons`). There is no end arrowhead, so direction stays readable where many links meet one node.

Drawing cost (Claude, 2026-11-08, review item 14): pointer moves repaint only when the hovered dot changes. Theme colours and wrapped label sizes are cached (`AtlasUI.theme`, `AtlasUI.labelBox`) and reset by the theme observer. While a dot is hovered or selected, `paint()` keeps the faded web in an off-screen canvas (`paintScene(ctx,'base')`), keyed on camera, view, depth, focus, canvas size and theme, and draws only the highlighted neighbourhood and labels over it (`paintScene(ctx,'overlay',active)`). With nothing highlighted it draws the full scene as before.

Compact controls (Claude, 2026-11-08, review item 15): the view is a flex column. One toolbar row holds the view switch, search (results as a dropdown), the levels select and icon buttons (`AtlasUI.iconButton`, which uses Obsidian's `setIcon` when the host passes it and a text glyph otherwise). The map stage fills the remaining height. Legend and status sit in an overlay in the map's bottom corners. The side panel holds the selection details (`panelBody`), **Browse all topics** and **Map checks**; `setPanel` hides it, and the view state saves it as `panel`. `resize()` keeps the map centre fixed when the stage changes size. The administration cluster (auxiliary records that are not cited sources) is laid out in `compile()` on a sunflower in the top-right corner, just beyond the outermost placed dot.

Notes only view (Claude, 2026-11-08, AGENTS A12): a fourth button in the view switch, mode `notes`. `AtlasCore.visible` hides every backbone and auxiliary node in this mode, so the only links drawn are note-to-note `connections`. Notes stay at their halo positions and the camera does not move; press Fit to zoom onto them. Levels do not apply, so the levels select is disabled. A branch focus carried over from another view keeps only the notes homed in that branch, and the side panel offers **Show all my notes**. With nothing selected, the panel lists the visible notes by subject, and search lists notes only. A topic picked from a note's panel (path, primary home, connection) switches to My learning, so it is visible. `AtlasCore.MODES` lists the four views, and the saved view state accepts `notes`. Covered by the Notes only block in `test-model.cjs`.


Publication portability (Codex, 2026-11-09): machine-readable migration evidence (`_system/Migrations/*.json`) is loaded as auxiliary source records, alongside raw sources and figures. `validate.py --export` includes matching non-Markdown records so the model checks reproduce the live plugin. The refresh test uses the same file scope. Validator regression fixtures compare full findings against the starting vault before reducing them to rule names, allowing approved backbone growth while still detecting new warnings.
