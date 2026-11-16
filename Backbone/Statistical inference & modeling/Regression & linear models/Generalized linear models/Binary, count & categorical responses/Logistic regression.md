---
id: categorical-logistic-regression
title: Logistic regression
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Regression & linear models → Generalized linear models → Binary, count & categorical responses → Logistic regression
created: '2026-11-08'
updated: '2026-11-15'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Binary, count & categorical responses/Binary, count & categorical responses]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/bda]]'
---

# Logistic regression

Statistical inference & modeling → Regression & linear models → Generalized linear models → Binary, count & categorical responses → Logistic regression

Parent: [[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Binary, count & categorical responses/Binary, count & categorical responses|Binary, count & categorical responses]]

## 1. See it and use it

Suppose you record study hours and whether each student passes an exam: $Y=1$ for pass, $Y=0$ for fail. **Binary logistic regression estimates the probability of $Y=1$ from predictors, by making the log-odds a linear function of those predictors.** Its output is a probability between 0 and 1. [Penn State STAT 504, §6.2, “Overview of Binary Logistic Regression”](https://online.stat.psu.edu/stat504/Lesson06#overview-of-binary-logistic-regression).

![[assets/figures/2026-11-15-logistic-regression/01-use-it.svg]]

*Original illustration: dots are individual 0/1 outcomes; the curve is their modeled pass probability.*

For a simple illustrative model,

$$
\widehat p(x)=\frac{1}{1+\exp(4-0.8x)},
$$

where $x$ is hours studied, entering 3, 5 or 7 gives approximately **17%, 50% or 83%**. The 83% prediction describes comparable students; it does not give one student a fractional outcome or a guarantee.

To use the method: fit coefficients from labeled training data, enter a new student's predictors, then read the predicted probability. If a decision is needed, choose a probability threshold: at 0.5, a 7-hour student is classified as “pass.” Evaluate predictions on held-out data. This describes an association; claiming that extra study *causes* the change needs additional evidence.

### Try it in Python or R

Both examples below fit the **same invented dataset**: 100 students at each of 1–9 study hours, with pass counts $(4,8,17,31,50,69,83,92,96)$. They estimate the coefficients rather than hard-code the opening curve. A separate invented test set demonstrates evaluation; these numbers are not evidence about real students.

> [!example]- Python — fit, predict, and evaluate
> ```python
> """Run with Python + NumPy + statsmodels. All observations below are invented."""
> import numpy as np
> import statsmodels.api as sm
>
> # 100 independent toy observations at each study-hour value.
> hours = np.repeat(np.arange(1, 10), 100)
> counts = [4, 8, 17, 31, 50, 69, 83, 92, 96]
> passed = np.concatenate([
>     np.r_[np.ones(k), np.zeros(100 - k)] for k in counts
> ])
> X = sm.add_constant(hours)  # columns: intercept, hours
> fit = sm.Logit(passed, X).fit(disp=False)
>
> new_hours = np.array([3., 6., 7.])
> p = fit.predict(sm.add_constant(new_hours))
> print("Intercept, slope:", fit.params.round(6))
> print("Hours, P(pass), class at threshold 0.5:")
> print(np.column_stack([new_hours, p, (p >= 0.5).astype(int)]))
> print("Odds multiplier per extra hour:", np.exp(fit.params[1]))
>
> # Separate, invented test observations; not used to fit or choose the threshold.
> test_hours = np.repeat(np.arange(1, 10), 20)
> test_counts = [1, 2, 4, 6, 10, 14, 16, 18, 19]
> test_y = np.concatenate([
>     np.r_[np.ones(k), np.zeros(20 - k)] for k in test_counts
> ])
> test_p = fit.predict(sm.add_constant(test_hours))
> q = np.clip(test_p, 1e-12, 1 - 1e-12)  # only for numerical safety in log
> log_loss = -np.mean(test_y * np.log(q) + (1-test_y) * np.log1p(-q))
> print("Test log loss:", log_loss)
> ```

> [!example]- R — the same model with glm
> ```r
> # Run with base R. All observations below are invented.
> counts <- c(4, 8, 17, 31, 50, 69, 83, 92, 96)
> train <- data.frame(
>   hours = rep(1:9, each = 100),
>   passed = unlist(lapply(counts, function(k) c(rep(1, k), rep(0, 100-k))))
> )
> fit <- glm(passed ~ hours, data = train, family = binomial(link = "logit"))
>
> new <- data.frame(hours = c(3, 6, 7))
> p <- predict(fit, newdata = new, type = "response")
> print(coef(fit))
> print(data.frame(hours = new$hours, p = p, class = as.integer(p >= 0.5)))
> print(exp(coef(fit)["hours"]))  # odds multiplier per extra hour
>
> # Separate, invented test observations; not used to fit or choose the threshold.
> test_counts <- c(1, 2, 4, 6, 10, 14, 16, 18, 19)
> test <- data.frame(
>   hours = rep(1:9, each = 20),
>   passed = unlist(lapply(test_counts, function(k) c(rep(1, k), rep(0, 20-k))))
> )
> test_p <- predict(fit, newdata = test, type = "response")
> q <- pmin(pmax(test_p, 1e-12), 1-1e-12)
> print(-mean(test$passed * log(q) + (1-test$passed) * log1p(-q)))
> ```

Both fits give approximately

$$
\widehat\beta_0=-4.0053,\qquad \widehat\beta_1=0.8011.
$$

For $x=3,6,7$, the predicted probabilities are approximately **0.1677, 0.6902, 0.8323**; at threshold 0.5 the predictions are **0, 1, 1**. The test log loss is **0.4419**. The scripts use unpenalized maximum likelihood. Python's `statsmodels` requires the explicit intercept column; R's formula includes it automatically. In R, `type="response"` returns probabilities, while the default `type="link"` returns log-odds. [statsmodels `Logit`, Parameters](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.html); [R `glm`, Details](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.html); [R `predict.glm`, Arguments](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.glm.html).

> [!tip]- If you use scikit-learn
> `LogisticRegression().fit(X_train, y_train)` fits a model; `predict_proba(X_new)` returns probabilities in `classes_` order. Select the column for the event you encoded as 1. Its default fit includes regularization, so its coefficients need not match the two unpenalized examples above. Use a pipeline for any learned preprocessing, fitting it on training data only. [Official `LogisticRegression` documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

## 2. How it works — probability → odds → log-odds

### Watch after the practical example

The two supplied videos are by **DataSense**, and their lesson order is the reverse of the order in the request:

1. [人话统计学51:逻辑回归01](https://www.bilibili.com/video/BV1nwWY6WEPR/) — 6:47. Revisit the binary-response problem; the [study-hours diagram around 4:10](https://www.bilibili.com/video/BV1nwWY6WEPR/?t=250) contrasts a straight line's constant change with the sigmoid's changing sensitivity. Section 3 below gives the derivative behind that picture.
2. [人话统计学51:逻辑回归02](https://www.bilibili.com/video/BV1A4sG66EHx/) — about 7:26. The [diagram around 2:35](https://www.bilibili.com/video/BV1A4sG66EHx/?t=155) connects logarithms with multiplicative/additive and reciprocal/symmetric relationships; [around 5:08](https://www.bilibili.com/video/BV1A4sG66EHx/?t=308), the sigmoid diagram shows its probability bounds and limiting behavior.

The following derivation develops your proposed route and checks it independently. Here “the whole number line” means the **real line** $\mathbb R$, including non-integers.

### First remove the upper bound with odds

Let $p=P(Y=1\mid x)$ with $0<p<1$. Probability compares successes with **all outcomes**; odds（胜算）compare successes with **failures**:

$$
o=\frac{p}{1-p}\in(0,\infty).
$$

For example, $p=0.8$ means 80 successes per 100 comparable trials; the odds are $80/20=4$, or $4:1$. Conversely, $p=o/(1+o)$. As $p\to1$, the denominator $1-p$ shrinks to zero and odds grow without bound. As $p\to0$, odds approach zero.

### Then take a log to obtain a balanced real-valued scale

Odds are positive, but evidence against success is squeezed between 0 and 1 while evidence for success stretches from 1 to infinity. The natural logarithm gives

$$
\operatorname{logit}(p)=\log\frac{p}{1-p}\in(-\infty,\infty).
$$

![[assets/figures/2026-11-15-logistic-regression/02-three-scales.svg]]

*Original analytic illustration. The left plot removes the probability ceiling; the right makes complementary probabilities equally far from zero in opposite directions. The axes show finite windows of unbounded ranges.*

| Probability $p$ | Odds $p/(1-p)$ | Log-odds |
| --- | --- | --- |
| $0.1$ | $1/9$ | $-\log9\approx-2.197$ |
| $0.5$ | $1$ | $0$ |
| $0.9$ | $9$ | $+\log9\approx+2.197$ |

The symmetry has a precise meaning:

$$
\operatorname{logit}(1-p)
=\log\frac{1-p}{p}
=-\operatorname{logit}(p).
$$

Swapping “success” and “failure” reverses the sign. It does **not** make the distribution of observed predictors or probabilities symmetric. At $p=0$ or $p=1$, the logit is an infinite limit, not a finite value.

### Now make the modeling assumption

With $d$ predictors, write

$$
\eta_i=\beta_0+\sum_{j=1}^{d}\beta_jx_{ij},
\qquad
\log\frac{p_i}{1-p_i}=\eta_i.
$$

Here $x_{ij}$ is predictor $j$ for observation $i$, $\beta_0$ is the intercept, $\beta_j$ is its coefficient, and $\eta_i$ is the real-valued linear predictor. **The transformation makes this assumption possible; it does not prove that a straight line describes the actual log-odds.** This is the role of a [[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Exponential families & GLMs/Link and mean–variance functions|link function]]: connecting a conditional mean to a linear predictor. [Penn State STAT 504, §6.1, “Introduction to GLMs”](https://online.stat.psu.edu/stat504/Lesson06#introduction-to-glms).

Solve backward to recover a valid probability:

$$
\frac{p_i}{1-p_i}=e^{\eta_i}
\quad\Longrightarrow\quad
p_i=e^{\eta_i}(1-p_i)
\quad\Longrightarrow\quad
\boxed{p_i=\frac{e^{\eta_i}}{1+e^{\eta_i}}
=\frac{1}{1+e^{-\eta_i}}=\sigma(\eta_i).}
$$

The **logit** maps a probability to a score; the **logistic sigmoid** $\sigma$ maps the score back to a probability. Every finite score yields $0<p_i<1$.

### What is random, and how do we fit it?

For the basic model, observations are conditionally independent given their predictors and

$$
Y_i\mid x_i\sim\operatorname{Bernoulli}(p_i),\qquad
E[Y_i\mid x_i]=p_i,\qquad
\operatorname{Var}(Y_i\mid x_i)=p_i(1-p_i).
$$

The [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Discrete families/Bernoulli and binomial|Bernoulli model]] supplies the randomness. Predictors need not be normally distributed; this model does not assume Gaussian errors or constant conditional variance. Repeated measurements of the same person need a model or inference procedure that accounts for their dependence.

Collect the coefficients as $\beta=(\beta_0,\ldots,\beta_d)^T$. For observed $y_i\in\{0,1\}$, its probability is $p_i^{y_i}(1-p_i)^{1-y_i}$. Multiply over independent observations, then maximize the log:

$$
L(\beta)=\prod_{i=1}^{n}p_i^{y_i}(1-p_i)^{1-y_i},
\qquad
\ell(\beta)=\sum_{i=1}^{n}\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right].
$$

This is [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation|maximum likelihood]]: choose coefficients that give the observed outcomes high probability. Equivalently, minimize **binary cross-entropy / log loss**, $-\ell(\beta)/n$. A confident wrong prediction receives a large penalty: if $y_i=1$ and $p_i\to0$, then $-\log p_i\to\infty$. [Duchi, *CS229 Supplemental Lecture Notes*, §2.1, pp. 5–6](https://cs229.stanford.edu/notes_archive/cs229-notes-all/loss-functions.pdf).

We do not take the logit of each observed $y_i$: those are zeros and ones, whose logits are infinite. We model the unobserved conditional probability and fit it through the likelihood.

## 3. Deeper understanding and connections

### A constant odds multiplier produces a changing probability effect

Holding all other predictors fixed, and assuming $x_j$ enters without an interaction or nonlinear transformation,

$$
\frac{\operatorname{odds}(x_j+\Delta)}{\operatorname{odds}(x_j)}
=e^{\beta_j\Delta}.
$$

Thus $\beta_j$ is an additive change in **log-odds**, and $e^{\beta_j}$ is the **odds multiplier** for one unit of $x_j$. Neither is a percentage-point change in probability. If the odds double, $p=0.1$ becomes $0.1818$, whereas $p=0.8$ becomes $0.8889$. Both changes follow the same formula

$$
p_{\mathrm{new}}=\frac{r p}{1-p+rp},\qquad r=e^{\beta_j\Delta}.
$$

### Why the curve is sensitive in the middle and flat at the ends

For one continuous predictor with $p(x)=\sigma(\beta_0+\beta_1x)$, differentiate:

$$
\sigma'(\eta)=\frac{e^{-\eta}}{(1+e^{-\eta})^2}
=\sigma(\eta)[1-\sigma(\eta)],
\qquad
\boxed{\frac{dp}{dx}=\beta_1p(x)[1-p(x)].}
$$

Since $p(1-p)=\tfrac14-(p-\tfrac12)^2$, the largest slope magnitude is $|\beta_1|/4$, attained at $p=0.5$. For $\beta_1\ne0$, that midpoint is $x_*=-\beta_0/\beta_1$; it may lie outside the observed predictor range.

![[assets/figures/2026-11-15-logistic-regression/03-sensitivity.svg]]

*Original illustration for $\beta_0=-4$, $\beta_1=0.8$. Increasing study time from 1 to 2 hours adds about 4.4 percentage points; 4.5 to 5.5 adds 19.7; 8 to 9 adds 4.4. The lower panel shows the instantaneous slope, with maximum 0.20 probability units per hour.*

This formalizes your intuition about realistic responses: extra input can matter strongly in a transition region and little near saturation. The curve is smooth, so “suddenly increases” means *rises steeply*, not a discontinuous jump. With a nonzero coefficient and finite $x$, its slope is small but not exactly zero at the tails. If $\beta_1<0$, the probability decreases; if $\beta_1=0$, it is constant. A single straight-line logit cannot represent every real pattern, such as a probability that first rises and then falls.

**Explore:** keep $\beta_0=-4$ and $\beta_1=0.8$, and move $x$ from 1 through 5 to 9. Compare the probability and its local slope. Then try the decreasing and flat presets.

```atlas-interactive
path: assets/figures/2026-11-15-logistic-regression/explorer.html
title: Logistic probability, odds, and sensitivity
height: 870
```

[[assets/figures/2026-11-15-logistic-regression/explorer.html|Open the standalone explorer]]. The static diagram above remains usable without the interactive renderer.

### Why these particular odds and logarithms are useful

Merely mapping $(0,1)$ onto $\mathbb R$ does not uniquely select the logit; other links exist. Log-odds add two useful structures:

1. **Multiplicative evidence becomes additive.** For two classes with positive priors and class-conditional densities or masses $f_1(x),f_0(x)$, Bayes' rule gives

   $$
   \log\frac{P(Y=1\mid x)}{P(Y=0\mid x)}
   =\log\frac{P(Y=1)}{P(Y=0)}+\log\frac{f_1(x)}{f_0(x)}.
   $$

   The right side is prior log-odds plus log likelihood ratio. Logistic regression assumes this posterior log-odds can be represented by an affine function of the selected features. The [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule|Bayes connection]] explains the evidence scale; fitting logistic regression does not require separately estimating $f_0$ and $f_1$.

2. **Log-odds are the Bernoulli natural parameter.** Substituting $p=\sigma(\eta)$ into the Bernoulli probability gives

   $$
   P(Y=y\mid\eta)=\exp\!\left[y\eta-\log(1+e^\eta)\right],\qquad y\in\{0,1\}.
   $$

   Thus $\eta=\log[p/(1-p)]$ is the parameter multiplying $y$ in its [[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Exponential families & GLMs/Exponential-family form|exponential-family form]]. This is why the logit is called the Bernoulli's **canonical link**. The identity follows directly from the preceding likelihood algebra.

> [!note]- A useful consequence: a simple gradient and a convex loss
> Let $z_i=(1,x_{i1},\ldots,x_{id})^T\in\mathbb R^{d+1}$, collect $z_i^T$ into $X\in\mathbb R^{n\times(d+1)}$, and set $\eta=X\beta$. The total negative log-likelihood is
>
> $$
> J(\beta)=\sum_i\left[\log(1+e^{\eta_i})-y_i\eta_i\right],\qquad
> \nabla J=X^T(p-y),\qquad
> \nabla^2J=X^TWX,
> $$
>
> where $p=(p_1,\ldots,p_n)^T$, $y=(y_1,\ldots,y_n)^T$, and $W=\operatorname{diag}(p_i(1-p_i))$. For any vector $v$, $v^TX^TWXv=\sum_i p_i(1-p_i)(z_i^Tv)^2\ge0$, so $J$ is convex. This derivation explains the familiar “prediction minus target” gradient and the weights used in [[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Exponential families & GLMs/IRLS - Fisher scoring|IRLS]]; it is an agent-added connection, not a claim about the videos.
>
> Convexity does not guarantee a finite minimizer. If a direction strictly separates all 0s from all 1s, scaling it sends every observed-label probability toward 1 and the loss toward 0 without attaining it at finite coefficients. Quasi-separation can also prevent a finite MLE. Check convergence and identifiability; [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|regularization]] can stabilize such fits. A full-rank design is needed to identify all unpenalized coefficients.

### A probability model and a decision threshold answer different questions

The fitted model estimates $p(x)$. A threshold $t\in(0,1)$ turns that probability into an action:

$$
\widehat y=\mathbf 1\{p(x)\ge t\}
\quad\Longleftrightarrow\quad
\eta(x)\ge\log\frac{t}{1-t}.
$$

Changing $t$ changes decisions without refitting the probability curve. At $t=0.5$, the boundary is $\eta=0$; with several raw predictors this is a hyperplane. A sigmoid is nonlinear in the probability scale but a linear-logit classifier still has a linear boundary in its chosen features. Nonlinear features can change that boundary.

Use [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/ROC and precision–recall|ROC and precision–recall]] to inspect threshold tradeoffs, and [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/Probability calibration|calibration]] to check whether predicted probabilities match observed frequencies. A good classifier need not supply well-calibrated probabilities; sigmoid-shaped outputs alone do not establish calibration.

