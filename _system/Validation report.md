---
id: system-validation
title: Validation report
layer: auxiliary
---

# Validation report

Completed on 2026-11-08 for the initial build in `D:\obsidian_centre\stats_ML_rebuild`.

## Backbone and files

- 756 backbone pages: L1 3; L2 22; L3 51; L4 104; L5 576.
- All 843 typed, directed baseline connections preserved: 753 hierarchy edges and 90 cross-links.
- All stable IDs, parents, study bands, subjects, breadcrumbs, and connection reasons matched against the frozen baseline. The approved display-title change is ELBO, retaining Calculate the ELBO as its alias.
- 28 source records. No broken generated wikilinks, duplicate IDs, or case-insensitive path collisions. The longest absolute backbone path is 234 characters.
- Backbone coordinates matched the original JavaScript layout formula to within 1e-8, with its original ordering and color families.
- Zero personal learning notes and no migrated raw files. The source-vault audit covered 158 files across wiki/, raw/, and AGENTS.md; all hashes remained unchanged. Five of the six tracked pre-existing rebuild files matched their original hashes, including the SOP draft and Welcome page. Obsidian's native graph.json changed during the live app session; the installer and plugin do not write that file, and its current app state was preserved.
- The preserved Welcome.md tutorial and historical SOP draft are outside the generated-content link audit. Their original content was retained.

## Graph behavior and interface

- Model tests passed for the complete backbone and level filters.
- Two synthetic learning notes and a shared PDF were tested outside the vault: one primary home each, three selected backbone links, a note-to-note link, one shared source dot, and no line from an incidental body mention. No fixture was installed as user learning material.
- The first two modes exclude auxiliary records. Sources appear only in Everything. Adding those fixtures did not change any backbone coordinate. Invalid primary homes were reported.
- Browser checks covered all three switches, fixed camera on mode changes, title/alias search, branch focus, level filtering, note-open callback, source visibility, and a 390-pixel layout without horizontal overflow. The final preview had no browser console errors.
- The JavaScript plugin bundle passed Node syntax checking.

## Live Obsidian check

Verified in Obsidian 1.15.0 after the user enabled the plugin at Obsidian's first-use trust prompt. The plugin loaded and displayed 756 backbone topics. Backbone showed 756 nodes and 843 edges; My learning showed the same backbone with the explicit zero-notes message; Everything showed 799 nodes and 2293 total conceptual/provenance connections, including the preserved administrative files.

Searching Calculate the ELBO returned ELBO. Selecting it showed its full five-level path and connection reasons. Open note opened the actual nested ELBO.md page, displaying the approved title/alias, level, subject, study band, tags, parent, sources, and plain-text breadcrumb.

The standalone [[_system/Previews/backbone-map.jpg|map preview]] uses the same renderer. It is a preview of this initial scaffold, not an imported learning note.

## Scope and rerunning

These are structural and application checks, not verification of mathematical explanations on every page. The initial reference pages intentionally contain titles and relationships rather than full lessons. Personal-note behavior was checked with synthetic fixtures; existing-note migration has not started.

Initial-build checks (Python with PyYAML and Node.js required):

```powershell
python _system/tools/validate.py . --export "$env:TEMP/statistics-atlas-check.json"
node _system/tools/test-model.cjs "$env:TEMP/statistics-atlas-check.json"
node --check .obsidian/plugins/statistics-atlas/main.js
```

The initial-build validator intentionally expects the frozen 756-node scaffold and no personal notes. Adapt its expectations during a separately authorized expansion or migration.

*[Claude · A3, 2026-11-08]* Superseded: `validate.py` now checks rules that always hold and reports baseline differences as non-failing changes; PyYAML is optional. Also run `python _system/tools/test_validate.py`. See [[_system/Claude/Validator|the validator notes]]. The plugin's own Map checks report current metadata/link issues. Do not rerun the initial page generator over edited content; its hash guard refuses overwriting changed files.
