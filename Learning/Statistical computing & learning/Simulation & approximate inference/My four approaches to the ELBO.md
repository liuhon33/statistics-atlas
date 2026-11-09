---
id: learning-elbo-four-approaches
title: My four approaches to the ELBO
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO]]"
subject: computing
backbone_path: "Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO"
study_band: M
note_types: [derivation, question, insight]
question_roles: [reconcile-approaches, concept-distinction, mechanism]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
learning_state: practicing
aliases: [ELBO learning summary, Orange and red ELBO forms]
tags: [atlas/learning, subject/computing, topic/elbo, study/masters]
connections:
  - "[[Backbone/Probability & mathematical foundations/Mathematical tools/Convexity & inequalities/Convex functions & bounds/Jensen inequality]]"
  - "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence]]"
  - "[[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Prior and posterior]]"
  - "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Efficient integration/Importance sampling]]"
sources:
  - "[[raw/notebooks/2026-11-08-VAE-opening-excerpt.json]]"
  - "[[raw/conversations/2026-10-22-ELBO-conversation-excerpt]]"
  - "[[raw/conversations/2026-10-22-ELBO-manifest.json]]"
  - "[[raw/assets/2026-10-22-ELBO-I01-posterior-KL-attempt.png]]"
  - "[[raw/assets/2026-10-22-ELBO-I02-Jensen-slide-annotations.png]]"
  - "[[raw/assets/2026-10-22-ELBO-I03-prior-posterior-comparison.png]]"
  - "[[raw/assets/2026-10-22-ELBO-I04-annotated-summary.png]]"
  - "[[raw/assets/2026-11-08-ELBO-I01-importance-sampling-derivation.png]]"
---

# My four approaches to the ELBO

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO

**The four perspectives describe one objective.** Jensen gives the lower bound; posterior KL identifies its exact gap; the likelihood/prior decomposition explains the regularization tradeoff; importance sampling explains the density ratio used to rewrite the evidence.

My orange/red comparison distinguishes **posterior approximation error** from **departure from the prior**. The first terms change along with the KL targets, leaving the same ELBO.

![[raw/assets/2026-10-22-ELBO-I04-annotated-summary.png]]

*My annotated summary, 2026-10-22. The clean derivations below restore the missing logarithms, put the complete ratio inside each logarithm, and replace the orange `log(x)` with $\log p(x)$. The original handwriting stays unchanged.*

## Shared setup

Fix the observed data $x$ and model parameters $\theta$. Let $z$ denote latent variables or unknown Bayesian parameters, and write $q(z)=q_\phi(z\mid x)$ for the normalized approximate posterior. Suppressing $x$ in this notation leaves its data dependence implicit.

The joint, evidence, and posterior are

$$
p_\theta(x,z)=p_\theta(x\mid z)p_\theta(z),\qquad
p_\theta(x)=\int p_\theta(x,z)\,dz,\qquad
p_\theta(z\mid x)=\frac{p_\theta(x,z)}{p_\theta(x)}.
$$

Evidence is the model's mass or density at the observed data after integrating out $z$. For discrete $z$, replace integrals by sums. Below, suppress $\theta$ and assume $0<p(x)<\infty$, matching support between $q$ and the posterior up to null sets, and absolute integrability of the displayed log terms. These sufficient conditions make all four derivations finite and justify the exact evidence rewriting.

## 1. Jensen: rewrite the evidence, then bound its logarithm

![[raw/assets/2026-10-22-ELBO-I02-Jensen-slide-annotations.png]]

*My upper-right handwriting introduces $q/q$ and applies Jensen. An expectation already includes the integration, so it needs no trailing $dz$.*

Insert $q$ to express the integral as an average under a distribution we can work with:

$$
p(x)=\int q(z)\frac{p(x,z)}{q(z)}\,dz
=\mathbb E_q[W(Z)],\qquad W(z)=\frac{p(x,z)}{q(z)}.
$$

Since $\log$ is concave,

