---
id: transforms-convolution-of-independent-sums
title: Convolution of independent sums
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Transforming random variables → Convolution of independent sums
created: '2026-11-08'
updated: '2026-11-15'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Transforming random variables]]'
sources:
- '[[_system/Sources/prob]]'
- '[[_system/Sources/process]]'
- '[[raw/assets/2026-11-15-convolution-uniform-handwriting.png]]'
---

# Convolution of independent sums

Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Transforming random variables → Convolution of independent sums

Parent: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Transforming random variables|Transforming random variables]]

## 1. See it and use it — the sum of two dice

Roll two fair, independent six-sided dice. Why is a sum of 7 more likely than a sum of 2? There are six pairs that make 7, but only $(1,1)$ makes 2. Each ordered pair has probability $1/36$.

![[assets/figures/2026-11-15-convolution/01-dice.svg]]

*Original illustration: each square is one outcome pair; each bar collects pairs with the same sum.*

**Convolution combines two functions by multiplying values at complementary positions and adding the products.** For independent random variables, convolving their probability distributions gives the distribution of their sum. The inputs describe each die separately; the output describes the total. [Pishro-Nik, §6.1.2](https://www.probabilitycourse.com/chapter6/6_1_2_sums_random_variables.php).

To find the chance of a total of 7, pair each first-die value with the required second-die value:

$$
P(U+V=7)=\underbrace{\frac16\frac16+\cdots+\frac16\frac16}_{6\text{ pairs}}=\frac16.
$$

The reusable idea is **multiply within each compatible pair; add across all compatible pairs**. With biased dice, keep the same procedure and use their actual probabilities. Independence is what permits multiplying the two separate probabilities.

## 2. How it works — the formula and your uniform example

### From compatible pairs to a convolution

Let $T=U+V$, with $U$ and $V$ independent. A [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Random variables & distribution functions/CDF, PMF and density|probability mass function]] gives the probability of an individual discrete value. For integer-valued variables, write $p_U(k)=P(U=k)$ and set it to zero outside the possible values. Then

$$
\begin{aligned}
p_T(t)
&=\sum_{k\in\mathbb Z}P(U=k,V=t-k)\\
&=\sum_{k\in\mathbb Z}p_U(k)p_V(t-k)
=(p_U*p_V)(t).
\end{aligned}
$$

