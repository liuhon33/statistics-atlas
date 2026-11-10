---
id: learning-ols-slope-three-routes
title: Three routes from least squares to slope and correlation
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Simple slope and correlation]]"
subject: statistics
backbone_path: "Statistical inference & modeling → Regression & linear models → Linear regression → OLS estimation & geometry → Simple slope and correlation"
study_band: U
note_types: [derivation, question, insight]
question_roles: [reconcile-approaches, special-to-general, cross-topic-connection]
source_format: supplied-summary-and-handwriting
created: 2026-11-08
updated: 2026-11-09
status: active
verification: checked
learning_state: practicing
aliases: [Three derivations of the OLS slope correlation identity, Slope equals correlation times scale]
tags: [atlas/learning, subject/statistics, topic/regression]
connections:
  - "[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Normal equations and OLS]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/One-restriction F equals t squared]]"
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared]]"
sources:
  - "[[raw/notes/2026-11-02-Regression-Geometry-OLS-Correlation-t-and-F]]"
  - "[[raw/assets/2026-11-02-my-handdrawn-regression-geometry.png]]"
  - "[[raw/notes/2026-11-02-regression-slope-derivations-manifest.json]]"
---

# Three routes from least squares to slope and correlation

Statistical inference & modeling → Regression & linear models → Linear regression → OLS estimation & geometry → Simple slope and correlation

**Component derivatives, projection, and the vector gradient find the same least-squares fit.** For simple regression with an intercept,

$$
\boxed{\widehat\beta_1=\frac{S_{xy}}{S_{xx}}=r_{xy}\frac{s_y}{s_x}.}
$$

Correlation supplies the signed alignment of the centered data; the standard-deviation ratio supplies the slope's scale and units.

**My question, paraphrased from the 2026-11-02 focus request:** How do sum notation, cosine projection, and a vector gradient produce this same slope, and why is it a special case of multiple regression?

## Shared setup

For observed real pairs $(x_i,y_i)$, $i=1,\ldots,n$, take $n\ge2$ and define

$$
\bar x=\frac1n\sum_i x_i,\qquad \bar y=\frac1n\sum_i y_i,
$$

$$
S_{xx}=\sum_i(x_i-\bar x)^2,\quad
S_{yy}=\sum_i(y_i-\bar y)^2,\quad
S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y).
$$

Assume $S_{xx}>0$ and $S_{yy}>0$. The sample standard deviations and Pearson correlation are

$$
s_x=\sqrt{\frac{S_{xx}}{n-1}},\qquad
s_y=\sqrt{\frac{S_{yy}}{n-1}},\qquad
r_{xy}=\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}.
$$

The three slope proofs are data identities. They do not require Gaussian errors or positive residual variance; those conditions enter the later inference discussion. The fitted coefficient $\widehat\beta_1$ is distinct from a population coefficient $\beta_1$.

## 1. Component derivatives reveal why we center

For candidate intercept $a$ and slope $b$, minimize

$$
L(a,b)=\sum_{i=1}^n(y_i-a-bx_i)^2.
$$

Differentiate each parameter:

$$
\frac{\partial L}{\partial a}=-2\sum_i(y_i-a-bx_i),\qquad
\frac{\partial L}{\partial b}=-2\sum_i x_i(y_i-a-bx_i).
$$

The first equation gives $a(b)=\bar y-b\bar x$. Substituting into the second equation eliminates the intercept:

$$
\begin{aligned}
0
&=\sum_i x_i\{(y_i-\bar y)-b(x_i-\bar x)\}\\
&=\sum_i(x_i-\bar x)\{(y_i-\bar y)-b(x_i-\bar x)\}\\
&=S_{xy}-bS_{xx}.
\end{aligned}
$$

The middle equality uses the zero sums of the centered values. Consequently,

$$
\widehat\beta_1=\frac{S_{xy}}{S_{xx}},\qquad
\widehat\beta_0=\bar y-\widehat\beta_1\bar x.
$$

The profiled loss $L(a(b),b)$ has second derivative $2S_{xx}>0$, so this is the unique minimum. Substituting the definitions of $r_{xy},s_x,s_y$ shows

