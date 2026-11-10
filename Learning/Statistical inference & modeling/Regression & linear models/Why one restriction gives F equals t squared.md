---
id: learning-one-restriction-f-equals-t-squared
title: Why one restriction gives F equals t squared
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/One-restriction F equals t squared]]"
subject: statistics
backbone_path: Statistical inference & modeling → Regression & linear models → Linear regression → Regression uncertainty → One-restriction F equals t squared
study_band: U–M
note_types:
  - derivation
  - question
  - insight
question_roles:
  - reconcile-approaches
  - assumption-boundary
  - cross-topic-connection
source_format: handwriting-and-archived-conversation
created: 2026-11-09
updated: 2026-11-10
status: active
verification: checked
learning_state: unknown
aliases:
  - Regression t and F relationship
  - One restriction not one predictor
  - Slope confidence interval by F test inversion
tags:
  - atlas/learning
  - subject/statistics
  - topic/regression
  - topic/hypothesis-testing
connections:
  - "[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Coefficient covariance]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Intervals & test inversion/Inverting a test]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation]]"
  - "[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways]]"
sources:
  - "[[raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics.pdf]]"
  - "[[raw/conversations/2026-11-02-F-and-t-statistics-conversation-excerpt]]"
  - "[[raw/conversations/2026-11-02-F-and-t-statistics-conversation-messages.json]]"
  - "[[raw/conversations/2026-11-02-F-and-t-statistics-conversation-manifest.json]]"
  - "[[assets/figures/2026-11-09-test-geometry/source-pdf-page-04.png]]"
  - "[[assets/figures/2026-11-09-test-geometry/draw_test_geometry.py]]"
  - "[[assets/figures/2026-11-09-test-geometry/checks.json]]"
---

# Why one restriction gives F equals t squared

Statistical inference & modeling → Regression & linear models → Linear regression → Regression uncertainty → One-restriction F equals t squared

**A t test measures a signed coefficient departure in standard-error units. Its matching F test measures the squared cost of imposing that same restriction, in noise-variance units. With one restriction, those measurements satisfy $F=t^2$.** The full model may contain many predictors.

Two questions from my earlier digest frame the connection:

> what is the relationship between the F score and t score

> does F = t^2 only works for single x predictor?

Exact excerpts: [[raw/conversations/2026-11-02-F-and-t-statistics-conversation-excerpt|November 2 conversation]], U01 and U03. My interpretation in U01 was improvement in fit relative to remaining squared error. The general formula also divides those quantities by their respective degrees of freedom.

## 1. The geometric bridge is the distance between two fits

![[assets/figures/2026-11-09-test-geometry/04-f-two-fits-and-sse.svg]]

*Original Codex illustration, shared with the z/t/F geometry note. The full fit $C$ is allowed to move in a larger space than the reduced fit $D$. The right triangle shows why the improvement is $DC^2=AD^2-CA^2$.*

Take the fixed-design simple-regression model

$$
Y_i=\beta_0+\beta_1x_i+\varepsilon_i,\qquad i=1,\ldots,n,
$$

with $n>2$, nonconstant $x$, and independent $N(0,\sigma^2)$ errors, $\sigma>0$. Normality supplies the exact reference distributions; the least-squares identities below are algebraic. Define

$$
x_c=x-\bar x\mathbf1,\qquad y_c=y-\bar y\mathbf1,\qquad
S_{xx}=x_c^\top x_c>0.
$$

The full fit and its residual are

$$
\hat y_F=\bar y\mathbf1+\hat\beta_1x_c,\qquad
e_F=y-\hat y_F,\qquad e_F^\top x_c=0.
$$

Test **any specified slope** $H_0:\beta_1=b$. Holding that slope fixed and refitting the intercept gives

$$
\tilde\beta_0(b)=\bar y-b\bar x,\qquad
\hat y_R(b)=\bar y\mathbf1+b x_c.
$$

The two fits differ by

$$
g(b)=\hat y_F-\hat y_R(b)=(\hat\beta_1-b)x_c.
$$

Since $e_R(b)=e_F+g(b)$ and $e_F\perp g(b)$, Pythagoras gives

$$
\boxed{\mathrm{SSE}_R(b)-\mathrm{SSE}_F
=\|g(b)\|^2
=(\hat\beta_1-b)^2S_{xx}.}
$$

