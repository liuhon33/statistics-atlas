---
id: learning-ols-coefficients-many-routes
title: OLS coefficients through algebra, projection, and likelihood
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Normal equations and OLS]]"
subject: statistics
backbone_path: "Statistical inference & modeling → Regression & linear models → Linear regression → OLS estimation & geometry → Normal equations and OLS"
study_band: U–M
note_types: [derivation, question, insight]
question_roles: [reconcile-approaches, cross-topic-connection, special-to-general, assumption-boundary]
source_format: handwriting-and-conversation
created: 2026-11-09
updated: '2026-11-12'
status: active
verification: checked
learning_state: unknown
aliases: [Ways to derive beta hat, OLS coefficient derivations, Normal equations and covariance]
tags: [atlas/learning, subject/statistics, topic/regression]
connections:
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation]]"
  - "[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection]]"
  - "[[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Vector means & covariance/Sample covariance matrix]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Coefficient covariance]]"
  - "[[Backbone/Statistical computing & learning/Numerical methods & optimization/Numerical analysis for statistics/Numerical linear algebra/QR least squares]]"
  - "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Frisch–Waugh–Lovell theorem]]"
  - "[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition]]"
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared]]"
  - '[[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]]'
sources:
  - "[[raw/assets/2026-11-09-OLS-I01-normal-equations-and-slope.png]]"
  - "[[raw/notes/2025-06-12-linear-algebra-summary.pdf]]"
---

# OLS coefficients through algebra, projection, and likelihood

Statistical inference & modeling → Regression & linear models → Linear regression → OLS estimation & geometry → Normal equations and OLS

**All the least-squares routes meet at one condition: the residual is orthogonal to every column of the design matrix.** Geometry explains this condition; calculus derives it by minimizing squared error; a Gaussian likelihood gives the same objective from a probability model. Matrix factorizations then provide useful ways to compute the coefficients.

**My questions, paraphrased from the 2026-11-09 request:** How do the supplied matrix and projection arguments produce $\widehat\beta$, which steps were skipped, and what other approaches give the same answer? How is $X^\top X$ connected to covariance?

The earlier slope note develops $\widehat\beta_1=r_{xy}s_y/s_x$ and its testing geometry. This note concentrates on the full coefficient vector and the assumptions behind the different routes.

## Shared setup and notation

Let $y\in\mathbb R^n$ contain one observed response per row, $X\in\mathbb R^{n\times p}$ be the design matrix, and $\beta\in\mathbb R^p$ a candidate coefficient vector. Ordinary least squares (OLS) chooses

$$
\widehat\beta\in\underset{\beta\in\mathbb R^p}{\operatorname{argmin}}\;
S(\beta),\qquad S(\beta)=\|y-X\beta\|_2^2.
$$

Here $\|v\|_2^2=v^\top v$, $X^\top$ is the transpose, and $I_m$ denotes the $m\times m$ identity. Write $\widehat y=X\widehat\beta$ and $e=y-\widehat y$. With an intercept and $k$ predictors, $p=k+1$ and $X=[\mathbf1\;Z]$, where $\mathbf1\in\mathbb R^n$ is all ones and $Z\in\mathbb R^{n\times k}$ contains the predictors.

Until the SVD section, assume **full column rank**, $\operatorname{rank}(X)=p\le n$. Then the coefficients are unique and

$$
\boxed{X^\top e=0
\quad\Longleftrightarrow\quad
X^\top X\widehat\beta=X^\top y
\quad\Longleftrightarrow\quad
\widehat\beta=(X^\top X)^{-1}X^\top y.}
$$

These are deterministic statements about the observed data. Distributional assumptions enter the likelihood and sampling-covariance sections. [Strang's MIT lecture summary, “Projections” and “Least squares,” pp. 1–3](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/198bde3a6536b62989b6cc09495575c1_MIT18_06SCF11_Ses2.3sum.pdf).

| Strang's notation in the supplied PDF | Notation here | Role |
| --- | --- | --- |
| $A$ | $X$ | Design matrix, $n\times p$ |
| $\widehat x$ | $\widehat\beta$ | Coefficients, $p\times1$ |
| $b$ | $y$ | Observed response, $n\times1$ |
| $p$ (a vector in the PDF) | $\widehat y$ | Fitted response, $n\times1$ |
| $P$ | $H$ | Projection matrix, $n\times n$ |

The letter $p$ here counts coefficients; it does not denote the fitted vector.

## 1. Expand the matrix algebra in the supplied screenshot

![[raw/assets/2026-11-09-OLS-I01-normal-equations-and-slope.png]]

*Supplied handwritten comparison, preserved unchanged. The top design orders its columns as predictor then intercept; the lower formula orders them as intercept then predictor. The coefficient order must change with the columns.*

For simple regression, use the lower convention:

$$
X=\begin{pmatrix}1&x_1\\\vdots&\vdots\\1&x_n\end{pmatrix},
\qquad \beta=\begin{pmatrix}\beta_0\\\beta_1\end{pmatrix}.
$$

Multiplication gives

$$
X^\top X=
\begin{pmatrix}n&\sum_i x_i\\\sum_i x_i&\sum_i x_i^2\end{pmatrix},
\qquad
X^\top y=\begin{pmatrix}\sum_i y_i\\\sum_i x_i y_i\end{pmatrix}.
$$

Define $\bar x=n^{-1}\sum_i x_i$, $\bar y=n^{-1}\sum_i y_i$,
$S_{xx}=\sum_i(x_i-\bar x)^2$, and $S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y)$.
The missing denominator calculation is

