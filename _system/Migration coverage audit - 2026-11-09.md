---
id: system-migration-coverage-audit-2026-11-09
title: Migration coverage audit - 2026-11-09
layer: auxiliary
created: 2026-11-09
updated: 2026-11-09
status: active
sources:
  - "[[_system/Migration ledger]]"
  - "[[_system/Digest Checkpoints]]"
  - "[[_system/Migrations/ELBO review copy]]"
  - "[[_system/Migrations/coverage-audit-2026-11-09.json]]"
---

# Migration coverage audit

**Yes: substantial old-vault learning content remains unmigrated.** This audit compares `D:/obsidian_centre/stats_ML` with `D:/obsidian_centre/stats_ML_rebuild`. It records remaining work; it does not migrate learning notes or originals, change their approval status, or advance a digest boundary.

The source vault has 91 wiki Markdown pages: 15 concepts, 19 equations, 8 derivations, 19 questions, 7 synthesis pages, 16 sources, and 7 navigation/log pages. The rebuild currently has 14 learning notes and 757 backbone pages. Those counts are not a completion percentage: the rebuild deliberately consolidates notes, and backbone titles can be empty reference scaffolds.

## Substantive content still to carry over

Old paths in this table are relative to `D:/obsidian_centre/stats_ML`. They identify existing evidence rather than proposed new notes. These groups can be consolidated according to the current SOP; missing old filenames do not require recreating every old node.

| Topic / source group | Coverage in the rebuild | Material still in the old vault |
| --- | --- | --- |
| Normal-threshold MLE exercise | No corresponding learning treatment found. | `wiki/synthesis/Normal threshold estimation - the complete picture.md`, its full-data and sign-data derivations, corrected handwriting, parameter/estimator distinction, invariance versus data coarsening, normal-threshold confidence intervals, efficiency comparison, and misspecification examples. The 13-page PDF and all three original MLE images have no byte-identical copy in the rebuild. |
| CLT, convergence notation, and delta method | The Delta method backbone entry is a scaffold; the old worked treatment is absent. | `wiki/derivations/Delta method for the squared sample mean.md`, the first-order theorem, square-root-n interpretation, normal-threshold application, the zero-mean exception and exact-moment calculations. The recently expanded six-step squared-mean derivation remains only in the old vault. |
| Empirical interval-probability exercise | Only the later bootstrap exercise from the same source is migrated. | `wiki/synthesis/Estimating an interval probability.md` and `wiki/equations/Empirical interval probability and its standard error.md`: binomial-count reasoning, empirical-CDF connection, exact moments, standard error and interval. The bootstrap checkpoint explicitly excludes PDF pp. 1–5 and images 1–2; both excluded images are absent from the rebuild. The whole PDF being present does not make these pages digested there. |
| Regression coefficient uncertainty and collinearity | The migrated OLS note explains the slope/correlation identity, not the whole uncertainty source. | `wiki/questions/Where does uncertainty in regression coefficients come from.md`, the broader `wiki/equations/OLS coefficient covariance and standard errors.md`, and `wiki/concepts/Multicollinearity and unique predictor variation.md`: matrix covariance propagation, the weighted-error SE derivation, variance inflation / residualized predictor variation, and model assumptions. The original Regression Coefficient Uncertainty PDF is absent. |
| Regression F/t tests, p-values and confidence intervals | Partially represented by the simple-regression drawing and t/F bridge in the OLS note. | `wiki/synthesis/Regression inference through projection geometry.md`, `wiki/derivations/Slope confidence intervals by inverting an F test.md`, `wiki/equations/Nested regression F test.md`, `wiki/equations/Classical regression t inference.md`, and the two test/CI and F/t question pages. Remaining scope includes constrained-slope interval inversion, general nested-model inference, individual versus joint restrictions, p-value/coverage interpretation and the Cauchy special case. The four-page regression PDF and the separate F/t conversation archive are absent. |
| R squared versus adjusted R squared | Backbone title exists, but no substantive comparison note found. | Both old question/equation pages, their checked 100-observation example, penalty/negative-value discussion and the complete archived comparison exchange. Source: `wiki/sources/R squared and adjusted R squared conversation - 2026-11-02.md`. |
| Jensen inequality and finite moments | Jensen's log-bound role is covered in the ELBO note; the standalone moment discussion is not. | `wiki/synthesis/Jensen inequality and finite moments.md`, `wiki/equations/Higher finite moments imply lower finite moments.md`, the general Jensen equation and convexity treatment: even-power statement, noncircular integrability argument, moment-size comparison and heavy-tail counterexamples. The clipping, shared-conversation capture, clarification and convex/concave source figure are absent. |
| Total expectation / variance group intuition | The general laws are represented by newer tower/total-expectation, L2 and bootstrap material. The old numerical illustration and its source are absent. | The 2026-10-27 source and the group sections of `wiki/concepts/Conditional and unconditional randomness.md`: 20%/80% groups, means 60/80, overall mean 76, within variance 25, between variance 64 and total variance 89. This is missing source-specific content, not an entirely missing theorem. |
| Bias–variance source and extensions | Substantial conceptual overlap in the newer L2 bias–variance note, based on a separately supplied image. Not a complete migration of the older two-page PDF. | `raw/notes/2026-11-01-Bias-variance-tradeoff-geometric-view.pdf` and its original provenance; the input-averaged risk / heteroskedastic form, average-squared-bias versus squared-average-bias example, and old finite-support numerical illustration in `wiki/equations/Bias variance decomposition for estimation and prediction.md`. The PDF's separate page-2 Student-t material belongs with the remaining regression inference. Extend/reconcile the current note rather than create a duplicate core explanation. |
| Sourced concept reference material and connections | Some definitions are reused inside migrated/new learning notes, but there is no complete transfer of the old reference package. | The 2026-11-08 reference bundle and the remaining content of the 15 concept notes, especially LLN/consistency, indicators, likelihood, sampling distributions, misspecification, collinearity and asymptotics. Shared pages such as event regions and conditioning have only source-specific portions represented. Existing cross-source learning-map/synthesis relationships need reconciliation where useful; a scaffold with the same title does not preserve their explanations. |

