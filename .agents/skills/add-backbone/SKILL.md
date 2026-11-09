---
name: add-backbone
description: Add a missing concept to the statistics atlas backbone as a new node at the right place in the hierarchy, with a short sourced definition. Use when the user says "add backbone" or asks for a new backbone topic, such as the Hilbert-space view of random variables.
---

# add-backbone: a new backbone node

Rules: AGENTS §2, §3 and §5. A node's placement is structural and costly to move later, so take care.

1. **Check it is really missing.** Search titles and aliases across `Backbone/` and `_system/Catalog.md`, including neighbouring branches and synonyms. For example, the Hilbert-space view of random variables already partly exists as "L2 conditional projection" (under Conditional expectation) and "Orthogonal projection" (under Vectors, spaces & projections). If an existing page covers the concept, propose an alias or `enrich` instead of a duplicate.
2. **Propose the placement:**
   - the parent, with one or two alternatives and why;
   - the level: one below the parent, usually level 5 under a level-4 chapter;
   - the title, `id` and `study_band`;
   - any typed links, each with its type, direction and a one-line reason. `prerequisite_for` means "needed to understand the target", `applied_in` means "used in the target", and `related` is a conceptual link without direction.

   Wait for the user's agreement unless they already gave the parent and the links. Changing an existing page's title, parent or links always needs explicit agreement.
3. **Create the page like its siblings:** copy a sibling's frontmatter and replace the values.
   - **Path.** Level 5: `<parent's folder>/<Title>.md`. Levels 2–4: a new folder, `<parent's folder>/<Title>/<Title>.md`. The file name must be unique in the vault (add a branch qualifier on a clash) and free of Windows-forbidden characters, and the full path under 240 characters.
   - **Properties:**
     - `id`: unique, kebab-case; at level 5, `<parent-id>-<title-slug>`.
     - `title`; `layer: backbone`; `level`; `subject` (the root's); `study_band`.
     - `backbone_path`: the full ancestry joined by ` → `.
     - `created` and `updated` as quoted dates; `aliases`.
     - `tags`: `atlas/backbone`, `subject/<subject>`, `level/<n>` and `study/<tag>`. The study tag follows the band: Foundation → `foundation`, U → `undergraduate`, U–M → `undergraduate-masters`, M → `masters`, M elective → `masters-elective`, U–M elective → `shared-elective`.
     - `node_kind`: `knowledge point` at level 5, `group` above.
     - `parent`: the full link to the parent page.
     - the agreed typed links, and `sources`.
   - **Body:** `# Title`, the plain-text path, `Parent: [[full/path|Title]]`, the reference block (`.agents/skills/enrich/SKILL.md`, step 3), then `## Connections` with a reason line for each outgoing typed link. The empty atlas block comes last: three backticks followed by `atlas`, then a closing fence.
   - An agreed *incoming* link belongs on the other page: add its property there, with a reason line under that page's `## Connections`.
4. **Map position.** Don't edit `_system/layout.json`. The validator warns W1 and the atlas shows a provisional placement. Saving a position is a separate decision; tell the user.
5. **Finish** as in digest §7 (`.agents/skills/digest/SKILL.md`), plus:
   - a line in `_system/Catalog.md` after the new node's siblings (`- L5 · [[path|Title]] · band`);
   - an entry in `_system/catalog.json`: `{"id", "title", "path", "level"}`;
   - the backbone count in `_system/Build status.md`;
   - a Log entry, `backbone | <title>`;
   - `node _system/tools/test-model.cjs <export>`, on an export written outside the vault by `python _system/tools/validate.py . --export <file>`.

   Expect W1 and an "added node" change, and nothing else new.
