---
layer: system
status: draft — step 1 (SOP configuration), nothing built yet
created: 2026-11-08
---

# SOP draft: stats_ML_rebuild

This is our working draft for the SOP. Once we agree on it, it becomes `AGENTS.md` / `CLAUDE.md`. Items marked **❓Qn** need your decision. Items marked *(rec)* are my recommendation.

---

## 0. What I gathered

| Input | What it contains | How the rebuild uses it |
|---|---|---|
| Codex backbone JSON (`statistics-backbone.json`) | **756 nodes**: 3 L1 · 22 L2 · 51 L3 · 104 L4 · 576 L5. **843 edges**: 753 `contains` (the tree) and **90 explained cross-links** (36 connection, 30 application, 24 prerequisite, each with a `reason`). Every node has `core` (probability / statistics / computing → your 3 colours), `stage` (Foundation, U, U–M, M, M elective, U–M elective) and `sources` (ASA, Stanford, UBC, PSU, Stat 110 …). | Copied in as `_system/backbone.json`, the **source of truth**. A script generates the backbone notes from it. |
| Old vault `stats_ML` | 130 md files: 15 concepts, 19 equations, 8 derivations, 19 questions, 7 synthesis, 16 sources, 6 maps, plus index/log/AGENTS/Start Here/templates. Raw: 14 images, 6 PDFs, conversation excerpts and manifests. | Step 3 migrates it into personal notes and raw. The old files stay untouched. |
| Old `AGENTS.md` (174 lines) | Digest trigger, per-chat checkpoints, raw immutability, folder contract, question selection, editorial rules, concept-definition standard, verification, lint, log format. | Section 9 lists each rule for you to keep, simplify or drop. |
| Karpathy LLM-wiki gist | Three layers (immutable raw → LLM-owned wiki → schema file); `index.md` (catalog, read first) and `log.md` (append-only, `## [date] op \| title`); ingest/query/lint operations; one source at a time with supervision. | Kept as the "auxiliary" layer, hidden from the graph by default. |

Data issues found in the JSON:
- **3 duplicate labels**: *Conditional probability* (L4 and L5), *Conditional expectation* (L4 and L5), *Spatial statistics* (L2 and L3). Obsidian needs unique filenames. **❓Q1** Rename the parent/child pair, e.g. L4 "Conditional probability (chapter)", or reword one of them?
- **7 labels with filename-illegal characters** (`/` or `?`), e.g. "Marginal likelihood / evidence", "Why do Jensen and KL give the same bound?". *(rec)* Keep the true label in the `title`/`aliases` property and sanitise only the filename ("Marginal likelihood - evidence").
- A few labels are awkward as concept names, e.g. L5 **"Calculate the ELBO"**. *(rec)* Rename it to "ELBO", with the old label kept as an alias. I'll list other candidates during step 2.

---

## 1. Three layers, three folders

```
stats_ML_rebuild/
├── backbone/        ← official knowledge web (756 nodes, L1–L5)    graph mode 1
├── notes/           ← YOUR learning notes (leaves on the backbone)  graph mode 2
├── raw/             ← immutable originals: pdf, png, chat exports   graph mode 3
│   ├── conversations/  notes/  assets/  articles/
└── _system/         ← agent plumbing: index, log, checkpoints,      graph mode 3
                       backbone.json, build script, templates, this SOP
AGENTS.md / CLAUDE.md (root)                                          graph mode 3
```

Hard rules:
1. **Backbone notes never link to personal notes.** Backbone ↔ backbone links are always present. A note's own backlinks pane still shows which notes attach to it. This keeps mode 1 clean and lets the script regenerate the backbone safely.
2. **Every personal note has exactly one `anchor`**, the backbone node it hangs from (outer L4/L5 preferred). It may have any number of extra connections to other backbone nodes or notes.
3. **Personal notes are leaves.** No backbone node depends on a note.
4. Everything technical (index, log, checkpoints, review queue, maps, templates, scripts, schema) lives in `_system/` or the root. You never need to open it.

*(rec)* Keep `backbone/` flat: every file in one folder, with level in metadata. Moving a node in the tree then changes only `up:`, not the file location. **❓Q2** Or do you want nested folders that mirror the hierarchy in the file explorer (`backbone/Inference/Bayesian inference/...`)?

---

## 2. The 3-way graph switch

| Mode | Shows | Graph filter |
|---|---|---|
| **1 · Backbone** | 756 backbone dots + tree edges + 90 cross-links | `path:backbone` |
| **2 · + My notes** | backbone + your notes and all their links | `path:backbone OR path:notes` |
| **3 · Everything** | + raw sources, index, log, schema, AGENTS, images | *(no filter, attachments on)* |

