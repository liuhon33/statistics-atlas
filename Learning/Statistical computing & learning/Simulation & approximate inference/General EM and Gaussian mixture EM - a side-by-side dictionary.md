---
id: learning-general-em-gmm-dictionary
title: General EM and Gaussian mixture EM - a side-by-side dictionary
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Modes, curvature & latent variables/Expectation–maximization]]'
subject: computing
backbone_path: Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Modes, curvature & latent variables → Expectation–maximization
study_band: M
note_types: [topic-note, question, derivation]
question_roles: [special-to-general, concept-distinction, mechanism]
source_format: course-slides-and-conversation
created: 2026-11-13
updated: 2026-11-16
status: active
verification: checked
aliases: [General EM versus GMM EM, EM formula dictionary]
tags: [atlas/learning, subject/computing, topic/em, topic/gaussian-mixtures]
connections:
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/Gaussian mixture models]]'
  - '[[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO]]'
sources:
  - '[[raw/assets/2026-11-13-EM-I01-general-algorithm.png]]'
  - '[[raw/assets/2026-11-13-EM-I02-p13-iteration-reference.png]]'
---

# General EM and Gaussian mixture EM - a side-by-side dictionary

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Modes, curvature & latent variables → Expectation–maximization

**GMM EM is general EM with a particular joint model plugged in.** The hidden variable becomes the component label of each point; the posterior becomes its soft membership probabilities; maximizing the expected complete-data log-likelihood becomes fitting weighted Gaussian means, covariances and mixing proportions.

**My question, paraphrased:** Why is each step of the earlier GMM EM algorithm an instance of general EM? Which letter, probability, expectation and maximization in the general formula produces each GMM derivation?

The tables are the lookup dictionary; **§3 performs the substitutions line by line**, including all three GMM parameter updates. These are not two competing algorithms.

**Original slides:** Thibault Randrianarisoa, EM algorithm, University of Toronto, 2026-02-25 (original course PDF retained privately).

> [!info]- Lecture source
> Thibault Randrianarisoa, EM algorithm, University of Toronto, 2026-02-25 (original course PDF retained privately), slide 14
> *Slide 14 contains the general EM algorithm. The original course PDF is retained privately.*

## 1. The side-by-side dictionary

Use $N$ observations, $D$ features and $K$ mixture components. The GMM slides write the feature dimension as $m$; here $D=m$. Assume independent observations under the usual mixture model, fixed $K$, $\pi_k>0$, $\sum_k\pi_k=1$, and positive-definite full covariances $\Sigma_k$. Each $x_n$ is a $D$-dimensional column vector; $X$ stacks their transposes as rows.

### Objects: what is observed, hidden, and learned?

| General EM | Gaussian mixture EM |
| --- | --- |
| **Observed data:** $X$ | The measured points $x_1,\ldots,x_N$; $X\in\mathbb R^{N\times D}$. These do **not** change during EM. |
| **Latent variables:** $Z$ | One unobserved label $z_n\in\{1,\ldots,K\}$ for each point: “which Gaussian generated $x_n$?” Collect them as $Z=(z_1,\ldots,z_N)$. |
| **Alternative latent encoding** | $s_{nk}=\mathbf1\{z_n=k\}$. The one-hot matrix $S\in\{0,1\}^{N\times K}$ has exactly one 1 per row. Labels $Z$ and indicators $S$ encode the same hidden assignments. |
| **Model parameters:** $\theta$ | $\theta=\{\pi_k,\mu_k,\Sigma_k\}_{k=1}^K$: mixing proportions, means, covariances. They are the unknown quantities fitted by maximum likelihood, **not** the latent labels. |
| **Complete-data model:** $p(X,Z\mid\theta)$ | $\prod_{n=1}^N\pi_{z_n}\mathcal N_D(x_n\mid\mu_{z_n},\Sigma_{z_n})$. Equivalently, $\prod_n\prod_k[\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)]^{s_{nk}}$. |
| **Marginalize the hidden variables:** $p(X\mid\theta)=\sum_Zp(X,Z\mid\theta)$ | $p(X\mid\theta)=\prod_n\sum_k\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)$. The sum over **all label configurations** has $K^N$ terms, but independence turns it into $N$ small $K$-term sums. |
| **Posterior:** $p(Z\mid X,\theta^{\mathrm{old}})$ | $\prod_n p(z_n\mid x_n,\theta^{\mathrm{old}})$. Each factor is a categorical distribution, summarized by responsibilities $r_{nk}^{\mathrm{old}}=p(z_n=k\mid x_n,\theta^{\mathrm{old}})$. |

**Do not confuse the hidden assignments with their probabilities.** A one-hot row could be $(1,0)$; a responsibility row could be $(0.8,0.2)$. The latter means uncertainty about the former, not that the hidden label itself is fractional. In fact, $\mathbb E[s_{nk}\mid X,\theta^{\mathrm{old}}]=r_{nk}^{\mathrm{old}}$.