$$
r_{xy}\frac{s_y}{s_x}
=\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}
\sqrt{\frac{S_{yy}}{S_{xx}}}
=\frac{S_{xy}}{S_{xx}}.
$$

This expands the component-derivative argument in the [[raw/notes/2026-11-02-Regression-Geometry-OLS-Correlation-t-and-F|supplied summary]], §§2–3.

## 2. The cosine route finds the nearest point geometrically

Let $x,y\in\mathbb R^n$ be the observation vectors, $\mathbf1\in\mathbb R^n$ the all-ones vector, and $I_n$ the identity matrix. Center with

$$
C_n=I_n-\frac{\mathbf1\mathbf1^\top}{n},\qquad x_c=C_nx,\qquad y_c=C_ny.
$$

Then $S_{xx}=\|x_c\|^2$, $S_{yy}=\|y_c\|^2$, and $S_{xy}=x_c^\top y_c$, using the Euclidean norm. Write $u=x_c/\|x_c\|$ for the unit predictor direction and $\theta\in[0,\pi]$ for the angle between $x_c$ and $y_c$.

The **signed** projection coordinate is $\ell=u^\top y_c=\|y_c\|\cos\theta$. Decompose $y_c=\ell u+e$, with $u^\top e=0$. For any slope $b$, Pythagoras gives

$$
\|y_c-bx_c\|^2=\|e\|^2+(\ell-b\|x_c\|)^2.
$$

The closest point therefore has $b\|x_c\|=\ell$, yielding

$$
\widehat\beta_1=\frac{\ell}{\|x_c\|}
=\cos\theta\frac{\|y_c\|}{\|x_c\|}
=r_{xy}\frac{s_y}{s_x}.
$$

Here

$$
\cos\theta=\frac{x_c^\top y_c}{\|x_c\|\|y_c\|}=r_{xy}.
$$

An obtuse angle gives a negative projection coordinate and a negative slope. Replacing that coordinate with its length would lose the sign. Standardizing both variables makes $s_y/s_x=1$, so the simple-regression slope becomes the correlation.

The angle lives in the $n$-dimensional **observation space**. It is not the visual tilt of the fitted line in an $x$–$y$ scatterplot, which changes when the plot axes are rescaled. These are the centered-vector and angle arguments of summary §§1, 3–4.

## 3. A vector gradient collects the same equations

Use the design matrix $Z=[\mathbf1\;x]\in\mathbb R^{n\times2}$ and coefficient vector $\beta=(a,b)^\top$. Expand the same loss:

$$
L(\beta)=(y-Z\beta)^\top(y-Z\beta)
=y^\top y-2\beta^\top Z^\top y+\beta^\top Z^\top Z\beta.
$$

Because $Z^\top Z$ is symmetric, the two-component gradient is

$$
\nabla_\beta L=-2Z^\top(y-Z\beta).
$$

Its entries are exactly the two component derivatives in route 1. Setting it to zero gives the normal equations and, since nonconstant $x$ makes $Z$ full rank,

$$
Z^\top Z\widehat\beta=Z^\top y,\qquad
\widehat\beta=(Z^\top Z)^{-1}Z^\top y.
$$

The positive-definite Hessian $2Z^\top Z$ establishes uniqueness. The same equation says $Z^\top e=0$: the residual is perpendicular to the intercept and predictor directions, recovering route 2.

In the equivalent centered design $Z_c=[\mathbf1\;x_c]$, the orthogonal columns make the slope explicit:

$$
Z_c^\top Z_c=\begin{pmatrix}n&0\\0&S_{xx}\end{pmatrix},\qquad
Z_c^\top y=\begin{pmatrix}n\bar y\\S_{xy}\end{pmatrix}.
$$

The centered-design coefficients are $(\bar y,S_{xy}/S_{xx})^\top$. Returning to the original predictor origin changes only the intercept. The supplied summary's §2 gives the matrix route; the diagonal Gram-matrix display makes its one-predictor specialization explicit.

## Several predictors couple the coefficient equations

