---
id: system-claude-validator
title: Vault validator (rules, not a snapshot)
layer: auxiliary
created: '2026-11-08'
updated: '2026-11-08'
tags:
- atlas/auxiliary
- claude
---

# Vault validator: rules, not a snapshot

Claude (Opus 5.5), 2026-11-08, at the user's request ("yes fix this"; review item 7). Signed in [[AGENTS]] as amendment **A3**.

Files:
- `_system/tools/validate.py`: the validator, rewritten.
- `_system/tools/test_validate.py`: new regression test.

## Why it changed

The initial-build validator compared the vault with the frozen 2026-11-08 snapshot: exactly 756 backbone pages, zero learning notes, and the original titles and edge set. That proved the first build was complete. But the vault is meant to grow, and from the first digest every legitimate change would fail it.

I tested both versions on 11 copies of the vault, each with one realistic change. Five changes were valid and six were mistakes.

| Change | Old validator | New validator |
|---|---|---|
| Vault as it is | pass | pass |
| Add a learning note (ELBO example) | **false alarm**: "Initial build must contain no learning notes" | pass |
| Add a backbone node | **crash**: `KeyError` | pass, plus warning W1 (save map position) |
| Add a typed cross-link | **false alarm**: "Edge set differs" | pass, reported as an added link |
| Retitle a node, old name kept as alias | **false alarm**: "Unexpected title" | pass, reported as retitled |
| Same link added as a second `related:` key | **vague**: "Edge set differs", the same message as the valid link | F0 error; the report also shows the silently dropped link |
| Learning note with two homes | wrong reason ("no learning notes") | L2 error |
| Learning note without `layer` and `primary_home` | **missed**: passes | L1 + L2 errors |
| Connections without reason lines | wrong reason | C2 errors |
| Backbone page links to a learning note | wrong reason | C5 error |
| New node with a 285-character path | **crash** before any path check | F3 error |

The old validator got 1 of 11 right; the new one gets 11 of 11. The duplicate-key case came up by accident. My own test script wrote a second `related:` key into the KL divergence page, and YAML silently kept only the second list. Agents editing properties will make that mistake, so it got a rule.

## Three result levels

- **Error**: a rule below is broken. The exit code is 1.
- **Warning**: allowed, but something needs doing later.
- **Change**: a deliberate difference from the frozen baseline (node added, removed, retitled or moved; cross-link added or removed). It is listed for review and never fails.

The baseline JSON (`_system/baseline/statistics-backbone.json`) is now only a reference for the change report. It never decides pass or fail. The approved rename "Calculate the ELBO → ELBO" shows up as a change in every run; that is expected.

## Rules

| Code | Rule |
|---|---|
| F0 | Properties parse, and no property key appears twice (YAML keeps only the last one) |
| F1 | Every link and embed resolves, in properties and body. Full-path and short `[[ELBO]]` links both work, as in Obsidian. Skipped for `Welcome.md`, the historical SOP draft and `_system/Templates/` placeholders |
| F3 | Full path ≤ 240 characters. Windows' limit is 260; the extra room is for longer titles |
| F4 | No character Windows forbids in a file name |
| B1 | Every backbone and learning note has an `id`, and ids are unique across the vault |
| B2 | Backbone `level` is an integer 1–5 |
| B3 | Level 1 has no parent; any other level has a backbone parent exactly one level up |
| B4 | No parent cycles |
| B5 | `subject` matches the id of the level-1 root |
| B6 | `backbone_path` equals the titles along the parent chain |
| B7 | No two Markdown files share a file name, so short links stay unambiguous |
| B9 | Each backbone page has exactly one live `atlas` block (AGENTS A2) |
| L1 | Pages in `Backbone/` and `Learning/` carry a `layer` property that matches the folder |
| L2 | A learning note has exactly one `primary_home`, and it is a backbone page |
| L3 | `note_types` (required) and `question_roles` use the vocabulary in AGENTS §3/§6 |
| L4 | A learning note's `backbone_path`, if present, equals its home's path |
| C1 | Every `prerequisite_for` / `applied_in` / `related` / `connections` target exists |
| C2 | Each such link has a `- [[target]] — reason` line in the body |
| C3 | No page links to itself |
| C4 | Backbone pages use typed links, never `connections` (AGENTS A1) |
| C5 | Backbone pages never link to learning notes, in properties or text: notes stay leaves |
| W1 | Warning: a backbone node has no saved position in `_system/layout.json`, so the map shows a provisional placement |
| W2 | Warning: several pages share one display title. This is currently the three L4/L5 pairs; their file names keep them apart |

The vocabularies (`NOTE_TYPES`, `QUESTION_ROLES`, `LINK_TYPES`) are constants at the top of `validate.py`. Change them together with the SOP.

## How to run

From the vault root (PowerShell or Git Bash):

```bash
python _system/tools/validate.py .
python _system/tools/test_validate.py
python _system/tools/validate.py . --export "$TEMP/atlas-check.json"
node _system/tools/test-model.cjs "$TEMP/atlas-check.json"
```

- `--json` gives machine-readable output.
- `--display-root` is for checking a copy stored somewhere else: it makes the path-length rule measure against the real vault path.
- PyYAML is optional. Without it, the built-in parser for this vault's flat frontmatter is used. Both give the same result on the current vault.
- On Windows, files are read through the long-path prefix (`\\?\`), so a copy in a deep folder doesn't crash the script.

`test_validate.py` copies the vault to a temporary folder outside the vault once per case and applies one change: the 11 above plus an unknown note type, an aliased `[[page\|alias]]` link inside a table (must pass), a broken image embed and a level-5 node under a level-3 parent. It checks the exact set of error rules, warnings and change kinds for each case. Nothing is written into the live vault (AGENTS §11). It takes about 20 seconds.

## Results on 2026-11-08

- Live vault: **pass**, with 756 backbone pages, 0 learning notes, 3 W2 warnings and 1 change (the ELBO retitle). The result is the same with and without PyYAML.
- `test_validate.py`: 15 of 15 cases pass. Writing these docs also turned up one real gap: table-escaped links like `[[page\|alias]]` were misread. It is fixed, and that case is now in the test.
- `test-model.cjs` on the export: passes.
- `build_plugin.py --check`: bundle up to date.

## Known limits and follow-ups

- *Fixed 2026-11-08 (AGENTS A4).* `test-model.cjs` used to assert 756 nodes / 843 edges / the original link set on the live vault, so it would fail after the first digest. It now runs those exact checks on a vault rebuilt in memory from the frozen baseline JSON (testing the plugin code on a fixed input). On the live vault it checks only rules that always hold: no map issues except the "save layout" warning for new nodes, every backbone node with a saved position stays exactly there, Backbone view shows only backbone pages, My learning never shows auxiliary pages. Checked on a copy with one new backbone node and one learning note: the old test failed, the new one passes (757 backbone, 1 learning).
- The validator checks structure, not mathematics, and not map rendering (colours, views, positions). The plugin's Map checks panel and `test-model.cjs` cover the map.
- A moved node (new parent) is reported as a change, but its descendants' `backbone_path` values must also be updated; B6 will flag each stale one.
