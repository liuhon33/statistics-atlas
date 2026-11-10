---
name: enrich-initial
description: "Add or refine only the beginner level of an existing statistics backbone page: a one-minute example, visual, definition, use and interpretation. Use when the user says enrich-initial or requests just the introductory explanation. Preserve any existing mechanics and deeper sections."
---

# enrich-initial: make the first encounter useful

Read the sibling [enrich skill](../enrich/SKILL.md) for source verification, figures, atlas invariants and finishing checks. This command uses its **level 1 only**, regardless of how many times the page has been enriched.

1. **Find the existing backbone target.** Use the named node and inspect its current content. If a name is genuinely ambiguous, resolve it before editing. Do not create or rename nodes to satisfy this command.
2. **Write one self-contained opening.** Start with the simplest concrete use case and a useful visual. Add a concise standard definition, what goes in and comes out, how to use the result, and how to interpret it. Include a tiny worked example with understandable units. Aim for about 120–180 words of prose and roughly a one-minute read including the equation and caption; avoid derivatives, proofs, competing methods and advanced connections. Cite a precise authoritative source that was actually read.
3. **Show the idea.** Reuse a suitable checked figure when available, or create an original reproducible diagram. Use a short GIF when motion helps, with a static view available. Keep its symbols, labels and example consistent with the text. Verify and inspect the result using the shared enrich workflow.
4. **Keep the edit local.** Place the introduction after `Parent:` and before existing mechanics/deeper material. On a page with a level 1 section, improve that section rather than adding another introduction. Preserve every section outside it, along with existing provenance, handwriting, links and figures. If advanced content is unsectioned, add the opening without rewriting or relocating that content. Do not add levels 2 or 3, empty headings, new typed map connections, or changes to the atlas structure. If the opening already meets the request, report that without an empty rewrite.
5. **Finish for review.** Apply the shared metadata, source-preservation and validation rules. Append an `enrich-initial | <page>` Log entry only for substantive work, stating that the scope was the introductory level. Report the page and visual; leave it uncommitted until `approve` or an explicit commit instruction. If the user also requests deeper work, treat that additional scope as `enrich`, not as an implicit expansion of this command.