## Already migrated within explicit source boundaries

The five approved migration notes are documented in the existing ledger and checkpoints. They should not be duplicated merely because old filenames differ:

- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|ELBO]] — consolidated ELBO reasoning and four archived originals; mapping in [[_system/Migrations/ELBO review copy]]. The later old concept-definition figure is a separate absent asset.
- [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness|Bootstrap mean]] — source pp. 6–10 and images 3–4, including conditional/unconditional moments and resampling explanation. Earlier interval-probability material is excluded.
- [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|OLS slope / correlation]] — focused three-route derivation, multiple-predictor specialization and original drawing. Shared regression covariance/inference pages are only partly represented.
- [[Proof of Gaussian's sample mean and variance are independent + rotational invariance|Density slices]] — old substantive question and conditional-density result, with subsequent extensions.
- [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Why half the square need not mean half the probability|Probability regions and density volumes]] — the two probability problems, geometry and conditioning. This does not cover every later reference addition to the old event-regions concept.

The other nine learning notes are separate digests or later supplied material. In particular, [[Learning/Statistical computing & learning/Statistical learning & prediction/Bias–variance decomposition as Pythagoras in L2|the newer bias–variance note]] and [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2|the L2 projection note]] preserve much related mathematics, but their existence alone does not establish coverage of old sources or old-only examples.

## Original files and diagrams

SHA-256 comparison searched all inventoried rebuild paths, so a byte-identical file counts even if renamed or relocated. Of **55 nonempty original source/asset files under the old `raw/`**, **20 have a byte-identical copy in the rebuild and 35 do not**. This excludes `raw/README.md`, `.gitkeep` placeholders and the empty `raw/notes/2026-11-08.md`. The count includes historical workflow/preference captures as well as learning sources. No same-path raw original was found replaced by different bytes.

All **30 files** in the old `assets/figures/2026-11-08-concept-definitions/` are absent as byte-identical copies: **14 SVG diagrams, 14 PNG previews, the plotting script and the numeric-check JSON**. Their topics are CLT/distribution, conditioning, consistency, delta method, empirical bootstrap, event regions, variational evidence, indicators, L2 geometry, likelihood, misspecification, MLE invariance, collinearity and parameters/estimators. Some current notes use different illustrations; this finding is about preserving the old figure package, not requiring redundant galleries.

The original Jensen convex/concave figure is separately absent from `raw/assets/`. `Clippings/Jensen's Inequality.md` also remains only in the old vault.

## Material outside the wiki

Two project folders have not been transferred to the rebuild:

- `experiment_visualizations/neuro-network-visualizer/` — the interactive visualizer, guide, source, tests and verification records.
- `experiment_visualizations/ResNet/` — the four learning labs, launcher, models/data, documentation and migration manifest.

The rebuild has no `experiment_visualizations/` directory, and the hash inventory found no identical copies of the inventoried project files elsewhere in it. These are separate application/source assets; deciding whether they belong in the new vault is a separate migration choice. This audit did not run either project.

The old `Untitled.canvas` contains only `{}`, and `raw/notes/2026-11-08.md` is empty. Their absence is not missing learning content. Templates, old navigation and settings likewise should not be copied mechanically into the redesigned vault.

## Historical coverage and open source gaps