This develops the fitted-point argument in PDF p. 2 and the $F=t^2$ calculation on p. 4. When $b=0$, the restricted fit is the intercept-only projection $\bar y\mathbf1$. When $b\ne0$, its possible fitted means form an **affine line** parallel to $\mathbf1$; the same perpendicular-triangle identity still holds.

Freeing a restriction weakly decreases SSE; the improvement can be zero. The test asks whether that improvement is unusually large compared with the noise estimate, not merely whether the full SSE is smaller.

## 2. Why the slope's estimated standard error is s divided by root Sxx

My earlier follow-up asked where this denominator comes from (conversation U02/A02; handwritten PDF pp. 3–4). Start with the slope estimate and substitute the model:

$$
\begin{aligned}
\hat\beta_1
&=\frac{\sum_i(x_i-\bar x)Y_i}{S_{xx}}\\
&=\beta_1+\frac{\sum_i(x_i-\bar x)\varepsilon_i}{S_{xx}}.
\end{aligned}
$$

The intercept cancels because $\sum_i(x_i-\bar x)=0$, while
$\sum_i(x_i-\bar x)x_i=S_{xx}$. The estimation error is therefore a weighted sum of observation errors. With zero cross-covariances and common variance,

$$
\begin{aligned}
\operatorname{Var}(\hat\beta_1\mid x)
&=\frac1{S_{xx}^2}\sum_i(x_i-\bar x)^2\sigma^2\\
&=\frac{\sigma^2}{S_{xx}}.
\end{aligned}
$$

Thus the **true** sampling standard error is $\sigma/\sqrt{S_{xx}}$. We estimate the unknown noise scale from the full fit:

$$
s^2=\frac{\mathrm{SSE}_F}{n-2},\qquad
\boxed{\widehat{\operatorname{SE}}(\hat\beta_1)=\frac{s}{\sqrt{S_{xx}}}.}
$$

Assume the observed full SSE is positive. The divisor $n-2$ counts the directions left after fitting an intercept and a slope. More noise increases uncertainty; more predictor spread makes the slope easier to estimate. Gaussianity is not required for the variance calculation, but it is required for the exact finite-sample t law used here.

## 3. Combine the two pieces to obtain F = t squared

One slope restriction means $q=1$, and the full-model residual degrees of freedom are $\nu=n-2$. Using the **same full-model** variance estimate for both tests,

$$
\begin{aligned}
F(b)
&=\frac{[\mathrm{SSE}_R(b)-\mathrm{SSE}_F]/1}{\mathrm{SSE}_F/(n-2)}\\
&=\frac{(\hat\beta_1-b)^2S_{xx}}{s^2}\\
&=\left(\frac{\hat\beta_1-b}{s/\sqrt{S_{xx}}}\right)^2
=\boxed{t(b)^2}.
\end{aligned}
$$

Squaring discards direction: $t=3$ and $t=-3$ both give $F=9$. For the no-slope null and the acute angle $\phi$ in the fitted-distance triangle,

$$
|t|=\sqrt{n-2}\cot\phi,\qquad
F=(n-2)\cot^2\phi.
$$

![[assets/figures/2026-11-09-test-geometry/source-pdf-page-04.png|650]]

*Unretouched rendering of p. 4 of my supplied six-page PDF. It contains the fitted-distance sketch, the weighted-error derivation of slope variance, and the final $F=t^2$ chain. The text above supplies explicit null values, dimensions, and true-versus-estimated SE notation. The full original remains in `raw/notes/`.*

## 4. One restriction can occur inside a many-predictor model

The number of **tested restrictions**, rather than the number of predictors, determines the equivalence. For example, take the full model with intercept, $x_1$, and $x_2$, with a full-rank design and $n>3$. Put $s^2=\mathrm{SSE}_F/(n-3)$.

| Test | Null | Restricted model, refitted | Statistic |
| --- | --- | --- | --- |
| Partial test of $x_1$ | $\beta_1=0$ | Intercept and $x_2$ | $F_1=(\mathrm{SSE}_{-1}-\mathrm{SSE}_F)/s^2=t_1^2$ |
| Partial test of $x_2$ | $\beta_2=0$ | Intercept and $x_1$ | $F_2=(\mathrm{SSE}_{-2}-\mathrm{SSE}_F)/s^2=t_2^2$ |
| Joint test | $\beta_1=\beta_2=0$ | Intercept only | $F_{\rm joint}=(\mathrm{SSE}_{\rm int}-\mathrm{SSE}_F)/(2s^2)$ |

