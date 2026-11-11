---
id: learning-categorical-association-cramers-v
title: Categorical association and Cramér's V
layer: learning
primary_home: '[[Backbone/Statistical inference & modeling/Regression & linear models/Generalized linear models/Binary, count & categorical responses/Contingency tables]]'
subject: statistics
backbone_path: Statistical inference & modeling → Regression & linear models → Generalized linear models → Binary, count & categorical responses → Contingency tables
study_band: U
note_types: [topic-note, insight]
source_format: agent-synthesis
created: '2026-11-11'
updated: '2026-11-11'
status: active
verification: needs-review
learning_state: unknown
aliases: [Cramér's V, Cramers V, Cramer's V, Chi-square test of independence, Phi coefficient]
tags: [atlas/learning, subject/statistics, topic/categorical-association]
connections:
  - '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Classical comparisons/Chi-square goodness of fit]]'
  - '[[Backbone/Statistical inference & modeling/Applied statistics & evidence/Biostatistics & evidence synthesis/Epidemiology & trials/Risk ratio and odds ratio]]'
  - '[[Backbone/Statistical inference & modeling/Nonparametric & robust inference/Nonparametric inference/Ranks & distribution-free procedures/Rank correlations]]'
  - '[[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation]]'
  - '[[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly]]'
sources:
  - 'https://online.stat.psu.edu/stat504/Lesson03'
  - 'https://online.stat.psu.edu/stat500/Lesson08'
  - '[[assets/figures/2026-11-11-cramers-v/draw_cramers_v.py]]'
  - '[[assets/figures/2026-11-11-cramers-v/checks.json]]'
  - '[[assets/figures/2026-11-11-cramers-v/01-three-tables.svg]]'
  - '[[assets/figures/2026-11-11-cramers-v/02-same-strength-more-data.svg]]'
---

# Categorical association and Cramér's V

Statistical inference & modeling → Regression & linear models → Generalized linear models → Binary, count & categorical responses → Contingency tables

**A chi-square test asks *is there any association?* Cramér's V asks *how strong is it?* V rescales Pearson's $\chi^2$ so that the sample size and the table's size drop out. What is left lies between 0 (the table looks exactly independent) and 1 (one variable completely determines the other).**

$$
V=\sqrt{\frac{\chi^2/n}{\min(r-1,\;c-1)}}
$$

Here $r$ and $c$ are the numbers of rows and columns, and $n$ is the total count.

## 1. What association means when there are no numbers

Take two **categorical** variables: $X$ with $r$ categories (housing: Apartment, House) and $Y$ with $c$ categories (preferred pet: Cat, Dog). Cross-classifying $n$ households gives an $r\times c$ **contingency table** of counts $n_{ij}$, with row totals $n_{i+}$ and column totals $n_{+j}$.

- **Independence:** $P(X=i,\,Y=j)=P(X=i)\,P(Y=j)$ for every cell. Equivalently, every row has the same **profile**, the same conditional distribution of $Y$. Apartments and houses have the same cat-versus-dog mix.
- **Association:** the row profiles differ, so knowing the row changes your prediction of the column.

"Cat" and "Dog" have no order, mean or slope, so Pearson's $r$ has nothing to work with. An association measure for categories has to be built from the counts themselves.

## 2. Three steps from a table to V

Running toy example, **Table B** (invented counts, $n=100$):

| | Cat | Dog | Row total |
| --- | ---: | ---: | ---: |
| Apartment | 35 | 15 | 50 |
| House | 15 | 35 | 50 |
| Column total | 50 | 50 | 100 |

**Step 1: what independence predicts.** If the rows had identical profiles, each cell would get its row's share of its column:

$$
E_{ij}=\frac{n_{i+}\,n_{+j}}{n},\qquad\text{here } E_{ij}=\frac{50\cdot 50}{100}=25\text{ in every cell.}
$$

**Step 2: how far the table is from that.** Pearson's statistic adds up the squared gaps, each scaled by its expected count:

$$
\chi^2=\sum_{i,j}\frac{(O_{ij}-E_{ij})^2}{E_{ij}}=4\times\frac{(\pm10)^2}{25}=16.
$$