The general slide's $Z\in\mathbb R^{N\times K}$ is schematic, not a universal EM requirement. For this GMM, an $N$-vector of categorical labels or an $N\times K$ one-hot matrix is appropriate. Other latent-variable models may have continuous or differently shaped hidden variables; then the corresponding sum becomes an integral where needed. [Lecture 7, slides 5–6, 8, 14–15.]

### Objectives and steps: which formula corresponds to which?

| General EM                                                                                                                   | Gaussian mixture EM                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall goal:** increase $\ell(\theta)=\log p(X\mid\theta)$ to seek maximum-likelihood parameters.                         | $\ell(\theta)=\sum_n\log[\sum_k\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)]$. This is the **observed-data** log-likelihood: a log of a sum for each point.                                                                                                                                   |
| **If the hidden data were known:** $\log p(X,Z\mid\theta)$                                                                   | $\sum_n\sum_k s_{nk}[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)]$. A label would tell us which Gaussian each point contributes to.                                                                                                                                                 |
| **Initialize:** choose $\theta^{\mathrm{old}}$.                                                                              | Choose starting weights, means and positive-definite covariances; labels need not be initialized as known facts.                                                                                                                                                                          |
| **E-step:** compute $q^{\mathrm{old}}(Z)=p(Z\mid X,\theta^{\mathrm{old}})$.                                                  | Compute every $r_{nk}^{\mathrm{old}}$ using Bayes' rule: $\displaystyle r_{nk}^{\mathrm{old}}=\frac{\pi_k^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_k^{\mathrm{old}},\Sigma_k^{\mathrm{old}})}{\sum_j\pi_j^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_j^{\mathrm{old}},\Sigma_j^{\mathrm{old}})}$. |
| **Expected complete-data objective:** $Q(\theta,\theta^{\mathrm{old}})=\mathbb E_{q^{\mathrm{old}}}[\log p(X,Z\mid\theta)]$. | $Q=\sum_n\sum_k r_{nk}^{\mathrm{old}}[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)]$. Replace each unknown indicator by its posterior expectation.                                                                                                                                   |
| **M-step:** $\theta^{\mathrm{new}}=\arg\max_\theta Q(\theta,\theta^{\mathrm{old}})$.                                         | Hold $r_{nk}^{\mathrm{old}}$ fixed and update $\pi_k,\mu_k,\Sigma_k$ using the weighted formulas in §3.                                                                                                                                                                                   |
| **Repeat and monitor**                                                                                                       | Set $\theta^{\mathrm{old}}\leftarrow\theta^{\mathrm{new}}$; recompute responsibilities next time. Monitor the **observed** log-likelihood, not raw $Q$ values with changing posterior weights.                                                                                            |

**The key distinction:** the final target is $\ell(\theta)$, but an M-step directly maximizes $Q(\theta,\theta^{\mathrm{old}})$. These are not the same function. The E-step holds $\theta$ fixed, so it does not change $\ell(\theta)$; it constructs the posterior weights used by the next M-step. [Lecture 7, slides 8–15.]

> [!example]- The supplied general-EM slide
> ![[raw/assets/2026-11-13-EM-I01-general-algorithm.png]]
> *Original supplied screenshot, preserved unchanged. Its formula matches Lecture 7 slide 14.*

## 2. Play with the two-Gaussian example

Start with **Crossed centers**, which resembles the arrangement in slide 13:

1. Click **E-step**. Only the colors change: blue means a high responsibility for component 1; red means a high responsibility for component 2; mixed colors mean uncertainty. The Gaussian parameters and observed likelihood stay fixed.
2. Click **M-step**. The crosses and ellipses move/reshape, and the weights update. The colors remain frozen at the probabilities that this M-step used.
3. Click **E-step** again. Now the probabilities are recomputed under the new Gaussians. Or use **Play** to alternate the two phases.
4. Try **Identical centers**. With identical starting Gaussian distributions, the posterior cannot distinguish them; both components receive the same weighted mean and covariance. Exact EM does not spontaneously break this symmetry. Then switch back or tune one initial mean.

```atlas-interactive
path: assets/figures/2026-11-13-em-gmm/explorer.html
title: General EM in action — two Gaussian components
height: 1450
```

[[assets/figures/2026-11-13-em-gmm/explorer.html|Open the standalone EM explorer]]

The point slider (or clicking a dot) shows one observation's stored $r_{n1},r_{n2}$. The likelihood trace records completed M-steps; $\Delta Q$ compares before/after parameters **under the same frozen posterior**. Initial-parameter changes reset the fit on the same 240 synthetic observations; they do not resample the data.

