---
id: system-migration
title: Migration ledger
layer: auxiliary
---

# Migration ledger

Source vault: D:/obsidian_centre/stats_ML. Its files remain intact. Each record below identifies a coherent source bundle, its retained material, and any partial coverage of shared pages.

## Approved reference

The ELBO migration is approved and was committed separately. Its original mapping, source hashes, and subsequent notebook extension remain in [[_system/Migrations/ELBO review copy]]. The fan-in observation is a separate new digest, not an old-vault migration.

## Three approved migrations — 2026-11-08

The user explicitly authorized multiple subagents to start migrating leftover digested items, with the instruction “don't commit, let me preview on obsidian, and I will approve for each subagents”. This chat is `01a1bda0-0ca8-7df0-ac5a-ec6417558777`. These are review copies of already-digested sources, not new ingestion of their live chats. After reviewing and updating these notes in Obsidian, the user approved all three on 2026-11-08: “I slightly updated the notes for all 3, go ahead and commit”. Their current contents, including the later density and probability extensions, are finalized with status: active. Editorial approval does not change their learning_state or expand earlier source boundaries.

| Subagent | Approved note in Obsidian | Primary home |
| --- | --- | --- |
| `ols_slope` | [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation\|Three routes from least squares to slope and correlation]] | [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Simple slope and correlation\|Simple slope and correlation]] |
| `density_slices` | [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Density slices, independence, and rotational invariance\|Density slices, independence, and rotational invariance]] | [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Conditional density\|Conditional density]] |
| `probability_regions` | [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Why half the square need not mean half the probability\|Why half the square need not mean half the probability]] | [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Joint CDF and density\|Joint CDF and density]] |

Each note is committed separately with its source/figure additions and corresponding record entries. The user’s latest approval covers all three reviewed notes. [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness|The bootstrap exercise]] was approved and committed separately in referenced chat 01a1ba3b-79ee-7411-844f-f9725f9a364e and is excluded from this batch; its mapping and source bounds remain in [[_system/Digest Checkpoints]].

### ols_slope

Kept the substantive comparison of three derivations and the special-to-general question. Source-authored recall prompts, repeated CI/Cauchy material, and routine tutoring phrases are not separate questions. Embedded the original projection/rejection sketch; no supplied image was omitted. A byte-identical compatibility mirror at `assets/my_handdrawn_regression_geometry.png` preserves the literal image target in the immutable raw summary; the dated raw/assets file remains canonical.

Additional connections: [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|Orthogonal projection]]; [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Normal equations and OLS|Normal equations and OLS]]; [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/One-restriction F equals t squared|One-restriction F equals t squared]]. Each reason is stated in the note.

| Old page (relative to source vault) | Retained scope in this note |
| --- | --- |
| `wiki/derivations/Three derivations of the OLS slope correlation identity.md` | All focused derivation material, consolidated into shared setup, three routes, multiple-predictor section and boundaries. |
| `wiki/synthesis/Regression inference through projection geometry.md` | Only the section Your hand-drawn angle and rejection-region picture; other PDF/F-t/R-squared sections excluded. |
| `wiki/equations/OLS coefficient covariance and standard errors.md` | Scope mapping for slope/correlation identity only; broader covariance/SE material remains for a separate migration. |
| `wiki/sources/Regression slope derivations and geometry - 2026-11-02.md` | Provenance, exact focused source coverage and corrections carried into Origin and handoff/ledger; not copied as a separate learning node. |

Added files for this subagent:

- `Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation.md`
- `raw/notes/2026-11-02-Regression-Geometry-OLS-Correlation-t-and-F.md`
- `raw/assets/2026-11-02-my-handdrawn-regression-geometry.png`
- `raw/notes/2026-11-02-regression-slope-derivations-manifest.json`
- `assets/my_handdrawn_regression_geometry.png`

Source hashes and precise included/excluded boundaries are recorded in [[_system/Digest Checkpoints]]. No earlier per-chat boundary is advanced.

### density_slices

Kept the independence-versus-rotation question, the user's hill/board wording, and the flat-support counterexample. The vertical-line and denominator clarifications are integrated into the explanation. The supplied conditional-density formula screenshot remains archived; on 2026-11-08 the user requested replacing its embed with a generated 3D Gaussian/unit-square comparison. The new figure, SVG and reproducible Python source are in `assets/figures/density-slices-gaussian-unit-square/`; the note distinguishes the illustrated unit square from its existing side-two square derivation. The newly supplied projection screenshot is included with the later normal-sample extension; other inherited parent material and the full video narration remain outside coverage. Omitted assistant paragraphs in the archived excerpt were not newly recovered.

Additional connections: [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Independence versus zero covariance|Independence versus zero covariance]]; [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian linear transformations|Gaussian linear transformations]]; [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Sample statistics & order/Sample mean and variance|Sample mean and variance]]. Each reason is stated in the note.