Fix the desired total $t$. Once $U=k$ is chosen, **$V$ must equal $t-k$**. These cases cannot happen together, so their probabilities add. Independence gives the product on the second line. [Taboga, “Probability mass function of a sum”](https://www.statlect.com/fundamentals-of-probability/sums-of-independent-random-variables).

For continuous variables with densities $f_U$ and $f_V$, the corresponding result is

$$
\boxed{f_T(t)=(f_U*f_V)(t)
=\int_{-\infty}^{\infty}f_U(\tau)f_V(t-\tau)\,d\tau.}
$$

Here $t$ is the fixed output location and $\tau$ runs through candidate values of $U$. The integral adds **density contributions**; a density at one point is not a point probability. The convolution integral defines a density almost everywhere; all the bounded, finite-support functions in the worked example below have a finite integral at every $t$. [Pishro-Nik, §6.1.2, final convolution formula](https://www.probabilitycourse.com/chapter6/6_1_2_sums_random_variables.php).

One way to see where the integral comes from is to condition on the first value:

$$
F_T(t)=P(U+V\le t)
=\int_{-\infty}^{\infty} f_U(\tau)F_V(t-\tau)\,d\tau.
$$

Independence lets us use the ordinary CDF $F_V$ inside the integral. Differentiating with respect to $t$ gives the density formula; for this uniform example the integrands are bounded and supported on a finite interval, which justifies the step. [Taboga, “Probability density function of a sum”](https://www.statlect.com/fundamentals-of-probability/sums-of-independent-random-variables).

### Why one function is flipped and shifted

Look at $f_V(t-\tau)$ **as a function of $\tau$**, keeping $t$ fixed:

$$
\underbrace{f_V(\tau)}_{\text{original}}
\quad\longrightarrow\quad
\underbrace{f_V(-\tau)}_{\text{reflect horizontally}}
\quad\longrightarrow\quad
\underbrace{f_V(-(\tau-t))}_{\text{shift by }t}
=f_V(t-\tau).
$$

Then multiply the two heights at each $\tau$ and integrate the product. Increasing $t$ slides the reflected function horizontally to the right. **“Flip” means reversing the input axis; it does not mean finding an inverse function $f_V^{-1}$ or taking $1/f_V$.**

![[assets/figures/2026-11-15-convolution/03-uniform-slide.gif]]

*Original animation for your example. Blue stays fixed; orange is reflected and slides. The middle panel shows their product; its green area becomes one point on the bottom density. The upper axes use $\tau$; the bottom axis uses $t$. [[assets/figures/2026-11-15-convolution/02-uniform-keyframes.svg|Static keyframes]] appear below.*

### Your practice — $U\sim\operatorname{Unif}[0,2]$ and $V\sim\operatorname{Unif}[0,3]$

Find the density of $T=U+V$, **assuming $U$ and $V$ are independent**. Your handwriting obtains the correct three pieces and trapezoidal graph. The explanation below makes the overlap limits explicit.

![[raw/assets/2026-11-15-convolution-uniform-handwriting.png|450]]

*Your original handwritten solution, preserved in its supplied orientation. The independence assumption is added explicitly here.*

**1. Write the two densities.** A [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Uniform|uniform density]] is constant over its interval, with height chosen so the total area is 1:

$$
f_U(\tau)=\frac12\mathbf1_{[0,2]}(\tau),
\qquad
f_V(v)=\frac13\mathbf1_{[0,3]}(v),
$$

where $\mathbf1_A$ is 1 inside the set $A$ and 0 outside.

**2. Find where both factors are nonzero.** The first requires $0\le\tau\le2$. The second requires

$$
0\le t-\tau\le3
\quad\Longleftrightarrow\quad
t-3\le\tau\le t.
$$

So the integration interval is the intersection

$$
[0,2]\cap[t-3,t]
=\bigl[\max(0,t-3),\,\min(2,t)\bigr]
$$

when the left endpoint does not exceed the right. On that overlap, the product has constant height $(1/2)(1/3)=1/6$. Thus

$$
\boxed{f_T(t)=\frac16\max\!\left(0,\min(2,t)-\max(0,t-3)\right).}
$$

**Density = product height × overlap length.** The outer maximum makes the answer zero when the two intervals do not overlap.

### The three overlap cases

![[assets/figures/2026-11-15-convolution/02-uniform-keyframes.svg]]

*Original analytic keyframes. At $t=1,2.5,4$, the overlap lengths are $1,2,1$, giving densities $1/6,1/3,1/6$. In the top panels, the green strip marks the interval of integration.*

**3. Evaluate the integral in each region.**

| Possible total $t$ | Overlap in $\tau$ | Integral | Density |
| --- | --- | --- | --- |
| $0\le t<2$ | $[0,t]$ | $\int_0^t\frac16\,d\tau$ | $t/6$ |
| $2\le t\le3$ | $[0,2]$ | $\int_0^2\frac16\,d\tau$ | $1/3$ |
| $3<t\le5$ | $[t-3,2]$ | $\int_{t-3}^2\frac16\,d\tau$ | $(5-t)/6$ |
| $t<0$ or $t>5$ | Empty | $0$ | $0$ |

The plateau occurs because the wider sliding interval still covers all of $[0,2]$. It starts at $t=2$ and ends when the sliding interval's left edge reaches 0, at $t=3$. The last line of your calculation simplifies correctly:

$$
\left[\frac{\tau}{6}\right]_{t-3}^{2}
=\frac26-\frac{t-3}{6}=\frac{5-t}{6}.
$$

**4. Check the answer.** Its support is $[0,5]$, it is nonnegative, the pieces meet at height $1/3$, and its area is

$$
\underbrace{\frac12\cdot2\cdot\frac13}_{\text{left triangle}}
+\underbrace{1\cdot\frac13}_{\text{rectangle}}
+\underbrace{\frac12\cdot2\cdot\frac13}_{\text{right triangle}}=1.
$$

This also explains the connection to the dice: equal-width boxes produce a triangle; unequal widths here leave a flat middle. Independence matters: if instead $V=\tfrac32U$, both stated uniform marginals still hold, but $U+V=\tfrac52U$ is uniform on $[0,5]$, not trapezoidal.

## 3. Deeper connections — kernels, CNNs, and EEG averages

### A kernel is a reusable set of local weights

For a sampled signal $x[n]$, let $n$ be an integer sample index and let $h[k]$ specify the weight at lag $k$. Discrete convolution is

$$
y[n]=(x*h)[n]
=\sum_{k\in\mathbb Z}h[k]x[n-k]
=\sum_{m\in\mathbb Z}x[m]h[n-m].
$$

The last equality just substitutes $m=n-k$. It exposes the same flip-and-slide pattern as the probability formula. For the finite kernels below, each sum has finitely many nonzero terms. At each output location, multiply aligned entries and add; then move to the next location. [Dive into Deep Learning, §7.2.1 and §7.2.5](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html).

| Setting | What the two inputs mean | What the output means |
| --- | --- | --- |
| Independent sum | Two probability mass functions or densities | Distribution of the sum |
| Signal filter | Signal values and fixed kernel weights | Filtered signal values |
| CNN layer | Input features and learned kernel weights | A new feature map |

The algebra is shared. A signal or CNN kernel can have negative entries and need not sum to 1; it is generally not a probability distribution.

### CNNs — learn the weights, reuse them across locations

In a [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Convolutional networks overview|convolutional neural network]], training learns local weights and the same weights are applied across positions. One one-dimensional, single-channel operation, with stride 1, no padding, no dilation, and zero bias, is

$$
r[n]=\sum_{k=0}^{M-1}w[k]x[n+k].
$$

This is **cross-correlation**: weights stay in their stored order as the window slides. PyTorch's `Conv1d` uses this convention. Mathematical convolution reverses that order on the same input patch. [PyTorch, `Conv1d` operator definition](https://docs.pytorch.org/docs/2.15/generated/torch.nn.Conv1d.html).

![[assets/figures/2026-11-15-convolution/04-kernel-products.svg]]

*Original arithmetic example: the input patch is $[2,4,8]$ and the stored weights are $[1,2,3]$. Cross-correlation gives $34$; convolution gives $22$. Here $r[0]$ anchors the patch at its first sample and $y[2]$ at its last, so the figure explicitly compares the same physical patch.*

Moving to the next patch $[4,8,10]$ gives $4\cdot1+8\cdot2+10\cdot3=50$ for cross-correlation. This is the repeated multiply–add operation you described. In two dimensions, slide over image patches; strict convolution reverses both kernel axes, equivalent to a 180° rotation. With freely learned weights, reversing the parameter array can represent the same family of operations, which is why CNN terminology commonly calls both “convolution.” [Dive into Deep Learning, §7.2.5](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html#cross-correlation-and-convolution).

### EEG — a finite constant kernel gives a running average

Your suggested example works: take **one EEG channel sampled at equally spaced times**, with amplitude $x[n]$ in microvolts. An $M$-sample trailing average uses a *boxcar kernel*: constant on a finite window and zero elsewhere,

$$
h[k]=
\begin{cases}
1/M,&k=0,1,\ldots,M-1,\\
0,&\text{otherwise}.
\end{cases}
\qquad
y[n]=\frac1M\sum_{k=0}^{M-1}x[n-k].
$$

The factor $1/M$ makes this an average; weights of 1 would give a running sum. This is an average **across time within one channel**. Averaging electrodes at one instant is a different operation. The finite boxcar interpretation is standard; the trailing time convention here uses current and past samples. [Smith, *The Scientist and Engineer's Guide to DSP*, Ch. 15, pp. 277–278](https://www.dspguide.com/CH15.PDF#page=1).

For $M=3$ and the invented first five samples $(x[0],\ldots,x[4])=(2,4,8,10,6)$:

$$
y[2]=\frac{8+4+2}{3}=\frac{14}{3},\qquad
y[3]=\frac{10+8+4}{3}=\frac{22}{3},\qquad
y[4]=\frac{6+10+8}{3}=8\quad(\mu\mathrm V).
$$

![[assets/figures/2026-11-15-convolution/05-moving-average.svg]]

*Original constructed signal, not recorded EEG. The first output uses samples 0, 1, and 2 and is plotted at sample 2. The equal weights soften rapid changes and introduce temporal lag.*

Because the finite coefficient list $[1/M,\ldots,1/M]$ is symmetric, reversing it does not change the average over a given patch. **The time anchor still matters:** a trailing average is available immediately; a centered average requires future samples. For $M=3$, centering uses $(x[n-1]+x[n]+x[n+1])/3$. Here we show only complete windows, beginning at $n=M-1$; zero padding or averaging fewer initial samples would change the boundary outputs.

Adjacent windows share almost all their samples, so the same convolution can be updated efficiently:

$$
y[n]=y[n-1]+\frac{x[n]-x[n-M]}{M},\qquad n\ge M,
$$

after computing the first complete window. Add the incoming sample's contribution and remove the outgoing one's.

A boxcar is a simple smoothing example. It can also attenuate EEG oscillations of interest and has weak frequency selectivity, so smoothness alone does not establish that useful signal has been preserved. The window length is part of the filter, not just a plotting choice. [Smith, Ch. 15, pp. 279–280, Fig. 15-1 and “Frequency Response”](https://www.dspguide.com/CH15.PDF#page=3).

## Origin

> [!info]- Source details
> Enriched at the user's request on 2026-11-15: two-dice intuition, the convolution formula and the supplied uniform-sum practice, then CNNs and an EEG running-average example. The three integral regions, final falling expression, and trapezoid come from the user's handwriting. The explicit independence assumption, general derivation, overlap notation, numerical kernel examples and application explanations are Codex additions.
>
> Original: [[raw/assets/2026-11-15-convolution-uniform-handwriting.png|one handwritten image]], copied byte-for-byte from `codex-clipboard-99ae47fa-600f-4d34-9768-0aa4a3e12b99.png`; no original exercise sheet or source date was supplied. The drawing's informal labels are replaced in the explanation by the unambiguous $f_V(t-\tau)$; the original is unchanged.
>
> References were read at the linked sections: Pishro-Nik §6.1.2, Taboga's PMF/PDF propositions, *Dive into Deep Learning* §7.2.1/§7.2.5, PyTorch `Conv1d`, and Smith Ch. 15 pp. 277–280. New graphics are original illustrations matched to these examples; no external figure is reproduced.
>
> [[assets/figures/2026-11-15-convolution/generate.py|Reproducible figures]] and [[assets/figures/2026-11-15-convolution/checks.json|mathematical checks]] include exact dice enumeration, uniform density normalization/continuity/moments, independent quadrature, kernel orientation, and moving-average arithmetic. Static previews and decoded animation frames are inspected separately from live Obsidian rendering.

```atlas
```
