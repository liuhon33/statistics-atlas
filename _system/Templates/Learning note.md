---
id: template-learning
title: Learning note template
layer: auxiliary
updated: 2026-11-08
---

# Learning note template

Approved reference: [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]]. The user chose this pattern on 2026-11-08. Use it for one authorized migration or digest at a time; adapt the sections to the actual learning material.

```yaml
id: learning-unique-stable-id
title: A useful question or topic
layer: learning
primary_home: "[[full/vault/path/to/backbone/page]]"
subject: computing
backbone_path: Exact plain-text ancestry of the primary home
study_band: M
note_types: [derivation, question, insight]
question_roles: [reconcile-approaches]
source_format: handwriting
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft
verification: needs-review
learning_state: unknown
aliases: []
tags: [atlas/learning, subject/computing]
connections: []
sources: []
```

Replace every example value with the note's real metadata. Inherit subject and home ancestry from the selected backbone page; choose study_band, note_types, question_roles, and source_format for this material. Omit optional fields when they add nothing. `backbone_path` ends at the home; the plugin derives the final personal-title segment. Do not assign a level to a learning note. Mark verification checked only after actual checks. Editorial approval does not establish mastery.

Use this sequence as an adaptable scaffold:

1. **Title, plain-text home path, and opening idea.** State the substantive question, result, or connection that makes the note worth revisiting.
2. **Selected original work.** Embed the most useful supplied handwriting or exercise screenshot beside the explanation it supports. Preserve other originals as sources; ask about uncertain selections.
3. **Setup and reasoning.** Define the needed symbols and assumptions, then develop the meaningful approaches, questions, or insights together. Use as many sections as the topic needs. Keep the user's reasoning distinct from corrections and added explanation.
4. **Connections.** Store only the agreed extra targets in `connections`, and give each the exact body form `- [[full/path|Title]] — reason`. The primary home remains separate. Incidental prerequisites and citations do not automatically become conceptual edges.
5. **Origin.** Cite actual originals and precise source coverage concisely. Put the full migration mapping, hashes, verification inventory, checkpoint boundaries, and review status in `_system/`.

For a source image use `![[raw/assets/actual-file.png]]`. Source and evidence links belong in `sources`; use full existing vault-relative targets. Reuse supported definitions and cite references near claims when needed, without duplicating a complete backbone reference page.

Keep one coherent personal note together. Write the draft into the vault with `status: draft`; the user reviews it in Obsidian, and only the `approve` command or an explicit commit instruction commits it. *[Claude · A9]* Revise after the user's review before moving to the next migration. Bulk migration needs a separate explicit instruction. This template itself is auxiliary and never becomes a learning node.