All comparisons use the same observations and the same full-model denominator. The partial t statistics use their **multiple-regression** standard errors, which account for the other predictor; $s/\sqrt{S_{xx}}$ from simple regression cannot be substituted unchanged.

The joint test removes two directions and asks a different question. It has no general identity with either individual $t_j^2$, although accidental numerical equality can occur. A useful $x_2$ can make the joint F large even if $x_1$ adds almost nothing after adjusting for $x_2$. This preserves the clarification in conversation U03–U04/A03–A04.

### The general one-restriction proof

Let $X\in\mathbb R^{n\times p}$ have full column rank, $n>p$, and write

$$
G=X^\top X,\qquad
\hat\beta=G^{-1}X^\top y,\qquad
s^2=\frac{\|y-X\hat\beta\|^2}{n-p}>0.
$$

Test a specified linear restriction $H_0:c^\top\beta=b$, with $c\in\mathbb R^p\setminus\{0\}$ and fixed $b\in\mathbb R$. A single coefficient is the special case where $c$ selects that coordinate.

From the normal equations,

$$
\mathrm{SSE}(\beta)
=\mathrm{SSE}(\hat\beta)+(\beta-\hat\beta)^\top G(\beta-\hat\beta).
$$

This is the [[Learning/Statistical inference & modeling/Regression & linear models/OLS coefficients through algebra, projection, and likelihood#6. Completing the square proves the answer algebraically|OLS completed-square identity]].

Let $\delta=c^\top\hat\beta-b$. Minimizing the final quadratic subject to the restriction gives the refitted coefficient vector

$$
\tilde\beta=\hat\beta-G^{-1}c\frac{\delta}{c^\top G^{-1}c}.
$$

Indeed, it satisfies $c^\top\tilde\beta=b$, and the Lagrange-multiplier equation makes its displacement proportional to $G^{-1}c$. Substitution yields

$$
\mathrm{SSE}_R-\mathrm{SSE}_F
=\frac{\delta^2}{c^\top G^{-1}c}.
$$

Meanwhile $\operatorname{Var}(c^\top\hat\beta\mid X)=\sigma^2c^\top G^{-1}c$. Therefore

$$
\boxed{F=\frac{\delta^2}{s^2c^\top G^{-1}c}
=\left(\frac{c^\top\hat\beta-b}{s\sqrt{c^\top G^{-1}c}}\right)^2=t^2.}
$$

This extends the old digest's coordinate-restriction proof to any single specified linear contrast. With $Y=X\beta+\varepsilon$ and $\varepsilon\sim N_n(0,\sigma^2I_n)$, under that null $T\sim t_{n-p}$ and $F\sim F_{1,n-p}$. The algebraic identity does not itself establish these sampling laws. The classical SSE F test also need not equal a t statistic computed with a different, for example heteroskedasticity-robust, standard-error estimator.

## 5. The matching p-values and confidence intervals

Under the null, if $T_\nu$ has a Student t distribution, $T_\nu^2$ has an $F_{1,\nu}$ distribution. Consequently

$$
\Pr(F_{1,\nu}\ge t_{\rm obs}^2)
=\Pr(|T_\nu|\ge|t_{\rm obs}|)
=2\Pr(T_\nu\ge|t_{\rm obs}|).
$$

Thus the **upper-tail F test** matches the **two-sided t test**. It does not preserve a one-sided directional alternative. The p-value is calculated under the specified null model, not a posterior probability that the null is true.

The critical values satisfy

$$
F_{1,\nu;1-\alpha}=t_{\nu,1-\alpha/2}^{\,2}.
$$

![[assets/figures/2026-11-09-test-geometry/06-f-t-ci-inversion.svg]]

*Original Codex illustration of the PDF's test-inversion argument (pp. 2–3). For fixed observed $\hat\beta_1$, $s$ and $S_{xx}$, varying the null slope $b$ traces a parabola $F(b)=t(b)^2$. The horizontal cutoff selects exactly the confidence interval. The numerical fit is illustrative, with residual df 8.*

The [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget#Invert the test to get a confidence set|null slopes not rejected]] by a level-$\alpha$ test satisfy

$$
\begin{aligned}
F(b)&\le F_{1,n-2;1-\alpha}\\
\frac{(\hat\beta_1-b)^2S_{xx}}{s^2}
&\le t_{n-2,1-\alpha/2}^{\,2}.
\end{aligned}
$$

Equivalently, with $t_*=t_{n-2,1-\alpha/2}$,

$$
\boxed{b\in\left[\hat\beta_1-t_*\frac{s}{\sqrt{S_{xx}}},\quad
\hat\beta_1+t_*\frac{s}{\sqrt{S_{xx}}}\right].}
$$

This is the usual slope confidence interval, obtained directly from the cost of imposing each candidate slope. Under strict rejection for $p<\alpha$, equality places the null value at [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways#3. My regression notes give the same equivalence with t|an interval endpoint]] and is retained. Repeated use of this interval procedure has coverage $1-\alpha$ under the stated model; after observing the interval, that is not a probability assigned to the fixed true coefficient.

### The three-observation example has a very wide interval

For $n=3$ simple regression, $\nu=1$. Student $t_1$ is standard Cauchy, and its square has distribution $F_{1,1}$. For $f\ge0$,

$$
\Pr(F_{1,1}\le f)=\frac2\pi\arctan\sqrt f,
\qquad
F_{1,1;1-\alpha}=\tan^2\!\left(\frac{\pi(1-\alpha)}2\right).
$$

At 5%, the F cutoff is $161.447639$, and the two-sided t cutoff is its square root, $12.706205$. The exact F wedge half-angle is therefore $\arctan(1/12.706205)=4.5^\circ$. This is the PDF p. 2 calculation. The [NIST Student t table, row df = 1 and column 0.975](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm) independently gives $12.706$.

The handwritten $1.96$ interval shorthand must be replaced by the appropriate t quantile when the variance is estimated. The large multiplier here comes from having just one residual degree of freedom, even though the model errors are Gaussian. For comparison, a **one-sample mean** from three observations has $\nu=2$ and cutoff $4.302653$: fitting a regression slope uses another direction.

## Connections

- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Coefficient covariance|Coefficient covariance]] — The quadratic form $c^\top(X^\top X)^{-1}c$ supplies both the variance of a linear contrast and the reciprocal factor in the constrained SSE increase.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Intervals & test inversion/Inverting a test|Inverting a test]] — Collecting the candidate slopes whose constrained fit is not rejected recovers the standard t confidence interval.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation|p-value interpretation]] — Squaring a central t statistic turns its two-sided tail probability into the matching upper-tail F probability, while discarding its sign.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget|Hypothesis testing - maximizing power under an error budget]] — The matching F/t confidence interval is an exact regression instance of test inversion; the general framework distinguishes null-tail p-values from power and the precision of rejections.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways|Confidence intervals and p-values - the same test viewed two ways]] — The matching t/F tests produce the same interval by collecting all non-rejected parameter values, with endpoint and coverage conventions made explicit.

