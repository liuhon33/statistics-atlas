---
name: connect
description: Find older learning notes in the statistics atlas that should link to a newer learning note, since they were written before it existed, propose each link with its reason, and write only the links the user picks. Learning notes only, never backbone pages. Use when the user says "connect", or asks to look for links between learning notes, for example after writing a new note.
---

# connect: link older notes to newer ones

A new note can link to the notes written before it, but those older notes never had the chance to link forward to it. This command finds those missing links. It works only between learning notes: it never edits a backbone page or adds a backbone target. Some candidates will be trivial, so the user picks which to keep, and nothing is written before that.

## 1. Which notes

- The user may name the newer note(s): a link, a title, or "the note I just wrote".
- Otherwise take every learning note that has not had a pass: no `connect` entry in `_system/Log.md` lists it, or it has been extended since its last pass. If none is waiting, say so and stop.
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

A pair gets one link, in the older note, pointing to the newer one: the link the older note never had the chance to make. Older means an earlier `created` date; on the same date, the note named first in `_system/Log.md`.

## 3. Propose, and wait

Send one message listing the candidates, numbered, strongest first, grouped under each newer note:

`1. <older note> → <newer note> — <reason line exactly as it will be written> (strong / borderline)`

Write the reason from the older note's side, naming the specific shared result, object or contrast, in one line. Include borderline candidates, marked as such, because the user decides what is trivial; never pad the list. Past about 15 candidates, send whole groups in batches and continue after each answer. If nothing qualifies, say so and go to §5.

The user answers with the numbers to keep ("1, 3", "all", "none") and any rewording. Never write a link the user has not picked.

## 4. Write the picked links

In the older note of each picked pair:

- Add `"[[full/vault/path/of/the newer note]]"` (no `.md`) to `connections`, quoted like the note's other entries.
- Add `- [[full/vault/path|Title]] — reason` to `## Connections`, after the existing lines. If the note has no such section, create it before `## Origin`.
- Set `updated` to today. Change nothing else: not the prose, `sources`, `primary_home`, `status` or `id`.

## 5. Finish

As in digest §7 (`.agents/skills/digest/SKILL.md`), with the Log as the only record:

1. Validate as in digest §7, step 1.
2. Add one Log entry per run, `## [YYYY-MM-DD] connect | <newer note title, or "n notes"> (<agent>)`. List every note passed (with "no candidates" where none were found), each link added, and each declined pair as `<older title> ↔ <newer title>`, so later runs neither repeat a pass nor propose a declined pair again.
3. Never stage, commit or push. Report the links added, as links, grouped by the note that now holds them, and the pairs declined. When links were added, end with: *Review them in Obsidian. Tell me what to change, or run approve.*