$$
\begin{aligned}
\det(X^\top X)
&=n\sum_i x_i^2-(\sum_i x_i)^2\\
&=n\left(\sum_i x_i^2-n\bar x^2\right)
=n\sum_i(x_i-\bar x)^2=nS_{xx}.
\end{aligned}
$$

Thus, for $S_{xx}>0$, the $2\times2$ inverse formula yields exactly the matrix in the screenshot:

$$
\widehat\beta=
\frac1{nS_{xx}}
\begin{pmatrix}\sum_i x_i^2&-\sum_i x_i\\-\sum_i x_i&n\end{pmatrix}
\begin{pmatrix}\sum_i y_i\\\sum_i x_i y_i\end{pmatrix}.
$$

For the slope, expand the second row and then center:

$$
\begin{aligned}
\widehat\beta_1
&=\frac{n\sum_i x_i y_i-(\sum_i x_i)(\sum_i y_i)}{nS_{xx}}\\
&=\frac{\sum_i x_i y_i-n\bar x\bar y}{S_{xx}}
=\frac{S_{xy}}{S_{xx}}.
\end{aligned}
$$

For the intercept, rewrite the numerator of the first row:

$$
\begin{aligned}
\widehat\beta_0
&=\frac{\bar y\sum_i x_i^2-\bar x\sum_i x_i y_i}{S_{xx}}\\
&=\frac{\bar y(S_{xx}+n\bar x^2)-\bar x(S_{xy}+n\bar x\bar y)}{S_{xx}}\\
&=\bar y-\bar x\frac{S_{xy}}{S_{xx}}
=\bar y-\widehat\beta_1\bar x.
\end{aligned}
$$

**Where does the normal equation come from?** In the screenshot, multiplying $X\beta=y$ by $X^\top$ skips the central justification. Usually $y\notin\operatorname{Col}(X)$, so the exact equation has no solution. The normal equation instead makes the *remaining error* orthogonal to the columns. The next three approaches establish why that condition minimizes the loss.

## 2. Projection gives the normal equations without calculus

![[assets/figures/2026-11-09-ols-coefficients/source-pdf-page-01.png]]

*Unretouched rendering of p. 1 of the supplied handwritten PDF, attributed by the user to Strang's lectures. The column-space sketch and perpendicular residual are the central geometric step. In the final handwritten line, the projection matrix itself should omit the trailing $b$: $P=A(A^\top A)^{-1}A^\top$, while the projected vector is $Pb$.*

Every possible fit is a linear combination of the columns:

$$
X\beta=\beta_1X_{\cdot1}+\cdots+\beta_pX_{\cdot p}
\in\operatorname{Col}(X)\subseteq\mathbb R^n,
$$

where $X_{\cdot j}$ denotes column $j$ (the generic column indices here run from $1$ to $p$). OLS asks for the point of this subspace closest to $y$.

Suppose $\widehat y=X\widehat\beta$ and $e=y-\widehat y$ is perpendicular to the subspace. For any other $\beta$,

$$
y-X\beta=e+X(\widehat\beta-\beta).
$$

The two terms are perpendicular, so Pythagoras gives

$$
\|y-X\beta\|^2
=\|e\|^2+\|X(\widehat\beta-\beta)\|^2
\ge\|e\|^2.
$$

This proves optimality. Full column rank makes equality possible only for $\beta=\widehat\beta$. Conversely, if $e$ has a nonzero component along a column-space direction, moving the fit a little in that direction shortens the residual; therefore a minimizer must have $e\perp\operatorname{Col}(X)$.

Being perpendicular to the whole column space is equivalent to being perpendicular to each column:

$$
X_{\cdot j}^\top e=0\quad\text{for every }j
\quad\Longleftrightarrow\quad X^\top(y-X\widehat\beta)=0.
$$

Solving gives the coefficient formula. Multiplying by $X$ gives the fitted vector:

$$
\widehat y=Hy,\qquad
H=X(X^\top X)^{-1}X^\top,\qquad e=(I_n-H)y.
$$

Here $H^\top=H$ and $H^2=H$; $I_n-H$ projects onto $\operatorname{Null}(X^\top)$. In the PDF's column-vector convention, the p. 3 expression for the residual must be $(I-P)b$, with the matrix multiplying on the left. [MIT summary, p. 1](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/198bde3a6536b62989b6cc09495575c1_MIT18_06SCF11_Ses2.3sum.pdf#page=1).

### Why is the inverse allowed?

The supplied PDF p. 4 already contains the key proof. For any $v\in\mathbb R^p$,

$$
v^\top X^\top Xv=\|Xv\|^2.
$$

If $X$ has independent columns, $v\ne0$ implies $Xv\ne0$, so $X^\top X$ is positive definite and invertible. Conversely, if $Xv=0$ for some nonzero $v$, then $X^\top Xv=0$ and the inverse does not exist. Thus

$$
X^\top X\text{ invertible}\quad\Longleftrightarrow\quad X\text{ has full column rank}.
$$

## 3. Vector calculus is the shortest general derivation

Set $r(\beta)=y-X\beta$. Its differential is $\mathrm dr=-X\,\mathrm d\beta$. Since $S=r^\top r$ is scalar,

$$
\begin{aligned}
\mathrm dS
&=(\mathrm dr)^\top r+r^\top\mathrm dr\\
&=2r^\top\mathrm dr
=-2r^\top X\,\mathrm d\beta.
\end{aligned}
$$

By the column-gradient convention $\mathrm dS=(\nabla_\beta S)^\top\mathrm d\beta$,

$$
\boxed{\nabla_\beta S=-2X^\top(y-X\beta).}
$$

The dimensions are $(p\times n)(n\times1)=p\times1$, one derivative per coefficient. Set the gradient to zero to obtain $X^\top X\widehat\beta=X^\top y$.

The equivalent expansion explains the familiar derivative rule:

$$
S(\beta)=y^\top y-2\beta^\top X^\top y+\beta^\top X^\top X\beta.
$$