Obsidian has no built-in preset switcher. Options:
- **(a)** *(rec)* A tiny **local plugin** I write into `.obsidian/plugins/graph-modes/`. It adds 3 commands/ribbon buttons ("Graph: backbone / notes / all") that set the filter and colour groups, and you can bind them to hotkeys. No third-party download.
- **(b)** Save the 3 filter strings in a note and paste them into the graph search box.
- **(c)** A community graph-preset plugin, which you would install yourself.

**❓Q3** Is (a) OK?

### Reproducing the exact radial shape — honest caveat
Obsidian's graph view is **force-directed**. It will show the same nodes, edges and colours, and the tree will cluster into three coloured lobes. It **cannot** pin nodes into the Codex radial layout. Node size also follows link count, not level, so L1 dots won't automatically be the biggest. If you want the *exact* picture:
- **(rec, additionally)** I generate `Backbone Atlas.canvas` from the same JSON, with all 756 cards at the radial coordinates, region colours and labelled cross-link arrows. Each card links to its backbone note. It is clickable and is regenerated whenever the backbone changes.
- Your digested notes can be drawn onto it as small satellite cards next to their anchor, toggled by regenerating with or without notes.

**❓Q4** Do you want the Canvas atlas as well as the native graph?

### Colours (graph colour groups, first match wins)
- Backbone: 🔵 probability & foundations · 🟡 inference & modeling · 🩷 computing & learning (same as the Codex web).
- My notes: **❓Q5** pick one:
  (a) *(rec)* a lighter or desaturated shade of their anchor's region colour, so they read as leaves of that region;
  (b) one distinct colour for all notes (e.g. green);
  (c) colour by note type (question / digest / insight …).
- Mode 3 extras: grey.

---

## 3. Backbone node format (generated)

Example: L4 *Prior, likelihood & posterior*

```markdown
---
layer: backbone
bb_id: posterior
level: 4
region: inference            # probability | inference | computing
stage: U–M                   # Foundation | U | U–M | M | M elective | U–M elective
up: "[[Bayesian inference foundations]]"
path: "Statistical inference & modeling › Bayesian inference › Bayesian inference foundations › Prior, likelihood & posterior"
aliases: []
tags: [backbone, region/inference, level/4, stage/U-M]
---
> 🧭 **Inference & modeling → Bayesian inference → Bayesian inference foundations → Prior, likelihood & posterior**

%% bb:auto:start — generated from _system/backbone.json; edit outside this block %%
**Contains:** [[Prior and posterior]] · [[Marginal likelihood - evidence]] · [[Conjugate updating]] · …
**Cross-links**
- prerequisite → [[...]]: *reason from JSON*
%% bb:auto:end %%

(space for future content: definition, key equations — empty for now)
```

- **The path line ("I am from Inference → Bayesian → … → Prior")** is in the `path` property and repeated as a breadcrumb at the top of the note. The breadcrumb must not be ordinary `[[wikilinks]]`. Those would draw extra graph edges to every grandparent and destroy the tree shape. *(rec)* Make each step a clickable `obsidian://open?...` link: it navigates but draws no graph edge. **❓Q6** OK?
- Only the `up:` link and the "Contains" list create tree edges. Obsidian renders those as the same edge.
- The generated block is fenced so the script can rerun without destroying content you add later.
- Undergrad/grad: `stage` property plus a `stage/...` tag, filterable in search.

### Adding a new backbone node
When you say "this is a **backbone** node", I add it to `backbone.json` with a parent, region and stage, regenerate, and log it. It then gets its region colour automatically.

---

## 4. Personal note format

```markdown
---
layer: note
note_type: derivation          # see ❓Q7
question_type:                 # only if note_type = question; see §5
anchor: "[[ELBO]]"             # exactly ONE backbone node
anchor_path: "Computing & learning › Simulation & approximate inference › Approximate & latent-variable inference › Variational inference › ELBO"
region: computing              # inherited from anchor (drives colour)
stage: M                       # inherited from anchor
sources: ["[[raw/conversations/2026-10-22-ELBO-conversation-excerpt]]"]
handwritten: ["[[raw/assets/2026-10-22-ELBO-I04-annotated-summary.png]]"]
created: 2026-10-22
tags: [note, note/derivation, region/computing]
---
> 🧭 Computing & learning → … → Variational inference → **ELBO** → *this note*

(content — idea first, kept as short as possible)

## Connections
- [[Jensen inequality]]: derivation 1 bounds log E[·] by concavity of log
- [[KL divergence]]: derivation 2 splits log p(x) = ELBO + KL(q‖p(z|x))
- [[Prior and posterior]]: derivation 3, data fit − KL(q‖prior)
- [[Importance sampling]]: derivation 4, the ELBO as log of an importance-weighted expectation
- [[Which KL term acts as regularization]]: related note
```