## Origin

> [!info]- Source details
> This note combines the regression/F/t portions of my newly supplied six-page [[raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics.pdf|handwritten PDF]] with the explicitly requested earlier [[raw/conversations/2026-11-02-F-and-t-statistics-conversation-excerpt|F/t conversation digest]]. The PDF was exported on November 9, 2026 and differs from the older four-page file in the source vault; the inherited November 1 filename label does not identify its current version. All six pages were inspected: pp. 1–4 provide the regression geometry, inference and variance argument; p. 5 supplies related one-sample t geometry; p. 6's proportions and two-sample formulas are outside this focused note.
>
> The earlier exact public-message excerpt covers U01–U05 and A01–A04 in chat `01a19ab7-d62e-7830-99d4-be0612352270`; its excerpt, message capture and manifest were copied unchanged into this vault. The two selected questions above retain their original wording and locators. The standard-error clarification is integrated into the derivation; the content-free follow-up is represented by its substantive individual-versus-joint comparison. No older unseen chat turns or new source-chat boundary are claimed.
>
> My contributions are the handwritten work, improvement-to-error interpretation, and the questions about the relationship and its single-predictor boundary. Earlier Codex explanations supply the weighted-error proof and model comparisons. The current synthesis adds the clean figures and the general linear-contrast proof, and carries forward the corrections to df, estimated standard errors, refitting, t critical values, and “no general identity” for joint tests. Ordinary slope-estimation derivations already covered by earlier notes are used as prerequisites rather than repeated in full.
>
> The projection, constrained-quadratic and sampling-law arguments were checked analytically. Reproducible calculations verify simple-slope and multi-predictor one-contrast identities, positive and negative t tail equivalence, and the small-df critical values: [[assets/figures/2026-11-09-test-geometry/draw_test_geometry.py|script]] and [[assets/figures/2026-11-09-test-geometry/checks.json|results]]. The handwritten page is an unretouched PDF rendering; the diagram and CI plot are new illustrations.
