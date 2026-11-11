---
id: learning-testing-power-optimization
title: Hypothesis testing - maximizing power under an error budget
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles]]"
subject: statistics
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles
study_band: U–M
note_types:
  - question
  - derivation
  - insight
question_roles:
  - mechanism
  - cross-topic-connection
  - assumption-boundary
source_format: handwriting-and-pasted-conversation
created: 2026-11-10
updated: 2026-11-11
status: active
verification: checked
learning_state: unknown
aliases:
  - What does maximizing power over test functions mean
tags:
  - atlas/learning
  - subject/statistics
  - topic/hypothesis-testing
connections:
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Neyman–Pearson lemma]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Intervals & test inversion/Inverting a test]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Power and sample size]]"
  - "[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways]]"
  - "[[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly]]"
sources:
  - "[[assets/figures/2026-11-10-testing-power/draw_precision_areas.py]]"
  - "[[assets/figures/2026-11-10-testing-power/precision-areas-checks.json]]"
  - https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc
  - "[[raw/assets/2026-11-10-Hypothesis-testing-I01-testing-objective.png]]"
  - "[[raw/assets/2026-11-10-Hypothesis-testing-I02-normal-and-randomized-binomial-tests.png]]"
  - "[[raw/assets/2026-11-10-Hypothesis-testing-I03-wald-and-p-values.png]]"
  - "[[raw/assets/2026-11-10-Hypothesis-testing-I04-Bayes-area-reference.png]]"
  - "[[raw/conversations/2026-11-10-testing-optimization-pasted-excerpt.md]]"
  - "[[assets/figures/2026-11-10-testing-power/build_testing_power.py]]"
  - "[[assets/figures/2026-11-10-testing-power/checks.json]]"
  - "[[assets/figures/2026-11-10-testing-power/draw_roc_relationships.py]]"
  - "[[assets/figures/2026-11-10-testing-power/roc-error-rates-checks.json]]"
  - "[[assets/figures/2026-11-10-testing-power/draw_decision_rule.py]]"
  - "[[assets/figures/2026-11-10-testing-power/decision-rule-checks.json]]"
  - https://chatgpt.com/share/6af2b4eb-b7f8-83ea-ba74-4602a596117d
  - https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html
---

# Hypothesis testing - maximizing power under an error budget

Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles

**We choose the entire decision rule, not the true parameter.** Among rules that rarely reject when the null is true, we want one that rejects as often as possible when a specified alternative is true. The same rule is evaluated under two different sampling distributions: one supplies the constraint, the other supplies the objective.

> **My question, preserved from the pasted conversation:** “I understand majority of testing hypothesis rejection, but I just wanna know this maximization abtact equation , can you give me some numerical example to demonstrate the max with constraint?”

## 1. What is being optimized?

![[raw/assets/2026-11-10-Hypothesis-testing-I01-testing-objective.png|800]]
*Original handwriting: maximize rejection probability under the alternative while controlling it under the null. Read the disjoint sets as $\Theta_0$ and $\Theta_1$ throughout.*

Let $X$ denote the **whole dataset**, with distribution $P_\theta$. The parameter $\theta$ is fixed but unknown. A test is a function $\phi:\mathcal X\to[0,1]$:

- $\phi(x)=1$: reject $H_0$ for dataset $x$.
- $\phi(x)=0$: do not reject.
- $\phi(x)=\gamma\in(0,1)$: after observing $x$, reject with probability $\gamma$ using independent randomization.

The **power function**, including its values on the null, is

$$
\beta_\phi(\theta)=E_\theta[\phi(X)].
$$

For a nonrandomized rule this is $P_\theta(X\in R)$, where $R$ is the rejection region. For a randomized rule, write the actual decision as $D=\mathbf1\{U\le\phi(X)\}$ with independent $U\sim\mathrm{Unif}(0,1)$. Then $P_\theta(D=1)=E_\theta[\phi(X)]$ as well.

| Evaluate the same function at… | Meaning of $\beta_\phi(\theta)$ |
|---|---|
| $\theta\in\Theta_0$ | Type I error probability |
| $\theta\in\Theta_1$ | Power; Type II error probability is $1-\beta_\phi(\theta)$ |

**Notation trap:** here $\beta_\phi$ means rejection probability, not Type II error. Textbooks also use plain $\beta$ for Type II error; below that latter quantity is $\beta_{\mathrm{II}}$.

For a fixed alternative $\theta_1$, the optimization is precisely

$$
\boxed{\max_{\phi:\mathcal X\to[0,1]}E_{\theta_1}[\phi(X)]
\quad\text{subject to}\quad
\sup_{\theta\in\Theta_0}E_\theta[\phi(X)]\le\alpha.}
$$

Think of $\phi(x)$ for **each possible dataset** as a decision variable. The distributions, hypotheses, sample size, and allowed error $\alpha$ are fixed while comparing rules. We are not maximizing over the observed $x$, choosing the truth $\theta$, or maximizing a posterior probability of $H_1$.