Labelling dimensions (from your item 8):

| Dimension | Property | Purpose |
|---|---|---|
| **Where in the backbone** (most important) | `anchor`, `anchor_path`, `region`, `stage` | colour, breadcrumb, U/M |
| **What kind of note** | `note_type` | digest / question / exercise / insight / derivation … |
| **Why the question is worth keeping** | `question_type` | the 8 categories in §5 |
| **Where it came from** | `sources`, `source_kind` (chatgpt-pdf, handwritten, article, book, video) | provenance; links go to raw (hidden in modes 1–2) |
| **My handwriting** | `handwritten` (+ embedded in body) | the selected derivation photos |

**❓Q7** Note types. Proposed set:
- `digest`: a summary of a source, e.g. a long ChatGPT PDF on a topic
- `question`: a question you raised that is worth revisiting (needs a `question_type`)
- `exercise`: a practice, quiz or homework problem with its solution; the problem screenshot is embedded
- `derivation`: your own derivation(s), usually with handwriting
- `insight`: a deep idea or connection you want to keep

Add, merge or rename?

---

## 5. Question notes

A question gets its own note **only when you say it is worth it**. When I think a question qualifies I propose it with a suggested `question_type`, and you decide. Categories:

| `question_type` | Example |
|---|---|
| `confusion` — distinguishes easily confused concepts | How do a regression p-value and its CI express the same inference? |
| `connection` — connects different topics | How does KL regularization relate to penalties and Bayesian priors? |
| `reconcile` — reconciles different approaches | Why do the Jensen and KL derivations produce the same ELBO? |
| `boundary` — exposes an assumption / failure boundary | When does zero covariance imply independence? |
| `counterexample` — surprising result | Why can a triangular event occupy half a square but have probability ¼? |
| `special-general` — special case ↔ general result | Why does F = t² for one restriction, and what changes for several? |
| `mechanism` — mechanism behind a formula / implementation | How does variance propagation explain initialization scaling? |
| `modeling-choice` — consequences of a modeling choice | Why do full observations and their signs give different likelihoods? |

Digesting a question:
1. Attach it to the most relevant backbone node (`anchor`).
2. **Ask you which extra connections you want.** I suggest a short list of the non-obvious ones and skip the obvious.
3. Add more connections later whenever you ask.

---

## 6. Digest protocol (per source)

1. **Trigger.** Only when you say **digest** (or explicitly "save X into the vault"). Ordinary study stays read-only.
2. **You classify.** Tell me *backbone node* or *my note*. If you don't say, I ask.
3. **Read** the source in full, including images.
4. **Preserve** originals in `raw/` and never edit them afterwards.
5. **Propose** in one message: anchor (with its path), note type, question type if any, title, the handwritten images I'd embed, and candidate extra connections. You confirm or adjust. This step is mandatory in the supervised phase and can be skipped for clear cases once we switch to bulk.
6. **Write** the note, keeping it short: idea first, no mastery disclaimers or agent self-talk.
7. **Bookkeeping, silent, in `_system/`:** index line, log entry, per-source checkpoint.
8. **Check:** exactly one anchor, all links resolve, no backbone → note links, images embedded.
9. **Report** in 3–5 lines.

### Handwritten notes
- I select the most meaningful handwriting, e.g. `2026-10-22-ELBO-I04-annotated-summary.png`, and embed it next to the matching explanation.
- **If I'm not sure which pages to include, I ask.** Rejected attempts stay in `raw/` only.
- I transcribe and check the math in your handwriting. Ambiguous symbols get a focused question, not a guess.

### Worked example: ELBO
- One note, *"Four derivations of the ELBO"*, `note_type: derivation`.
- Embeds your I04 photo plus a short summary of the 4 routes.
- Connections: Jensen (route 1), KL divergence (route 2), Prior and posterior (route 3: data fit − KL from prior), Importance sampling (route 4), and your other ELBO notes.
- **❓Q8** Anchor on **ELBO** (L5 under Variational inference) or on **KL divergence**? Item 10 says "main attachment should be to the ELBO node" but also "lived under a backbone of KL". My recommendation is ELBO, with KL as a connection.

