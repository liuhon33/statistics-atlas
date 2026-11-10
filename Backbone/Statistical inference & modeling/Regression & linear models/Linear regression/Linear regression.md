---
id: linear-models
title: Linear regression
layer: backbone
level: 3
subject: statistics
study_band: U
backbone_path: Statistical inference & modeling → Regression & linear models → Linear regression
created: '2026-11-08'
updated: '2026-11-09'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/3
- study/undergraduate
node_kind: group
parent: '[[Backbone/Statistical inference & modeling/Regression & linear models/Regression & linear models]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/isl]]'
---

# Linear regression

Statistical inference & modeling → Regression & linear models → Linear regression

Parent: [[Backbone/Statistical inference & modeling/Regression & linear models/Regression & linear models|Regression & linear models]]

## 1. See it and use it — about one minute

Suppose you know someone's height and want a rough prediction of their weight. Plot a few paired measurements, then fit a line through the overall trend.

![[assets/figures/2026-11-09-regression-layers/01-predict-weight.gif]]

*Original illustration with five invented measurements. Green guides show how to read a prediction. [[assets/figures/2026-11-09-regression-layers/01-predict-weight.svg|Static view]].*

**Simple linear regression models the average response using a straight-line function of one predictor.** Here, height is the predictor and weight is the response. Software estimates the line from the paired data. In this example it gives

$$
\text{predicted weight (kg)}=60+0.8\,[\text{height (cm)}-170].
$$

**Use it:** enter a height of 175 cm: $60+0.8(175-170)=64$ kg.

**Interpret it:** the fitted average is 60 kg at 170 cm, and rises by 0.8 kg per extra centimetre. Individual weights can differ from the line. This describes an association; it does not establish that changing height causes a particular weight change. Predict within the observed range, here 150–190 cm.