In plain language: we choose a decision rule that specifies which values of 𝑋 lead to rejection (1) and which lead to failure to reject (0). We want to maximize power—our probability of correctly rejecting the null when a real effect exists (𝜃1)—while keeping the probability of rejection when no effect exists (𝜃0) at or below 𝛼 (for example, 0.05).

![[assets/figures/2026-11-10-testing-power/decision-rule-two-worlds.svg]]
*Added illustration: one fixed rejection region, evaluated under two possible sampling distributions. The shaded orange area is the false-positive probability; the shaded green area is power—not the probability that the alternative is true.*

Here $X\sim N(\theta,1)$, with $\theta_0=0$ and a specified alternative $\theta_1=2$. We choose the cutoff $c$, not either distribution: reject when $X>c$. Lowering $c$ increases both shaded areas. Among these upper-tail rules, $c\approx1.645$ gives the greatest power allowed by the $\alpha=0.05$ budget: **5% false positives under the null and about 63.9% power under this alternative**. This is a one-sided illustration; a general rejection region need not be a single upper tail.

## 2. Two flips: the abstract problem becomes four numbers

**Numerical example from the supplied conversation.** Independently flip a coin twice and test

$$
H_0:p=0.5\qquad\text{versus}\qquad H_1:p=0.8,
\qquad\alpha=0.25.
$$

The unusually large $\alpha$ makes the finite example transparent; it is not a recommended default.

| Dataset $x$ | $P_{0.5}(x)$: cost of rejecting | $P_{0.8}(x)$: power gained | Ratio $P_{0.8}(x)/P_{0.5}(x)$ |
| ----------- | ------------------------------: | -------------------------: | ----------------------------: |
| TT          |                            0.25 |           0.2 * 0.2 = 0.04 |                          0.16 |
| TH          |                            0.25 |                       0.16 |                          0.64 |
| HT          |                            0.25 |                       0.16 |                          0.64 |
| HH          |                            0.25 |                       0.64 |                          2.56 |

Both probability columns sum to 1. Including an outcome in the rejection region uses its **null probability** from the error budget and adds its **alternative probability** to power.

### Compare rules, not parameter values

| Rule | Rejection region | Type I error | Power at $p=0.8$ | Allowed? |
|---|---|---:|---:|---|
| A | HH only | 0.25 | **0.64** | Yes |
| B | TH only | 0.25 | 0.16 | Yes, but worse |
| C | TH, HT, HH | 0.75 | 0.96 | **No** |
| Always reject | All four outcomes | 1 | 1 | **No** |
| Never reject | None | 0 | 0 | Yes, but uninformative |

A and B spend the **same** Type I error budget. A gets much more power. C has greater power but is not a feasible competitor. Without the constraint, “always reject” would trivially win.

### Write the actual optimization—and prove the maximum

Set $a=\phi(TT)$, $b=\phi(TH)$, $c=\phi(HT)$, $d=\phi(HH)$. Then

$$
\max_{a,b,c,d}\;0.04a+0.16b+0.16c+0.64d
$$

subject to

$$
0.25(a+b+c+d)\le0.25,
\qquad 0\le a,b,c,d\le1.
$$

The constraint is $a+b+c+d\le1$. Consequently,

$$
0.04a+0.16b+0.16c+0.64d
\le0.64(a+b+c+d)\le0.64.
$$

The rule $(a,b,c,d)=(0,0,0,1)$ attains the bound. Therefore **0.64 is the global maximum, even allowing randomized rules**, not merely the best of A, B, and C. The inequality is the proof; enumerating all 16 nonrandomized rules is an additional check.

![[assets/figures/2026-11-10-testing-power/coin-feasible-tests.png]]
*Original reconstruction: each dot is a deterministic rule's error/power pair; some of the 16 rules overlap. Randomized rules fill their convex hull. The highest attainable point with horizontal coordinate at most 0.25 is A.*

### ROC space connects the optimization to classification

**My follow-up question:** “can I think of the ROC table, precision and specification similar to alpha and power?” Here the intended classification term is **specificity**. Treat rejecting $H_0$ as a positive prediction, and a true alternative as an actually positive case.

| Testing | Classification | Conditional probability |
|---|---|---|
| Type I error rate | False-positive rate (FPR) | $P(\text{reject}\mid H_0\text{ true})$ |
| Power | Sensitivity / recall / true-positive rate (TPR) | $P(\text{reject}\mid H_1\text{ true})$ |
| Probability of not rejecting a true null | Specificity | $1-\mathrm{FPR}$ |
| Type II error rate | False-negative rate (FNR) | $1-\mathrm{TPR}$ |

