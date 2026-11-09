---
name: extend
description: Continue an existing learning note with new material instead of creating a new note, keeping its writing, home and connections and adding the new part where it belongs. Use when the user says "extend", or asks to resume, continue or follow up a named note.
---

# extend: continue an existing note

The user names the note: a link, a title, or a clear description such as "the ELBO note". Never create a new note. If the target is ambiguous, ask.

1. Read the target note in full, and its entries in `_system/Digest Checkpoints.md`, to see what it already covers and where earlier material ended.
2. Secure the originals and read the new material as in digest §2–§3 (`.agents/skills/digest/SKILL.md`), with the same rules for questions and handwriting. For a chat digested before, take only what comes after its last checkpoint.
3. Check the fit. If most of the new material is a different topic, say so and suggest `digest` or `chop` instead.
4. Integrate the new material.
   - Keep the existing writing, section order, home and connections. Change earlier text only to fix a real error, and say so in the report.
   - Put the new material where it belongs: extend the relevant section, or add a subsection after it, as the ELBO note did with "Notebook extension: why introduce the encoder in the first place?". Never append a chat log.
   - Add new files to `sources`. Add a connection only with its reason line (digest §4–§5). Set `updated` to today, and record the new part's attribution in `## Origin`.
   - Never change `primary_home` or `id` without the user's agreement. Leave `status` as it is.
5. Finish as in digest §7, with one checkpoint entry (added to which note and section, with the boundaries) and one Log entry, `extend | <title>`. No new catalog entry.
