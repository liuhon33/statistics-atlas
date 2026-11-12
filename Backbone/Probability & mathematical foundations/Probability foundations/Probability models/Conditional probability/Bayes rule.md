---
id: bayesrule
title: Bayes rule
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule
created: '2026-11-08'
updated: '2026-11-11'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional probability (L4)]]'
prerequisite_for:
- '[[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Prior, likelihood & posterior]]'
sources:
- '[[_system/Sources/prob]]'
---

# Bayes rule

Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule

Parent: [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional probability (L4)|Conditional probability]]

$$
\begin{aligned}
P(H\mid D)
&=\frac{P(D\mid H)P(H)}{P(D)}\\
\end{aligned}
$$
$P(H\mid D)$: Likelihood (according to our belief, how likely is the observed data)
$P(H)$: Prior Belief
$P(H\mid D)$: Posterior (what is our belief after we observed this data)
$P(D)$: Normalizing factor. Probability of data
## 1. See it and use it

Suppose Steve could be a librarian or a farmer. He is described as quiet, orderly, and attentive to detail. How much should that change your guess?

**Bayesian inference** represents uncertainty with probabilities, then updates them using observed evidence. The **prior** describes uncertainty before this evidence; the **posterior** describes it afterward. **Bayes' rule** is the probability identity that performs the update. [Pishro-Nik, §9.1.0](https://www.probabilitycourse.com/chapter9/9_1_0_bayesian_inference.php).

To use it, list the possibilities, assign their starting probabilities, and ask how often each would produce the evidence. Multiply those two numbers for each possibility, then divide by their total.

For a tiny example, imagine 10 librarians and 200 farmers. Suppose 40% of librarians and 10% of farmers fit Steve's description. That leaves 4 librarians and 20 farmers:

![[assets/figures/2026-11-11-bayes-rectangles/01-bayes-area-update.gif]]