> [!example]- Try it in Python and R — fit a line and predict
> Use the same five invented height–weight pairs as the figure. In both languages, `weight ~ height` means “model weight using height”; an intercept is included automatically.
>
> **Python — pandas + statsmodels**
>
> If needed, install once in your Python environment: `python -m pip install pandas statsmodels`.
>
> ```python
> import pandas as pd
> import statsmodels.formula.api as smf
>
> data = pd.DataFrame({
>     "height": [150, 160, 170, 180, 190],  # cm
>     "weight": [47, 49, 60, 65, 79],      # kg
> })
> fit = smf.ols("weight ~ height", data=data).fit()
> print(fit.params.round(3))  # Intercept: -76.0; height: 0.8
> prediction = fit.predict(pd.DataFrame({"height": [175]}))
> print(round(prediction.iloc[0], 1))  # 64.0 kg
> # print(fit.summary())  # Optional: full regression table
> ```
>
> **Python alternative — scikit-learn**
>
> If needed, install once: `python -m pip install scikit-learn`.
>
> ```python
> from sklearn.linear_model import LinearRegression
>
> X = [[150], [160], [170], [180], [190]]  # 2D: rows = people, columns = features
> y = [47, 49, 60, 65, 79]               # 1D: weights in kg
> model = LinearRegression().fit(X, y)   # Includes an intercept by default
> print(round(model.intercept_, 3))      # -76.0
> print(round(model.coef_[0], 3))        # 0.8
> print(round(model.predict([[175]])[0], 1))  # 64.0 kg
> ```
>
> Even with one predictor, scikit-learn expects a **2D feature array**, so predict with `[[175]]`, not `[175]`. All three examples fit the same OLS line; statsmodels and R additionally provide regression summary tables with standard errors and tests.
>
> **R — built-in `lm()`, no extra packages**
>
> ```r
> data <- data.frame(
>   height = c(150, 160, 170, 180, 190),  # cm
>   weight = c(47, 49, 60, 65, 79)       # kg
> )
> fit <- lm(weight ~ height, data = data)
> round(coef(fit), 3)  # (Intercept): -76.0; height: 0.8
> predict(fit, newdata = data.frame(height = 175))  # 64 kg
> # summary(fit)  # Optional: full regression table
> ```
>
> Both fit $\widehat{\text{weight}}=-76+0.8\,\text{height}=60+0.8(\text{height}-170)$. The raw intercept $-76$ is the line's value at 0 cm, outside the observed range—not a meaningful weight prediction. The 64 kg output is a fitted average, not a guarantee for one individual. Summary-table tests and intervals require the noise assumptions discussed below.
>
> Documentation: [statsmodels formula interface](https://www.statsmodels.org/stable/example_formulas.html), [scikit-learn `LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html), [R `lm`](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html), [R `predict.lm`](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.lm.html).

Reference: [Berkeley STAT 151A, “Simple least squares” and interpretation](https://stat151a.berkeley.edu/spring-2026/lectures/unit1/simple_linear_regression.html#simple-least-squares).

## 2. How it works

### Fit the coefficients by minimizing squared residuals

For observation $i=1,\ldots,n$, let $x_i$ be the predictor and $y_i$ the response. A candidate line is $a+bx_i$. Its vertical gap from the observation is a **residual**. Ordinary least squares (OLS) chooses the intercept $a$ and slope $b$ to minimize

$$
S(a,b)=\sum_{i=1}^n(y_i-a-bx_i)^2.
$$

Squaring prevents positive and negative gaps from cancelling and gives larger gaps more influence. Differentiate with respect to the two coefficients:

$$
\frac{\partial S}{\partial a}=-2\sum_i(y_i-a-bx_i)=0,
\qquad
\frac{\partial S}{\partial b}=-2\sum_i x_i(y_i-a-bx_i)=0.
$$

Write $\bar x=n^{-1}\sum_i x_i$ and $\bar y=n^{-1}\sum_i y_i$. The first equation gives $a=\bar y-b\bar x$. Substitute into the second and use the fact that centered values sum to zero:

$$
0=\sum_i(x_i-\bar x)(y_i-\bar y)-b\sum_i(x_i-\bar x)^2.
$$

Thus, provided the predictor varies,

$$
\widehat b=\frac{S_{xy}}{S_{xx}},\qquad
\widehat a=\bar y-\widehat b\bar x,
\qquad
S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y),\quad
S_{xx}=\sum_i(x_i-\bar x)^2>0.
$$

The loss is a strictly convex quadratic under this condition, so this stationary point is the unique minimum. Reference: [Ng, CS229 notes, least-squares objective and normal equations, pp. 3–4 and 8–10](https://cs229.stanford.edu/summer2023/cs229-notes1.pdf#page=8).

For our five pairs, $x=(150,160,170,180,190)$ and $y=(47,49,60,65,79)$. We obtain $\bar x=170$, $\bar y=60$, $S_{xx}=1000$ and $S_{xy}=800$. Therefore $\widehat b=0.8$ and $\widehat a=-76$: the same line as $60+0.8(x-170)$. Its residuals are $(3,-3,0,-3,3)$ kg, with squared sum $36\text{ kg}^2$.

![[assets/figures/2026-11-09-regression-layers/02-loss-and-projection.svg]]

*Original illustration of the same data. Left: refit the intercept at each slope, keeping the line through $(\bar x,\bar y)$. Right: the five responses are now coordinates of one vector, with their mean removed; $\mathbf1$ denotes the all-ones vector. The perpendicular residual has length $\sqrt{36}=6$; it is not a distance measured on the height–weight scatterplot.*

### The vector form makes multiple regression possible

Let $y\in\mathbb R^n$ collect the responses and $X\in\mathbb R^{n\times p}$ contain the chosen features, including an all-ones column for an intercept. A coefficient vector $\beta\in\mathbb R^p$ produces the fit $X\beta$. OLS minimizes $\|y-X\beta\|_2^2$, the squared Euclidean length of its residual.

The [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Normal equations and OLS|normal equations]] are

$$
X^\top(y-X\widehat\beta)=0.
$$

They say that $e=y-\widehat y$ is perpendicular to every model direction, where $\widehat y=X\widehat\beta$. Consequently $\widehat y$ is the [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|orthogonal projection]] of $y$ onto $\operatorname{Col}(X)$, the space of all possible fitted vectors. If $X$ has full column rank, the unique coefficients are

