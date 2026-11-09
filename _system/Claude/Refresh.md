---
id: system-claude-refresh
title: Atlas refresh (incremental)
layer: auxiliary
created: '2026-11-08'
updated: '2026-11-08'
tags:
- atlas/auxiliary
- claude
---

# Atlas refresh: rebuild only when the map changes

Claude (Opus 5.5), 2026-11-08, at the user's request ("fix 8"). Review item 8, signed in [[AGENTS]] as amendment **A5**.

Files:
- `_system/plugin-src/core.js`: new `RecordStore` (pure, no Obsidian dependency)
- `_system/plugin-src/plugin.js`: event handling and `update()` / `load()` rewritten
- `_system/tools/test-refresh.cjs`: new regression test
- `.obsidian/plugins/statistics-atlas/main.js`: rebuilt with `build_plugin.py`

## What was wasteful

The plugin rebuilt everything whenever anything happened:

- **Every autosave triggered a refresh.** Any change to any note fired Obsidian's `changed` and `resolved` events. Obsidian autosaves while you type, so this happened every couple of seconds while editing.
- **Every refresh re-read `layout.json`** (106 KB) from disk and parsed it.
- **Every refresh rebuilt the whole model** for all ~800 files.
- **Every refresh redrew everything**: the atlas canvas, the topic tree and search results, and every open backbone page's live block.
- **Prose edits counted too.** Most of those edits changed nothing the map draws, since the map uses only properties and reason lines.
- **YAML was parsed twice.** The plugin parsed each changed note's properties itself with `parseYaml`, although Obsidian's metadata cache had already parsed them.
- **All note text stayed in memory**, 520 KB of body text, although only the reason lines are ever used.

In absolute terms the computation is small: a full model build takes about 5 ms in Node. The cost was doing it, and the redraws, constantly and for no reason, and it would grow with every learning note.

## What it does now

1. **Per-file events.** `changed`, `create`, `delete` and `rename` mark only the file they concern. A short debounce (300 ms) collects them.
2. **Properties from Obsidian's cache.** `load()` takes properties from `metadataCache.getFileCache(file).frontmatter`. It reads the note text only if the note declares links (`prerequisite_for`, `applied_in`, `related`, `connections`), and keeps only its `- [[target]] — reason` lines. A note Obsidian hasn't indexed yet is parsed directly, as before.
3. **Signatures decide.** `RecordStore.set()` compares a stable signature of the properties (key order ignored) plus the reason lines. If nothing changed, there is no rebuild and no redraw.
4. **Full rescans only when needed**: on load, once on the first `resolved` event after startup (when Obsidian has finished indexing), after a folder rename, and on the **Refresh statistics atlas** command.
5. **`layout.json` is cached**, and re-read only when that file is modified or on the Refresh command.

Nothing in the map's output changed. The test checks that the incrementally maintained model equals a from-scratch build after every step.

## Test

`test-refresh.cjs` loads the real bundle against a small fake Obsidian app filled with the live vault export, then replays events:

| Step | Event | Expected |
|---|---|---|
| 1 | Prose added to a backbone page without links | no rebuild, note text not even read |
| 2 | Prose added to a page that declares links | no rebuild |
| 3 | Property order changes, values identical | no rebuild |
| 4 | A reason line edited | rebuild, new reason on the edge |
| 5 | A title property edited | rebuild, new label |
| 6 | Indexing finishes (`resolved`), then again | one full rescan with no rebuild; the second does nothing |
| 7 | New learning note created | rebuild, attached to its home (ELBO) |
| 8 | Note renamed | rebuild, new path |
| 9 | Note deleted | rebuild, node gone |
| 10 | Folder renamed | full rescan, moved note found at its new path |
| 11 | `layout.json` modified, then an unrelated file | layout re-read once, not on the unrelated change |
| 12 | Refresh command | full rescan and layout re-read, one notice |
| 13 | `RecordStore` unit checks | key order ignored, value order matters, delete and prefix delete |

After steps 4, 5 and 7–10 the test checks that nodes, edges, reasons, issues and positions equal a fresh build.

Results on 2026-11-08:
- `test-refresh.cjs`: pass. 10 rebuilds across the whole script: the initial load, the 7 semantic changes, the layout change and the Refresh command. Prose edits, reordering and indexing caused none. `layout.json` was read 3 times: at load, when modified, and on Refresh.
- Note text kept in memory: **23,671 characters instead of 520,772**.
- `test-model.cjs`, `validate.py` and `build_plugin.py --check`: pass.

To run:

```bash
python _system/tools/validate.py . --export "$TEMP/atlas-check.json"
node _system/tools/test-refresh.cjs "$TEMP/atlas-check.json"
```

## Limits

- *Update 2026-11-08: confirmed working in Obsidian after the `loadRecord` fix below.* Original note: **Not yet checked live in Obsidian.** The test uses a fake app that implements only the calls the plugin makes. Reload the plugin (Settings → Community plugins → Statistics atlas off and on) to pick up the new version.
- When a change does matter, the whole model is still rebuilt (about 5 ms) and the canvas fully redrawn. Rebuilding only part of the model isn't worth the complexity at this size.
- Labels are still re-measured on every frame the canvas redraws. That is review item 14 (cache label layouts), not part of this fix.

## Fix: the plugin would not start (2026-11-08)

The A5 change added a plugin method named `load(file)` to read one note into the record store. Obsidian starts every plugin by calling its `load()` method (inherited from Obsidian's `Plugin`/`Component`), so the new method replaced it. Obsidian then called `load()` with no file, startup threw, and Settings showed "Failed to load plugin statistics-atlas". The fake app in `test-refresh.cjs` called `onload()` directly, so the test never noticed.

- Renamed the method to `loadRecord(file)`.
- `test-refresh.cjs` now starts the plugin the way Obsidian does (`plugin.load()`). It also fails if the plugin class defines any Obsidian lifecycle name (`load`, `unload`, `loadCSS`, `onUserEnable`, `loadData`, `saveData`, `register`, `addChild`, `removeChild`). On the old code it fails with "plugin class overrides Obsidian's load()"; on the fixed code it passes.
- Found with a temporary diagnostic build that logged the startup steps to a file. With the wrapper in place Obsidian's own `load()` was restored, so the plugin opened, but every file read went to it instead of `loadRecord` and the map came up empty. That build has been replaced by the normal one.