For simple hypotheses, these probabilities use the specified null and alternative sampling laws. For composite hypotheses, the testing quantities depend on the parameter: a level-$\alpha$ rule bounds FPR at **every** null parameter, while power is a function over alternative parameters. A single classification TPR or FPR generally averages within its class, so it requires a specified class-conditional distribution. In particular, $\alpha$ is an **upper bound** on actual FPR, not automatically its value; specificity is at least $1-\alpha$ under a controlled null.

An **ROC curve** plots $x=\mathrm{FPR}$ against $y=\mathrm{TPR}$. A confusion matrix is the associated table of decisions versus truth at one chosen operating point. Thus our optimization says:

> **Get as high as possible in ROC space without moving to the right of $\alpha$.**

The figure immediately above is already in ROC coordinates: A is $(0.25,0.64)$, B is $(0.25,0.16)$, and C is $(0.75,0.96)$. A dominates B; C is infeasible at $\alpha=0.25$. The shaded convex hull represents **all randomized rules** for this finite experiment. An ordinary ROC curve instead varies the threshold of one fixed score; it need not describe all possible rules. Maximizing power at one FPR budget is also not the same objective as maximizing area under the entire ROC curve.

### Precision reverses the conditioning—and needs a base rate

Power asks: **among true alternatives, how often do we reject?** Precision asks: **among rejections, how often is the alternative actually true?**

$$
\mathrm{TPR/Sensitivity}=P(\text{reject}\mid H_1\text{ true}),
\qquad
\mathrm{Precision}=P(H_1\text{ true}\mid\text{reject}).
$$

To define the second probability, introduce a population of cases or repeated testing problems with alternative prevalence $\pi=P(H_1\text{ true})$, and specified within-class sampling laws. Bayes' rule gives, when the rejection probability is positive,

$$
\boxed{\mathrm{Precision}
=\frac{\pi\,\mathrm{TPR}}
{\pi\,\mathrm{TPR}+(1-\pi)\,\mathrm{FPR}}.}
$$

This is an additional mixture or prior model: the original frequentist problem with one fixed unknown parameter does not itself supply $\pi$. With composite classes, use the corresponding class-averaged rates, not power at an arbitrary single effect size.

**Added numerical illustration:** suppose 1,000 cases include 100 true alternatives and 900 true nulls. At TPR $0.80$ and FPR $0.05$, the expected confusion-matrix counts are:

| Decision | True alternative: 100 | True null: 900 |
|---|---:|---:|
| Reject / predict positive | 80 true positives | 45 false positives |
| Do not reject / predict negative | 20 false negatives | 855 true negatives |

These are expected counts, not a guarantee for every realized sample. The resulting population ratios are

$$
\mathrm{Recall}=\frac{80}{100}=80\%,\qquad
\mathrm{Specificity/(1-FPR)}=\frac{855}{900}=95\%,\qquad
\mathrm{Precision}=\frac{80}{80+45}=64\%.
$$

So **power $=80\%$, specificity $=95\%$, and precision $=64\%$ answer three different questions**. Holding the class-conditional rates fixed while changing prevalence changes precision, but not the ROC point. Neither a 5% significance level nor an observed p-value means that only 5% of rejections are false.

### One picture: ROC, both errors, sensitivity, specificity, and precision

![[assets/figures/2026-11-10-testing-power/roc-error-rates.svg]]

*Original coordinated illustration. Read top left → top right → bottom left → bottom right: the same score cutoff divides the two sampling distributions, creates the ROC point, supplies expected counts after adding a 10% alternative prevalence, and yields precision among rejections. Colors stay fixed: true positives green, true negatives blue, false positives red, false negatives amber. This constructed normal-score example reproduces the 80/20/45/855 expected-count table above; it is not an empirical ROC curve or a replacement for the two-flip experiment.*

- **Vertical coordinate:** sensitivity / recall / power $=0.80$. The remaining vertical distance to 1 is Type II error $=0.20$.
- **Horizontal coordinate:** Type I error / FPR $=0.05$. The remaining horizontal distance to 1 is specificity $=0.95$.
- **Precision is not either ROC coordinate.** Add the base rate, then restrict attention to the predicted-positive row: $80/(80+45)=0.64$. This is also a ratio of **population areas**, as shown below.

The score model is $S\mid H_0\sim N(0,1)$ and $S\mid H_1\sim N(\delta,1)$, with $\delta=z_{0.95}+z_{0.80}\approx2.48647$. For a cutoff $c$, its ROC coordinates are $(1-\Phi(c),\,1-\Phi(c-\delta))$. Choosing $c=z_{0.95}$ gives exactly $(0.05,0.80)$. Lowering $c$ moves up and right: power increases, but so does Type I error. Raising $c$ moves down and left. Here the budget is fully used ($\mathrm{FPR}=\alpha$); that equality is not automatic for every test.

### Precision as an area ratio, and what ROC area measures

**Follow-up, paraphrased:** Can precision be represented by an area ratio, and can areas in the preceding graphic reveal other quantities?