For one response and $k$ predictors with an intercept, let $X_c\in\mathbb R^{n\times k}$ contain the centered predictor columns. Assume full column rank and $y_c\ne0$; in particular $k+1\le n$. The same gradient gives the slope vector

$$
\widehat\beta_s=(X_c^\top X_c)^{-1}X_c^\top y_c.
$$

Put the predictor sample standard deviations in $D_x=\operatorname{diag}(s_{x_1},\ldots,s_{x_k})$. Define the predictor correlation matrix $R_{XX}\in\mathbb R^{k\times k}$ and the vector of marginal response correlations $r_{Xy}\in\mathbb R^k$ by

$$
R_{XX}=\frac{D_x^{-1}X_c^\top X_cD_x^{-1}}{n-1},\qquad
r_{Xy}=\frac{D_x^{-1}X_c^\top y_c}{(n-1)s_y}.
$$

Thus $X_c^\top X_c=(n-1)D_xR_{XX}D_x$ and $X_c^\top y_c=(n-1)s_yD_xr_{Xy}$. Substitution gives

$$
\boxed{\widehat\beta_s=s_yD_x^{-1}R_{XX}^{-1}r_{Xy}.}
$$

For standardized variables, the coefficient vector is

$$
\widehat\gamma=\frac{D_x\widehat\beta_s}{s_y}
=R_{XX}^{-1}r_{Xy},\qquad R_{XX}\widehat\gamma=r_{Xy}.
$$

**One predictor** gives $R_{XX}=[1]$, recovering $\widehat\beta_1=r_{xy}s_y/s_x$. **Several predictors** generally require the inverse correlation matrix: each coefficient adjusts for the other directions. The separate simple formulas still hold when the centered predictor columns are mutually orthogonal, so $R_{XX}=I_k$.

An earlier assistant-added example shows why the adjustment matters. Let $u=(-1,-1,1,1)^\top$ and $v=(-1,1,-1,1)^\top$. They are centered and orthogonal. With $x_1=u$, $x_2=u+v$, and $y=v$, the marginal correlation of $x_1$ with $y$ is zero, yet

$$
y=x_2-x_1
$$

has the unique multiple-regression slopes $(-1,1)$. The coefficient of $x_1$ is not its marginal correlation times an SD ratio. This standardized system and example were added in the earlier digest to develop the supplied summary's multiple-regression paragraph.

## My drawing connects the same projection to t and F

![[raw/assets/2026-11-02-my-handdrawn-regression-geometry.png]]

*My original projection and rejection-region sketch. The ratio marked $b/a$ uses side lengths; below, its denominator is clarified as residual length and the exact $n-2$ normalization is supplied. The colors and unlabeled surfaces remain a qualitative sketch.*

For the simple-regression fit, write $\widehat y_c=\widehat\beta_1x_c$ and $e=y_c-\widehat y_c$. Orthogonality gives

$$
\mathrm{TSS}=\|y_c\|^2=\underbrace{\|\widehat y_c\|^2}_{\mathrm{ESS}}
+\underbrace{\|e\|^2}_{\mathrm{RSS}},\qquad
R^2=\frac{\mathrm{ESS}}{\mathrm{TSS}}=r_{xy}^2.
$$

Now assume $n>2$ and positive RSS. Let $\widehat\sigma^2=\mathrm{RSS}/(n-2)$, and use the usual homoskedastic OLS standard-error formula. Since $\mathrm{RSS}=(1-r_{xy}^2)S_{yy}$,

$$
\widehat{\mathrm{SE}}(\widehat\beta_1)=\frac{\widehat\sigma}{\sqrt{S_{xx}}}
=\frac{s_y}{s_x}\sqrt{\frac{1-r_{xy}^2}{n-2}}.
$$

For the zero-slope statistic,

$$
t=\frac{\widehat\beta_1}{\widehat{\mathrm{SE}}(\widehat\beta_1)}
=r_{xy}\sqrt{\frac{n-2}{1-r_{xy}^2}}
=\sqrt{n-2}\cot\theta.
$$