> [!example]- Static view of the same simulation
> ![[assets/figures/2026-11-13-em-gmm/overview.svg]]
> *Original deterministic example, not recovered lecture data. All four panels use identical point coordinates and axis scales. Solid/dashed ellipses have Mahalanobis radii 1/2; they are component-density contours, not confidence intervals.*

> [!example]- Lecture inspiration: slide 13
> ![[raw/assets/2026-11-13-EM-I02-p13-iteration-reference.png]]
> *Full-page render of Thibault Randrianarisoa's Lecture 7, slide 13. The embedded explorer is a new implementation inspired by this sequence, not an extraction of its original animation or sample.*

## 3. Instantiate the general recipe, one line at a time

### 3.1 General model and goal → the GMM joint and observed likelihood

The general recipe leaves $p(X,Z\mid\theta)$ unspecified. For GMM, **choose**

$$
\underbrace{p(x_n,z_n=k\mid\theta)}_{\text{one point's joint model}}
=\underbrace{\pi_k}_{p(z_n=k\mid\theta)}
\underbrace{\mathcal N_D(x_n\mid\mu_k,\Sigma_k)}_{p(x_n\mid z_n=k,\theta)}.
$$

Independence makes the whole-data joint a product. Substitute that product into the general objective, and write out what its $\sum_Z$ means:

$$
\begin{aligned}
\underbrace{\ell(\theta)=\log\sum_Zp(X,Z\mid\theta)}_{\text{general observed-data objective}}
&=\log\sum_{z_1=1}^K\cdots\sum_{z_N=1}^K
\prod_{n=1}^N\pi_{z_n}\mathcal N_D(x_n\mid\mu_{z_n},\Sigma_{z_n})\\
&=\log\prod_{n=1}^N
\left[\sum_{k=1}^K\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right]\\
&=\underbrace{\sum_{n=1}^N\log
\left[\sum_{k=1}^K\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right]}_{\text{exactly the GMM objective on slide 8}}.
\end{aligned}
$$

Thus the GMM's log-of-a-mixture-sum is not a new objective: it is the general marginal log-likelihood with this joint model substituted. The sum over $k$ is **inside** each logarithm; it cannot simply be pulled outside.

### 3.2 General E-step posterior → the GMM responsibility formula

The general instruction is “compute $p(Z\mid X,\theta^{\mathrm{old}})$.” For independent mixture observations, this posterior factorizes over $n$. For each categorical factor, substitute the GMM joint into Bayes' rule:

$$
\begin{aligned}
\underbrace{p(z_n=k\mid x_n,\theta^{\mathrm{old}})}_{r_{nk}^{\mathrm{old}}}
&=\frac{p(x_n,z_n=k\mid\theta^{\mathrm{old}})}{p(x_n\mid\theta^{\mathrm{old}})}\\
&=\underbrace{\frac{\pi_k^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_k^{\mathrm{old}},\Sigma_k^{\mathrm{old}})}
{\sum_{j=1}^K\pi_j^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_j^{\mathrm{old}},\Sigma_j^{\mathrm{old}})}}_{\text{exactly the GMM E-step on slides 6 and 12}}.
\end{aligned}
$$


**What corresponds to what:** the entire $p(Z\mid X,\theta^{\mathrm{old}})$ is a distribution over all label vectors; the $N\times K$ responsibility array compactly specifies its independent categorical factors. It is not literally one scalar probability. Every parameter used to compute it comes from $\theta^{\mathrm{old}}$.

### 3.3 General $Q$ expectation → the weighted GMM log-likelihood

Now unpack each part of the general formula from the screenshot:

$$
Q(\underbrace{\theta}_{\text{candidate parameters}},
\underbrace{\theta^{\mathrm{old}}}_{\text{determines fixed posterior weights}})
=\sum_Z\underbrace{p(Z\mid X,\theta^{\mathrm{old}})}_{\text{from the E-step}}
\underbrace{\log p(X,Z\mid\theta)}_{\text{evaluate the joint at candidate }\theta}.
$$

For GMM, taking the logarithm of the indicator-form joint gives

$$
\log p(X,Z\mid\theta)
=\sum_{n=1}^N\sum_{k=1}^K
s_{nk}\left[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right].
$$

$s_{nk}$: the latent assignment indicator for data point $n$; if it belongs to component $k$, it's 1; otherwise it's 0.
$r_{nk}^{\mathrm{old}}$: the responsibility of component $k$ for data point $n$ under the old model, or the posterior probability that this point belongs to component $k$. Notice that $r_{nk}^{\mathrm{old}}=\frac{p(x_n,z_n=k\mid\theta^{\mathrm{old}})}{p(x_n\mid\theta^{\mathrm{old}})}$. For example, suppose the old model assigns one point responsibilities $(0.8,0.2)$; its contribution to $Q$ is $0.8\log[\pi_1\mathcal N_D(x_n\mid\mu_1,\Sigma_1)] + 0.2\log[\pi_2\mathcal N_D(x_n\mid\mu_2,\Sigma_2)]$. **The probabilities are old and fixed; the parameters inside the logarithms are candidates, not fixed old parameters.**

