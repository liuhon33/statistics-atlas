---
name: connect
description: Find meaningful links between learning notes, propose them for approval, and record picked connections with concise inline pointers and fuller end-of-note reasons. Also supports an inline-only pass on selected text or existing connections without a discovery sweep. Use for "connect", "connect inline", or requests to link a passage to another learning note. Never edits or targets backbone pages.
---

# connect: connect learning notes without interrupting the reading

A new note can link to the notes written before it, but those older notes never had the chance to link forward to it. The normal pass finds those missing connections; an inline-only pass makes a selected passage or an existing connection easier to follow. Both work only between learning notes. Keep the reading text quiet: short pointers in the prose, fuller reasons in `## Connections`.

## 0. Choose the scope

- **Normal pass** (default for "connect"): follow §§1–4. Propose new relationships, wait for the user's selection, then add the selected map connections and useful minimal inline pointers. Do not force a pointer where it interrupts the reasoning.
- **Inline-only pass** ("connect inline", or a request to put a link at selected text): go to §4b. Work only on the selected passage, named note or specified pairs. Do not trigger the waiting-note discovery sweep. Already-connected pairs remain eligible.
- New relationships chosen by the agent still need approval. A target the user explicitly requests, or an already-approved connection the user asks to surface inline, needs no repeated approval. If the target is uncertain, propose the candidate with a brief reason first.

## 1. Which notes

- The user may name the newer note(s): a link, a title, or "the note I just wrote".
- Otherwise take every learning note that has not had a discovery pass: no entry with the exact action `connect` in `_system/Log.md` lists it, or it has been extended since its last pass. Do not count `connect-inline` entries. If none is waiting, say so and stop.
- For a full sweep, when the user asks for one, treat every learning note as waiting.

## 2. Find candidates

For each waiting note N, one at a time:

1. Read N in full: its home, its connections, and the objects, results, techniques and questions it actually works with.
2. Screen every other learning note with a search rather than a full read: its properties (`primary_home`, `backbone_path`, `connections`, `aliases`), its opening idea and headings, and a text search for N's key terms. Shortlist a note when there is a specific reason to look:
   - the same or a neighbouring home, or one note's home among the other's connections;
   - a backbone connection both notes share;
   - the same object, technique or counterexample in both;
   - a question in one that the other answers.
3. Drop settled pairs: notes already linked in either direction, pairs proposed earlier in this run, and pairs a `connect` Log entry records as declined, unless either note has been extended since.
4. Read each remaining shortlisted note in full. Keep a pair only when reading one note genuinely helps with the other:
   - the same result or object, reached or used another way;
   - a result in one is used, generalized, limited or contradicted in the other;
   - a question in one is answered or sharpened in the other;
   - a contrast worth seeing side by side, such as an assumption one needs and the other drops.

   Leave out shared vocabulary or a broad shared topic, a common prerequisite (both use expectation), and a relation the backbone already shows, such as two notes related only through their shared home.

A pair gets one conceptual map connection, in the older note, pointing to the newer one: the link the older note never had the chance to make. Older means an earlier `created` date; on the same date, the note named first in `_system/Log.md`. Inline navigation is not another map connection; it does not justify a duplicate or reciprocal `connections` entry.

## 3. Propose, and wait

Send one message listing the candidates, numbered, strongest first, grouped under each newer note:

`1. <older note> → <newer note> — <reason line exactly as it will be written> (strong / borderline)`

Write the reason from the older note's side, naming the specific shared result, object or contrast, in one line. Include borderline candidates, marked as such, because the user decides what is trivial; never pad the list. Past about 15 candidates, send whole groups in batches and continue after each answer. If nothing qualifies, say so and go to §5.

Where a natural insertion exists, include a compact inline preview and its destination heading or block with the proposal. The detailed reason above belongs at the end of the note, not in the study paragraph. Do not invent a sentence just to supply a preview.

The user answers with the numbers to keep ("1, 3", "all", "none") and any rewording. Never write a relationship the user has not picked or explicitly requested.

