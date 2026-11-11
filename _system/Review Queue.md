---
id: system-review
title: Review queue
layer: auxiliary
---

# Review queue

The ELBO learning note is the approved migration reference. All three migrations in [[_system/Migration ledger]] are now approved. The source gaps below remain distinct from that editorial approval.

Do not treat absent old review items as resolved. Retain and reconcile their provenance during later authorized migrations.

- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|ELBO note]] — Approved as the migration reference; source notes remain intact.
- [[Learning/Probability & mathematical foundations/Random variables & distributions/Why divide weights by the square root of fan-in|Fan-in scaling observation]] — Editorially approved on 2026-11-08 with the existing home and two extra links. The video-source gap remains open. Screenshot preservation resolved: the user pasted [[kaiming_scaling.png]] into the note; its local file and embed were checked on 2026-11-08. Math delimiters corrected to Obsidian syntax. The linked video was not retrievable; no transcript verification is claimed. Details: [[_system/Digests/Fan-in scaling]].

### R-004 — Underlying regression conversation remains outside the migrated document scope

The old review queue records no original-turn coverage for conversation `6ae77b4b-48ec-83ea-9efb-c5eb7516b4a1` (“Regression p Values and Confidence Intervals”), referenced from chat `01a19956-9844-76b0-9efe-6e174bc0ae08`. The supplied summary and drawing are fully available and support [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|the OLS note]]; they are not a recovered transcript. This migration does not resolve or advance the separate source-chat boundary.

- Next action, if further source ingestion is requested: obtain readable original turns or an export, compare them with the preserved document scope in [[_system/Digest Checkpoints]], and ingest only new evidence. No source or mathematical gap blocks the current focused OLS note.

### Density-slices video — full narration not verified

The user supplied a projection screenshot and https://www.youtube.com/watch?v=KgqwRQowFLo&t=7s for [[Proof of Gaussian's sample mean and variance are independent + rotational invariance|the density-slices note]]. The screenshot is preserved and explained, and the normal-sample theorem was independently checked. Video/oEmbed retrieval failed; no claim of full-video viewing, exact narration, creator identity, or screenshot timestamp is made. This does not block the screenshot-based explanation. If precise video attribution or further video digestion is requested, obtain its transcript or accessible content first.

## [2026-11-08] Validator regression fixtures assume no backbone additions

After the approved [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation|Law of total expectation]] addition, validate.py and test-model.cjs pass, but `_system/tools/test_validate.py` compares each copied live-vault fixture against absolute warning/change sets. The legitimate existing W1 plus added-node/added-link differences contaminate every fixture expectation: 0/15 assertions pass, despite all expected error-rule sets matching. Run with Python -X utf8 to avoid the separate Windows output-encoding failure. A scoped test-maintenance task should compare fixture deltas against the starting vault or use a stable independent fixture; do not remove the approved node or alter the frozen baseline to make these assertions pass. No test-tool changes made during the content addition.


## [2026-11-09] Resolved — validation fixtures and source-record export

Publication checks repaired the regression fixtures to compare warning/change findings against the starting vault, preserving checks for new findings with the same rule. All 15 cases pass. The validator export now includes the non-Markdown source records used by the plugin; both the model and refresh tests pass on that export. Migration-evidence JSON under `_system/Migrations/` is included by the plugin so the coverage-audit source resolves. No backbone identity, layout, learning content, or original source bytes changed.

## [2026-11-09] Validation environment — PyYAML unavailable

During Conditional probability enrichment, both `C:\Python314\python.exe` and the bundled Codex Python used validate.py's fallback YAML parser, which rejects existing indented block lists (including Hilbert spaces and Cauchy distribution). Both validate.py and test_validate.py then crash at level-count sorting with `TypeError: '<' not supported between instances of 'NoneType' and 'int'`. This is independent of the enriched page, whose metadata and links parse and resolve. Re-run using an environment with PyYAML before claiming full-vault or regression success; no parser or existing-note changes were authorized or made here.

**Resolved during approval (2026-11-09):** the existing `D:\anaconda\python.exe` imports PyYAML correctly. Live-vault validation passes with existing W1/W2 warnings only, and test_validate.py passes 15/15 cases. No package installation, validator edits or content workaround was needed. The default/bundled runtime limitation remains, but no longer blocks this approval.

## [2026-11-09] Gaussian video-caption access and broad editorial approval

The later proof-summary extension retrieved and read the complete available automatic captions (0:00–19:10); the included proof covers 3:36–13:41, as recorded in [[_system/Digest Checkpoints]]. This supersedes the earlier inability to retrieve a transcript, but does not establish exact narration or viewing of every frame. Other source gaps, including R-004 and the fan-in video, remain open. The user approved all pending work, including both new test-geometry drafts; editorial approval changes neither mathematical verification nor learning state.


## [2026-11-10] Bayes-rule screenshot — original attachment unavailable for archiving

For [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget|the testing note]], the user supplied a screenshot headed “This is Bayes’ rule”, identified by them as 3Blue1Brown, and requested the Bayesian interpretation beneath the area graphic. Its visible content informed the checked H/E mapping, but D:/CODEXS~1/temp/claudian-codex-images-kvBa6I/1-image.png had expired before preservation. No original copy/hash or independently verified video attribution is claimed. User asked to reattach the image; on receipt, preserve bytes and add its source link/hash without redigesting the already completed explanation. This archival gap does not block the mathematics or note text.

**Resolved (2026-11-10):** the user supplied `C:/Users/Hongrui_Liu/Downloads/Screenshot 2026-11-10 031958.png`. Visually inspected and preserved unchanged as [[raw/assets/2026-11-10-Hypothesis-testing-I04-Bayes-area-reference.png]], now linked in the note's sources and Origin. Source and archived copy are 82,429 bytes with matching SHA-256 `bb661e85e6a7c51f73e2125d0d2aa74d12f6df9af1585214595ccc04b86d9365`. This resolves file preservation, not independent video attribution or byte identity with the expired temporary attachment. No explanation or diagram was redigested or regenerated.

## [2026-11-11] DAT112 diffusion source — untrained zero-time sampling call

[[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code|Diffusion in PyTorch - why U-Net and how the formulas become code]] documents a confirmed issue in the supplied source: the cumulative schedule includes beta[0], training samples indices 1..T, and sampling visits T..0, evaluating time zero without training examples at that level. The digest's explanation, source hashes, shape/algebra checks and all eight supplied tests pass; those tests check implementation behavior, not correctness of this endpoint as standard DDPM. The external code and trained checkpoint were deliberately left unchanged. If code correction is requested, align schedule/training/time conditioning/sampling together and assess checkpoint compatibility; do not silently switch the existing trained model to a new schedule. No unread source or uncertain transcription blocks this note.
