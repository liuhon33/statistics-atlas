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

The user supplied a projection screenshot and https://www.youtube.com/watch?v=KgqwRQowFLo&t=7s for [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Density slices, independence, and rotational invariance|the density-slices note]]. The screenshot is preserved and explained, and the normal-sample theorem was independently checked. Video/oEmbed retrieval failed; no claim of full-video viewing, exact narration, creator identity, or screenshot timestamp is made. This does not block the screenshot-based explanation. If precise video attribution or further video digestion is requested, obtain its transcript or accessible content first.

## [2026-11-08] Validator regression fixtures assume no backbone additions

After the approved [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation|Law of total expectation]] addition, validate.py and test-model.cjs pass, but `_system/tools/test_validate.py` compares each copied live-vault fixture against absolute warning/change sets. The legitimate existing W1 plus added-node/added-link differences contaminate every fixture expectation: 0/15 assertions pass, despite all expected error-rule sets matching. Run with Python -X utf8 to avoid the separate Windows output-encoding failure. A scoped test-maintenance task should compare fixture deltas against the starting vault or use a stable independent fixture; do not remove the approved node or alter the frozen baseline to make these assertions pass. No test-tool changes made during the content addition.


## [2026-11-09] Resolved — validation fixtures and source-record export

Publication checks repaired the regression fixtures to compare warning/change findings against the starting vault, preserving checks for new findings with the same rule. All 15 cases pass. The validator export now includes the non-Markdown source records used by the plugin; both the model and refresh tests pass on that export. Migration-evidence JSON under `_system/Migrations/` is included by the plugin so the coverage-audit source resolves. No backbone identity, layout, learning content, or original source bytes changed.