| Old page (relative to source vault) | Retained scope in this note |
| --- | --- |
| `wiki/questions/How do density slices distinguish independence from rotational invariance.md` | Full substantive content consolidated: core paraphrased question, selected exact U05 wording, Gaussian/square/disk examples, rotation/sign clarification, covariance and n=2 statistics. |
| `wiki/equations/Conditional density as a normalized slice.md` | Ratio and finite-positive denominator; marginal-a.e. scope; units, normalization, defining conditional averaging identity, factorization criterion and marginal integrals. |
| `wiki/sources/Density slices and rotational invariance side conversation - 2026-11-04.md` | Original/source boundary and attribution preserved concisely in the note; detailed historical locators and limitations supplied in this handoff for the shared ledger. |

Added files for this subagent:

- `Learning/Probability & mathematical foundations/Joint variation & conditioning/Density slices, independence, and rotational invariance.md`
- `raw/conversations/2026-11-04-density-slices-rotation-side-chat-excerpts.md`
- `raw/conversations/2026-11-04-density-slices-rotation-side-chat-manifest.json`
- `raw/assets/2026-11-04-conditional-density-denominator.png`
- `raw/assets/2026-11-08-normal-sample-I01-projection-video.png`
- `assets/figures/density-slices-gaussian-unit-square/gaussian-vs-unit-square.png`
- `assets/figures/density-slices-gaussian-unit-square/gaussian-vs-unit-square.svg`
- `assets/figures/density-slices-gaussian-unit-square/render.py`

Source hashes and precise included/excluded boundaries are recorded in [[_system/Digest Checkpoints]]. No earlier per-chat boundary is advanced.

### probability_regions

Kept the density/value question and the volume insight, with the rising-diagonal correction integrated. The routine request to show an integral becomes worked reasoning. Embedded a labeled extraction of the corrected PDF p. 5 diagram. The erroneous p. 3 figure, misleading labels on p. 7, and redundant p. 9 diagram stay only in the unchanged PDF. Both problem statements were supplied as text; no original exercise screenshot or handwriting is invented. The reviewed extension places the problems first, clarifies conditioning, and adds the maximum-of-two-uniforms/ranking solution with assistant attribution.

Additional connections: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Random variables & distribution functions/Support and event regions|Support and event regions]]; [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/CDF transformation method|CDF transformation method]]; [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property|Tower property]]. Each reason is stated in the note.

| Old page (relative to source vault) | Retained scope in this note |
| --- | --- |
| `wiki/questions/Why does the density comparison not give the event probability.md` | Full substantive question, valid square, density/value distinction, and user boundary correction. |
| `wiki/questions/Can density volumes replace a double integral.md` | Full substantive insight, exercise origin, prism/tetrahedron correction and integral connection; ritual resolution prose omitted. |
| `wiki/derivations/Probability that a uniform variable is below a product.md` | CDF, density, support/endpoint conditions, weighted integral and independent shortcut retained. |
| `wiki/derivations/Your density volume argument for two thirds.md` | Full geometric construction, vertices, volumes, both integration orders; determinant check retained in verification handoff. |
| `wiki/equations/Comparison with an independent uniform variable.md` | Indicator/tower proof, two applications, arbitrary independent-X generalization, clipped uniform CDF and dependent counterexample retained. |
| `wiki/concepts/Event regions and probability mass.md` | Only material belonging to this source: event region, density-weighted area, volume and slices. Later density-slice connections and November 8 reference/figure enrichment are outside this migration; do not mark the entire concept migrated. |
| `wiki/sources/Clarify Probability Error - 2026-10-18.md` | Preserved full 11-page source coverage, distinction of user vs assistant contributions, original errors and supplied-reference identity limit; detailed provenance moved to existing root records. |

Added files for this subagent:

- `Learning/Probability & mathematical foundations/Joint variation & conditioning/Why half the square need not mean half the probability.md`
- `raw/conversations/2026-10-18-Clarify-Probability-Error.pdf`
- `raw/conversations/2026-10-18-Clarify-Probability-Error-manifest.json`
- `raw/conversations/2026-10-18-Clarify-Probability-Error-reference.json`
- `assets/figures/2026-11-08-probability-regions/pdf-p05-corrected-event-region.png`
- `assets/figures/2026-11-08-probability-regions/extract_diagram.py`

Source hashes and precise included/excluded boundaries are recorded in [[_system/Digest Checkpoints]]. No earlier per-chat boundary is advanced.

## Coverage still pending

Only the specified scopes above are migrated by this batch. The OLS covariance/SE page, broader regression synthesis, and event-regions concept are only partially represented; their remaining content must not be treated as migrated. Other old source bundles remain pending. The pre-existing Jensen-image gap R-003 remains in the source vault; the distinct underlying regression-chat gap R-004 is retained in [[_system/Review Queue]].

## Verification

Each subagent checked its mathematics and inspected the relevant originals; the parent also reviewed all three notes and their embedded figures. Combined structural and preservation checks are recorded in [[_system/Log]]. The user reviewed the notes in Obsidian and approved their current contents. Agent checks cover mathematics, source/figure inspection, files, and the map model; they do not claim agent inspection of the live Obsidian renderer.


## Coverage audit — 2026-11-09

[[_system/Migration coverage audit - 2026-11-09|The current old-to-new coverage audit]] identifies the remaining source groups, partial migrations, missing original files and concept diagrams, and separate visualization projects. It records gaps only; no source coverage or approval status is advanced.