$$
\widehat\beta=(X^\top X)^{-1}X^\top y.
$$

Reference: [Strang, MIT 18.06SC, “Projection matrices and least squares,” pp. 1–3](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/198bde3a6536b62989b6cc09495575c1_MIT18_06SCF11_Ses2.3sum.pdf).

These fitting identities require no normal-error assumption. For a random response vector $Y$, interpreting the model as a conditional mean adds $\mathbb E[Y\mid X]=X\beta$; inference adds noise assumptions. “Linear” refers to the coefficients: columns such as $x$ and $x^2$ still define a linear regression in those coefficients. With multiple predictors, a coefficient describes the fitted change when that predictor increases by one unit **holding the other predictors fixed**. For numerical computation, [[Backbone/Statistical computing & learning/Numerical methods & optimization/Numerical analysis for statistics/Numerical linear algebra/QR least squares|QR least squares]] solves the system without forming an explicit inverse; [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|SVD]] also handles rank deficiency.

## 3. Deeper understanding and connections

### The F statistic measures the squared distance gained by a larger model

Fit two nested models to the same observations. The reduced model permits fitted vectors in a subspace $\mathcal M_R$ of dimension $p_R$; the full model permits the larger subspace $\mathcal M_F$, of dimension $p_F$, with $p_R<p_F<n$. Include the intercept in these dimensions when present. Define

$$
g=\widehat y_F-\widehat y_R,\qquad
e_F=y-\widehat y_F,\qquad
e_R=y-\widehat y_R=g+e_F.
$$

The added-fit vector $g$ lies in $\mathcal M_F$, and $e_F$ is perpendicular to that space. Therefore

$$
\mathrm{SSE}_R-\mathrm{SSE}_F=\|g\|^2,
\qquad \mathrm{SSE}_R=\|e_R\|^2,\quad
\mathrm{SSE}_F=\|e_F\|^2.
$$

This is Pythagoras: improved fit is the squared distance **between the fitted vectors**. With $q=p_F-p_R$ added directions, $\nu=n-p_F$ residual [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom|degrees of freedom]], and $\mathrm{SSE}_F>0$,

$$
F=\frac{(\mathrm{SSE}_R-\mathrm{SSE}_F)/q}{\mathrm{SSE}_F/\nu}
=\frac{\|g\|^2/q}{\|e_F\|^2/\nu}.
$$