Under independence, $\chi^2$ is approximately chi-square with $(r-1)(c-1)$ degrees of freedom ([STAT 504 §3.3](https://online.stat.psu.edu/stat504/Lesson03)). Like [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget#7. Where Wald and asymptotic tests enter the framework|Wald's χ²]], it is a squared length of standardized gaps. Here df $=1$ and $p=P(\chi^2_1\ge16)\approx6.3\times10^{-5}$. The degrees of freedom come from counting: there are $rc$ cells, minus 1 because $n$ is fixed, minus the $(r-1)+(c-1)$ margins that were estimated to build $E$. Each constraint removes one dimension, as with [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic#1. Split the sample into one mean direction and n − 1 residual directions|n − 1 residual directions]]. The approximation needs reasonably large expected counts; Penn State's working rule is that at least 80% of cells should have $E_{ij}\ge5$ ([STAT 500 Lesson 8](https://online.stat.psu.edu/stat500/Lesson08)).

**Step 3: turn the distance into a strength.** $\chi^2$ is a poor strength scale for two reasons:

1. **It grows with $n$.** Double every count and $\chi^2$ doubles, though the pattern is unchanged. So divide by $n$.
2. **Its ceiling depends on the table's shape.** $\chi^2/n$ can reach $\min(r-1,c-1)$ (proof below). So divide by that.

For Table B, $V=\sqrt{16/(100\cdot1)}=0.40$.

![[assets/figures/2026-11-11-cramers-v/01-three-tables.svg]]

*Original illustration with invented counts. All three tables have the same row and column totals, so independence predicts 25 per cell. Each housing row is split left/right by its cat share, so tile area is proportional to count. The dashed line is where every row would split under independence. Teal means more households than independence predicts and orange means fewer. The bar shows V on its 0–1 scale.*

How to read it:

- **A, V = 0.** Both rows split exactly at the dashed line: apartments and houses have the same pet mix. Knowing the housing type tells you nothing about the pet.
- **B, V = 0.40.** Apartments split at 70% cats and houses at 30%. The rows disagree, but not completely.
- **C, V = 1.** Every apartment has a cat and every house a dog. Knowing either variable tells you the other exactly.

> [!info]- Why $\chi^2/n$ can never exceed $\min(r-1,\,c-1)$
> Expand the square and use $\sum O_{ij}=\sum E_{ij}=n$:
> $$\chi^2=\sum\frac{O_{ij}^2}{E_{ij}}-n=n\Big(\sum_{i,j}\frac{n_{ij}^2}{n_{i+}\,n_{+j}}-1\Big).$$
> Each term is $\frac{n_{ij}}{n_{i+}}\cdot\frac{n_{ij}}{n_{+j}}\le\frac{n_{ij}}{n_{i+}}$, because a cell cannot exceed its column total. Summing over $j$ gives 1 for each row, so the double sum is at most $r$ and $\chi^2/n\le r-1$. The same argument with rows and columns swapped gives $\chi^2/n\le c-1$.
>
> Equality in the row bound needs $n_{ij}=n_{+j}$ wherever $n_{ij}>0$: each column's households all sit in one row. So **V = 1 exactly when the variable with more categories determines the other**. For a square table that means a one-to-one match. **V = 0 exactly when every $O_{ij}=E_{ij}$**, which means the *sample* table is perfectly independent. (Assumes every row and column total is positive.)

## 3. Toy example: same strength, more data

Scale Table B up and down without changing its proportions:

| Table | Counts (Apt Cat, Dog / House Cat, Dog) | $\chi^2$ | p-value | V |
| --- | --- | ---: | ---: | ---: |
| $n=20$ | 7, 3 / 3, 7 | 3.2 | 0.074 | 0.40 |
| $n=100$ | 35, 15 / 15, 35 | 16 | $6.3\times10^{-5}$ | 0.40 |
| $n=1000$ | 350, 150 / 150, 350 | 160 | $1.1\times10^{-36}$ | 0.40 |

![[assets/figures/2026-11-11-cramers-v/02-same-strength-more-data.svg]]

*Original illustration. The curves hold the cell proportions at 0.35, 0.15 / 0.15, 0.35 and let $n$ vary; the dots are the three integer tables above. Uncorrected Pearson $\chi^2$ with df = 1.*

The association is equally strong in all three tables. Only the evidence that it is not chance changes: at $n=20$ the test cannot rule out noise, and at $n=1000$ it is overwhelming. **The p-value answers "could this be noise?", and V answers "how big is it?"** Report both. At $n=20$ every expected count is exactly 5, the edge of the approximation; Fisher's exact test is the usual small-table alternative.

## 4. Toy example: why divide by $\min(r-1,\,c-1)$

A 3×3 table of 90 students, with Major (Stats, Biology, Art) by usual study spot (Library, Café, Home). Every row and column totals 30, so $E_{ij}=10$:

| | Library | Café | Home |
| --- | ---: | ---: | ---: |
| Stats | 18 | 6 | 6 |
| Biology | 9 | 15 | 6 |
| Art | 3 | 9 | 18 |

$$
\chi^2=\frac{8^2+4^2+4^2+1^2+5^2+4^2+7^2+1^2+8^2}{10}=25.2,\quad \text{df}=4,\quad p\approx4.6\times10^{-5}.
$$

**Why divide by 10:** every term is $(O-E)^2/E$, and every $E_{ij}=30\cdot30/90=10$, so the 10 factors out, as in the [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F#1. See it and use it — chi-square|dice χ²]].
**Why df = 4, not 9 − 1 = 8:** "cells − 1" holds only when no probabilities are fitted, as in the [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F#2.2 Why the dice statistic has five degrees of freedom|dice df]].
Here E is built from the row and column totals, so the gaps $O-E$ sum to zero along every row and column. That gives 5 independent constraints and leaves $9-5=4=(3-1)(3-1)$ free gaps.

Without the size correction, $\sqrt{\chi^2/n}=0.53$; with it, $V=\sqrt{25.2/(90\cdot2)}=0.37$. The correction matters most at the extreme. If each major used only its own spot (diagonal 30, 30, 30), then $\chi^2=180$ and $\sqrt{\chi^2/n}=\sqrt2\approx1.41$, above 1, while $V=1$. Dividing by $\min(r-1,c-1)$ gives every table shape the same ceiling of 1.

**V hides the pattern.** The $O-E$ table (Stats +8 at Library, Biology +5 at Café, Art +8 at Home) shows *where* the association lives. An $r\times c$ table can depart from independence in $(r-1)(c-1)$ separate directions ([STAT 504 §3.8](https://online.stat.psu.edu/stat504/Lesson03)), and V compresses them all into one number. Look at the residuals, $(O-E)/\sqrt E$, to see the pattern.

## 5. The 2×2 special case: V = |φ|

Label a 2×2 table $\begin{smallmatrix}a&b\\c&d\end{smallmatrix}$. Then

$$
\phi=\frac{ad-bc}{\sqrt{(a+b)(c+d)(a+c)(b+d)}},\qquad \chi^2=n\phi^2,\qquad V=|\phi|.
$$

For Table B, $\phi=(35\cdot35-15\cdot15)/\sqrt{50^4}=1000/2500=0.40$. Code Apartment = 1, House = 0 and Cat = 1, Dog = 0, and $\phi$ is exactly [[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation#6. The sphere–plane intersection and Pearson correlation|Pearson's correlation]] between the two 0/1 columns. Its sign depends only on how you coded the categories: swap Cat and Dog and $\phi$ becomes $-0.40$. V drops that arbitrary sign. Some software (SAS `PROC FREQ`, as in the STAT 504 §3.3 output) reports the signed value as "Cramér's V" for 2×2 tables.

## 6. What V does not tell you

- **Direction and order.** Shuffling the rows or columns leaves V unchanged. That suits nominal categories, but for ordered ones (low/medium/high) V ignores the order that rank-based measures such as [[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly#Definition and interpretation|concordance]] use.
- **Which variable predicts which.** V is symmetric: $V(X,Y)=V(Y,X)$.
- **Independence of the sampling design.** V depends on the margins. Survey four times as many houses (Table B's House row becomes 60, 140): the odds ratio stays $35\cdot140/(15\cdot60)=5.44$, but V falls from 0.40 to 0.33.
- **Zero under independence in small samples.** Noise alone makes V positive. With truly independent 2×2 data, simulated V averaged 0.18 at $n=20$, 0.08 at $n=100$ and 0.025 at $n=1000$. A bias-corrected version exists (Bergsma, 2013).
- **Which χ² it uses.** V uses the uncorrected Pearson $\chi^2$. R's `chisq.test` and SciPy's `chi2_contingency` apply Yates' continuity correction to 2×2 tables by default, which shrinks $\chi^2$.
- **The 0–1 range depends on Pearson's χ².** Use the likelihood-ratio $G^2$ instead and the bound fails: Table C gives $\sqrt{G^2/n}=\sqrt{2\ln2}\approx1.18$.
- **What counts as "large".** That depends on the field. Cohen's conventions of 0.1, 0.3 and 0.5 for $w=\sqrt{\chi^2/n}$ (equal to V for 2×2) are rough rules of thumb, not laws.
- **Causation.** Like any association, a large V can come from confounding.

## 7. Self-check prompts

*These prompts were written for you, not taken from a source.*

> [!question]- Multiply every count in Table C by 3. What happens to $\chi^2$ and V?
> $\chi^2$ triples from 100 to 300, and V stays at 1. The proportions, which are all V sees, did not change.

> [!question]- A 2×5 table has $\chi^2=12$ with $n=200$. What is V?
> $\min(r-1,c-1)=\min(1,4)=1$, so $V=\sqrt{12/200}\approx0.24$.

> [!question]- Swap the Cat and Dog columns of Table B. What changes?
> $\phi$ flips from $+0.40$ to $-0.40$. $\chi^2=16$ and $V=0.40$ do not change.

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Classical comparisons/Chi-square goodness of fit|Chi-square goodness of fit]] — The independence test is Pearson's goodness-of-fit statistic with expected counts estimated from the margins, which is why its df is (r−1)(c−1); V rescales that same statistic.
- [[Backbone/Statistical inference & modeling/Applied statistics & evidence/Biostatistics & evidence synthesis/Epidemiology & trials/Risk ratio and odds ratio|Risk ratio and odds ratio]] — For 2×2 tables the odds ratio is a signed alternative that does not depend on the margins; oversampling one row leaves it at 5.44 while V falls from 0.40 to 0.33.
- [[Backbone/Statistical inference & modeling/Nonparametric & robust inference/Nonparametric inference/Ranks & distribution-free procedures/Rank correlations|Rank correlations]] — V ignores category order; for ordered categories, rank-based measures use the order that V throws away.
- [[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation|Standardization geometry - means, lengths, and correlation]] — For a 2×2 table, V = |φ| is the absolute Pearson correlation of the two 0/1 indicator columns: the |cosine| between their centered vectors.

- [[Learning/Statistical computing & learning/Statistical learning & prediction/Concordance and C-statistics - ranking pairs correctly|Concordance and C-statistics - ranking pairs correctly]] — V ignores category order, whereas concordance evaluates whether a specified score direction correctly orders outcomes.

## Origin

> [!info]- Source details
> No study material was supplied. The user asked on 2026-11-11 in a Claudian chat: "now I want to study /digest categorial association and cramer's V. i don't have materials yet, just set up a new learning node, with some basic information and basic visual and toy examples to help me understand".
>
> Everything here was written by Claude: the explanation, the invented toy tables, both figures, the proof sketch and the self-check prompts. None of it is the user's own work yet.
>
> References read for this note: Penn State STAT 504 Lesson 3, §3.3 (Pearson $X^2$ for independence, expected counts, df, and SAS output showing a signed Cramér's V for a 2×2 table) and §3.8 (an $I\times J$ table departs from independence in $(I-1)(J-1)$ dimensions), and STAT 500 Lesson 8 (expected counts, df, the 80%-of-cells rule). Cited but **not read** here: Cramér (1946), *Mathematical Methods of Statistics*, where V originates; Bergsma (2013), "A bias-correction for Cramér's V and Tschuprow's T", *Journal of the Korean Statistical Society* 42; and Cohen's (1988) effect-size conventions.
>
> Checks: every toy value was computed by hand and matched SciPy's independent `chi2_contingency(correction=False)` and `association(method='cramer')` to within 4×10⁻¹⁵. Four identities ($\chi^2=n\phi^2$, $V=|\phi|$, φ equals the indicator correlation, and V's invariance to scaling, permutation and transposition) and $0\le V\le1$ held on 4,000 random tables. The small-sample bias figures come from 20,000 simulated tables per $n$ (seed 20261111). These numerical checks support the stated results; they are not proofs. Generator and results: [[assets/figures/2026-11-11-cramers-v/draw_cramers_v.py]] and [[assets/figures/2026-11-11-cramers-v/checks.json]].