$$
\log p(x)=\log\mathbb E_q[W]
\geq\mathbb E_q[\log W]
=\underbrace{\mathbb E_q[\log p(x,z)]-\mathbb E_q[\log q(z)]}_{\mathcal L(q)}.
$$

This defines the ELBO, also written $\mathbb E_q[\log p(x,z)]+H(q)$ with $H(q)=-\mathbb E_q[\log q(z)]$.

**My question, paraphrased from U06:** Why does this particular use of Jensen give exactly the expression obtained by expanding KL?

The choice of $W$ is deliberate: its $q$-expectation is the evidence. Once $q$ and this rewriting are fixed, Jensen produces a specific gap. The next route identifies that gap.

## 2. Posterior KL: identify exactly what the bound leaves out

Follow the Bayes substitution in my black handwriting:

$$
\begin{aligned}
D_{\mathrm{KL}}(q\|p(\cdot\mid x))
&=\mathbb E_q\left[\log\frac{q(z)}{p(z\mid x)}\right]\\
&=\mathbb E_q\left[\log\frac{q(z)p(x)}{p(x,z)}\right]\\
&=\log p(x)+\mathbb E_q[\log q(z)]-\mathbb E_q[\log p(x,z)]\\
&=\log p(x)-\mathcal L(q).
\end{aligned}
$$

Here $\log p(x)$ leaves the expectation because the averaging variable is $z$. Thus my orange form is

$$
\boxed{\mathcal L(q)=\log p(x)-D_{\mathrm{KL}}(q\|p(\cdot\mid x)).}
$$

In particular,

$$
\underbrace{\log\mathbb E_q[W]-\mathbb E_q[\log W]}_{\text{Jensen gap}}
=\mathbb E_q\left[\log\frac{p(x)q(z)}{p(x,z)}\right]
=D_{\mathrm{KL}}(q\|p(\cdot\mid x)).
$$

Jensen establishes nonnegativity; Bayes' rule identifies the gap as posterior KL. Equality holds when $q(z)=p(z\mid x)$ almost everywhere: then $W(z)=p(x)$ is constant under $q$.

**Why a lower bound if we maximize it?** The ordering is $\mathcal L(q)\leq\log p(x)$. If log evidence is $-10$, moving ELBO from $-15$ to $-11$ tightens the bound. A restricted variational family may leave a positive gap; an upper bound alone does not guarantee an attained maximum.