It compares improvement **per added direction** with remaining error **per residual direction**. The formula becomes an exact $F_{q,\nu}$ null test for prespecified nested models with fixed design and independent $N(0,\sigma^2)$ errors, $\sigma>0$, when the true mean lies in $\mathcal M_R$. Orthogonal Gaussian components give independent numerator and denominator sums of squares. [Purdue STAT 512, Topic 7, slides 10–11 and 18–20](https://www.stat.purdue.edu/~bacraig/notes512/Topic_7.pdf#page=18).

![[assets/figures/2026-11-09-regression-layers/03-fit-gain-and-test-region.svg]]

*Original illustration. In our data, the reduced model predicts the mean 60 for everyone; the full model fits height. Their squared errors are 676 and 36. The new direction explains 640, giving $F=640/(36/3)=53.33$. The right panel illustrates the Gaussian 5% test, not an empirical claim about height and weight.*

### The same triangle explains t, cotangent, and the rejection region

For simple regression with $n>2$, test the zero-slope null using $s^2=\mathrm{SSE}_F/(n-2)>0$. The signed slope statistic is

$$
t=\frac{\widehat b}{s/\sqrt{S_{xx}}},
\qquad
F=\frac{\widehat b^{,2}S_{xx}}{s^2}=t^2.
$$

Thus $t$ retains the slope's direction and $F$ measures its squared standardized size. The [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/One-restriction F equals t squared|one-restriction identity]] also applies inside multiple regression, using the matching restriction and the same full-model variance estimate.

For the acute angle $\phi$ between $e_R$ and $g$ when both legs are nonzero, $\cot\phi=\|g\|/\|e_F\|$. Hence

$$
F=\frac{\nu}{q}\cot^2\phi,
\qquad |t|=\sqrt{n-2}\cot\phi\quad\text{for this slope test}.
$$

In the figure, set $u=(x-\bar x\mathbf1)/\sqrt{S_{xx}}$, $c=u^\top(y-\bar y\mathbf1)$ and $r=\|e_F\|$; $\mathbf1$ is the all-ones vector. Here $t=\sqrt3\,c/r$. A two-sided 5% test rejects where $|t|>3.182$, equivalently $r<\sqrt3|c|/3.182$. **The statistic assigns a number to the data; a cutoff turns that number into a rejection region.** The shaded plot is a radial cross-section: the residual has three dimensions, giving a cone after removing the mean direction. The full region extends along that unrestricted mean direction. The angle and cross-section follow directly from the displayed identities; the threshold uses the $t_3$ null distribution.

### A best straight line and a conditional mean project onto different spaces

Now consider population random variables $Y,Z$ with finite second moments. The best population line minimizes $\mathbb E[(Y-a-bZ)^2]$ over $a,b$: it projects $Y$ onto $\operatorname{span}\{1,Z\}$. [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection|Conditional expectation as an L² projection]] instead allows **all** square-integrable measurable functions of $Z$:

$$
\mathbb E[Y\mid Z]
=\underset{h(Z)\in L^2}{\operatorname{argmin}}\;
\mathbb E[(Y-h(Z))^2],
$$

with equality and uniqueness understood almost surely. The conditioning space is closed and can be infinite-dimensional; a drawn “plane” is a schematic. The two projections agree when the conditional mean lies in the chosen linear span. Sample OLS estimates the population linear fit; its fitted coefficients need not equal the population coefficients. [Tropp, Caltech CMS/ACM 117, Lecture 19, §§19.1.2–19.2.2, printed pp. 287–290](https://tropp.caltech.edu/notes/Tro24-Probability-Theory-LN.pdf#page=302).

![[assets/figures/2026-11-09-regression-layers/04-linear-versus-conditional-mean.svg]]

*Original counterexample: $Z\sim\operatorname{Uniform}[-1,1]$, $Y=Z^2+\varepsilon$, $\mathbb E[\varepsilon\mid Z]=0$, with finite variance. Symmetry gives $\operatorname{Cov}(Z,Y)=0$, so the best straight line is $1/3$. Yet $\mathbb E[Y\mid Z]=Z^2$. Adding $Z^2$ as a feature lets a richer linear model represent that curve.*

## Origin and checks

> [!info]- Source details
> The three-level presentation follows the user's 2026-11-09 enrichment-design request. The existing personal OLS, F/t geometry and conditional-projection notes informed the connections; their full derivations remain in the learning layer. Definitions and results were checked against the precise university references cited above. The five height–weight pairs, nonlinear population example and all four figures are original Codex teaching constructions.
>
> The [[assets/figures/2026-11-09-regression-layers/draw_regression_layers.py|figure generator]] reproduces the GIF, static figures and [[assets/figures/2026-11-09-regression-layers/checks.json|26 numerical checks]]. Algebra verifies the general identities; numerical checks cover the example's coefficients, normal equations, projections, sums of squares, cotangent formula, F/t identity and test thresholds. Generated previews and frames spanning every GIF phase were inspected. No live Obsidian rendering check is implied.

```atlas
```