**Yes—but first specify what the area represents.** The density plots above each condition on a different true class and each integrate to 1. Their raw shaded areas cannot be pooled as if the two classes were equally common. The ROC plot, in turn, has rates on both axes: its area has a different meaning from population probability mass.

![[assets/figures/2026-11-10-testing-power/precision-population-area-vs-auc.svg]]

*important: the first grean bar width: 0.1, prior rate of a true alternative. height: 0.8, power. Red width 0.9 (1-0.1), red height: 0.05 alpha*

*Original area construction using the same model and cutoff as the four-view figure. Left: the whole rectangle represents the population, with widths equal to the true-class proportions and heights equal to conditional decision probabilities. Green, amber, red and blue retain their TP, FN, FP and TN meanings. Below it, only the green and red regions are retained and renormalized. Right: purple distinguishes ROC area from those population areas; it summarizes ranking across thresholds.*

> [!important] Panel A is a Bayes-rule area diagram, not a rearranged ROC plot
> It uses the same probability-area construction as the supplied Bayes-rule screenshot. Set $H=\{H_1\text{ is true}\}$ and $E=\{\text{reject }H_0\}$:
>
> - **Width:** $P(H)=\pi$ is the prevalence (or prior probability) of a true alternative.
> - **Conditional heights:** $P(E\mid H)$ is sensitivity/power; $P(E\mid\neg H)$ is the Type I error rate/FPR.
> - **Area ratio:** $P(H\mid E)$ is precision—the fraction of rejection area belonging to true alternatives.
>
> $$
> P(H\mid E)=\frac{P(H)P(E\mid H)}{P(H)P(E\mid H)+P(\neg H)P(E\mid\neg H)}.
> $$
>
> **Panel A is not an area-preserving rearrangement of the ROC plot.** It takes the ROC point's two conditional rates and adds the class proportions. Its green area is $\pi\times\mathrm{power}=0.10\times0.80=0.08$. By contrast, the rectangle from the origin to the ROC point has area $\mathrm{FPR}\times\mathrm{power}=0.05\times0.80=0.04$: that product is neither the true-positive population probability nor AUC.
>
> The Bayesian interpretation needs the extra prevalence/prior model; a frequentist test at one fixed unknown parameter does not itself supply $P(H)$. Here precision is a posterior probability **given rejection**, not necessarily the posterior given the complete observed dataset.

#### Population areas: multiply the ROC coordinates by class proportions

At the selected ROC point $(x,y)=(\mathrm{FPR},\mathrm{TPR})$, let $\pi$ be the proportion of true alternatives. The four **joint probability areas** are

$$
\begin{aligned}
A_{\mathrm{TP}}&=\pi y=0.10(0.80)=0.080, &
A_{\mathrm{FN}}&=\pi(1-y)=0.020,\\
A_{\mathrm{FP}}&=(1-\pi)x=0.90(0.05)=0.045, &
A_{\mathrm{TN}}&=(1-\pi)(1-x)=0.855.
\end{aligned}
$$

The areas sum to 1. **Rejecting means landing in either the green TP region or the red FP region.** Conditioning on rejection keeps their union (area $0.125$) and rescales it to 1:

$$
\boxed{\mathrm{Precision}
=\frac{A_{\mathrm{TP}}}{A_{\mathrm{TP}}+A_{\mathrm{FP}}}
=\frac{\text{green area}}{\text{green area}+\text{red area}}
=\frac{0.080}{0.125}=0.64.}
$$

**The same construction works directly with density areas.** If $f_1(s)$ and $f_0(s)$ are the class-conditional score densities and rejection is $S>c$, first weight the entire curves by $\pi$ and $1-\pi$. Their right-tail areas are

$$
A_{\mathrm{TP}}=\int_c^\infty\pi f_1(s)\,ds,
\qquad
A_{\mathrm{FP}}=\int_c^\infty(1-\pi)f_0(s)\,ds.
$$

Their ratio gives the same precision. Using $0.80/(0.80+0.05)$ without class weights would instead implicitly assume equal prevalence and give about $94.1\%$—not this population's $64\%$.

Other quantities are now different selections and normalizations of these **same four areas**:

| Quantity | Area calculation | Value |
|---|---|---:|
| Sensitivity / recall / power | $A_{\mathrm{TP}}/(A_{\mathrm{TP}}+A_{\mathrm{FN}})$ | 80% |
| Type II error | $A_{\mathrm{FN}}/(A_{\mathrm{TP}}+A_{\mathrm{FN}})$ | 20% |
| Specificity | $A_{\mathrm{TN}}/(A_{\mathrm{TN}}+A_{\mathrm{FP}})$ | 95% |
| Type I error / FPR | $A_{\mathrm{FP}}/(A_{\mathrm{TN}}+A_{\mathrm{FP}})$ | 5% |
| Precision | $A_{\mathrm{TP}}/(A_{\mathrm{TP}}+A_{\mathrm{FP}})$ | 64% |
| False-positive share among positive predictions | $1-\mathrm{Precision}$ | 36% |
| Negative predictive value (NPV) | $A_{\mathrm{TN}}/(A_{\mathrm{TN}}+A_{\mathrm{FN}})$ | 97.71% |
| Accuracy | $A_{\mathrm{TP}}+A_{\mathrm{TN}}$ | 93.5% |

