---
id: migration-elbo-review-copy
title: ELBO review copy
layer: auxiliary
created: 2026-11-08
updated: 2026-11-08
status: active
connections:
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO]]"
---

# ELBO review copy

The user first authorized adding the prepared draft to Learning for inspection without a commit, then approved it on 2026-11-08 and requested committing the migration. It is now the reference example for future one-at-a-time migrations. No source-vault files were modified, moved, or deleted.

## Destination

- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]] — Consolidates the existing ELBO reasoning and selected handwriting into one personal learning note, homed at ELBO.

## Source coverage

Source vault: `D:\obsidian_centre\stats_ML`.

Existing source chat: `01a164b0-3238-7a41-9d34-e391ed82b15f`. Archived excerpt: U01–U09 and A01–A07; images I01–I04. The existing coverage ends at U09, `msg_01a164de-4ca6-7520-9b1e-9cb3cc433edc`, 2026-10-22T18:27:32.648Z. This operation does not import or advance a per-chat checkpoint and makes no claim about later turns.

The draft was checked before placement: Bayes/Jensen algebra and both KL decompositions, support and integrability assumptions, Gaussian loss dimensions, ridge scaling, and finite Monte Carlo distinctions. An independent two-state calculation confirmed the identities; this numerical check supplements the algebra. Authoritative references are cited in the learning note. I04 and I02 are embedded; I01 and I03 remain available as original evidence. Importance sampling is identified as added synthesis from the ratio in the Jensen handwriting.

## Old-to-new mapping

Each path below is relative to the source vault and contributes to the single destination above. Originals and existing incoming links there are preserved.

- `wiki/synthesis/ELBO - evidence Jensen and regularization.md`
- `wiki/sources/ELBO conversation and annotated summary - 2026-10-22.md`
- `wiki/equations/ELBO identities and the two KL divergences.md`
- `wiki/derivations/ELBO from Bayes rule and Jensen inequality.md`
- `wiki/concepts/Evidence and variational posterior approximations.md`
- `wiki/equations/Gaussian negative log likelihood and squared error.md`
- `wiki/questions/Which KL term acts as regularization in the ELBO.md`
- `wiki/questions/Why does expected log likelihood measure data fit.md`
- `wiki/questions/Why do Jensen and KL give the same ELBO.md`
- `wiki/questions/Why is the ELBO a lower bound when we maximize it.md`

## Preserved original bytes

| Source file | SHA-256 |
| --- | --- |
| `raw/conversations/2026-10-22-ELBO-conversation-excerpt.md` | `aa897182021e5d12496e27726e651b9ed5cfb7f1a6c84727e69088cb1bae570d` |
| `raw/conversations/2026-10-22-ELBO-manifest.json` | `dd1ba6e51489cede21f5a420c4e12b110fc921101125e609cb634f33af42aa3f` |
| `raw/assets/2026-10-22-ELBO-I01-posterior-KL-attempt.png` | `f59bb6f2584a3e9aa3d1aa747fce994757b79c27fdec4d8d7a4dd1eb65f0132e` |
| `raw/assets/2026-10-22-ELBO-I02-Jensen-slide-annotations.png` | `729b85d4b1a2cc9cd54c9a831fa2461470e843af895241020c63335d61400974` |
| `raw/assets/2026-10-22-ELBO-I03-prior-posterior-comparison.png` | `4177b14d0d0ba511f50b54f81aba117a26a825d5324d2433eb3d20f86715ecdf` |
| `raw/assets/2026-10-22-ELBO-I04-annotated-summary.png` | `159173d7e0f70f2927f35e97248e58f955f0cb8cfa0c66fd462b3b6549d58fea` |

## Review status

Approved by the user on 2026-11-08: “Looks good, git commit this ELBO migration. Use this note as the template for future migrations, but let's keep going one by one before doing a bulk migration.” The learning note is active, and its existing `learning_state: practicing` remains unchanged. Future migrations follow the approved reference and [[_system/Templates/Learning note]] one at a time. Bulk migration requires a separate instruction. Validation results are recorded in the activity log.

The current note also includes the separately authorized VAE notebook opening extension. Its preserved source is [[raw/notebooks/2026-11-08-VAE-opening-excerpt.json]] (SHA-256 `f7d8c457b7ebf31656c986d36ca3345e768b3b37faf21d9ebdc9dd409c645e2c`), covering only the first three Markdown cells. The exact boundaries and attribution are retained in [[_system/Digest Checkpoints]].