The signed angle $\theta\in(0,\pi)$ retains the sign of $t$. The **length ratio** in my sketch instead gives

$$
\frac{L_{\mathrm{fit}}}{L_{\mathrm{res}}}
=\frac{\|\widehat y_c\|}{\|e\|}=|\cot\theta|,\qquad
F=\frac{\mathrm{ESS}/1}{\mathrm{RSS}/(n-2)}=t^2.
$$

This is just [[Why one restriction gives F equals t squared]]. And notice that F is the ratio of projection (difference in fit) squared over the perpendicular squared, which geometrically is exactly cotangent squared.

If the fitted centered vector is nonzero, its acute angle with $y_c$ gives this unsigned length ratio. When the fitted vector is zero, the ratio is zero even though an angle involving that zero vector is undefined.

For exact inference, additionally assume fixed nonconstant $x$ and the model $Y_i=\beta_0+\beta_1x_i+\varepsilon_i$, with independent $\varepsilon_i\sim\mathcal N(0,\sigma^2)$ and $\sigma^2>0$. Under $H_0:\beta_1=0$, $t\sim t_{n-2}$ and $F\sim F_{1,n-2}$. A two-sided level-$\alpha$ test, $0<\alpha<1$, rejects when

$$
|\cot\theta|>\frac{t_{n-2,1-\alpha/2}}{\sqrt{n-2}},
$$

where $t_{\nu,p}$ is the $p$-quantile of Student's t distribution with $\nu$ degrees of freedom. Alignment with either $+x_c$ or $-x_c$ can lead to rejection. The exact angular boundary depends on $n$ and $\alpha$.

These identities develop summary §§4–6 and the drawing. A matching one-coefficient restriction in multiple regression also has $F=t^2$ under the classical test formulas; the global test of several coefficients generally differs. The projection alone does not establish the null distributions.

## Boundaries of the slope identity

- Without an intercept, the slope is $x^\top y/(x^\top x)$ for $x\ne0$; the centered Pearson identity need not apply.
- A constant predictor makes the separate slope and intercept unidentifiable.
- With constant $y$ and nonconstant $x$, the slope is zero, but Pearson correlation is undefined.
- A perfect linear fit still satisfies the slope identity; its zero residual standard error makes the usual t statistic undefined.

The algebra, dimensions, rank conditions, centering, signs, and inference assumptions were checked directly. Exact arithmetic confirms agreement of all three routes for $r_{xy}=-3/5$, $s_y/s_x=2$, and $\widehat\beta_1=-6/5$, and confirms the two-predictor counterexample. These calculations support the derivations above.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|Orthogonal projection]] — The nearest-point argument derives the slope without differentiation and explains why the residual cross term vanishes.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Normal equations and OLS|Normal equations and OLS]] — The vector gradient combines the component derivatives and extends the one-predictor identity to the coupled multiple-regression system.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/One-restriction F equals t squared|One-restriction F equals t squared]] — The same fit/residual triangle yields the signed t statistic and the squared-length F comparison for the matching restriction.

- [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared|Why one restriction gives F equals t squared]] — Expands the fit/residual triangle into a constrained-SSE proof, distinguishing one restriction from one predictor.

## Origin

> [!info]- Source details
> This note consolidates the already-digested 2026-11-02 [[raw/notes/2026-11-02-Regression-Geometry-OLS-Correlation-t-and-F|supplied summary]] and my original drawing. Its focus is §§1–3, the multiple-predictor extension, and selected §§4–6/§9 qualifications. The [[raw/notes/2026-11-02-regression-slope-derivations-manifest.json|original manifest]] preserves the exact focus request, hashes, and earlier coverage.
>
> I supplied the summary and identified the drawing as mine. The expanded sum proof, diagonal Gram-matrix presentation, standardized multiple-regression system, counterexample, and precise sign/assumption corrections include earlier assistant contributions. The summary is not a verbatim transcript; its complete authorship and described underlying chat turns are not established. The earlier CI/Cauchy/L2 source material remains outside this focused migration, and its source-authored recall prompts are not recorded as questions I asked.