Notice that $A_{\mathrm{FP}}=4.5\%$ is a fraction of **all cases**, FPR $=5\%$ is a fraction of **actually negative cases** ($\mathrm{TN}+\mathrm{FP}$), and $1-\mathrm{Precision}=36\%$ is a fraction of **predicted positives**. They use the same false-positive region but different denominators. Accuracy can also hide class imbalance: always predicting negative here already achieves $90\%$ accuracy, despite zero sensitivity.

#### ROC area: AUC is a ranking probability, not precision

The area under the full ROC curve is

$$
\mathrm{AUC}=\int_0^1\mathrm{TPR}(u)\,du,
\qquad u=\mathrm{FPR}.
$$

For independent scores $S_1$ from the actually positive class and $S_0$ from the actually negative class, continuous score distributions give $\mathrm{AUC}=P(S_1>S_0)$. With ties, the [[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly#Count the same pairs through ROC strips|standard interpolated-ROC convention]] adds $\tfrac12P(S_1=S_0)$. This is ranking across thresholds, not the precision, accuracy or power at the marked cutoff. See [Google ML Crash Course, ROC and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc).

For this specific illustration, $S_1-S_0\sim N(\delta,2)$ by independence. Hence

$$
\mathrm{AUC}=P(S_1-S_0>0)
=\Phi\!\left(\frac{\delta}{\sqrt2}\right)
\approx0.96064.
$$

Thus the same model has **AUC 96.06%, power 80%, precision 64%, and accuracy 93.5%**. These values describe different questions. The area *above* this continuous ROC curve is $1-\mathrm{AUC}=P(S_1<S_0)$, a pairwise ranking error—not Type I or Type II error at one threshold.

If only false-positive rates up to $\alpha$ are relevant, the **raw partial AUC** $\int_0^\alpha\mathrm{TPR}(u)\,du$ summarizes that portion of the curve. Here it is about $0.03290$ for $\alpha=0.05$. It is still an integral across operating points, **not** the power $0.80$ at the endpoint. Maximizing full AUC need not maximize power at the particular error budget we care about.

### Why likelihood ratios appear

With unequal null probabilities, the largest alternative probability alone need not be the best use of the budget. Compare **power gained per unit of null probability**, $f_1(x)/f_0(x)$. The Neyman–Pearson lemma makes this precise for simple hypotheses: reject at the largest likelihood ratios, randomizing on a threshold if needed to attain the chosen size. The two-flip ratios above put HH first. See [Berkeley Stat 210A, §3.1](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html#likelihood-ratio-test).

## 3. What changes when the alternative contains many parameters?

For $H_1:p>0.5$, “maximize for $p\in\Theta_1$” describes **many objectives**, one power value for each $p$. It does not mean $\max_p\beta_\phi(p)$, nor an average over $p$ without a specified weighting distribution.

A uniformly most powerful (UMP) level-$\alpha$ rule would satisfy

$$
\beta_{\phi^*}(p)\ge\beta_\phi(p)
\quad\text{for every }p>0.5
\text{ and every feasible }\phi.
$$

In the two-flip example, HH remains the outcome with largest probability whenever $p>0.5$: $p^2>p(1-p)$ and $p^2>(1-p)^2$. Since null costs are still all $0.25$, the same bound proves that HH-only is UMP at level $0.25$, with power $p^2$. It also controls the composite null $p\le0.5$, because $\sup_{p\le0.5}p^2=0.25$.

**Do not assume a UMP rule exists.** For a two-sided alternative, negative and positive departures can favor different rejection regions. Maximizing every alternative's power simultaneously can be impossible. This distinction is also made in [Berkeley Stat 210A, §§2.1 and 3.3](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html).

## 4. Why randomize at a discrete boundary?

![[raw/assets/2026-11-10-Hypothesis-testing-I02-normal-and-randomized-binomial-tests.png|800]]
*Original handwriting: a normal upper-tail test and a binomial test that may need fractional rejection at the cutoff. For the binomial statistic, use $T=\sum_{i=1}^nX_i$.*

With $T\sim\mathrm{Bin}(n,p)$, test $H_0:p\le1/2$ against $p>1/2$. Reject more often for larger $T$. Because $T$ is stochastically increasing in $p$, the largest null rejection probability occurs at $p=1/2$. Choose an integer cutoff $c$ satisfying

$$
P_{1/2}(T>c)\le\alpha\le P_{1/2}(T\ge c).
$$

Reject above $c$, and at $c$ reject with probability

$$
\gamma=\frac{\alpha-P_{1/2}(T>c)}{P_{1/2}(T=c)}.
$$

Then the null rejection probability is exactly $\alpha$. The denominator is positive for an attainable boundary; the bracketing inequalities ensure $\gamma\in[0,1]$.

**Small extension of the two-flip example:** if $\alpha$ were $0.10$, even always rejecting HH would cost too much. Reject with probability $0.4$ on HH and never otherwise. Its size is $0.25(0.4)=0.10$ and power is $0.64(0.4)=0.256$. The same coefficient bound proves optimality. Here no nonrandomized test can reject anything while meeting the constraint.

Randomization is a theoretical way to use otherwise inaccessible fractions of the budget. A conservative nonrandomized test is also valid; having size strictly below $\alpha$ is not a mathematical error.

## 5. Normal testing: power, effect size, sample size, and significance

The following is **added synthesis of the handwritten normal example**, separate from the supplied coin example. Assume iid $X_i\sim N(\mu,\sigma^2)$ with known $\sigma>0$. Test $H_0:\mu\le\mu_0$ versus $H_1:\mu>\mu_0$. Write

$$
Z=\frac{\sqrt n(\bar X-\mu_0)}{\sigma},
\qquad d=\frac{\mu-\mu_0}{\sigma},
\qquad z_q=\Phi^{-1}(q).
$$

Since $Z\sim N(\sqrt n\,d,1)$, rejecting when $Z>z_{1-\alpha}$ gives

$$
\boxed{\operatorname{Power}(d;n,\alpha)
=1-\Phi\!\left(z_{1-\alpha}-\sqrt n\,d\right).}
$$

This is a concrete **power–effect size–sample size–significance equation**, not a universal formula for all tests. The null supremum is at $d=0$, where rejection probability is $\alpha$; for $d<0$ it is smaller.

For target power $1-\beta_{\mathrm{II}}$ at a specified positive effect $d$, solve the inequality:

$$
\sqrt n\,d\ge z_{1-\alpha}+z_{1-\beta_{\mathrm{II}}},
\qquad
n\ge\left(\frac{z_{1-\alpha}+z_{1-\beta_{\mathrm{II}}}}{d}\right)^2.
$$

This squared expression assumes a positive numerator, as in ordinary power planning; otherwise $n\ge1$ already suffices. Round upward to an integer. With $d=0.2$, $\alpha=0.05$, and target power $0.80$, the bound is $154.564$, so **$n=155$**.

### The optimization is not simply “lower the cutoff”

Take $n=100$, $\sigma=1$, $\mu_0=0$, and evaluate power at $\mu=0.2$. Then $Z=10\bar X\sim N(2,1)$ under this alternative.

| Rule | Size | Power at $\mu=0.2$ | Meets $\alpha=0.05$? |
|---|---:|---:|---|
| Reject if $Z>1.2816$ | 0.100 | 0.764 | No |
| Reject if $Z>1.6449$ | 0.050 | **0.639** | Yes |
| Reject if $Z>1.9600$ | 0.025 | 0.516 | Yes, conservative |
| Ignore 99 observations; reject if $X_1>1.6449$ | 0.050 | 0.074 | Yes, wasteful |

The first row gains power by violating the budget. The last two valid rules show that satisfying the constraint alone does not make a test good. Within the upper-tail $Z$ family, the smallest permitted cutoff is best; optimality among **all** rules needs an argument such as Neyman–Pearson, not just a cutoff comparison.

![[assets/figures/2026-11-10-testing-power/testing-power.png]]
*Left: one rejection region, integrated under two different distributions. Right: two rules with the same null size have very different power functions. The parameter on the horizontal axis evaluates each fixed rule; it is not the variable optimized over.*

For the two-sided test $H_0:\mu=\mu_0$, reject when $|Z|>z_{1-\alpha/2}$. Its exact power is

$$
1-\Phi\!\left(z_{1-\alpha/2}-\sqrt n\,d\right)
+\Phi\!\left(-z_{1-\alpha/2}-\sqrt n\,d\right).
$$

Replacing $z_{1-\alpha}$ by $z_{1-\alpha/2}$ in the sample-size expression gives a common conservative approximation for positive $d$, omitting the opposite-tail contribution; solve the two-tail equation for exact planning. With unknown variance, finite-sample normal-mean testing instead uses $t$ and noncentral-$t$ distributions.

## 6. How the same test connects to a p-value and a confidence interval

**Power asks about future datasets at a specified truth; a p-value summarizes the dataset actually observed using the null distribution.** They are not interchangeable probabilities.

For a nested family of rejection regions $R_\alpha$ increasing with $\alpha$,

$$
p(x)=\inf\{\alpha:x\in R_\alpha\}.
$$

Thus the p-value is the smallest significance threshold at which the observed result enters the rejection region, interpreted as an infimum when the endpoint is not attained. For the normal examples:

$$
p_{\text{one-sided}}=1-\Phi(z_{\mathrm{obs}}),
\qquad
p_{\text{two-sided}}=2\{1-\Phi(|z_{\mathrm{obs}}|)\}.
$$

With a strict cutoff $Z>z_{1-\alpha}$, the exact algebraic rule is $p<\alpha$; with the matching non-strict cutoff it is $p\le\alpha$. For a continuous null, equality has probability zero, but exact endpoints matter when matching decisions to intervals. Discrete tests require their own tail and randomization conventions.

**The coin example has a p-value too.** For the upper-tail count of heads $T$, use $p_{\mathrm{obs}}=P_{0.5}(T\ge t_{\mathrm{obs}})$. It equals $0.25$ for HH, $0.75$ for either mixed outcome, and $1$ for TT. The rule $p_{\mathrm{obs}}\le0.25$ therefore reproduces test A. Its power at coin bias $0.8$ is $0.64$: that is a repeated-sampling property of the rule, **not** the p-value of HH.

### Invert the test to get a confidence set

For each candidate value $\mu_0$, test that null using the same procedure. Collect the [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways#1. The decision rule becomes a family indexed by the null value|values not rejected]]:

$$
C_{1-\alpha}(x)=\{\mu_0:\text{the level-}\alpha\text{ test does not reject }\mu_0\}.
$$

If every point-null test controls its error at $\alpha$, then $P_\mu\{\mu\in C_{1-\alpha}(X)\}\ge1-\alpha$. This is repeated-sampling coverage, not a posterior probability for a fixed observed interval.

For the two-sided known-$\sigma$ test with strict rejection,

$$
C_{1-\alpha}(x)=
\left[\bar x-z_{1-\alpha/2}\frac{\sigma}{\sqrt n},
\bar x+z_{1-\alpha/2}\frac{\sigma}{\sqrt n}\right].
$$

At $n=100$, $\sigma=1$, $\bar x=0.2$, the test of $\mu_0=0$ has $z_{\mathrm{obs}}=2$, two-sided $p=0.04550$, and 95% CI $[0.00400,0.39600]$. Zero is excluded, exactly matching rejection at 5%.

Here $\bar x=0.2$ is an **observed estimate**. In the earlier power calculation, $\mu=0.2$ was an **assumed true effect**. Equal numerical values do not make them the same object, and plugging the observed effect into a power formula does not supply new evidence beyond the data. One-sided upper-tail tests correspond to one-sided lower confidence bounds, not the two-sided 95% interval above.

## 7. Where Wald and asymptotic tests enter the framework

![[raw/assets/2026-11-10-Hypothesis-testing-I03-wald-and-p-values.png|700]]
*Original handwriting: standardized estimation error leads to a chi-square statistic, followed by p-values as rejection thresholds. The checked formulas below correct the inverse-square-root/norm notation.*

Suppose a $k$-vector estimator obeys

$$
\sqrt n(\hat\theta_n-\theta)\xrightarrow{d}N_k(0,\Sigma(\theta)),
\qquad \hat\Sigma_n\xrightarrow{p}\Sigma(\theta),
$$

where $\Sigma(\theta)$ is positive definite. Here $\hat\Sigma_n$ estimates the covariance of the **scaled** estimation error; the estimator's covariance itself is approximately $\Sigma/n$. Under $H_0:\theta=\theta_0$,

$$
W_n=n(\hat\theta_n-\theta_0)^\top\hat\Sigma_n^{-1}(\hat\theta_n-\theta_0)
=\left\|\sqrt n\,\hat\Sigma_n^{-1/2}(\hat\theta_n-\theta_0)\right\|^2
\xrightarrow{d}\chi_k^2.
$$

There is **one squared norm of the standardized vector**, not a componentwise square inside the norm. Reject when $W_n>\chi^2_{k,1-\alpha}$; the asymptotic p-value is $1-F_{\chi_k^2}(W_n)$. For one scalar two-sided restriction, $W_n=Z_n^2$ and this agrees asymptotically with $2\{1-\Phi(|Z_n|)\}$.

The degrees of freedom count independent tested restrictions. Testing $r$ smooth independent restrictions on a larger parameter uses $r$ degrees of freedom and the corresponding delta-method covariance, not automatically the full parameter dimension.

**Calibration is not optimality.** An asymptotic null law helps construct a rule with approximately controlled Type I error; it does not by itself prove maximum power. Nor does pointwise asymptotic normality guarantee the stronger, uniform null constraint

$$
\limsup_{n\to\infty}\sup_{\theta\in\Theta_0}
E_\theta[\phi_n(X)]\le\alpha.
$$

The weaker pointwise statement puts the limit first for each fixed $\theta$. Uniform validity needs additional control; boundaries, singular covariance, and nonregular models can invalidate ordinary Wald calibration. In contrast, the known-variance Gaussian and calibrated binomial examples above are finite-sample statements.

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Neyman–Pearson lemma|Neyman–Pearson lemma]] — Solves the simple-null/simple-alternative power maximization by ranking power gained per unit of Type I error budget.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation|p-value interpretation]] — A nested family of calibrated rules turns an observed dataset into a rejection threshold; this is distinct from the rule's power at a true alternative.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Intervals & test inversion/Inverting a test|Inverting a test]] — Keeping all candidate null parameters not rejected converts error control into confidence coverage, with matching tails and endpoint conventions.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Power and sample size|Power and sample size]] — The normal power function explicitly connects effect size, sample size, significance level, and desired detection probability.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Confidence intervals and p-values - the same test viewed two ways|Confidence intervals and p-values - the same test viewed two ways]] — A calibrated decision rule for each candidate null converts Type I error control into confidence coverage; fixing the data reveals the matching p-value and interval decisions.

