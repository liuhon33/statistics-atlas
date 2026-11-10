---
id: learning-z-t-f-test-geometry
title: Geometric interpretation of z, t, and F tests
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles]]"
subject: statistics
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles
study_band: U–M
note_types:
  - topic-note
  - derivation
  - insight
source_format: video-screenshots-and-handwriting
created: 2026-11-09
updated: 2026-11-10
status: active
verification: checked
learning_state: unknown
aliases:
  - Hypothesis testing as planes cones and wedges
  - Geometry of rejection regions
tags:
  - atlas/learning
  - subject/statistics
  - topic/hypothesis-testing
  - topic/geometry
connections:
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Classical comparisons/One- and two-sample t procedures]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Nested-model F tests]]"
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared]]"
  - "[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget]]"
sources:
  - https://www.youtube.com/watch?v=AvUtMSI_4pM
  - "[[raw/notes/2026-11-09-Hidden-Geometry-Hypothesis-Testing-auto-captions.txt]]"
  - "[[raw/assets/2026-11-09-Test-geometry-I01-z-test-statement.png]]"
  - "[[raw/assets/2026-11-09-Test-geometry-I02-z-test-parallel-planes.png]]"
  - "[[raw/assets/2026-11-09-Test-geometry-I03-z-test-projection-view.png]]"
  - "[[raw/assets/2026-11-09-Test-geometry-I04-t-test-double-cone.png]]"
  - "[[raw/assets/2026-11-09-Test-geometry-V01-F-wedge-18m58s.jpg]]"
  - "[[raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics.pdf]]"
  - "[[assets/figures/2026-11-09-test-geometry/draw_test_geometry.py]]"
  - "[[assets/figures/2026-11-09-test-geometry/checks.json]]"
---

# Geometric interpretation of z, t, and F tests

Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles

**A hypothesis test draws a boundary in the space of possible datasets.** The shape tells us what counts as a large departure from the null: an absolute mean displacement when the noise scale is known, a mean-to-spread ratio when it is estimated, or an improvement-to-residual ratio when comparing two fitted models.