The new checkpoint ledger explicitly says old chat boundaries have not been imported or advanced. Old history remains in `wiki/maps/Digest Checkpoints.md`, `wiki/log.md`, source summaries and workflow records. Consult those boundaries before later ingestion of the same chats.

- **R-003**: the detailed Jensen original-image provenance gap remains in the old review queue. The new migration ledger mentions it, but the new review queue has no full R-003 entry. It is still open; the missing original image was already unavailable before this rebuild.
- **R-004**: the inaccessible underlying regression conversation is explicitly retained in the new review queue. Migrating supplied PDFs/notes does not establish coverage of unseen chat turns.

These source-access gaps are different from files that exist in the old vault but have not yet been copied.

## Verification and scope

Compared current file inventories and hashes; read migration mappings, source boundaries, index/topic descriptions and relevant old/current note content; searched current Learning and Backbone content for the remaining subjects, formulas and distinctive examples. Checked that representative same-named backbone pages are scaffolds. This establishes migration gaps and explicit partial coverage; it is not a line-by-line mathematical re-proof of every old note or an inspection of the live Obsidian renderer.

Post-write verification: the read-only vault validator passes with the same four pre-existing warnings (three duplicate display titles and the unsaved Law of total expectation map position). SHA-256 checks confirm all 1,185 protected inventoried source-vault and existing rebuild content files are unchanged. Earlier ledger/log bytes remain exact prefixes.

Machine-readable file evidence is in [[_system/Migrations/coverage-audit-2026-11-09.json]]. Only this audit and its administrative links/log are added. The source vault, all existing learning/backbone/raw/figure content and digest checkpoints are preserved. No migration or Git commit is performed.

## Original source/asset files without a byte-identical copy

Paths below are relative to the old vault. This list includes historical preference records; it is a preservation inventory, not a request to create 35 learning notes.

- `raw/articles/2026-10-18-Jensen-Inequality-clipping.md`
- `raw/articles/2026-11-08-concept-reference-excerpts.md`
- `raw/assets/2026-10-18-Jensen-convex-concave.png`
- `raw/assets/2026-10-18-interval-probability-01-exercise.png`
- `raw/assets/2026-10-18-interval-probability-02-count-reasoning.png`
- `raw/assets/2026-11-08-vault-workflow-redesign-example.png`
- `raw/assets/mle-2026-10-18/01-problem.png`
- `raw/assets/mle-2026-10-18/02-first-attempt.png`
- `raw/assets/mle-2026-10-18/03-revised-attempt.png`
- `raw/conversations/2026-10-18-Jensen-Moment-Condition-extracted-messages.json`
- `raw/conversations/2026-10-18-Jensen-Moment-Condition-shared-page.html`
- `raw/conversations/2026-10-18-Jensen-bundle-manifest.json`
- `raw/conversations/2026-10-18-MLE-conversation-reference.json`
- `raw/conversations/2026-10-18-MLE-conversation.pdf`
- `raw/conversations/2026-10-18-MLE-source-manifest.json`
- `raw/conversations/2026-10-18-Regression-Coefficient-Uncertainty-manifest.json`
- `raw/conversations/2026-10-18-Regression-Coefficient-Uncertainty.pdf`
- `raw/conversations/2026-10-27-total-expectation-and-variance-group-intuition-excerpt.md`
- `raw/conversations/2026-11-02-F-and-t-statistics-conversation-excerpt.md`
- `raw/conversations/2026-11-02-F-and-t-statistics-conversation-manifest.json`
- `raw/conversations/2026-11-02-F-and-t-statistics-conversation-messages.json`
- `raw/conversations/2026-11-02-R-squared-and-adjusted-R-squared-conversation-excerpt.md`
- `raw/conversations/2026-11-02-R-squared-and-adjusted-R-squared-conversation-manifest.json`
- `raw/conversations/2026-11-02-R-squared-and-adjusted-R-squared-conversation-messages.json`
- `raw/notes/2026-10-18-Jensen-note-statement-excerpt.md`
- `raw/notes/2026-10-18-core-question-capture-preference.md`
- `raw/notes/2026-10-18-digest-workflow-preferences.md`
- `raw/notes/2026-10-18-vault-setup-request.md`
- `raw/notes/2026-11-01-Bias-variance-tradeoff-geometric-view.pdf`
- `raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics.pdf`
- `raw/notes/2026-11-01-regression-and-bias-variance-manifest.json`
- `raw/notes/2026-11-08-concept-definition-and-diagram-preference.md`
- `raw/notes/2026-11-08-insightful-question-preferences.md`
- `raw/notes/2026-11-08-review-note-editorial-preferences.md`
- `raw/notes/2026-11-08-vault-workflow-redesign-request.md`