- [[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly|Concordance and C-statistics - ranking pairs correctly]] — The AUC ranking probability here becomes explicit pair counting, with a proof including score ties; neither measures power at one chosen cutoff.

## Origin

> [!info]- Source details
> The subsequent clarification below the area graph incorporates my comparison with the [[raw/assets/2026-11-10-Hypothesis-testing-I04-Bayes-area-reference.png|Bayes-rule screenshot]], which I identified as 3Blue1Brown. After the temporary attachment expired, I supplied the Downloads copy on 2026-11-10; that file is now preserved byte-for-byte. The video attribution remains user-provided, not independently verified. The added notation distinguishes prevalence-weighted population areas from products of ROC coordinates and conditions the Bayesian interpretation on an explicit prevalence/prior model.
>
> The area-ratio follow-up added the original population-area/ROC-AUC comparison, with [[assets/figures/2026-11-10-testing-power/draw_precision_areas.py|generator]] and [[assets/figures/2026-11-10-testing-power/precision-areas-checks.json|checks]]. The existing constructed score laws, cutoff and prevalence are retained. The new prose derives weighted tail areas, precision, accuracy, NPV and the normal-score AUC; Google's ROC/AUC lesson was read to cross-check the ranking interpretation. No new source-original file or unseen conversation was ingested.
>
> Extended on 2026-11-10 at the requests “design a diagram for this sentence” and “and extend it below the sentence”. The two-world decision-rule figure and its caption are assistant-added illustration, placed immediately after the user's plain-language paragraph without changing it. The illustrative normal distributions are not new observations or user-supplied data. See the [[assets/figures/2026-11-10-testing-power/draw_decision_rule.py|reproducible diagram source]] and [[assets/figures/2026-11-10-testing-power/decision-rule-checks.json|tail-probability checks]].
>
> The three embedded screenshots are the supplied handwritten originals, preserved byte-for-byte. The exact question and two-flip example come from the [[raw/conversations/2026-11-10-testing-optimization-pasted-excerpt.md|user-pasted shared-chat excerpt]]. The shared URL itself could not be read; no other turns or original interactive graphics are claimed as ingested.
>
> This note captures only the requested testing-focused first part. The linked Rao–Blackwell page was not the requested home and was not modified. The separate existing z/t/F geometry note remains unchanged.
>
> Extended on 2026-11-10 from my current-chat ROC/precision/specificity question and its answer, at my request “extend this to the note too”. The two new subsections connect the existing feasible-test plot to ROC space and distinguish precision from power and specificity. The confusion-matrix example and mixture-model qualifications are added explanation; no additional source files or unseen shared-chat turns were ingested.
>
> The later request for an ROC visual added the original four-view SVG above, its PNG preview, [[assets/figures/2026-11-10-testing-power/draw_roc_relationships.py|reproducible generator]] and [[assets/figures/2026-11-10-testing-power/roc-error-rates-checks.json|checks]]. The normal-score separation is deliberately constructed to give 5% FPR and 80% power; the base rate is an explicit extra assumption. A static overview keeps all complements and denominators visible together. No supplied image was changed.
>
> Added synthesis: the explicit global-optimality bound, reconstructed feasible-set figure, fractional-budget example, normal numerical comparison and power-planning derivation, coin p-values, test/CI inversion, and Wald/uniformity qualifications. These are checked explanations, not newly attributed user questions. Berkeley Stat 210A §§2–3 was read to cross-check the testing framework and Neyman–Pearson/UMP statements; its numerical example is not the supplied two-flip example and is not copied here.
>
> Reproducible [[assets/figures/2026-11-10-testing-power/build_testing_power.py|figure/check source]] and [[assets/figures/2026-11-10-testing-power/checks.json|numerical results]] include exact enumeration of all deterministic two-flip rules, normal tail calculations, binomial calibration, sample-size thresholds, and CI inversion. Numerical checks support the examples; the inequalities and stated distributional assumptions carry the mathematical arguments. Editorially approved on 2026-11-10; this does not establish mastery or resolve the stated source-access limits.
