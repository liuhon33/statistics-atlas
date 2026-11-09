---
name: digest
description: Turn study material (this conversation since its last digest, or a supplied PDF, chat export, notebook, slides or screenshots) into ONE personal learning note attached to the closest backbone page of the statistics atlas. Use when the user says "digest" or asks to save study material as a learning note.
---

# digest: one source, one learning note

`AGENTS.md` holds the rules (§5–§9 for digests); this file is the procedure. The user's words after the command can name the source, the home, or what to keep. Anything they specify needs no confirmation.

**Keep it minimal.** A digest produces exactly one note in `Learning/`. Never create separate concept, equation, question, derivation or synthesis pages, and no per-digest pages in `_system/`. If the material belongs in an existing note, use `extend`. If it truly spans topics with different homes, use `chop`. Ask the user before switching to either. If the material is an official source to file as reference content rather than the user's own learning, that is `enrich`; ask.

## 1. Scope

- By default the material is the current conversation, from its last entry in `_system/Digest Checkpoints.md` to now. A later digest of the same chat covers only the new part, and usually extends the note the earlier digest made.
- Only material you can actually read counts. A chat you were only told about, or an attachment you cannot open, is not access. Say what is missing.

## 2. Secure the originals first

Temporary attachment files vanish within minutes, so do this before anything else.

- Copy each supplied image into `raw/assets/` as `YYYY-MM-DD-<Topic>-I01-<what-it-shows>.<ext>`, using the source's date and numbering I01, I02, … in source order.
- Put supplied documents in the matching `raw/` folder: `conversations`, `papers`, `books`, `articles`, `notebooks` or `notes`. Save long pasted text once as a `.md` file labelled "pasted excerpt". A live conversation needs no transcript file; its checkpoint entry records the boundaries.
- Never edit, crop, re-encode or rename an original afterwards. Images the user pasted into Obsidian are already in `raw/assets/`; leave them where they are.
- If you can see an image but have no file for it (for example, one pasted into a terminal chat), ask the user to paste it into the draft note in Obsidian, which saves it to `raw/assets/`, or to give its path. Never recreate an original.
- Record each saved file's SHA-256 for the checkpoint entry.

## 3. Read and select

Read everything, including every image. Transcribe handwriting faithfully; ask about an unreadable symbol instead of guessing.

**Questions.** Keep a question only when its framing is worth revisiting. Keep its exact wording (or a paraphrase labelled as one) and give it a `question_roles` value:

- `concept-distinction`: separates easily confused ideas. *How do a regression p-value and its confidence interval agree? At p = 0.05 exactly, the interval touches 0.*
- `cross-topic-connection`: draws topics together. *Why does the ELBO's KL term act as regularization, like an L1/L2 penalty or a zero-centred Gaussian prior in Bayesian regression?*
- `reconcile-approaches`: different routes to one result. *The ELBO via Jensen, via the KL definition, via importance sampling.*
- Also `assumption-boundary`, `surprising-result`, `special-to-general`, `mechanism`, `modeling-consequence` (AGENTS §6).

Leave out factual questions whose answer belongs in the text (*what is KL divergence*), quickly fixed gaps (*how can I derive an MLE without numerical data*), and confusion-only or tutoring messages (*I'm stuck*, *explain this in detail*, *give me a hint*, *don't tell me the answer*). Keep their useful content, without the question. Ask about borderline cases.

**Handwriting.** Embed only the pivotal pages (key derivations, comparisons, corrections, realizations), each beside the paragraph it supports. The other pages stay in `raw/assets/` and in `sources`. Always embed a screenshot of an exercise statement beside the statement. Ask when unsure.

## 4. Home and connections

- Search `Learning/` (titles, aliases, headings) for a note on the same topic. If one exists, propose `extend` instead.
- Choose the home: the most specific fitting backbone page, usually level 5 or 4; a broad note may sit higher. Search titles and aliases in `_system/Catalog.md` and the frontmatter under `Backbone/`. If nothing fits, propose `add-backbone`; never expand the taxonomy silently.
- Connect each kept question or insight to the backbone pages and earlier learning notes it genuinely relates to, each with a one-line reason. Skip incidental prerequisites and anything the home already implies.

## 5. Decide or ask, once

When the home, questions, images and connections are clear, write without asking and list your choices in the report. Otherwise send one message containing only the open decisions, each with your recommendation, and continue the independent work meanwhile. Never act on an answer the user has not given.

## 6. Write the note

- Path: `Learning/<level-1 title>/<level-2 title>/<Title>.md`, using the home's level-1 and level-2 titles. The file name must be unique in the vault and free of `< > : " / \ | ? *`, and the full path under 240 characters.
- Shape it like `_system/Templates/Learning note.md` and the approved reference, `Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO.md`:
  - Properties: `id: learning-<slug>`, `layer: learning`, `primary_home`, plus `subject` and `backbone_path` copied from the home, `status: draft`, and the rest of the template.
  - Body: the title, the plain-text home path, then the opening idea. Add only the setup the note needs. Build sections around the questions or approaches, with selected handwriting beside its explanation.
  - `## Connections` with one `- [[full/path|Title]] — reason` line per `connections` entry.
  - A short `## Origin` that separates the user's own work from corrections and added synthesis.
- Write math the Obsidian way: `$…$` inline, and `$$` on lines of their own for display. Embed images as `![[raw/assets/<file>]]` with a one-line italic caption.
- Check every claim, assumption, algebra step, dimension and condition. A numerical check supports a result but does not prove it. Set `verification: checked` only after real checks; otherwise `needs-review`.

## 7. Finish (every writing command ends this way)

1. **Validate.** Run `python _system/tools/validate.py .` and `python _system/tools/test_validate.py`. Expect only the known warnings. The validator needs PyYAML. Without it, it reports false F0 errors on notes with indented lists; don't "fix" those notes, tell the user PyYAML is missing.
2. **Records.** A few lines each, and no new pages:
   - `_system/Digest Checkpoints.md`: the source key; the included and excluded boundary (real message IDs or exact quoted locators, never invented ones); the destination; file hashes; gaps.
   - `_system/Log.md`: `## [YYYY-MM-DD] digest | <title> (<agent>)`, what changed, and which checks passed.
   - For a new note, `_system/Catalog.md` (Personal learning section) and `_system/catalog.json`: `{"id", "title", "path", "layer": "learning", "primary_home": <home id>, "status"}`.
   - `_system/Build status.md`: the counts, if they changed.
   - `_system/Review Queue.md`: only real gaps (missing source files, uncertain transcription, unverified claims), not "awaiting review".
3. **Hand over.** Never stage, commit or push. Report the note as a link, its home, its connections, the questions kept and left out, the images embedded and those kept only as sources, and any open uncertainty. End with: *Review it in Obsidian. Tell me what to change, or run approve.*