For constant $a\in\mathbb R^p$ and $G\in\mathbb R^{p\times p}$,
$\nabla_\beta(a^\top\beta)=a$ and
$\nabla_\beta(\beta^\top G\beta)=(G+G^\top)\beta$.
Here $G=X^\top X$ is symmetric, so the last derivative is $2G\beta$.
The Hessian is $2X^\top X\succ0$: the stationary point is the unique global minimum. [Andrew Ng, CS229 notes, §2, pp. 8–10](https://cs229.stanford.edu/summer2023/cs229-notes1.pdf#page=8).

## 4. Sum-of-squares partial derivatives work for multiple regression too

For one predictor, minimize

$$
S(a,b)=\sum_{i=1}^n(y_i-a-bx_i)^2.
$$

Differentiating the intercept and slope gives

$$
\frac{\partial S}{\partial a}=-2\sum_i(y_i-a-bx_i)=0,
\qquad
\frac{\partial S}{\partial b}=-2\sum_i x_i(y_i-a-bx_i)=0.
$$

The first equation gives $a=\bar y-b\bar x$. Substituting this into the second gives

$$
0=\sum_i x_i\{(y_i-\bar y)-b(x_i-\bar x)\}
=S_{xy}-bS_{xx}.
$$

Hence $\widehat b=S_{xy}/S_{xx}$ and $\widehat a=\bar y-\widehat b\bar x$.
The centering equality uses $\sum_i(y_i-\bar y)=\sum_i(x_i-\bar x)=0$.

For **any number of predictors**, write row $i$ of the design as $x_i^\top$, and let $x_{ij}$ denote its $j$th entry. Then

$$
S(\beta)=\sum_{i=1}^n\left(y_i-\sum_{\ell=1}^p x_{i\ell}\beta_\ell\right)^2,
$$

$$
\frac{\partial S}{\partial\beta_j}
=-2\sum_{i=1}^n x_{ij}\left(y_i-\sum_{\ell=1}^p x_{i\ell}\beta_\ell\right)=0,
\qquad j=1,\ldots,p.
$$

These $p$ equations are precisely the entries of $X^\top(y-X\beta)=0$. The method is fully general; one predictor only makes solving the coupled equations especially short.

The objective is the **sum of squared residuals**, not their signed sum. With a fitted intercept, $\sum_i e_i=0$ is one consequence of optimality. Minimizing the signed sum itself would not define least squares.

## 5. Gaussian maximum likelihood produces the same objective

Now add a statistical model, conditional on the observed design:

$$
Y=X\beta+\varepsilon,\qquad
\varepsilon\mid X\sim\mathcal N_n(0,\sigma^2I_n),\qquad \sigma^2>0.
$$

Thus the response errors are conditionally independent Gaussian variables with a common variance. At the observed value $y$, the likelihood is

$$
L(\beta,\sigma^2;y,X)
=\prod_{i=1}^n\frac1{\sqrt{2\pi\sigma^2}}
\exp\!\left[-\frac{(y_i-x_i^\top\beta)^2}{2\sigma^2}\right].
$$

Taking logs converts the product to a sum:

$$
\ell(\beta,\sigma^2)
=-\frac n2\log(2\pi\sigma^2)-\frac1{2\sigma^2}S(\beta).
$$

For every fixed positive $\sigma^2$, maximizing this is equivalent to minimizing $S$. Explicitly,

$$
\nabla_\beta\ell=\frac1{\sigma^2}X^\top(y-X\beta)=0
\quad\Longrightarrow\quad
\widehat\beta_{\mathrm{MLE}}=\widehat\beta_{\mathrm{OLS}}.
$$

OLS can be computed without a Gaussian assumption; the model above supplies this particular likelihood interpretation. [CS229 notes, §3 “Probabilistic interpretation,” pp. 10–12](https://cs229.stanford.edu/summer2023/cs229-notes1.pdf#page=10).

If $\sigma^2$ is unknown and the minimized $\mathrm{SSE}=S(\widehat\beta)>0$, differentiation with respect to $v=\sigma^2$ gives

$$
\frac{\partial\ell}{\partial v}
=-\frac n{2v}+\frac{\mathrm{SSE}}{2v^2}=0,
\qquad \widehat\sigma^2_{\mathrm{MLE}}=\frac{\mathrm{SSE}}n.
$$

The coefficient estimate stays the same. The usual unbiased variance estimate is instead $\mathrm{SSE}/(n-p)$ when $n>p$. If SSE is zero and the variance is an unrestricted unknown positive parameter, the likelihood grows without bound as $\sigma^2\downarrow0$, so there is no finite joint MLE in that parameter space; the OLS fit still exists.

Changing the noise model may change the estimator. For example, a known positive-definite covariance $\Omega$ gives a quadratic loss $(y-X\beta)^\top\Omega^{-1}(y-X\beta)$ and generalized least squares

$$
\widehat\beta_{\mathrm{GLS}}=(X^\top\Omega^{-1}X)^{-1}X^\top\Omega^{-1}y.
$$

It reduces to ordinary least squares for $\Omega=\sigma^2I_n$. This follows by applying the same differential calculation to the weighted quadratic form.

## How the Gram matrix becomes a covariance matrix

**$X^\top X$ is a Gram matrix:** entry $(j,\ell)$ is the inner product of columns $j$ and $\ell$. Raw inner products retain the column means. Sample covariance first subtracts those means and then divides by $n-1$.

To keep the intercept separate, use $X=[\mathbf1\;Z]$ and $\beta=(\beta_0,\beta_s^\top)^\top$, where $\beta_s\in\mathbb R^k$ contains the slopes. Define

$$
C=I_n-\frac{\mathbf1\mathbf1^\top}{n},\quad
Z_c=CZ,\quad y_c=Cy,\quad
\bar z=\frac1n Z^\top\mathbf1\in\mathbb R^k.
$$

$C$ removes the mean. For $n\ge2$, the sample predictor covariance and predictor–response covariance vector are

$$
\widehat\Sigma_{ZZ}=\frac1{n-1}Z_c^\top Z_c,
\qquad
\widehat\Sigma_{Zy}=\frac1{n-1}Z_c^\top y_c.
$$

For example, entry $(j,\ell)$ of $\widehat\Sigma_{ZZ}$ is
$\sum_i(z_{ij}-\bar z_j)(z_{i\ell}-\bar z_\ell)/(n-1)$.
This is the centered Gram-matrix identity in [Illinois CS 357, “Data Centering” and “Covariance Matrix”](https://cs357.cs.illinois.edu/textbook/notes/pca.html#covariance-matrix).

The intercept normal equation gives
$\widehat\beta_0=\bar y-\bar z^\top\widehat\beta_s$.
Substituting it into the other equations leaves

$$
Z_c^\top Z_c\widehat\beta_s=Z_c^\top y_c.
$$

Divide both sides by the same $n-1$:

$$
\boxed{\widehat\beta_s=\widehat\Sigma_{ZZ}^{-1}\widehat\Sigma_{Zy},
\qquad \widehat\beta_0=\bar y-\bar z^\top\widehat\beta_s.}
$$

Full rank of $[\mathbf1\;Z]$ ensures $\widehat\Sigma_{ZZ}$ is invertible. Using a common denominator $n$ in both covariance estimates would cancel in exactly the same way.

The uncentered Gram matrix shows precisely what must be removed:

$$
X^\top X=
\begin{pmatrix}
n & n\bar z^\top\\
n\bar z & (n-1)\widehat\Sigma_{ZZ}+n\bar z\bar z^\top
\end{pmatrix}.
$$

For the centered-predictor design $[\mathbf1\;Z_c]$, it becomes block diagonal:

$$
[\mathbf1\;Z_c]^\top[\mathbf1\;Z_c]
=\begin{pmatrix}n&0\\0&(n-1)\widehat\Sigma_{ZZ}\end{pmatrix}.
$$

The intercept coordinate in this centered design is $\bar y$. Centering the intercept column itself would turn it into zero; it is excluded from the predictor covariance being inverted.

For one predictor this is simply

$$
\widehat\beta_1=
\frac{\widehat{\operatorname{Cov}}(x,y)}{\widehat{\operatorname{Var}}(x)}
=\frac{S_{xy}}{S_{xx}}.
$$

When both sample standard deviations are positive, this equals $r_{xy}s_y/s_x$. With several correlated predictors, the inverse *matrix* adjusts for shared variation; separate marginal covariance/variance ratios generally do not give the multiple-regression slopes. The [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation#Several predictors couple the coefficient equations|standardized correlation-system derivation]] gives a counterexample to using separate marginal slopes.

### Predictor covariance and coefficient covariance are different objects

Under $Y=X\beta+\varepsilon$ with $\mathbb E[\varepsilon\mid X]=0$ and $\operatorname{Cov}(\varepsilon\mid X)=\sigma^2I_n$,

$$
\widehat\beta-\beta=(X^\top X)^{-1}X^\top\varepsilon.
$$

Applying $\operatorname{Cov}(A\varepsilon)=A\operatorname{Cov}(\varepsilon)A^\top$ gives

$$
\operatorname{Cov}(\widehat\beta\mid X)=\sigma^2(X^\top X)^{-1},\qquad
\operatorname{Cov}(\widehat\beta_s\mid X)
=\frac{\sigma^2}{n-1}\widehat\Sigma_{ZZ}^{-1}.
$$

$\widehat\Sigma_{ZZ}$ describes predictor variation **within the observed dataset**; $\operatorname{Cov}(\widehat\beta\mid X)$ describes coefficient variation **across repeated response samples at that design**. Gaussianity is unnecessary for these covariance identities. A direction with little independent predictor variation has a small covariance eigenvalue, which becomes large when inverted and increases coefficient uncertainty in that direction.

## 6. Completing the square proves the answer algebraically

Let $G=X^\top X\succ0$, $h=X^\top y$, and $b_*=G^{-1}h$. Expand and regroup:

$$
\begin{aligned}
S(\beta)
&=y^\top y-2\beta^\top h+\beta^\top G\beta\\
&=y^\top y-h^\top G^{-1}h
 +(\beta-b_*)^\top G(\beta-b_*).
\end{aligned}
$$

The final term is nonnegative and is zero only at $\beta=b_*$. Therefore $\widehat\beta=b_*$. This supplies a complete derivation with neither differentiation nor a pre-assumed normal equation. It is the algebraic form of the Pythagorean argument.

This same quadratic gives the [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared#The general one-restriction proof|SSE cost of one linear restriction]].

## 7. QR computes coefficients in an orthonormal basis

Factor a full-column-rank design as $X=QR$, where
$Q\in\mathbb R^{n\times p}$ satisfies $Q^\top Q=I_p$ and
$R\in\mathbb R^{p\times p}$ is invertible and upper triangular. Split $y$ into its component in the columns of $Q$ and its perpendicular remainder:

$$
y-QR\beta=Q(Q^\top y-R\beta)+(I_n-QQ^\top)y.
$$

The terms are orthogonal, and $\|Qv\|=\|v\|$, so

$$
S(\beta)=\|Q^\top y-R\beta\|^2+\|(I_n-QQ^\top)y\|^2.
$$

The second term does not depend on $\beta$. Set the first to zero:

$$
\boxed{R\widehat\beta=Q^\top y.}
$$

Compute $Q^\top y$ and solve by back-substitution. Here $Q^\top y$ contains coordinates in the *orthonormal* basis; $R$ converts the original predictor coefficients into those coordinates. [Stanford linear-algebra refresher, “Least Squares with QR”](https://web.stanford.edu/~lanhuong/refresher/notes/LinearAlgebraP2_2.html).

The supplied PDF ends p. 4 with the heading “Gram–Schmidt.” For $X=[\mathbf1\;x]$, carrying that idea through gives

$$
q_1=\frac{\mathbf1}{\sqrt n},\quad
q_2=\frac{x-\bar x\mathbf1}{\sqrt{S_{xx}}},\quad
R=\begin{pmatrix}\sqrt n&\sqrt n\bar x\\0&\sqrt{S_{xx}}\end{pmatrix},
$$

$$
Q^\top y=\begin{pmatrix}\sqrt n\bar y\\S_{xy}/\sqrt{S_{xx}}\end{pmatrix}.
$$

The second triangular equation gives $\widehat\beta_1=S_{xy}/S_{xx}$; the first gives $\widehat\beta_0=\bar y-\bar x\widehat\beta_1$. Centering is exactly the step that removes the intercept direction from $x$.

## 8. Residualization isolates one coefficient at a time

Partition $X=[W\;z]$, with $W\in\mathbb R^{n\times(p-1)}$ containing the other columns and $z\in\mathbb R^n$ the target predictor. Write the coefficients as $(\gamma^\top,b)^\top$. Let

$$
M_W=I_n-W(W^\top W)^{-1}W^\top,
\qquad r_z=M_Wz,\quad r_y=M_Wy.
$$

For a fixed $b$, fitting $\gamma$ projects $y-zb$ onto $\operatorname{Col}(W)$. After that fit, the remaining loss is

$$
\min_\gamma\|y-W\gamma-zb\|^2
=\|M_W(y-zb)\|^2=\|r_y-br_z\|^2.
$$

This is one-predictor regression through the origin:

$$
\boxed{\widehat b=\frac{r_z^\top r_y}{r_z^\top r_z},\qquad
\widehat\gamma=(W^\top W)^{-1}W^\top(y-z\widehat b).}
$$

Full rank of $[W\;z]$ makes $r_z\ne0$. The result is the **Frisch–Waugh–Lovell theorem**: remove the other predictors from both the target predictor and the response, then regress the resulting residuals. [Michael Lovell, “A Simple Proof of the FWL Theorem,” theorem on printed p. 2 / PDF p. 3](https://repec.wesleyan.edu/pdf/mlovell/2005012_lovell.pdf#page=3).

Taking $W=\mathbf1$ makes $M_W=C$ and recovers ordinary centering. With several predictors, $r_z$ is the part of $z$ that the others cannot explain linearly; its squared length is the denominator for that adjusted coefficient.

## 9. SVD handles dependent columns and identifies the minimum-norm answer

Now allow $\operatorname{rank}(X)=r<p$. For $r>0$, write the compact singular value decomposition

$$
X=U_rD_rV_r^\top,
$$

where $U_r\in\mathbb R^{n\times r}$ and $V_r\in\mathbb R^{p\times r}$ have orthonormal columns, and $D_r$ is diagonal with positive singular values $d_1,\ldots,d_r$. Then

$$
S(\beta)=\|U_r^\top y-D_rV_r^\top\beta\|^2
+\|(I_n-U_rU_r^\top)y\|^2.
$$

Only the coordinates $V_r^\top\beta$ affect the fit. Set them to $D_r^{-1}U_r^\top y$ and set the unidentifiable null-space component to zero:

$$
\boxed{\widehat\beta_{\min}=V_rD_r^{-1}U_r^\top y=X^+y.}
$$

$X^+$ is the Moore–Penrose pseudoinverse. All OLS minimizers are

$$
\widehat\beta=\widehat\beta_{\min}+v,\qquad v\in\operatorname{Null}(X).
$$

They have the same unique fit $\widehat y=U_rU_r^\top y$, but different coefficient vectors. Since $\widehat\beta_{\min}\perp\operatorname{Null}(X)$,
$\|\widehat\beta_{\min}+v\|^2=\|\widehat\beta_{\min}\|^2+\|v\|^2$:
the pseudoinverse selects the smallest Euclidean coefficient norm. For $X=0$, every coefficient minimizes the loss and the minimum-norm choice is zero. [MIT 18.065, Lecture 9: pseudoinverse and least-squares methods](https://github.com/mitmath/18065/blob/main/README.md#lecture-9-feb-24).

For example, duplicate the predictor in the three-point problem: $X=[\mathbf1\;x\;x]$. Only the sum of its two slopes is identified. Every pair with $\beta_1+\beta_2=1/2$ and intercept $2/3$ gives the same fit; the minimum-norm answer has slopes $1/4$ and $1/4$.

For full rank, SVD reduces to the usual unique OLS solution. It also explains a computation issue: if $d_{\max}$ and $d_{\min}$ are the extreme singular values,

$$
\kappa_2(X)=\frac{d_{\max}}{d_{\min}},\qquad
\kappa_2(X^\top X)=\left(\frac{d_{\max}}{d_{\min}}\right)^2.
$$

Thus forming $X^\top X$ can magnify numerical difficulties. The inverse formula explains OLS; QR or SVD is usually a better way to compute it in floating point. A [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit#2. How the prior becomes an L2 penalty|positive ridge penalty]] changes the objective and generally changes the estimator; it is not another formula for the same OLS coefficients.

## 10. Iterative optimization reaches the same solution

For $J(\beta)=\tfrac12S(\beta)$ and a full-rank design, gradient descent uses

$$
\beta^{(t+1)}=\beta^{(t)}+\eta X^\top(y-X\beta^{(t)}).
$$

Subtracting the normal equation gives the exact error recurrence

$$
\beta^{(t+1)}-\widehat\beta
=(I_p-\eta X^\top X)(\beta^{(t)}-\widehat\beta).
$$

If $0<\eta<2/\lambda_{\max}(X^\top X)$, every eigenvalue of this update matrix has absolute value less than one, so the iterates converge to $\widehat\beta$. Here $\lambda_{\max}$ is the largest eigenvalue and $t$ is the iteration index. A finite iteration count generally gives an approximation.

Newton's method uses the constant Hessian $X^\top X$ and reaches the minimizer in one step in exact arithmetic:

$$
\beta_{\mathrm{new}}
=\beta-(X^\top X)^{-1}X^\top(X\beta-y)
=(X^\top X)^{-1}X^\top y.
$$

This is a computational route to the same quadratic minimum. It still requires solving a linear system.

## One example checks all the views

The screenshot and supplied PDF pp. 2–3 use $(x_i,y_i)=(1,1),(2,2),(3,2)$, also the example in [Strang's lecture summary, pp. 1–3](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/198bde3a6536b62989b6cc09495575c1_MIT18_06SCF11_Ses2.3sum.pdf).

$$
X^\top X=\begin{pmatrix}3&6\\6&14\end{pmatrix},\qquad
X^\top y=\begin{pmatrix}5\\11\end{pmatrix},\qquad
\widehat\beta=\begin{pmatrix}2/3\\1/2\end{pmatrix}.
$$

For elimination, subtract twice $3\widehat\beta_0+6\widehat\beta_1=5$ from $6\widehat\beta_0+14\widehat\beta_1=11$: this gives $2\widehat\beta_1=1$, then $\widehat\beta_0=2/3$.

$$
\widehat y=\begin{pmatrix}7/6\\10/6\\13/6\end{pmatrix},\qquad
e=\frac16\begin{pmatrix}-1\\2\\-1\end{pmatrix},\qquad
X^\top e=\begin{pmatrix}0\\0\end{pmatrix},\qquad
\mathrm{SSE}=\frac16.
$$

For covariance, $\bar x=2$, $\bar y=5/3$, $S_{xx}=2$, $S_{xy}=1$; hence the predictor sample variance is $1$, the sample covariance is $1/2$, and their ratio gives the slope $1/2$. For Gaussian MLE, $\widehat\sigma^2=1/18$, while the unbiased estimate is $1/6$ because $n-p=1$.

![[assets/figures/2026-11-09-ols-coefficients/ols-data-and-projection.svg]]

*Original Codex illustration of the supplied example. Left: squared vertical residuals in the predictor–response plot. Right: after removing the mean, the same residuals form one vector perpendicular to $x_c$ in observation space. The right panel uses the orthonormal basis $u=x_c/\sqrt2$, $v=e/\|e\|$, so its lengths and right angle are exact. The projection is onto the line spanned by $x_c$; before centering, the fitted subspace is the plane spanned by $\mathbf1$ and $x$ in $\mathbb R^3$.*

In the supplied PDF p. 3, the written sum $e_1^2+e_2^2+e_3^2$ is the **squared** norm $\|A\widehat x-b\|^2$, and its derivative is a derivative of that squared loss. The displayed fitted and residual vectors agree with the values above under the convention $e=y-\widehat y$.

| Approach | What it contributes |
| --- | --- |
| Matrix expansion | Converts the general coefficient formula into intercept and slope expressions. |
| Projection / Pythagoras | Explains why the residual must be perpendicular to the fitted subspace. |
| Vector and component calculus | Produce the same normal equations, with any number of predictors. |
| Gaussian likelihood | Explains squared-error fitting under a specified noise model. |
| Centered covariance | Expresses slopes as predictor-covariance inverse times predictor–response covariance. |
| Completing the square | Proves global minimality directly by algebra. |
| QR | Uses orthonormal coordinates and a triangular solve. |
| FWL residualization | Computes a coefficient from variation left after adjusting for the other columns. |
| SVD | Exposes identifiable directions and selects a minimum-norm solution when needed. |
| Gradient descent / Newton | Compute the quadratic minimizer by updates. |

The algebraic identities and rank/variance conditions above were checked directly. Exact symbolic calculations reproduce the supplied example; independent multiple-predictor calculations agree across normal equations, covariance, QR, SVD, FWL and Newton to below $10^{-13}$. Gradient descent converges to within $10^{-9}$ under its stated step-size condition. Reproducible calculations and figure code: [[assets/figures/2026-11-09-ols-coefficients/verify_and_draw.py|verification and drawing script]]; results: [[assets/figures/2026-11-09-ols-coefficients/checks.json|checks]]. Numerical agreement supports the general proofs rather than replacing them.

## Connections

- [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|Three routes from least squares to slope and correlation]] — Specializes the full coefficient system to the signed correlation–slope identity and develops the related t/F geometry.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|Orthogonal projection]] — Converts closest-fit geometry into $X^\top e=0$ and proves optimality using perpendicular components.
- [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Vector means & covariance/Sample covariance matrix|Sample covariance matrix]] — Centering and dividing the predictor Gram matrix by $n-1$ turns the normal equations into a covariance system.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation|Maximum likelihood estimation]] — A conditionally independent Gaussian noise model makes maximizing likelihood equivalent to minimizing squared residuals.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Coefficient covariance|Coefficient covariance]] — Error propagation through the OLS linear map explains why the inverse Gram matrix controls coefficient uncertainty.
- [[Backbone/Statistical computing & learning/Numerical methods & optimization/Numerical analysis for statistics/Numerical linear algebra/QR least squares|QR least squares]] — Replaces the original predictor coordinates with orthonormal ones and computes the coefficients by a triangular solve.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/OLS estimation & geometry/Frisch–Waugh–Lovell theorem|Frisch–Waugh–Lovell theorem]] — Generalizes removing the mean to removing every other predictor before estimating a chosen coefficient.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|Singular value decomposition]] — Separates identifiable and null-space directions, supplies the pseudoinverse, and explains sensitivity to small singular values.