---

## 7. Steps

| Step | What | Output |
|---|---|---|
| **1 · SOP** (now) | Agree on this draft | `AGENTS.md` + `CLAUDE.md`, templates, graph-mode plugin, colour groups |
| **2 · Backbone** | Script: JSON → 756 notes, 843 edges, path breadcrumbs, tags, (Canvas atlas) | `backbone/`, `_system/build_backbone.py`; title-only notes, no math yet. Verified by counting files and links against the JSON. |
| **3a · Supervised migration** | Old vault notes one by one: I propose anchor, type, connections and handwriting; you confirm | first ~5–10 notes; refine SOP with what we learn |
| **3b · Bulk migration** | Rest of old vault under the refined rules; borderline cases batched into one question list | `notes/`, `raw/` |

Step 2 scope: the full 756/843 web is cheap to generate from the JSON, so *(rec)* generate all of it and keep each note to title + metadata + links. **❓Q9** Or do you want a smaller subset first?

---

## 8. Open decisions (summary)

Q1 duplicate labels · Q2 flat vs nested backbone folder · Q3 graph-mode plugin · Q4 Canvas atlas · Q5 note colours · Q6 breadcrumb style · Q7 note types · Q8 ELBO anchor · Q9 step-2 scope · Q10 old rules below

---

## 9. ❓Q10 Old SOP rules: keep / simplify / drop

| # | Old rule (stats_ML/AGENTS.md) | My rec |
|---|---|---|
| R1 | Save only on explicit **"digest"**; ordinary study is read-only; honor "don't digest yet" | **Keep** |
| R2 | **Per-chat checkpoints**: later digests only cover material after the last boundary; separate *Digest Checkpoints* page | **Simplify**: keep the logic, store it in `_system/` only |
| R3 | **Raw is immutable**: preserve bytes; excerpts labelled as excerpts; new versions get new filenames | **Keep** |
| R4 | Folder contract by note role (concepts/equations/derivations/questions/synthesis/maps) | **Drop**: replaced by backbone/notes/raw/_system plus `note_type` |
| R5 | Canonical **equation pages** for reused results | **Drop for now**: equations live in notes; maybe later inside backbone notes |
| R6 | **Concept-note standard**: externally sourced definition, explanation and a diagram per concept | **Defer** to a later "enrich the backbone" phase (backbone is title-only now) |
| R7 | **Question selection**: only insightful framings; simple gaps folded into concepts; ask on borderline cases | **Keep and change**: you decide; the 8 categories in §5 |
| R8 | Exclude **tutoring-control phrases** ("give me a hint", "don't tell me yet") from notes | **Keep** |
| R9 | **Editorial style**: idea first; no mastery disclaimers, confusion quotes or agent self-reporting; provenance concise | **Keep**, plus "as simplified as possible" |
| R10 | **Math verification**: check algebra, assumptions and limits; `verification` property; never present wrong formulas as accepted | **Keep, lighter**: one `verification` property |
| R11 | **Handwriting**: select crucial images, no galleries, transcribe faithfully, ask on ambiguity | **Keep**, plus ask when unsure what to include |
| R12 | **Problem screenshot** embedded in the exercise's main note | **Keep** |
| R13 | **Frontmatter**: type, status, verification, learning_state, sources, prerequisites, related, aliases | **Simplify** to the §4 fields; drop `learning_state` and `prerequisites`/`related` (replaced by anchor + Connections) |
| R14 | `index.md` + append-only `log.md` (Karpathy) | **Keep**, in `_system/` |
| R15 | Learning Map, Review Queue, Synthesis hub, Notation & Conventions, Start Here | **Drop** Learning Map (the backbone *is* the map) and the Synthesis hub. Fold Review Queue into `_system/`. Keep Notation in `_system/`? |
| R16 | Reciprocal **Builds on / Used by** links on both pages | **Drop**: notes link out and backlinks show the reverse; backbone is never edited by hand |
| R17 | Explain each link's meaning in prose ("uses this to justify step 2") | **Keep**, one short clause per connection |
| R18 | **Lint** on request: broken links, orphans, unsupported "checked", duplicates | **Keep**, plus backbone checks: tree integrity, one anchor per note, no backbone → note links |
| R19 | Never invent sources, questions or user wording; a referenced chat is not access | **Keep** |
| R20 | Dates in America/New_York, `YYYY-MM-DD` | **Keep** |