## Origin

> [!info]- Source details
> Enriched at the user's request on 2026-11-15: practical use first, foldable Python/R examples, then the two DataSense videos as deeper study material. The probability → odds → log-odds route and sensitivity/saturation emphasis were explicitly proposed by the user; the worked data, calculus, Bayes/canonical-link connections and figures are agent-added explanations.
>
> Source review covered the pages and selected on-screen diagrams/Chinese captions, including episode 01 at approximately 4:11 and episode 02 at approximately 2:36, 2:57, 3:22 and 5:09. This is not full-transcript coverage. More detail is recorded in the enrichment entry of [[_system/Log]].
>
> Definition/GLM reference: Penn State STAT 504 §§6.1–6.2. Likelihood/loss reference: John Duchi's CS229 supplemental notes §2.1, pp. 5–6, using labels $\{-1,1\}$ rather than this page's $\{0,1\}$. Software behavior was checked against official docs and by running both examples.
>
> Original figures and analytic checks: [[assets/figures/2026-11-15-logistic-regression/draw.py|plot generator]], [[assets/figures/2026-11-15-logistic-regression/checks.json|check results]]. Runnable examples: [[assets/figures/2026-11-15-logistic-regression/example.py|Python]], [[assets/figures/2026-11-15-logistic-regression/example.R|R]]. The diagrams are original mathematical illustrations, not recovered frames or exact reproductions of the videos.

```atlas
```