Maximizing ELBO over $q$ minimizes posterior KL **with the model fixed**. If $\theta$ also changes, log evidence changes too. The decomposition remains valid, but the constant-in-$q$ argument does not extend to joint optimization over $\theta$ and $q$. The standard identities are given in [Blei et al., §2.2, equations 12–14](https://arxiv.org/html/1601.00670v9#S2.SS2).

## 3. Likelihood and prior: expose data fit and regularization

Factor the joint inside the same ELBO:

$$
\begin{aligned}
\mathcal L(q)
&=\mathbb E_q[\log p(x\mid z)+\log p(z)-\log q(z)]\\
&=\mathbb E_q[\log p(x\mid z)]
-\mathbb E_q\left[\log\frac{q(z)}{p(z)}\right]\\
&=\underbrace{\mathbb E_q[\log p(x\mid z)]}_{\text{expected data fit}}
-\underbrace{D_{\mathrm{KL}}(q\|p(z))}_{\text{prior regularization}}.
\end{aligned}
$$

This is my red form. Equivalently, minimize expected data loss plus prior KL:

$$
-\mathcal L(q)=\mathbb E_q[-\log p(x\mid z)]+D_{\mathrm{KL}}(q\|p(z)).
$$

| My notation | First term | KL target | What changes with $q$? |
| --- | --- | --- | --- |
| Orange | $\log p(x)$ | Posterior $p(z\mid x)$ | Only the approximation gap |
| Red | $\mathbb E_q[\log p(x\mid z)]$ | Prior $p(z)$ | Both data fit and prior KL |

The posterior already combines likelihood and prior. Red exposes those ingredients; orange measures error against their combined target. The prior KL need not vanish at the optimum: informative data can justify moving away from the prior. The two terms are balanced together.

### My green question: why does expected log likelihood measure fit?

My summary uses a Gaussian observation model. Let $x,\mu_\theta(z)\in\mathbb R^d$, and assume $x\mid z\sim\mathcal N(\mu_\theta(z),\sigma^2I_d)$ with fixed $\sigma^2>0$. Then

$$
p_\theta(x\mid z)=(2\pi\sigma^2)^{-d/2}
\exp\left[-\frac{\|x-\mu_\theta(z)\|^2}{2\sigma^2}\right],
$$

so

$$
\mathbb E_q[-\log p_\theta(x\mid z)]
=\frac{\mathbb E_q\|x-\mu_\theta(z)\|^2}{2\sigma^2}
+\frac d2\log(2\pi\sigma^2).
$$

Higher expected log likelihood therefore means lower expected squared error in this model. If variance is learned, retain its weighting and normalization terms. Other likelihood families give other losses.

My sampling interpretation is: draw latent explanations from $q$, calculate each explanation's loss, and average those losses. For iid $z_1,\ldots,z_S\sim q$ and finite expected absolute loss,

$$
\widehat J_S=\frac1S\sum_{s=1}^S[-\log p_\theta(x\mid z_s)]
$$

is unbiased for the expected loss and converges to it by the law of large numbers. The observation $x$ stays fixed.

A useful clarification from the earlier digest: averaging losses differs from computing the loss of an average prediction. For finite second moments and $M=\mu_\theta(Z)$,

$$
\mathbb E_q\|x-M\|^2
=\|x-\mathbb E_qM\|^2+\operatorname{tr}(\operatorname{Cov}_q(M)).
$$

For $x=0$ and equally likely predictions $-1$ and $1$, the average squared loss is $1$, while the averaged prediction has squared loss $0$.

### The penalized-regression connection I asked about

For $X\in\mathbb R^{n\times d}$, $y\in\mathbb R^n$, $w\in\mathbb R^d$, and fixed positive variances, suppose

$$
y\mid w\sim\mathcal N(Xw,\sigma^2I_n),\qquad
w\sim\mathcal N(0,\tau^2I_d).
$$

MAP minimizes $\|y-Xw\|^2/(2\sigma^2)+\|w\|^2/(2\tau^2)$. Multiplying by $2\sigma^2$ gives ridge with summed squared error and $\lambda=\sigma^2/\tau^2$:

$$
\widehat w=\arg\min_w\{\|y-Xw\|^2+\lambda\|w\|^2\},\qquad
(X^\top X+\lambda I_d)\widehat w=X^\top y.
$$

For $\lambda>0$ the matrix is positive definite even when $X$ is rank deficient. This isotropic prior penalizes every coefficient, including an intercept if included in $w$. Using mean squared error changes the scaling of $\lambda$. This extension was supplied in the original conversation; see [MIT 6.790, Bayesian view on regression](https://gradml.mit.edu/supervised/explicit_regularization/#bayesian-view-on-regression).

Variational inference instead chooses a distribution $q(w)$ and minimizes, up to a constant,

$$
\frac{\mathbb E_q\|y-Xw\|^2}{2\sigma^2}
+D_{\mathrm{KL}}(q(w)\|\mathcal N(0,\tau^2I_d)).
$$

The KL contains an expected negative log prior and negative entropy, so it acts on the distribution's location and spread.

## 4. Importance sampling: interpret the same ratio computationally

The $q/q$ step in my Jensen handwriting also has an importance-sampling interpretation. With proposal $q$,

$$
W(z)=p(x\mid z)\frac{p(z)}{q(z)}=\frac{p(x,z)}{q(z)},\qquad
\mathbb E_q[W]=p(x).
$$

Sampling under $q$ and reweighting recovers the evidence integral. For iid $z_1,\ldots,z_S\sim q$,

$$
\widehat p_S(x)=\frac1S\sum_{s=1}^S W(z_s),\qquad
\mathbb E[\widehat p_S(x)]=p(x).
$$

This evidence estimator is the construction in [Stanford CS228, Importance sampling](https://ermongroup.github.io/cs228-notes/inference/sampling/#importance-sampling). Its unbiasedness requires $q$ to cover the region contributing to the integral. If $q$ misses positive posterior mass, the expectation recovers only the covered region.

ELBO takes the logarithm **before** averaging:

$$
\mathcal L(q)=\mathbb E_q[\log W],\qquad
\log p(x)=\log\mathbb E_q[W].
$$

This ordering is the link back to Jensen. At the true posterior, every weight is $p(x)$ and the gap vanishes. The fourth perspective makes the reweighting and computation explicit; it uses the same mathematical step as route 1.

For finite simulation, distinguish the mean of log weights, $S^{-1}\sum_s\log W(z_s)$, from the log of the mean weight, $\log\widehat p_S(x)$. The former is unbiased for ELBO under our integrability assumptions; the latter is generally biased for log evidence. Neither individual random estimate is guaranteed to be below $\log p(x)$.

### Notebook extension: why introduce the encoder in the first place?

The opening of the [VAE notebook, especially the linked cell](https://colab.research.google.com/drive/19yg2hMc8iq35vICJKK7bit3vTWI8NSJW?usp=sharing#scrollTo=aXTnEvdTmhKj) motivates the same fourth route **from a sampling problem**, rather than starting with the algebraic insertion of $q/q$:

1. **Start with prior sampling.** Since $p_\theta(x)=\mathbb E_{p(z)}[p_\theta(x\mid Z)]$, we could average likelihoods at draws from the prior. But for a particular observed $x$, many draws may give negligible likelihood: a prior that generates many kinds of observations is not tailored to explaining this one.
2. **Use an $x$-dependent proposal.** The encoder $q_\phi(z\mid x)$ learns to propose plausible latent explanations. Correct the changed sampling distribution with $p(z)/q_\phi(z\mid x)$; this is an exact change of measure under our support assumptions, not yet a bound.
3. **Apply Jensen, then split the log.** This converts the evidence expression into the same reconstruction/prior-KL form as route 3:

$$
\begin{aligned}
\log p_\theta(x)
&=\log\mathbb E_{p(z)}[p_\theta(x\mid Z)]\\
&=\log\mathbb E_{q_\phi(z\mid x)}
\left[p_\theta(x\mid Z)\frac{p(Z)}{q_\phi(Z\mid x)}\right]\\
&\geq\mathbb E_{q_\phi}[\log p_\theta(x\mid Z)]
-D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))
=\mathcal L(\theta,\phi;x).
\end{aligned}
$$

**What this adds to my fourth interpretation:** $q$ is not merely an arbitrary distribution inserted to enable Jensen. It is a learnable, data-dependent sampling proposal. This connects **route 4 → route 1 → route 3** without introducing a different ELBO.

**Added clarification:** the importance correction is the *multiplicative ratio* $p/q$. Its expected logarithm becomes $-D_{\mathrm{KL}}(q\|p)$ inside the bound. That **prior KL is not the error caused by Jensen**; the exact gap remains the **posterior KL** from route 2. Nor does learning $q$ automatically guarantee lower importance-weight variance; its support and tails still matter.

For a concrete illustration, let the prior be uniform over 100 latent states, with $p(x\mid z)=1$ in one state and $0.001$ in each other state. Then $p(x)=0.01099$, but a prior draw hits the dominant state only 1% of the time. Its posterior probability is about 91%. Sampling from the exact posterior would make every corrected weight $0.01099$: the proposal changes where we look, not the integral.

In VAE training, minimize $-\mathcal L$: expected **negative** log likelihood plus prior KL. Only the KL term is analytic for suitable families, such as a Gaussian encoder with a standard-normal prior; reconstruction generally still needs sampling. Here $q_\phi$ is the **encoder**, not the decoder (a typo in the notebook's final sentence). These implementation distinctions agree with [Kingma and Welling, §§2.2–2.3, equations (3) and (7)](https://arxiv.org/html/1312.6114v11#S2.SS3).

### My handwritten derivation: from prior sampling to the VAE objective

![[raw/assets/2026-11-08-ELBO-I01-importance-sampling-derivation.png]]

*My derivation for one observation $x_i$, 2026-11-08: the notebook route worked by hand, from a prior Monte Carlo estimate to the bound I circled in red. The orange marks are my own sign and ratio correction.*

My $\hat p(x_i)$ is the model's evidence $p_\theta(x_i)$, not a Monte Carlo estimate: the first line equates it with the exact integral. Written cleanly, the chain is

$$
\begin{aligned}
\log p_\theta(x_i)
&=\log\int p_\theta(x_i\mid z)\,p(z)\,dz
=\log\mathbb E_{z\sim p(z)}[p_\theta(x_i\mid z)]\\
&=\log\int p_\theta(x_i\mid z)\,\frac{p(z)}{q_\phi(z\mid x_i)}\,q_\phi(z\mid x_i)\,dz\\
&=\log\mathbb E_{z\sim q_\phi(z\mid x_i)}\left[p_\theta(x_i\mid z)\,\frac{p(z)}{q_\phi(z\mid x_i)}\right]\\
&\geq\mathbb E_{q_\phi}[\log p_\theta(x_i\mid z)]
+\mathbb E_{q_\phi}\left[\log\frac{p(z)}{q_\phi(z\mid x_i)}\right]\\
&=\mathbb E_{q_\phi}[\log p_\theta(x_i\mid z)]
-D_{\mathrm{KL}}(q_\phi(z\mid x_i)\|p(z)).
\end{aligned}
$$

The sample index $j$ belongs only to the draws. Inside an integral, $z$ is the integration variable, so the page's $p(z_j)$ and $q(z_j\mid x_i)$ become $p(z)$ and $q_\phi(z\mid x_i)$. The reconstruction term in the last line should carry $x_i$, like the KL term.

**Green: the naive estimate.** For iid draws $z_1,\ldots,z_N\sim p(z)$,

$$
\log p_\theta(x_i)\approx\log\left[\frac1N\sum_{j=1}^N p_\theta(x_i\mid z_j)\right].
$$

The bracket is unbiased for the evidence, but its logarithm is not: by Jensen, the expected log estimate is at most $\log p_\theta(x_i)$. It still converges almost surely as $N\to\infty$. The practical problem is the one in the 100-state example: most prior draws barely explain $x_i$.

**Underline and circle: the change of measure.** The underlined $q_\phi(z\mid x_i)\,dz$ is the new sampling distribution. The circled $p(z)/q_\phi(z\mid x_i)$ is the importance weight that corrects for it. Times the likelihood, it is route 4's $W(z)=p(x_i,z)/q_\phi(z\mid x_i)$, so this step is still exact.

**Blue and orange: Jensen, then KL.** The $\geq$ is route 1's Jensen step, after which the logarithm of the product splits into two expectations. My orange marks flip the ratio and the sign: $\mathbb E_q[\log(p/q)]=-\mathbb E_q[\log(q/p)]$. In my orange definition $D_{\mathrm{KL}}(P\|Q)=\int P\log(P/Q)$, the first argument is both the averaging distribution and the numerator. Here that role belongs to $q_\phi$, so the term is $-D_{\mathrm{KL}}(q_\phi(z\mid x_i)\|p(z))$; the definition's $p$ is only a placeholder.

**Red: what "maximize this" asks for.** Three refinements of my labels:

- The blue-underlined term is an expected **log-likelihood**, to be maximized. The reconstruction *loss* is its negative, $-\mathbb E_{q_\phi}[\log p_\theta(x_i\mid z)]$. For a Gaussian decoder it is expected squared error up to constants (the green question in route 3).
- "Maximize $p(x\mid z)$" means maximizing the *average* log-likelihood over the codes the encoder proposes for $x_i$, not the likelihood at a single $z$.
- "Minimize distance from $q$ to $p$": KL is not a distance, since it is asymmetric, and its target here is the **prior**, not the posterior. It is not minimized on its own. If $D_{\mathrm{KL}}(q_\phi(z\mid x)\|p(z))=0$ for every $x$, then $q_\phi(z\mid x)=p(z)$, and the code ignores the data.

The 100-state example shows the trade-off:

| $q$ | $\mathbb E_q[\log p(x\mid z)]$ | $D_{\mathrm{KL}}(q\Vert p(z))$ | ELBO | Posterior-KL gap |
| --- | --- | --- | --- | --- |
| Prior (my green sampler) | $-6.84$ | $0$ | $-6.84$ | $2.33$ |
| Exact posterior | $-0.62$ | $3.89$ | $-4.51$ | $0$ |

Moving $q$ from the prior to the posterior raises the reconstruction term by $6.22$ at a prior-KL cost of $3.89$. The net gain, $2.33$, is exactly the posterior-KL gap that closes (route 2). At the optimum, the prior KL is far from zero.

**From "≈" to "≥" (added).** My green line averages before taking the logarithm; the bound averages after it. Importance-weighted bounds sit between the two. For iid $z_1,\ldots,z_K\sim q_\phi(z\mid x_i)$, the quantity $\mathbb E\bigl[\log\frac1K\sum_k W(z_k)\bigr]$ equals the ELBO at $K=1$, never decreases as $K$ grows, stays at most $\log p_\theta(x_i)$, and approaches it when $W$ is bounded ([Burda, Grosse and Salakhutdinov, Theorem 1](https://arxiv.org/abs/1509.00519)). My green line is one random draw of this quantity with the prior as proposal. In the 100-state example, its expectation rises from $-6.84$ at $N=1$ to $-4.55$ at $N=1000$.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Convexity & inequalities/Convex functions & bounds/Jensen inequality|Jensen inequality]] — Concavity of log turns the exact importance-ratio expectation into the ELBO lower bound.
- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]] — Posterior KL is the exact Jensen gap; prior KL is the regularization term in the likelihood/prior decomposition.
- [[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Prior and posterior|Prior and posterior]] — Bayes' rule explains why fitting the posterior and balancing likelihood against prior regularization give the same objective.
- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Efficient integration/Importance sampling|Importance sampling]] — The ratio $p(x,z)/q(z)$ permits evidence estimation under $q$ and exposes the difference between averaging weights and averaging log weights.

## Origin

My questions and handwriting come from the [[raw/conversations/2026-10-22-ELBO-conversation-excerpt|2026-10-22 conversation]], U01–U09 and A01–A07, with images I01–I04. I04 and I02 are displayed here; all four originals remain source evidence. Their identities and hashes are recorded in the original [[raw/conversations/2026-10-22-ELBO-manifest.json|source manifest]].

The handwritten Bayes/Jensen routes, orange/red distinction, and green Gaussian reasoning are mine. The clean notation, explicit assumptions, gap/equality proof, MAP/ridge extension, and prediction-variance clarification include the earlier assistant's contributions. The explicit importance-sampling interpretation and finite-estimate comparison are added synthesis for this consolidated note.

The notebook extension was requested on 2026-11-08 and summarizes its opening three Markdown cells, preserved in the [[raw/notebooks/2026-11-08-VAE-opening-excerpt.json|opening excerpt]]. The comparison, qualifications, and 100-state example are assistant-added synthesis, not additional handwritten work. Later notebook examples and code are outside this addition.

The handwritten derivation was added on 2026-11-08 from [[raw/assets/2026-11-08-ELBO-I01-importance-sampling-derivation.png|one page]] supplied in a Claudian chat. The prior Monte Carlo line, the importance-sampling rewrite, the Jensen split, the orange sign and ratio correction, and the red and blue labels are mine. The notation fixes, the reconstruction-loss sign, the KL-target qualification, the trade-off table and the importance-weighted-bound remark were added by the assistant.