> [!note]- Why define Q, and what does it look like for a GMM?
> **The question behind $Q$:** given our current beliefs about the missing labels, which candidate parameters fit the completed data best on average? The ultimate goal is still maximizing $\ell(\theta)=\log p(X\mid\theta)$. $Q$ is an easier objective used to improve that goal, not a replacement for it.
>
> **1. Use the old parameters to decide the weights.** For GMM, $\theta=\{\pi_k,\mu_k,\Sigma_k\}_{k=1}^K$. The old model supplies the responsibilities through Bayes' rule:
>
> $$
> \begin{aligned}
> \underbrace{p(z_n=k\mid x_n,\theta^{\mathrm{old}})}_{r_{nk}^{\mathrm{old}}}
> &=\frac{p(x_n,z_n=k\mid\theta^{\mathrm{old}})}{p(x_n\mid\theta^{\mathrm{old}})}\\
> &=\underbrace{\frac{\pi_k^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_k^{\mathrm{old}},\Sigma_k^{\mathrm{old}})}
> {\sum_{j=1}^K\pi_j^{\mathrm{old}}\mathcal N_D(x_n\mid\mu_j^{\mathrm{old}},\Sigma_j^{\mathrm{old}})}}_{\text{exactly the GMM E-step on slides 6 and 12}}.
> \end{aligned}
> $$
>
> **2. Average the easier complete-data objective.** If the labels were known, we would maximize the complete-data log-likelihood displayed above: each point would contribute to the Gaussian indicated by $s_{nk}$. Since the labels are unknown, average over their possible assignments under the old posterior rather than pretending one guessed assignment is certain. Linearity of expectation gives
>
> $$
> \begin{aligned}
> Q(\theta,\theta^{\mathrm{old}})
> &=\mathbb E_{Z\mid X,\theta^{\mathrm{old}}}[\log p(X,Z\mid\theta)]\\
> &=\sum_{n,k}\underbrace{\mathbb E[s_{nk}\mid X,\theta^{\mathrm{old}}]}_{r_{nk}^{\mathrm{old}}}
> [\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)].
> \end{aligned}
> $$
>
> Thus the GMM $Q$-function is
>
> $$
> \boxed{
> Q(\theta,\theta^{\mathrm{old}})
> =\sum_{n=1}^N\sum_{k=1}^K
> \underbrace{r_{nk}^{\mathrm{old}}}_{\text{fixed weight}}
> \underbrace{[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)]}_{\text{score at candidate }\theta}.
> }
> $$
>
> The two arguments have different jobs: $\theta^{\mathrm{old}}$ determines how much each observation contributes to each component; $\theta$ contains the candidate weights, means and covariances being optimized. In the $(0.8,0.2)$ example, the $0.8$ and $0.2$ stay fixed throughout the M-step while the parameters inside both logarithms change. We average the log-likelihood over missing assignments, not over new observed data.
>
> Expanding the Gaussian density makes the weighted-fitting problem explicit. With $N_k=\sum_n r_{nk}^{\mathrm{old}}$,
>
> $$
> \begin{aligned}
> Q(\theta,\theta^{\mathrm{old}})
> ={}&\sum_kN_k\log\pi_k-\frac12\sum_kN_k\log|\Sigma_k|\\
> &-\frac12\sum_{n,k}r_{nk}^{\mathrm{old}}
> (x_n-\mu_k)^\top\Sigma_k^{-1}(x_n-\mu_k)
> -\frac{ND}{2}\log(2\pi).
> \end{aligned}
> $$
>
> Maximizing these terms produces the mixture-proportion, weighted-mean and weighted-covariance updates derived in §3.4. Unlike the observed log-likelihood, there is no logarithm enclosing a sum over mixture components.
>
> **3. Why this average helps the real likelihood: a tight lower bound.** The posterior choice is not arbitrary. Write $q_{\mathrm{old}}(Z)=p(Z\mid X,\theta^{\mathrm{old}})$. In the positive-probability GMM setting, insert it into the observed likelihood and apply [[Jensen inequality|Jensen's inequality]] to the concave logarithm:
>
> $$
> \begin{aligned}
> \ell(\theta)
> &=\log\sum_Zq_{\mathrm{old}}(Z)
> \frac{p(X,Z\mid\theta)}{q_{\mathrm{old}}(Z)}\\
> &\geq\sum_Zq_{\mathrm{old}}(Z)
> \log\frac{p(X,Z\mid\theta)}{q_{\mathrm{old}}(Z)}\\
> &=\underbrace{\sum_Zq_{\mathrm{old}}(Z)\log p(X,Z\mid\theta)}_{Q(\theta,\theta^{\mathrm{old}})}
> +\underbrace{\left[-\sum_Zq_{\mathrm{old}}(Z)\log q_{\mathrm{old}}(Z)\right]}_{H(q_{\mathrm{old}})}.
> \end{aligned}
> $$
>
> **This is where $Q$ naturally emerges:** it is the parameter-dependent part of the lower bound. The entropy $H(q_{\mathrm{old}})$ is constant while the old posterior is fixed. At the old parameters the bound is exact, because
>
> $$
> \frac{p(X,Z\mid\theta^{\mathrm{old}})}{p(Z\mid X,\theta^{\mathrm{old}})}
> =p(X\mid\theta^{\mathrm{old}}),
> $$
>
> which does not depend on $Z$, so [[Jensen inequality|Jensen's inequality]] becomes equality.
>
> **Why can every sign remain $=$ at $\theta^{\mathrm{old}}$?** Put $c=p(X\mid\theta^{\mathrm{old}})>0$. This is one fixed number as $Z$ varies, and the posterior weights satisfy $\sum_Zq_{\mathrm{old}}(Z)=1$. Therefore
>
> $$
> \begin{aligned}
> \ell(\theta^{\mathrm{old}})
> &=\log c
> =\log\left[\sum_Zq_{\mathrm{old}}(Z)c\right]\\
> &=\sum_Zq_{\mathrm{old}}(Z)\log c\\
> &=\sum_Zq_{\mathrm{old}}(Z)
> \log\frac{p(X,Z\mid\theta^{\mathrm{old}})}{q_{\mathrm{old}}(Z)}\\
> &=Q(\theta^{\mathrm{old}},\theta^{\mathrm{old}})+H(q_{\mathrm{old}}).
> \end{aligned}
> $$
>
> The key step is exact because **both** $\log[\sum_Zq_{\mathrm{old}}(Z)c]$ and $\sum_Zq_{\mathrm{old}}(Z)\log c$ equal $\log c$. Only the expression changes; the parameter value does not. We are not claiming that logarithms generally commute with expectations. For another candidate $\theta$, keeping $q_{\mathrm{old}}$ fixed, the ratio $p(X,Z\mid\theta)/q_{\mathrm{old}}(Z)$ generally varies with $Z$; then Jensen gives only $\geq$.
>
> Consequently, with finite quantities, any M-step that increases or preserves $Q$ satisfies
>
> $$
> \begin{aligned}
> \ell(\theta^{\mathrm{new}})
> &\geq Q(\theta^{\mathrm{new}},\theta^{\mathrm{old}})+H(q_{\mathrm{old}})\\
> &\geq Q(\theta^{\mathrm{old}},\theta^{\mathrm{old}})+H(q_{\mathrm{old}})\\
> &=\ell(\theta^{\mathrm{old}}).
> \end{aligned}
> $$
>
> **In short:** $Q$ turns uncertain assignments into weighted fitting, and its tight-bound construction guarantees that improving it cannot decrease the observed-data likelihood. The tight lower bound is $Q+H$, not $Q$ alone; this does not guarantee a global optimum.


Take its expectation under the **old** posterior. The bracket depends on observed $x_n$ and the candidate $\theta$, not on the random indicator; it can come outside the expectation:

$$
\begin{aligned}
Q(\theta,\theta^{\mathrm{old}})
&=\sum_{n,k}\mathbb E[s_{nk}\mid X,\theta^{\mathrm{old}}]
\left[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right]\\
&=\sum_{n,k}\underbrace{r_{nk}^{\mathrm{old}}}_{\text{fixed weights in this M-step}}
\left[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right].
\end{aligned}
$$

Why did the enormous $\sum_Z$ disappear? For any chosen $n,k$, averaging the indicator leaves only its marginal probability:

$$
\begin{aligned}
\sum_Z p(Z\mid X,\theta^{\mathrm{old}})\,\mathbf1\{z_n=k\}
&=p(z_n=k\mid x_n,\theta^{\mathrm{old}})
\prod_{m\ne n}\underbrace{\sum_{z_m=1}^Kp(z_m\mid x_m,\theta^{\mathrm{old}})}_{1}\\
&=r_{nk}^{\mathrm{old}}.
\end{aligned}
$$

This is exactly the bridge from slide 14's general expectation to slide 15's GMM weighted sum. We average over possible hidden assignments—not over a fresh observed dataset, and not by inserting an “average label” into the log-density. Only the random indicators were averaged; the candidate $\pi_k,\mu_k,\Sigma_k$ remain variables to optimize.

### 3.4 General $\arg\max_\theta Q$ → all three GMM update formulas

In general EM, the M-step does not prescribe a particular formula: it says **maximize this $Q$ over this model's parameters**. Here $\theta=(\pi,\mu,\Sigma)$, so we must maximize the GMM $Q$ in those three parameter groups.

Let $N_k=\sum_n r_{nk}^{\mathrm{old}}$. This is an **effective count**, possibly noninteger, and $\sum_kN_k=N$. Start from the **general definition of $Q$**, then substitute the GMM joint model before expanding its Gaussian density:

$$
\begin{aligned}
Q(\theta,\theta^{\mathrm{old}})
&=\mathbb E_{Z\mid X,\theta^{\mathrm{old}}}[\log p(X,Z\mid\theta)]\\
&=\sum_Zp(Z\mid X,\theta^{\mathrm{old}})\log p(X,Z\mid\theta)\\
&=\sum_Zp(Z\mid X,\theta^{\mathrm{old}})
\log\prod_{n=1}^N\prod_{k=1}^K
\left[\pi_k\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right]^{s_{nk}}\\
&=\sum_{n,k}\underbrace{\left[\sum_Zp(Z\mid X,\theta^{\mathrm{old}})s_{nk}\right]}_{\mathbb E[s_{nk}\mid X,\theta^{\mathrm{old}}]=r_{nk}^{\mathrm{old}}}
\left[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right]\\
&=\sum_{n,k}r_{nk}^{\mathrm{old}}
\left[\log\pi_k+\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)\right].
\end{aligned}
$$

The product becomes a sum after taking its logarithm; averaging each indicator $s_{nk}$ produces its old responsibility. Now plug in the **multivariate normal density at the candidate parameters** and take its logarithm explicitly:

$$
\begin{aligned}
\log\mathcal N_D(x_n\mid\mu_k,\Sigma_k)
&=\log\left[
\frac{\exp\!\left(-\frac12(x_n-\mu_k)^\top\Sigma_k^{-1}(x_n-\mu_k)\right)}
{(2\pi)^{D/2}|\Sigma_k|^{1/2}}
\right]\\
&=-\frac D2\log(2\pi)-\frac12\log|\Sigma_k|
-\frac12(x_n-\mu_k)^\top\Sigma_k^{-1}(x_n-\mu_k).
\end{aligned}
$$

Substitute this log-density into the preceding weighted sum, then collect terms using $N_k$:

$$
\begin{aligned}
Q(\theta,\theta^{\mathrm{old}})
&=\sum_{n,k}r_{nk}^{\mathrm{old}}\left[
\log\pi_k-\frac D2\log(2\pi)-\frac12\log|\Sigma_k|
-\frac12(x_n-\mu_k)^\top\Sigma_k^{-1}(x_n-\mu_k)
\right]\\
&=\underbrace{\sum_kN_k\log\pi_k}_{\text{mixing-weight term}}
-\underbrace{\frac12\sum_kN_k\log|\Sigma_k|}_{\text{covariance normalization}}\\
&-\underbrace{\frac12\sum_{n,k}r_{nk}^{\mathrm{old}}
(x_n-\mu_k)^\top\Sigma_k^{-1}(x_n-\mu_k)}_{\text{weighted Gaussian distances}}
-\frac{ND}{2}\log(2\pi).
\end{aligned}
$$

The last line uses $\sum_n r_{nk}^{\mathrm{old}}=N_k$ for terms independent of $n$, and $\sum_{n,k}r_{nk}^{\mathrm{old}}=N$ for the Gaussian constant. The quadratic term keeps both sums because it still depends on each $x_n$ and each component $k$.

Here $|\Sigma_k|$ denotes determinant. **This is the function that the general $\arg\max$ tells us to differentiate.** The $r_{nk}^{\mathrm{old}}$ and $N_k$ are constants throughout this maximization.

#### A. Maximize in $\mu_k$ → the weighted mean on slide 12

Only the quadratic-distance term depends on $\mu_k$. Holding the covariance fixed and using its symmetry,

$$
\begin{aligned}
\nabla_{\mu_k}Q
&=\Sigma_k^{-1}\sum_n r_{nk}^{\mathrm{old}}(x_n-\mu_k)=0\\
&\Longrightarrow\quad
\sum_n r_{nk}^{\mathrm{old}}x_n-\mu_k\sum_n r_{nk}^{\mathrm{old}}=0\\
&\Longrightarrow\quad
\boxed{\mu_k^{\mathrm{new}}=\frac{\sum_n r_{nk}^{\mathrm{old}}x_n}{N_k}}.
\end{aligned}
$$

Because this optimum does not depend on the covariance value, we can plug the new mean into the covariance optimization next.

#### B. Maximize in $\Sigma_k$ → the weighted covariance on slide 12

Define the unnormalized weighted scatter around that **new mean**,

$$
A_k=\sum_n r_{nk}^{\mathrm{old}}
(x_n-\mu_k^{\mathrm{new}})(x_n-\mu_k^{\mathrm{new}})^\top.
$$

For cleaner differentiation, write the precision matrix $\Lambda_k=\Sigma_k^{-1}$. Use $\log|\Sigma_k|=-\log|\Lambda_k|$ and $d^\top\Lambda_k d=\operatorname{tr}(\Lambda_kdd^\top)$. The terms of $Q$ involving this covariance become

$$
Q_k=\frac{N_k}{2}\log|\Lambda_k|
-\frac12\operatorname{tr}(\Lambda_kA_k)+\text{constant}.
$$

Since $\Lambda_k$ and $A_k$ are symmetric, $\nabla_{\Lambda_k}\log|\Lambda_k|=\Lambda_k^{-1}$ and $\nabla_{\Lambda_k}\operatorname{tr}(\Lambda_kA_k)=A_k$. Therefore

$$
\begin{aligned}
\nabla_{\Lambda_k}Q_k=\frac{N_k}{2}\Lambda_k^{-1}-\frac12A_k=0
&\Longrightarrow N_k\Sigma_k^{\mathrm{new}}=A_k\\
&\Longrightarrow\boxed{\Sigma_k^{\mathrm{new}}=\frac{A_k}{N_k}}.
\end{aligned}
$$

This is a maximum when $N_k>0$ and $A_k$ is positive definite: the precision objective is concave (strictly so for positive $N_k$). The result is maximum-likelihood covariance, so divide by $N_k$, **not** $N_k-1$.

#### C. Maximize in $\pi_k$ → the mixture proportions on slide 12

The weight term is $\sum_kN_k\log\pi_k$, with $\sum_k\pi_k=1$. Introduce a Lagrange multiplier:

$$
\begin{aligned}
\mathcal J(\pi,\lambda)&=\sum_kN_k\log\pi_k+\lambda\left(\sum_k\pi_k-1\right),\\
\frac{\partial\mathcal J}{\partial\pi_k}=\frac{N_k}{\pi_k}+\lambda=0
&\Longrightarrow\pi_k=-\frac{N_k}{\lambda},\\
1=\sum_k\pi_k=-\frac{\sum_kN_k}{\lambda}=-\frac{N}{\lambda}
&\Longrightarrow\lambda=-N
\quad\Longrightarrow\quad\boxed{\pi_k^{\mathrm{new}}=\frac{N_k}{N}}.
\end{aligned}
$$

So the single general instruction $\theta^{\mathrm{new}}=\arg\max_\theta Q$ produces **exactly the three familiar GMM M-step formulas**, collected here:

$$
\boxed{
\pi_k^{\mathrm{new}}=\frac{N_k}{N},\qquad
\mu_k^{\mathrm{new}}=\frac{1}{N_k}\sum_{n=1}^N r_{nk}^{\mathrm{old}}x_n
}
$$

$$
\boxed{
\Sigma_k^{\mathrm{new}}
=\frac{1}{N_k}\sum_{n=1}^N r_{nk}^{\mathrm{old}}
(x_n-\mu_k^{\mathrm{new}})(x_n-\mu_k^{\mathrm{new}})^\top
}
$$

These are, respectively, **fraction of effective membership**, **weighted mean**, and **weighted covariance**. The covariance uses the **new mean**, but the **old responsibilities**, and its maximum-likelihood denominator is $N_k$, not $N_k-1$. The outer product is $D\times D$, as a covariance matrix must be. [Lecture 7, slides 9–12, 15.]

### 3.5 General replacement $\theta^{\mathrm{old}}\leftarrow\theta^{\mathrm{new}}$ → repeat GMM E/M

Replace **all three** parameter groups by their new values. The next E-step uses the new weights, means and covariances to recompute responsibilities. That is the “repeat” instruction on slide 12.

**Why the earlier GMM differentiation did not give a one-shot answer:** on slides 9–11, differentiating the observed log-likelihood produces stationary equations involving $r_{nk}(\theta)$, which itself depends on the unknown parameters. General EM explains the workable iteration: evaluate those probabilities at $\theta^{\mathrm{old}}$, **freeze** them, and solve the explicit $Q$ maximization above. Do not differentiate through $r_{nk}^{\mathrm{old}}$ in the M-step. These are closed-form conditional updates, not a closed-form global GMM MLE.

## 4. Why maximizing $Q$ helps the actual likelihood

For a fixed distribution $q$ over the latent variables, define

$$
\mathcal F(q,\theta)
=\mathbb E_q[\log p(X,Z\mid\theta)]+H(q)
=\ell(\theta)-\operatorname{KL}\!\left(q\,\|\,p(Z\mid X,\theta)\right).
$$

The exact E-step sets $q^{\mathrm{old}}=p(Z\mid X,\theta^{\mathrm{old}})$, so the bound touches $\ell$ at the old parameters. During the M-step, $H(q^{\mathrm{old}})$ is constant; maximizing the bound in $\theta$ is therefore exactly maximizing $Q$. Thus, when these quantities are finite and the M-step succeeds,

$$
\ell(\theta^{\mathrm{new}})
\ \geq\ \mathcal F(q^{\mathrm{old}},\theta^{\mathrm{new}})
\ \geq\ \mathcal F(q^{\mathrm{old}},\theta^{\mathrm{old}})
\ =\ \ell(\theta^{\mathrm{old}}).
$$

This is the same evidence/ELBO/posterior-KL decomposition in [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|my four ELBO approaches]], now used as an optimization algorithm. [Lecture 7, slides 18–19.]

> [!warning] What this does not guarantee
> A nondecreasing likelihood is not a global-optimum guarantee. Initialization matters, identical components can remain identical, and unconstrained GMM likelihood can become unbounded when a component collapses onto an observation. The explorer uses ordinary full-covariance EM; near-empty or nearly singular components trigger a warning and stop, rather than silently adding regularization. A small likelihood increment is only its stopping criterion.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/Gaussian mixture models|Gaussian mixture models]] — Supplies the concrete joint model whose posterior and weighted Gaussian fits instantiate the general E- and M-steps.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]] — The same posterior-KL identity explains why exact E tightens the bound and M can maximize $Q$ instead of the observed log-likelihood directly.

