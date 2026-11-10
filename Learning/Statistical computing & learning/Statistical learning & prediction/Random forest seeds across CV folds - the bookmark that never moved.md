---
id: learning-random-forest-seeds-across-cv-folds
title: Random forest seeds across CV folds - the bookmark that never moved
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Trees & ensembles/Random forests]]"
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Trees & ensembles → Random forests
study_band: U–M
note_types:
  - insight
  - question
question_roles:
  - surprising-result
  - mechanism
source_format: article
created: 2026-11-08
updated: 2026-11-09
status: active
verification: checked
learning_state: unknown
aliases:
  - When the docs get randomness wrong
  - random_state in cross-validation
  - RandomState instances and clone
tags:
  - atlas/learning
  - subject/computing
  - topic/random-forests
  - topic/cross-validation
  - tool/scikit-learn
connections:
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Cross-validation]]"
  - "[[Backbone/Statistical computing & learning/Programming, data & visualization/Statistical programming/Reliable computation/Random seeds and RNG streams]]"
  - "[[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness]]"
sources:
  - "[[raw/articles/2026-11-04-random-state-blog-post.html]]"
  - "[[raw/assets/2026-11-04-random-state-I01-sklearn-docs-estimators-section.png]]"
---

# Random forest seeds across CV folds - the bookmark that never moved

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Trees & ensembles → Random forests

**Passing a `RandomState` instance to a random forest does not make its randomness vary across `cross_val_score` folds.** Before each fold, scikit-learn calls `clone()` on the estimator. `clone()` deep-copies the generator while it is still unused, so every fold starts from the same random numbers, just as with an integer seed. In scikit-learn 1.8.0, `random_state=np.random.RandomState(0)` and `random_state=0` give identical cross-validation scores.

**My question, from my blog post:**

> What do you think prints out?
> A) 5 different seeds (the bookmark moved!)
> B) The exact same seed 5 times

## 1. Two seeds, two jobs

The usual pattern fixes two seeds:

```python
cv = StratifiedKFold(5, shuffle=True, random_state=42)
forest = RandomForestClassifier(random_state=42)
scores = cross_val_score(forest, X, y, cv=cv)
```

The splitter seed fixes the 5 test folds, which is what we want: every experiment is scored on the same splits. The forest seed does something less obvious. Every fold builds its trees from the same sequence of random choices. So the 5 scores do not test robustness to the forest's randomness. They replay one lucky or unlucky streak 5 times.

*Precision added in checking:* with `random_state=42`, all 100 per-tree seeds are identical in every fold. The training rows differ between folds, so the trees still differ. What repeats is the random-number stream that drives the bootstrap draws and the feature subsampling, now applied to different data.

## 2. The documented fix and the book analogy

![[raw/assets/2026-11-04-random-state-I01-sklearn-docs-estimators-section.png]]

*The scikit-learn "Common pitfalls" page, section 12.3.2.1 Estimators: it claims that with an instance, "each call to `fit` starts from a different RNG".*

The docs recommend passing a generator object instead of an integer:

```python
rng = np.random.RandomState(0)
forest = RandomForestClassifier(random_state=rng)
scores = cross_val_score(forest, X, y, cv=cv)
```

Think of a generator as a large book of random numbers:

- **Integer `42`.** Buy a new book and start reading at page 42, line 1, every time.
- **Instance `rng`.** Hand over one book, open at page 0, with a bookmark inside. Each fold should read a few lines and move the bookmark forward for the next fold.

At least, that is what the docs say happens.

## 3. The reveal: `clone()` photocopies the book

Print the seed of the first tree in each fold's fitted forest:

```python
result = cross_validate(forest, X, y, cv=cv, return_estimator=True)
print([m.estimators_[0].random_state for m in result["estimator"]])
```

```text
[209652396, 209652396, 209652396, 209652396, 209652396]
```

**The answer is B.** Instead of sharing one book with a moving bookmark, scikit-learn photocopies the book at page 0, line 1 and gives each fold an identical copy. The original bookmark never moves.

The chain, checked in the 1.8.0 source:

1. `cross_validate`, which `cross_val_score` calls, hands `clone(estimator)` to every fold, never the estimator itself (`model_selection/_validation.py`, lines 365–388).
2. `clone()` rebuilds the estimator from `get_params(deep=False)`, cloning each parameter with `safe=False`. A `RandomState` has no `get_params`, so it is copied with `copy.deepcopy` (`base.py`, lines 98–130).
3. The forest's `fit` then uses that copy directly through `check_random_state`. Each tree receives `random_state.randint(np.iinfo(np.int32).max)` (`ensemble/_base.py`, `_set_random_states`).

So `209652396` does not depend on the data. It is simply the first draw of a fresh `RandomState(0)`: `np.random.RandomState(0).randint(2**31 - 1)` returns exactly that number.

**Consequence: under `cross_val_score`, `RandomState(0)` behaves exactly like the integer `0`.** On the docs' own example (`make_classification(random_state=0)`, default 5-fold), `random_state=0` reproduces the docs' "instance" output exactly:

| Forest `random_state` | Scores (1.8.0) |
| --- | --- |
| `123` | `[0.85, 0.95, 0.95, 0.9, 0.9]` |
| `RandomState(0)` | `[0.9, 0.95, 0.95, 0.9, 0.9]` |
| `0` | `[0.9, 0.95, 0.95, 0.9, 0.9]` |

The two scenarios in the docs differ only in which seed they use, not in the cross-validation procedure.

*Added in checking:* the next section of the same docs page, "Cloning", has the same problem. It says that after `b = clone(a)`, `a` and `b` share one internal RNG and remain different models. In 1.8.0, `b.random_state is a.random_state` is `False`. Fitting both on the same data gives identical tree seeds and identical predicted probabilities.

## 4. Moving the bookmark

To keep the splits fixed while the forest makes new random choices in every fold, skip the cloning and call `.fit()` on the same object:

```python
cv = StratifiedKFold(5, shuffle=True, random_state=42)
forest = RandomForestClassifier(random_state=np.random.RandomState(0))

scores = [forest.fit(X[tr], y[tr]).score(X[te], y[te]) for tr, te in cv.split(X, y)]
```

- ✅ The 5 data splits stay fixed by the seed 42 across runs.
- ✅ Calling `.fit()` directly moves the bookmark forward in every fold.
- ✅ Re-running the cell gives the same result.

This works because `fit` now draws from the one shared generator. Each fit takes 100 tree seeds and leaves the bookmark there. In the check, the first-tree seeds were `[209652396, 301492857, 763716221, 641875581, 1339153094]`. The first fold matches the `cross_val_score` fold exactly; every later fold gets new seeds.

*Boundary added in checking:* the third ✅ holds because the cell creates the forest, and therefore the generator, again. Re-running only the list comprehension continues from the bookmark's last position and gives different scores; I confirmed this. The order of the folds is also part of the result, so the folds cannot be fitted in parallel. A more explicit alternative gives each fold its own integer seed, drawn once from one generator. That version survives cloning, parallel fitting and partial re-runs.

## 5. What the fold-to-fold spread measures

*Added synthesis.* With a fixed forest seed, the spread of the 5 scores is the variability from the data split, conditional on one draw of the forest's randomness. Moving the bookmark gives each fold a different seed, but still only one per fold. The spread then mixes both sources and cannot separate them. To see how much the score depends on the seed, repeat the whole cross-validation with several seeds and compare the mean scores across seeds. For the score $S$ and the forest seed $G$, the total variance splits as

$$
\operatorname{Var}(S)=\mathbb E\big[\operatorname{Var}(S\mid G)\big]+\operatorname{Var}\big(\mathbb E[S\mid G]\big).
$$

Compare the [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness#2. Let the original data vary: my total-variance derivation|bootstrap's within- and between-dataset variance split]], where the conditioning variable is the dataset rather than the forest seed.

A fixed-seed run sees only the conditional part, $\operatorname{Var}(S\mid G=g)$ for its one seed $g$, and none of the second term. The docs themselves note that a constant RNG across folds "isn't inherently wrong". The real problem is reading a fixed-seed spread as robustness to the forest's randomness.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Cross-validation|Cross-validation]] — `cross_val_score` clones the estimator for every fold. The clone resets the forest's generator, so the seed type decides whether the fold spread contains any algorithmic randomness.
- [[Backbone/Statistical computing & learning/Programming, data & visualization/Statistical programming/Reliable computation/Random seeds and RNG streams|Random seeds and RNG streams]] — An integer is a seed and an instance is a stream with state. Deep-copying a stream duplicates its state instead of sharing it, which is the whole surprise.
- [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness|Bootstrap mean - two layers of randomness]] — Fixing the forest seed makes the CV spread conditional on the algorithm's randomness. This is the same split into conditional and unconditional variance as the bootstrap's two layers.

## Origin

> [!info]- Source details
> My blog post "When the docs get randomness wrong", published at <https://liuhon33.github.io/blog/random-state/> (first commit 2026-11-04) and archived as [[raw/articles/2026-11-04-random-state-blog-post.html|the original page]] with its [[raw/assets/2026-11-04-random-state-I01-sklearn-docs-estimators-section.png|docs screenshot]]. The two-seed critique, the book-and-bookmark analogy, the quiz, all four code snippets, the printed output, the `clone()`/`deepcopy()` diagnosis and the direct-fit fix are mine.
>
> Added by Claude while checking against scikit-learn 1.8.0 (source and a run on `make_classification(random_state=0)`): the call chain with the forest's seed drawing, the origin of `209652396`, the `RandomState(0)` ≡ `0` equivalence and table, the contradiction in the "Cloning" section, the per-tree note in §1, the reproducibility boundary and per-fold seed alternative in §4, and all of §5. The current docs page (1.9.1) still carries both passages; only 1.8.0's code was checked.