**Video backlink:** [Math with Ming — The Hidden Geometry Behind Hypothesis Testing](https://www.youtube.com/watch?v=AvUtMSI_4pM). Jump to [z: 3:26](https://www.youtube.com/watch?v=AvUtMSI_4pM&t=206s), [t: 9:27](https://www.youtube.com/watch?v=AvUtMSI_4pM&t=567s), or [F: 13:18](https://www.youtube.com/watch?v=AvUtMSI_4pM&t=798s).

| Test | What is compared? | Shape in the illustrated 3D example |
| --- | --- | --- |
| z | Mean departure / known noise scale | Reject outside two parallel planes. |
| t | Mean departure / estimated noise scale | Reject inside a double cone. |
| F | Added squared fit per restriction / remaining squared error per residual df | Reject in wedges around the full-model plane, away from the null line. |

## First identify the vector and its two components

One entire sample is one point $x=(x_1,\ldots,x_n)^\top\in\mathbb R^n$. Each coordinate represents an observation, not a predictor. We draw $n=3$ so this space is visible; the equations below allow general $n\ge2$.

For the one-sample tests, assume $X_1,\ldots,X_n$ are iid $N(\mu,\sigma^2)$, with $\sigma>0$, and test $H_0:\mu=\mu_0$ against $H_A:\mu\ne\mu_0$. The null value $\mu_0$ is specified before looking at the sample. Define

$$
\mathbf1=(1,\ldots,1)^\top,\quad u=\frac{\mathbf1}{\sqrt n},\quad
d=x-\mu_0\mathbf1,
$$

$$
a=u^\top d=\sqrt n(\bar x-\mu_0),\qquad
r=x-\bar x\mathbf1,\qquad \rho=\|r\|.
$$

Then

$$
\boxed{d=au+r,\qquad u^\top r=0,\qquad \|d\|^2=a^2+\rho^2.}
$$

The signed coordinate $a$ measures the mean's departure from the null. The perpendicular residual length $\rho$ measures sample spread. Since $u$ is a **unit** vector, the mean-displacement length is $|a|=\sqrt n|\bar x-\mu_0|$. The all-ones vector itself has length $\sqrt n$.

![[raw/assets/2026-11-09-Test-geometry-I01-z-test-statement.png|650]]

*Supplied statement of the three-observation testing problem. The original is preserved unchanged; the diagrams below are new analytic illustrations.*

## 1. z test — parallel planes perpendicular to the all-ones direction

![[assets/figures/2026-11-09-test-geometry/01-z-parallel-planes.svg]]

*Original Codex illustration. The blue arrow is parallel to $\mathbf1$; the dashed middle plane has $\bar x=\mu_0$. The two red boundary planes are parallel and perpendicular to that direction. The origin of the drawing is the null point $\mu_0\mathbf1$. The right panel fixes one residual coordinate and shows an exact cross-section. Here $\sigma=1$ and $\alpha=0.05$.*

### Read the picture

[[Standardization geometry - means, lengths, and correlation|how to read the graph]]

Moving along $u$ changes every observation equally, so it changes the sample mean without changing the residuals. Moving parallel to one of the planes changes residual coordinates without changing the mean. Every point on the same plane therefore has the same z statistic.

Because the **population variance is known**, the test already has a noise ruler. The sample variance does not set this test's threshold. Reject when the endpoint lies beyond either red plane; points between them do not lead to rejection. This is the video's argument at 5:10–9:27.

### Derive the planes

Under $H_0$, the sample mean has variance $\sigma^2/n$, so

$$
Z=\frac{\bar X-\mu_0}{\sigma/\sqrt n}=\frac{a}{\sigma}\sim N(0,1).
$$

Let $z_*=\Phi^{-1}(1-\alpha/2)$, where $\Phi$ is the standard normal CDF and $0<\alpha<1$. The two-sided decision is

$$
|z|>z_*
\quad\Longleftrightarrow\quad
|a|>z_*\sigma
\quad\Longleftrightarrow\quad
\left|\sum_i x_i-n\mu_0\right|>z_*\sigma\sqrt n.
$$

Thus the boundaries are

$$
\boxed{\mathbf1^\top x=n\mu_0\pm z_*\sigma\sqrt n.}
$$

For $n=3$, these are two planes with the same normal $(1,1,1)^\top$. In general they are hyperplanes. Their **perpendicular separation** is $2z_*\sigma$: divide the difference of the right-hand constants by $\|\mathbf1\|=\sqrt n$. In scalar sample-mean units, the half-width is $z_*\sigma/\sqrt n$.

At 5%, $z_*=1.959964$. A smaller significance level makes $z_*$ larger and the slab wider. The null sampling law is the normal-sample theorem's standardized-mean result in [Lockhart, STAT 801, opening theorem](https://www.sfu.ca/~lockhart/richard/801/01_1/lectures/normal_samples/web.html).

## 2. t test — the mean departure must be large relative to spread

![[assets/figures/2026-11-09-test-geometry/02-t-double-cone.svg]]

*Original Codex illustration for $n=3$ and $\alpha=0.05$. The cone apex is $\mu_0\mathbf1$ and the axis is the all-ones line. **The interiors of both cones are rejection regions.** Perspective changes the apparent opening; the calculated half-angle is $18.195^\circ$. The cone rims only truncate the drawing.*

### Why the planes become cones

Now the unknown quantity is the **population variance $\sigma^2$**. We calculate the sample variance

$$
s^2=\frac{\sum_i(x_i-\bar x)^2}{n-1}=\frac{\rho^2}{n-1}
$$

and use it to estimate the noise scale. A larger $s$ makes a fixed mean departure less surprising. The rule should therefore compare the two perpendicular components, rather than use the mean displacement alone.

**My intuition, paraphrased from this request:** as sample spread grows, the test should tolerate a larger departure of the sample mean. Rejection requires the mean component to remain large *relative to* that spread.

![[assets/figures/2026-11-09-test-geometry/03-t-spread-and-angle.svg]]

*Original Codex illustration. Left: the arrow A → B increases residual length while holding the mean departure fixed; the observation leaves the rejection region. Right: an equal-scale right triangle makes the cotangent visible. Its angle is measured from the mean axis, with $|a|$ adjacent and $\rho$ opposite. Only the positive-mean half is shown in the left panel; the negative half is its reflection.*

For fixed $n$ and $\alpha$, the rejection condition can be written

$$
\boxed{|\bar x-\mu_0|>t_*\frac{s}{\sqrt n}.}
$$

Doubling $s$ doubles the required absolute mean departure. This does **not** change the chosen significance level or critical t value. It changes the threshold in the original measurement units. Conversely, multiplying both $a$ and $\rho$ by the same positive factor leaves the decision unchanged: the relevant information is an angle. This is the video's rationale at 9:28–11:30.

### Derive the cotangent and the cone boundary

For $\rho>0$,

$$
t=\frac{\sqrt n(\bar x-\mu_0)}s
=\sqrt{n-1}\frac a\rho.
$$

Let $\theta\in(0,\pi/2]$ be the acute-or-right angle between $d$ and the **unoriented** all-ones line. Then

$$
|a|=\|d\|\cos\theta,\qquad
\rho=\|d\|\sin\theta,
\qquad \boxed{|t|=\sqrt{n-1}\cot\theta.}
$$

The [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic#3. The t ratio is a cotangent|signed angle]] to $+u$ instead lies in $(0,\pi)$ and gives $t=\sqrt{n-1}\cot\theta_{\rm signed}$. Using $|t|$ includes departures toward both ends of the mean line.

Under $H_0$, with $\nu=n-1$,

$$
\frac a\sigma\sim N(0,1),\qquad
Q=\frac{\rho^2}{\sigma^2}\sim\chi^2_\nu,
\qquad \frac a\sigma\ \perp\ Q.
$$

The independent normal/chi-square ratio therefore gives

$$
T=\frac{a/\sigma}{\sqrt{Q/\nu}}\sim t_\nu.
$$

The independence uses the **Gaussian** model: orthogonal projections are jointly normal with zero cross-covariance. A right triangle alone does not prove independence. See the independent mean/variance and t statements in [Lockhart's opening theorem](https://www.sfu.ca/~lockhart/richard/801/01_1/lectures/normal_samples/web.html).

Put $t_*=t_{\nu,1-\alpha/2}$, the indicated Student quantile. Then

$$
|t|>t_*
\quad\Longleftrightarrow\quad
\rho<\frac{\sqrt\nu}{t_*}|a|
\quad\Longleftrightarrow\quad
\boxed{\theta<\arctan\!\left(\frac{\sqrt\nu}{t_*}\right).}
$$

Rotating this two-sided triangular region around the mean line gives the double cone. With $n=3$, $\nu=2$ and $\alpha=0.05$, $t_*=4.302653$, giving $\theta_*=18.194872^\circ$, consistent with the supplied t screenshot and video 11:33–12:42. Smaller $\alpha$ makes the cones narrower. Zero sample variance makes the ordinary ratio undefined; it has probability zero under the stated continuous nondegenerate model.

### Why the sample variance divides by n − 1

The residual vector satisfies $\mathbf1^\top r=0$. Once its first $n-1$ coordinates are chosen, the last is determined. Hence it lives in an $(n-1)$-dimensional subspace.

More precisely, let $P=uu^\top$ and $\varepsilon=X-\mu\mathbf1$. Under iid observations with common finite variance $\sigma^2$,

$$
r=(I_n-P)\varepsilon,\qquad
\mathbb E\|r\|^2
=\operatorname{tr}\!\left((I_n-P)\sigma^2 I_n\right)
=(n-1)\sigma^2.
$$

Here $I_n$ is the identity and $\operatorname{tr}$ is the sum of diagonal entries; the projector has one eigenvalue 0 and $n-1$ eigenvalues 1. Dividing by $n-1$ makes $S^2$ unbiased. Normality is unnecessary for this expectation identity; it is needed for the exact chi-square and t laws above. Fitting a full-rank regression with $p_F$ coefficients uses $p_F$ directions and similarly leaves $n-p_F$ residual degrees of freedom.

## 3. F test — compare the extra fit with the error that remains

![[assets/figures/2026-11-09-test-geometry/04-f-two-fits-and-sse.svg]]

*Original Codex illustration of the triangle in the video (17:14–18:18) and handwritten PDF pp. 1–2, 4. $A=y$ is the response vector, $C=\hat y_F$ the full fit, and $D=\hat y_R$ the reduced fit. The left view shows their nested spaces; the right view shows their exact right triangle. These are observation-space projections, not vertical residuals in a scatterplot.*

### Read the three sides

For simple regression with an intercept and a nonconstant fixed predictor $x$, the full model allows

$$
\mathcal M_F=\operatorname{span}(\mathbf1,x),
$$

whereas the no-slope null allows only

$$
\mathcal M_R=\operatorname{span}(\mathbf1)\subset\mathcal M_F.
$$

For three observations, these are a plane and a line. Fit both by orthogonal projection. The full model has more freedom, so it cannot fit worse in ordinary least squares on the same observations.

| Side | Vector | Squared length |
| --- | --- | --- |
| $DA$ | $e_R=y-\hat y_R$ | Reduced-model $\mathrm{SSE}_R$ |
| $CA$ | $e_F=y-\hat y_F$ | Full-model $\mathrm{SSE}_F$ |
| $DC$ | $g=\hat y_F-\hat y_R$ | Improvement $\mathrm{SSE}_R-\mathrm{SSE}_F$ |

The added-fit vector $g$ lies in the full-model space; $e_F$ is perpendicular to that whole space. Therefore

$$
e_R=g+e_F,\qquad g^\top e_F=0,
$$

$$
\boxed{\mathrm{SSE}_R=\|g\|^2+\mathrm{SSE}_F,
\qquad \mathrm{SSE}_R-\mathrm{SSE}_F=\|\hat y_F-\hat y_R\|^2.}
$$

This is why the difference between the two SSEs is the squared distance **between their fitted vectors**. It is not the squared difference of their residual lengths. The Pythagorean identity depends on nested least-squares spaces.

A long $DC$ relative to $CA$ means that allowing the extra directions removes a great deal of error compared with the unexplained variation that remains. A short $DC$ gives little evidence for needing those extra directions.

### Derive the general statistic and its null distribution

Prespecify nested linear mean spaces with dimensions $p_R<p_F<n$. Let $P_R,P_F$ be their orthogonal projectors, set

$$
q=p_F-p_R,\qquad \nu=n-p_F,
$$

and assume $Y=\mu+\varepsilon$, $\mu\in\mathcal M_F$, with $\varepsilon\sim N_n(0,\sigma^2 I_n)$, $\sigma>0$. Here $p_F$ includes an intercept if present; $q$ counts tested independent restrictions.

Nestedness gives $P_FP_R=P_RP_F=P_R$. Consequently $P_F-P_R$ is a rank-$q$ projector, $I_n-P_F$ is a rank-$\nu$ projector, and their product is zero. Under $H_0:\mu\in\mathcal M_R$,

$$
\frac{\|g\|^2}{\sigma^2}\sim\chi^2_q,\qquad
\frac{\|e_F\|^2}{\sigma^2}\sim\chi^2_\nu,
$$

independently by Gaussian orthogonal coordinates. Thus

$$
\boxed{F=\frac{(\mathrm{SSE}_R-\mathrm{SSE}_F)/q}{\mathrm{SSE}_F/\nu}
=\frac{\|g\|^2/q}{\|e_F\|^2/\nu}\sim F_{q,\nu}\quad\text{under }H_0.}
$$

The numerator is improvement **per added direction**. The denominator estimates $\sigma^2$ using the **full model's** remaining residual directions. Reject for $F>F_{q,\nu;1-\alpha}$. These degrees-of-freedom factors are essential beyond the video's $q=\nu=1$ example. The two original SSEs are correlated; it is the *improvement* and the full SSE that are independent under this model.

For the acute angle $\phi=\angle ADC$, when both legs are nonzero,

$$
\cot\phi=\frac{DC}{CA}=\frac{\|g\|}{\|e_F\|},
\qquad \boxed{F=\frac\nu q\cot^2\phi.}
$$

Large F corresponds to a small angle: the reduced residual points mostly along an added model direction, rather than away from the full-model space.

### Why the video's boundary is a wedge

![[assets/figures/2026-11-09-test-geometry/05-f-wedge-and-cross-section.svg]]

*Original Codex illustration. The red plane is the full model and the blue line the null model. Both green boundary planes contain that line. The left opening is deliberately enlarged to $18^\circ$ (20% for this $F_{1,1}$ example); the right panel shows the exact 5% opening of $4.5^\circ$ with equal coordinate scales.*

For $n=3$, $p_R=1$, $p_F=2$, both the added direction and full residual direction are one-dimensional. In orthonormal coordinates write

$$
y=h u_0+b u_1+c u_2,
$$

where $u_0$ spans the null line, $u_1$ is the added direction, and $u_2$ is normal to the full plane. Here $F=b^2/c^2$. At critical value $F_*$,

$$
c=\pm\frac{b}{\sqrt{F_*}}
$$

describes **two planes**, because $h$ is unrestricted. Reject in the two opposite sectors $|c|<|b|/\sqrt{F_*}$, swept along the entire null line. Changing $h$ changes the fitted intercept but not the evidence about the slope. These are the wedges shown at [18:48–19:32](https://www.youtube.com/watch?v=AvUtMSI_4pM&t=1128s).

![[raw/assets/2026-11-09-Test-geometry-V01-F-wedge-18m58s.jpg|550]]

*Source frame captured at 18:58 from Math with Ming's video. Its colored planes motivate the labeled reconstruction above; its displayed angle is not treated as a calibrated 5% boundary.*

This is just [[Three routes from least squares to slope and correlation#My drawing connects the same projection to t and F|the same as here]].

For larger $q$ or $\nu$, replace the scalars $b,c$ by vectors in their respective subspaces. The boundary is

$$
\|c\|^2=\frac{\nu}{qF_*}\|b\|^2,
$$

a quadratic cone in the residualized space, extended along the null-model directions. **Two planes are a special case, not the general shape of every F test.** Nonzero coefficient restrictions can give affine null sets; translate to a point satisfying the restriction before using the corresponding centered picture.

For one tested direction, the signed standardized coordinate is a t statistic and its square is this F statistic. The [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared#3. Combine the two pieces to obtain F = t squared|one-restriction proof]] develops that identity, multiple-regression restrictions, and confidence intervals.

## Rejection regions, p-values, and confidence intervals

A level-$\alpha$ test has null probability at most $\alpha$ of landing in its rejection region, for every parameter allowed by the null (compare [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget#ROC space connects the optimization to classification|ROC space]]). For the continuous Gaussian models here, the stated cutoffs give equality. The p-value is the null probability of a statistic at least as extreme as the observed one, using the test's chosen notion of extremeness:

$$
p_z=2\{1-\Phi(|z|)\},\qquad
p_t=2\{1-T_\nu(|t|)\},\qquad
p_F=1-G_{q,\nu}(F),
$$

where $T_\nu$ and $G_{q,\nu}$ are the Student and F CDFs. With the strict rejection rules used here, reject when $p<\alpha$. This is a probability under the null model, not the probability that the null is true. A non-rejection does not establish the null.

There is a particularly direct visual check for the one-sample $n=3$ t test: under $H_0$, the direction of $d$ is uniform on a sphere. The two caps whose directions are at least as aligned with the mean axis as the observed angle $\theta$ occupy the fraction

$$
p_t=\frac{2[2\pi R^2(1-\cos\theta)]}{4\pi R^2}
=1-\cos\theta.
$$

At the boundary $\theta=18.194872^\circ$, this is $0.05$. Radius $R$ cancels. This cap formula is specific to three observations; angles are not uniformly distributed in arbitrary dimension. It also explains why merely comparing geometric volumes would be wrong for a general nonuniform sampling distribution.

Finally, hold the data fixed and vary the hypothesized value. The null values not rejected form a confidence set. For the one-sample t test,

$$
\left|\frac{\bar x-\mu_0}{s/\sqrt n}\right|\le t_*
\quad\Longleftrightarrow\quad
\mu_0\in\left[\bar x-t_*\frac{s}{\sqrt n},\ \bar x+t_*\frac{s}{\sqrt n}\right].
$$

The geometry is now inverted: the data point stays still while the candidate null point moves. The companion regression note performs the same inversion for a slope.

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Classical comparisons/One- and two-sample t procedures|One- and two-sample t procedures]] — The one-sample decision rule becomes a double cone when written as mean departure divided by residual length; two-sample variants need their own variance and df formulas.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation|p-value interpretation]] — Tail probabilities calibrate the geometric rejection regions, with a spherical-cap interpretation for the three-observation t example.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom|Residual variance and degrees of freedom]] — Residual subspace dimensions explain the divisors $n-1$ and $n-p_F$, and the dimension factors in the cotangent formulas.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Nested-model F tests|Nested-model F tests]] — Pythagoras turns the distance between two nested fitted vectors into the numerator of the model-comparison test.
- [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared|Why one restriction gives F equals t squared]] — The same fitted-distance triangle yields a squared coefficient t statistic for one restriction and links that geometry to p-values and interval inversion.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget|Hypothesis testing - maximizing power under an error budget]] — Integrating the same rejection region under null and alternative distributions turns its geometry into Type I error and power, the coordinates of ROC space.