*Original animation using the illustrative Steve inputs from [3Blue1Brown's lesson](https://www.3blue1brown.com/lessons/bayes-theorem/): whole population → colored matches → tip blue 90° and slide the pieces side by side → blue area divided by their combined area, $4/(4+20)=1/6$; after selection, areas and camera scale stay unchanged.*

> [!info]- Static views and animation source
> ![[assets/figures/2026-11-11-bayes-rectangles/01c-side-by-side-ratio.svg]]
>
> Earlier keyframes: [[assets/figures/2026-11-11-bayes-rectangles/01a-whole-population.svg|whole population]] · [[assets/figures/2026-11-11-bayes-rectangles/01b-retained-areas.svg|colored matches]].
>
> [[assets/figures/2026-11-11-bayes-rectangles/animate_intro.py|Reproducible animation source]] · [[assets/figures/2026-11-11-bayes-rectangles/intro-animation-checks.json|Area-preservation checks]] · [[assets/figures/2026-11-11-bayes-rectangles/01-one-minute.svg|Original count diagram]].

Let $H$ mean librarian, $H^c$ farmer in this two-occupation population, and $E$ fitting the description, so the priors are $P(H)=10/210$ and $P(H^c)=200/210$.
[Bayes' rule](https://www.probabilitycourse.com/chapter1/1_4_3_bayes_rule.php) combines these with the likelihoods $P(E\mid H)=0.4$ and $P(E\mid H^c)=0.1$:

$$
\begin{aligned}
P(H\mid E)
&=\frac{P(E\mid H)P(H)}{P(E\mid H)P(H)+P(E\mid H^c)P(H^c)}\\
&=\frac{0.4\times(10/210)}{0.4\times(10/210)+0.1\times(200/210)}
=\frac{4}{4+20}=\frac16\approx16.7\%.
\end{aligned}
$$

The evidence raises Steve's librarian probability from $1/21\approx4.8\%$ to $1/6\approx16.7\%$, though farmer remains more likely; this conclusion relies on the assumed population and description rates matching the sampling setup.

## 2. How it works — width, height, retained area

### Turn the video's rectangle into a calculation

The requested [3Blue1Brown video, starting at 8:44](https://www.youtube.com/watch?v=HZGCoVF3YvM&t=524s) develops an area view. Its official text counterpart is [“Thinking with area”](https://www.3blue1brown.com/lessons/bayes-theorem/#thinking-with-area). The construction below uses the same Steve inputs; they are a teaching model, not current occupational statistics or measured personality rates.

Let $H$ mean librarian, $H^c$ mean farmer **within this two-occupation population**, and $E$ mean fitting the description. The whole rectangle has probability area 1.

1. **Set widths using the prior:** $P(H)=1/21$ and $P(H^c)=20/21$.
2. **Set retained heights using the likelihood:** $P(E\mid H)=0.4$ and $P(E\mid H^c)=0.1$. A likelihood here asks how often the evidence would occur within a specified occupation.
3. **Multiply width by height:** the two retained areas are $P(H\cap E)$ and $P(H^c\cap E)$.
4. **Condition on $E$:** discard the unretained area, and ask what fraction of the retained total belongs to $H$.

![[assets/figures/2026-11-11-bayes-rectangles/02-steve-rectangles.svg]]

*Original analytic illustration inspired by 3Blue1Brown's area construction. Widths and heights are to probability scale; blue is librarian and amber is farmer. The lower bar displays normalized area shares, not the original column widths.*

| Quantity | Librarian | Farmer |
| --- | --- | --- |
| Prior width | $1/21$ | $20/21$ |
| Evidence height | $0.4$ | $0.1$ |
| Retained joint area | $2/105$ | $2/21$ |
| Share of all retained area | $1/6$ | $5/6$ |

Thus

$$
P(H\mid E)
=\frac{\text{blue retained area}}{\text{all retained area}}
=\frac{P(H)P(E\mid H)}{P(H)P(E\mid H)+P(H^c)P(E\mid H^c)}
=\frac{2/105}{4/35}=\frac16.
$$

The denominator $P(E)=4/35$ is the **evidence probability**: how much of the original space survives. The posterior divides by that number so the surviving shares sum to 1.

### Why the formula must be true

The definition of [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional probability (L5)|conditional probability]] gives two expressions for the same joint area:

$$
P(H\cap E)=P(E\mid H)P(H)=P(H\mid E)P(E).
$$

Divide by $P(E)>0$ to obtain Bayes' rule. More generally, if $H_1,\ldots,H_k$ are disjoint and exhaust the possibilities, then

$$
\boxed{P(H_i\mid E)=\frac{P(E\mid H_i)P(H_i)}{\sum_{j=1}^{k}P(E\mid H_j)P(H_j)}}.
$$

The denominator adds the nonoverlapping retained rectangles. Hypotheses with prior zero contribute zero; their conditional likelihood need only be specified on positive-prior hypotheses. If the denominator is zero, this event-conditioning formula is undefined. [Pishro-Nik, §1.4.3, Bayes' Rule](https://www.probabilitycourse.com/chapter1/1_4_3_bayes_rule.php).

### What the picture prevents you from mixing up

**Likelihood and posterior have different denominators.** $P(E\mid H)=0.4$ is a retained height inside the librarian column. $P(H\mid E)=1/6$ is the librarian area divided by *all* evidence-compatible area. A tall slice can still have little area if its column is narrow.

The likelihoods $0.4$ and $0.1$ need not sum to 1: each is conditioned on a different occupation. The posterior probabilities do sum to 1 because both describe the same conditioned population.

**An update can favor a hypothesis without making it the most likely one.** Posterior odds equal prior odds times the likelihood ratio:

$$
\frac{P(H\mid E)}{P(H^c\mid E)}
=\frac{1}{20}\times\frac{0.4}{0.1}=\frac15.
$$

Equal positive heights preserve the prior shares. Unequal heights reweight them. This is why the mechanism that produces the observation belongs in the model.

```atlas-interactive
path: assets/figures/2026-11-11-bayes-rectangles/bayes-explorer.html
title: Bayes rectangles — change prior widths and likelihood heights
height: 1050
```

*Try “Equal likelihoods,” then increase only the librarian likelihood. Predict the posterior before reading the number. “Impossible evidence” shows why a positive denominator is required.*

[[assets/figures/2026-11-11-bayes-rectangles/bayes-explorer.html|Open the offline rectangle explorer]]. The static construction above carries the same reference values.

## 3. Deeper understanding — Bayes becomes variational inference

### The same retained areas become an unnormalized posterior

Relabel the hypothesis as a hidden state $z$, and the observation as $x$. In Steve's example $z\in\{L,F\}$ and $x=E$. Write

$$
a_z=p(z)p(x\mid z)=p(x,z),\qquad
Z=\sum_z a_z=p(x),\qquad
p(z\mid x)=\frac{a_z}{Z}.
$$

| Rectangle role | Latent-variable role |
| --- | --- |
| Column width | Prior $p(z)$ |
| Retained height | Likelihood $p(x\mid z)$ |
| Retained area $a_z$ | Joint probability $p(x,z)$ |
| Total retained area $Z$ | Evidence $p(x)$ |
| Normalized area share | Posterior $p(z\mid x)$ |

Steve has just two areas, so normalization is easy. With many hidden variables, evaluating $p(x,z)$ at one $z$ can be practical while summing or integrating over *all* $z$ is expensive. [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Variational inference|Variational inference]] chooses a tractable family of normalized distributions $q$ and fits one to the posterior. The difficult normalizer motivates the calculation below. [Blei, Kucukelbir & McAuliffe, §§2.1–2.2](https://arxiv.org/html/1601.00670v9#S2.SS2).

For continuous $z$, replace the sum by an integral. If $x$ is continuous too, $p(x\mid z)$ is a **density**, not a probability height bounded by 1; the picture becomes an unnormalized density profile. The normalization algebra survives, while the literal unit-square interpretation needs that distinction.

### Derive the ELBO directly from these areas

Keep the model and observation fixed. For this finite example take $q_z>0$ wherever $a_z>0$, with $\sum_zq_z=1$. Define

$$
\mathcal L(q)=\sum_zq_z\log\frac{a_z}{q_z}.
$$

Substituting the normalized area shares into [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]] gives

$$
\begin{aligned}
D_{\mathrm{KL}}(q\|p(\cdot\mid x))
&=\sum_zq_z\log\frac{q_z}{a_z/Z}\\
&=\sum_zq_z\log q_z-\sum_zq_z\log a_z+\log Z\sum_zq_z\\
&=\log Z-\mathcal L(q).
\end{aligned}
$$

Therefore the [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO|ELBO]] satisfies

$$
\boxed{\mathcal L(q)=\log p(x)-D_{\mathrm{KL}}(q\|p(\cdot\mid x))\leq\log p(x).}
$$

This identity explains why optimizing a quantity that uses the **unnormalized areas** fits the **normalized shares**. At fixed model, $\log p(x)$ is constant with respect to $q$. The optimizer does not have to calculate that constant to maximize $\mathcal L$. A restricted family can leave a positive gap; changing model parameters also changes the evidence and posterior target. [Blei et al., §2.2, equations (10)–(14)](https://arxiv.org/html/1601.00670v9#S2.SS2).

### Work through Steve's ELBO

Let $q(L)=r$ and $q(F)=1-r$. Here $a_L=2/105$, $a_F=2/21$, so

$$
\mathcal L(r)=r\log\frac{2/105}{r}+(1-r)\log\frac{2/21}{1-r},\qquad 0<r<1.
$$

Differentiate:

$$
\mathcal L'(r)=\log\frac{a_L(1-r)}{a_Fr},\qquad
\mathcal L''(r)=-\frac1r-\frac1{1-r}<0.
$$

The unique maximum solves $a_L(1-r)=a_Fr$, giving $r=a_L/(a_L+a_F)=1/6$: exactly the Bayes answer. Endpoints use the continuous convention $0\log 0=0$.

![[assets/figures/2026-11-11-bayes-rectangles/03-elbo-shares.svg]]

*Original analytic illustration. The bar compares posterior shares with a candidate $q$; the curve shows the corresponding ELBO. The vertical gap is posterior KL in nats, not an area difference between the bars.*

| Candidate $q(L)$ | Expected log likelihood | Prior KL | ELBO | Posterior KL gap |
| --- | --- | --- | --- | --- |
| Prior: $1/21$ | $-2.2366$ | $0$ | $-2.2366$ | $0.0675$ |
| Equal shares: $1/2$ | $-1.6094$ | $0.8535$ | $-2.4629$ | $0.2939$ |
| Exact posterior: $1/6$ | $-2.0715$ | $0.0975$ | $-2.1691$ | $0$ |

The model's log evidence stays $\log(4/35)=-2.1691$. Equal shares improve expected log likelihood relative to the prior, but pay too much prior KL. Maximizing either term alone misses their balance.

Indeed, factor $a_z=p(x\mid z)p(z)$:

$$
\begin{aligned}
\mathcal L(q)
&=\sum_zq_z\log p(x\mid z)+\sum_zq_z\log\frac{p(z)}{q_z}\\
&=\mathbb E_q[\log p(x\mid z)]-D_{\mathrm{KL}}(q\|p(z)).
\end{aligned}
$$

The **prior KL** measures departure from the original column widths. The **posterior KL** measures error against the normalized retained areas. At the exact posterior, the second is zero and the first is positive. They have different targets and different jobs.

```atlas-interactive
path: assets/figures/2026-11-11-bayes-rectangles/elbo-explorer.html
title: Steve's ELBO — fit q to the normalized areas
height: 1150
```

*Try $q=$ prior, $q=$ equal shares, and $q=$ posterior. The model stays fixed. Compare the two KL readouts and watch where the ELBO touches the dashed log-evidence line.*

[[assets/figures/2026-11-11-bayes-rectangles/elbo-explorer.html|Open the offline ELBO explorer]].

### Why Jensen gives the very same gap

Give the trial distribution its own strip widths $q_z$. To keep each original area $a_z$, assign the strip height $W_z=a_z/q_z$. These heights are **importance weights**, not conditional probabilities; they may exceed 1. Then

$$
\mathbb E_q[W]=\sum_zq_z\frac{a_z}{q_z}=Z,\qquad
\mathbb E_q[\log W]=\mathcal L(q).
$$

Concavity of the logarithm gives $\mathbb E_q\log W\leq\log\mathbb E_qW=\log Z$. At $q_z=a_z/Z$, all strip heights equal $Z$, so Jensen is tight. Its gap is exactly the posterior KL derived above. The rectangle calculation, Bayes normalization, importance weighting, and the ELBO are four views of the same numbers.

In a VAE, $x$ is an observed image and $z$ its latent code; $q_\phi(z\mid x)$ is the encoder's approximation to these posterior shares. In diffusion, the hidden object can be the entire noisy path. The algebra applies to the whole path, even though its state space is much larger. A tractable Gaussian term does not by itself make all expectations or the full posterior analytic.

## Connections

- [[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Prior, likelihood & posterior|Prior, likelihood & posterior]] — Bayes rule updates the prior using the likelihood and its normalizing evidence.

## Origin

> [!info]- Source details
> Enriched at the user's request on 2026-11-11. The Steve inputs and rectangle inspiration are from Grant Sanderson's [Bayes lesson](https://www.3blue1brown.com/lessons/bayes-theorem/), with text adaptation by Josh Pullen; “Thinking about a sample,” “Building a formula,” and “Thinking with area” were read. The supplied video URL begins at 8:44; direct YouTube retrieval failed, so this does not claim a complete video/transcript review. The existing archived Bayes screenshot was inspected as visual context and left unchanged.
>
> Definitions and formulas were checked against the references cited beside them. The explicit Steve ELBO, strip-height interpretation, plots and explorers are original agent-added calculations. [[assets/figures/2026-11-11-bayes-rectangles/build_figures.py|Reproducible source]] and [[assets/figures/2026-11-11-bayes-rectangles/checks.json|mathematical checks]] accompany the figures. No claim is made that the ELBO extension appeared in the video.

```atlas
```
