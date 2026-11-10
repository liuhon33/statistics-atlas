---
name: enrich
description: "Enrich existing statistics backbone pages in three progressive levels: a one-minute visual introduction, textbook mechanics, and deeper connections. Use when the user says enrich or asks to develop a backbone concept, including from supplied notes. Default to the introductory level on a first unspecified enrichment."
---

# enrich: revisit a concept at increasing depth

Build a reference that a newcomer can use immediately and a returning learner can revisit for a new insight: 温故而知新. Keep one backbone page with progressively deeper sections. These are reading levels within a page, separate from the atlas's structural levels and study bands. Follow AGENTS §§5, 8 and 14.

## Choose the scope and depth

- Use the named existing page; otherwise find the best match by title, alias and current content. Ask only when the target is materially ambiguous. A missing concept needs an agreed `add-backbone`, not a duplicate page.
- **First `enrich`, without further direction:** write level 1 only. Do not prefill advanced sections or add empty headings.
- **`enrich-initial` or an explicit beginner-only request:** use the sibling `enrich-initial` skill. It limits every visit to level 1, including on a page that already has deeper sections.
- **A later `enrich`:** preserve the short opening and existing useful material; add a focused next step at the next useful level. Do not repeat earlier explanations or manufacture depth to fill a template.
- **Supplied notes or a requested insight:** read the authorized material, then place each contribution where it belongs, commonly in levels 2 or 3. Add a brief level 1 opening if missing. Explicit requests for a particular level or for all levels take precedence.
- On an already detailed page, retain its mathematics and provenance while arranging it by depth. Do not discard advanced content to satisfy the beginner default. A substantive request may fill more than one level; do not infer the reader's mastery from previous exposure.

## The three reading levels

### 1. See it and use it — about one minute

Open with the simplest concrete situation in which the concept helps, and a focused visual. Then give a concise standard definition, what the input/output mean, how to use the result, and one plain-language interpretation with units where relevant. Use a tiny worked example so the reader can perform one useful action immediately.

Aim for roughly 120–180 words of reader-facing prose, one small example, and minimal notation; judge the reading burden including captions and equations. Explain terms on first use. Keep only the applicability caveat needed to avoid misuse. Do not derive coefficients, introduce competing methods, or assume statistical background here. The requested StatQuest-like qualities are concrete examples, clear visual explanation and brevity; write original prose.

### 2. How it works

Build from the first example into the standard statistical account: notation and assumptions, the central formula or procedure, a short derivation or beginner proof, and interpretation of the result. Introduce prerequisites locally instead of assuming a linked page was mastered. One well-chosen derivation usually suffices; place alternative derivations and richer connections at level 3 or keep their full development in existing learning notes.

Use concise inline links to relevant existing backbone concepts exactly where they help the reasoning. Aim for the core a statistics student needs, rather than an exhaustive chapter.

### 3. Deeper understanding and connections

Explain a few substantial connections, reconciled representations, surprising consequences, or boundaries of an earlier intuition. Start each with the new insight, then show why it follows and under which conditions. Geometry, alternative derivations and counterexamples belong here when they add understanding. Reuse the earlier example where it makes the new view easier to see.

Use checked insights from the user's connected notes as material for a standalone explanation; preserve their attribution and originals. Keep extended personal derivations in their learning notes unless the user requests their inclusion. Check informal claims before promoting them: distinguish a statistic from its rejection region, retain scaling and degrees of freedom, and identify the exact subspace in a projection analogy. Do not fill this level with an unexplained link list.

## Visuals and sources

- Include at least one explanatory visual at each level actually developed. Add more only when each reveals a different useful relationship. A suitable existing figure counts; do not create a redundant gallery. If no honest visual adds value, state that specific exception briefly in the work report.
- Inspect figures in connected notes and supplied sources first. Reuse suitable originals or generated assets unchanged, with captions and attribution. External images need a verified source and permission to embed; otherwise link or draw an original. Shareable notes must not depend on unexplained private chat context.
- Use a GIF when motion explains a process. Provide an inspectable static keyframe or link alongside it; prefer deterministic mathematical plotting to generated raster art. The local `animate-geometry` skill supplies the detailed workflow when animation is useful. Keep colors and notation consistent across levels, and explicitly explain changes of coordinate space.
- Store new figures, their reproducible code and checks under `assets/figures/`. Keep original supplied files immutable under `raw/`. Inspect static renders and decoded frames from every animation phase; check scales, labels, endpoints and the mathematical invariants.
- Read precise authoritative sources for definitions, methods and new claims, preferably textbooks, university courses or original papers. Cite the relevant section/page near the claim. Distinguish sourced results, the user's reasoning and agent-added examples or repairs. If access or verification is incomplete, mark the specific gap instead of attributing unseen content.
- Keep detailed Origin/provenance material in an initially collapsed source-details callout as required by AGENTS §3; ordinary inline citations and the three explanations stay visible.

## Preserve the atlas and finish

Write between `Parent:` and `## Connections` (or the final atlas block). Use clear headings for the populated levels. Preserve stable IDs, title, hierarchy, saved coordinates and earlier links. Change only `updated`, relevant vault-file `sources`, and user-agreed aliases; one-off web references stay inline. Use full vault-relative paths.

Meaningful inline navigation to existing backbone pages is part of the explanation and does not add a map edge. For a new typed map link, obtain agreement to its type, direction and reason unless the user already authorized that scope; record it in `prerequisite_for`, `applied_in` or `related` with its reason under `## Connections`. Never add backbone `connections`, links to learning notes, copied Topics/Connected-from lists, or extra atlas blocks. Reuse assets from learning notes directly; record their detailed provenance in the log, and let the live atlas expose the attached notes.

Validate the changed skill when editing it, and run the vault validator and required regression checks for note edits. Verify that the first level stands alone, each developed level adds understanding and a checked visual, and sources/links resolve. Append an `enrich | <page>` Log entry recording levels added, checks and gaps. Advance a digest checkpoint only when actually ingesting new chat learning material. Report the changed page and leave the work uncommitted for review; only `approve` or an explicit commit instruction commits.