## Origin

> [!info]- Source details
> Based on my request for a visual comparison, four supplied screenshots, and Math with Ming's [video](https://www.youtube.com/watch?v=AvUtMSI_4pM) (published April 10, 2026). The complete available [[raw/notes/2026-11-09-Hidden-Geometry-Hypothesis-Testing-auto-captions.txt|automatic captions]] were read; the z/t statements and source diagrams were inspected, together with the F frame at 18:58. Automatic captions are checked against the formulas rather than treated as exact mathematical transcription. The handwritten PDF's projection triangle supplies the link to my regression work.
>
> Codex added the analytic diagrams, explicit notation and general-$n$ derivations, the n−1 trace argument, general nested-model proof, and spherical-cap p-value interpretation. The requested intuition is labeled as a paraphrase; no extra question is attributed to me. The originals remain intact. Screenshots I02–I04 remain linked in `sources`; their geometry is represented by the clean figures instead of repeating a gallery.
>
> Verification: algebra, orthogonality, projection ranks, Gaussian independence, critical values, angular boundaries, and matching F/t tail probabilities were checked. The [[assets/figures/2026-11-09-test-geometry/draw_test_geometry.py|figure and verification script]] reproduces the illustrations; [[assets/figures/2026-11-09-test-geometry/checks.json|numerical checks]] support the proofs. Perspective diagrams show subspaces; only the flat equal-scale panels are intended for measuring angles.