## Origin

> [!info]- Source details
> **Source:** Thibault Randrianarisoa, University of Toronto, *EM algorithm*, Winter 2026, dated February 25, 2026; user-supplied `PML_Lec07.pdf`, 20 pages. Focused coverage: model/posterior and likelihood in slides 2, 5–6, 8–12; iteration picture in 13; general EM/GMM mapping in 14–15; bound interpretation in 18–19. Slide 1 establishes attribution. This is not a full lecture digest; the crab/three-component examples and K-means limiting argument are outside the note's scope.
>
> **User contribution:** the requested side-by-side general/GMM correspondence table, the embedded two-component simulation, and the clarification that every general letter/equation/operation should be traced to its GMM derivation. The opening question is a labeled paraphrase, not a verbatim quotation. The exposition, latent-shape clarification, objective distinction, expanded mean/precision/weight derivations, and simulation are assistant-added synthesis checked against the cited slides and equations; the expanded matrix calculus is not presented as verbatim slide content.
>
> **Follow-up, 2026-11-15:** the user asked why $Q$ is defined this way and what its GMM form looks like, then requested the answer inside the selected §3.3 callout. The expanded callout is assistant-added explanation from that exchange: expected complete-data fitting, fixed old responsibilities versus candidate parameters, the Gaussian expansion, and Jensen's tight-bound rationale. The user's nearby $(0.8,0.2)$ example is retained with a mathematical correction: component-specific candidate means/covariances and the entire weighted joint density inside each logarithm, rather than old Gaussian parameters. The indicator/probability distinction is clarified. A subsequent request expands the selected §3.4 equation from the general definition, through the indicator-form joint and posterior expectation, to the explicit normal log-density and collected terms; those intermediate steps are assistant-added derivation. This adds no new lecture-page coverage or source files.
>
> **Equality clarification, 2026-11-15:** at the user's request, the §3.3 callout now includes an assistant-derived equality chain using a constant likelihood ratio and normalized posterior weights, explaining why the old-parameter bound is exact while the general candidate-parameter step is an inequality.
>
> **Evidence and privacy:** the supplied screenshot is preserved byte-for-byte; the second image is a complete slide-13 render. The original PDF is preserved byte-for-byte under `raw/notes/private-course-slides/` and Git-ignored. At the user's request on 2026-11-15, the opening now includes a clickable Lecture notes link and a collapsed local PDF embed. Screenshots, this note and generated explorer assets are not excluded by that PDF-only rule. Any public export must omit the original PDF, remove its embed, and replace its private link/source entry with plain lecture attribution; no publication occurred in this task.
>
> **Reproducibility and checks:** [[assets/figures/2026-11-13-em-gmm/build.py|generator]], [[assets/figures/2026-11-13-em-gmm/math.js|model equations]], [[assets/figures/2026-11-13-em-gmm/verify_math.py|independent verification]], [[assets/figures/2026-11-13-em-gmm/math-checks.json|numerical results]]. Analytic indicator/expectation and ELBO reasoning; independent SciPy/NumPy responsibilities, weighted moments and likelihood checks; exhaustive eight-assignment comparison of general $Q$ with the GMM sum; 36 initialization configurations × 60 iterations and contour checks. Numerical checks support, rather than replace, the derivation. Detailed coverage, hashes and rendering limits are in the existing checkpoint/log records.