## 4. Write the picked links

In the older note of each picked pair:

- Add `"[[full/vault/path/of/the newer note]]"` (no `.md` or heading/block suffix) to `connections`, quoted like the note's other entries. Do not duplicate an existing entry.
- Add `- [[full/vault/path|Title]] — reason` to `## Connections`, after the existing lines. Keep the specific, substantive reason here; it can be more explanatory than the inline pointer while remaining one meaningful reason line. If the note has no such section, create it before `## Origin` (or at the end if there is no Origin).
- Add a minimal inline pointer only where it helps, using §4a. Prefer one useful placement over repeated links to the same target.
- Set `updated` to today in America/New_York. Apart from those links and the smallest necessary surrounding phrase, preserve prose, mathematics, `sources`, `primary_home`, `status` and `id`.

### 4a. Minimal inline style and precise destinations

- Prefer turning an existing phrase into a link, with no added words. Otherwise use one short pointer, such as `This is the same [[full/vault/path#Exact heading|F = t² result]].` This is illustrative syntax: read the target and substitute its actual path and heading.
- Use a short, meaningful display label. Do not repeat the target's full title, explain its contents, or restate the connection reason in the study paragraph unless that wording is needed for accuracy. Do not call results "the same" when their assumptions or scope differ; use a short accurate label such as "special case" or "contrast".
- Read the relevant source passage and destination section. Prefer `[[full/vault/path#Exact heading|short label]]`, or an existing `[[full/vault/path#^block-id|short label]]` for a specific paragraph/equation. Confirm the anchor exists and identifies the intended passage; never guess a heading or use a line number or absolute disk URL.
- Prefer existing anchors. If no precise anchor exists, use the nearest useful heading or the note itself; ask before adding a block ID or restructuring a target note outside the requested edit scope.
- A heading/block link targets a location; it does not guarantee visual highlighting. Do not insert permanent highlight markup, change the target's formatting, or install navigation features merely to make a link. Only report live jump/highlight behavior if it was actually checked.

### 4b. Inline-only pass

1. Read the selected passage in context and the relevant destination section(s). Reuse the named targets or established connections. If the user asks to find a particular remembered result, use a focused search for that result, not a vault-wide connection sweep; propose an agent-selected relationship before writing it.
2. Add or shorten the pointer using §4a. Work in the note the user is reading, regardless of which note is older. Skip a duplicate pointer already serving that passage; replace an existing verbose pointer rather than appending another.
3. Leave `connections` properties and existing `## Connections` reasons unchanged. The fuller rationale stays in the existing Connections section of the note that owns the relationship; do not duplicate that record in the other note. If a missing map connection or reason should be added, propose that separately through the normal picked-pair workflow rather than silently widening this pass.
4. Update the date only on notes actually changed. Preserve all other content and metadata, then finish below. An inline-only pass does not count as a completed discovery pass.

## 5. Finish

As in digest §7 (`.agents/skills/digest/SKILL.md`), with the Log as the only record:

1. When files changed, validate as in digest §7, step 1. Also check every added heading/block destination and the local diff: no duplicated map connections, unnecessary prose, changed mathematical claims or unrelated edits. An unchanged inline-only rerun needs only the relevant link/destination check. Distinguish file-level checks from live Obsidian navigation checks.
2. For a normal discovery pass, add one Log entry per run, `## [YYYY-MM-DD] connect | <newer note title, or "n notes"> (<agent>)`. List every note passed (with "no candidates" where none were found), each map connection and inline pointer added, and each declined pair as `<older title> ↔ <newer title>`, so later runs neither repeat a pass nor propose a declined pair again. For inline-only work, use `connect-inline | <note title>` instead, recording only the edited passages and targets; do not mark a discovery pass complete or turn a declined pointer placement into a declined conceptual pair. If nothing changes, report that without a redundant inline-only Log entry.
3. Never stage, commit or push. Report the links added, as links, grouped by the note that now holds them, and the pairs declined. When links were added, end with: *Review them in Obsidian. Tell me what to change, or run approve.*