- [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared|Why one restriction gives F equals t squared]] — Uses the completed-square identity and coefficient covariance to derive the cost of any single linear restriction.

- [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit|Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]] — Shows how a Gaussian prior changes the OLS quadratic, and when removing the penalty recovers OLS.

## Origin

> [!info]- Source details
> This note digests the 2026-11-09 request, the [[raw/assets/2026-11-09-OLS-I01-normal-equations-and-slope.png|supplied screenshot]], and the five-page [[raw/notes/2025-06-12-linear-algebra-summary.pdf|handwritten linear-algebra PDF]]. The PDF's filename supplies the June 12, 2025 source-date label; it was exported and received on November 9, 2026. All five pages were inspected. Pages 1–3 provide projection, least squares and the numerical example; p. 4 provides the invertibility proof and a Gram–Schmidt heading. Page 5's symmetry/skew-symmetry examples were read as context; the relevant symmetry of the projector is used above, without creating another topic note.
>
> The user attributes the PDF to Gilbert Strang's lectures. MIT 18.06 Lecture 16 and its summary match the projection argument and exact three-point example; the relevant transcript passage also matches the fitted line. This identifies a matching lecture, without claiming full-video viewing. The supplied image and PDF are preserved byte-for-byte. Only the screenshot and PDF p. 1 are displayed as source handwriting; the other PDF pages remain accessible in the original.
>
> The worked inverse expansion and geometric argument develop the supplied reasoning. The differential proof, multiple-predictor clarification, covariance and coefficient-uncertainty distinction, Gaussian likelihood, completed-square proof, QR completion, FWL, SVD, iterative methods, and clean figure are Codex additions. The two substantive questions above are labeled paraphrases of the user's focus; requests for more steps were incorporated into the explanations. Source references were consulted for the stated sections, not ingested as complete additional publications. The earlier slope note was read for the comparison and remains separate.
