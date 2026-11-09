---
name: enrich
description: Add concise, sourced reference content (definition, assumptions, short explanation, citation, optional diagram) to existing backbone pages of the statistics atlas, from an authoritative source such as a textbook, lecture slides, a paper, a tutorial or a 3Blue1Brown video. Use when the user says "enrich" or asks to fill a backbone page from such a source.
---

# enrich: official reference content for backbone pages

Backbone pages are the reference layer: official definitions, not personal learning. Questions, handwriting and the user's own reasoning belong in learning notes (`digest`). Rules: AGENTS §5 and §8.

1. **Target.** Use the page or pages the user names. Otherwise find the matching backbone pages by title and alias, and confirm if unsure. If no page exists for the concept, propose `add-backbone`. One source can enrich several pages; each page gets only its own part.
2. **Read the source itself:** the textbook section, the slide, the paper's statement, or the video at the relevant timestamps.
   - Preserve a supplied file (PDF, slides, screenshots) in `raw/` first (digest §2) and add it to the page's `sources`.
   - If you cannot read the source, say so. Never write from memory and attribute it to the source.
   - Where reasonable, check the mathematics against a second authoritative reference: a textbook, a university course, or the original paper.
3. **Write the reference block** between the `Parent:` line and `## Connections` (or the atlas block, if the page has no connections):
   - **Definition.** One or two sentences in standard notation, with every symbol and assumption defined. For a theorem, give the exact statement and its conditions; for a method, its inputs, steps and output.
   - **Scope:** when it applies and where it breaks.
   - **Explanation:** two to five sentences of the intuition the source gives, such as the 3Blue1Brown picture.
   - **Diagram (at most one):** first look for a suitable figure in the source or other authoritative material. Embed it only if its licence allows; otherwise link to it. If none fits, make a minimal original: put the script and PNG in `assets/figures/` and embed it with a caption saying it is original. Leave the diagram out if it adds nothing.
   - **Sources** line: precise citations (author, title, section, page, equation or timestamp, and URL).
   - Paraphrase in your own words. Quote only a short definition whose exact wording matters, with attribution. Aim for a reference card: about 100–250 words plus the math.
4. **Properties.** Change only these:
   - `updated`;
   - `sources`, which lists vault files only: the `raw/` originals, or for a book or course cited on many pages, one `_system/Sources/<key>.md` record shaped like the existing 28. One-off web links stay inline in the body;
   - `aliases`, if the user agrees.

   If the source suggests a new typed link (`prerequisite_for`, `applied_in` or `related`), propose its type, direction and reason, and write it only after agreement. It goes on the page where the arrow starts, with a reason line under `## Connections`. Never put `connections` or links to learning notes on a backbone page, never add `## Topics` or `## Connected from` sections, and keep the single empty atlas block last.
5. **Finish** as in digest §7: validate, and add one Log entry, `enrich | <page>`. Add a checkpoint entry only if the source was a chat. Report the changed pages and the sources you used. Never commit.
