---
id: learning-r-squared-versus-adjusted-r-squared
title: R squared versus adjusted R squared
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Diagnostics & model building/R squared and adjusted R squared]]"
subject: statistics
backbone_path: "Statistical inference & modeling → Regression & linear models → Linear regression → Diagnostics & model building → R squared and adjusted R squared"
study_band: U
note_types: [topic-note, insight]
source_format: conversation
created: 2026-11-09
updated: 2026-11-12
status: active
verification: checked
aliases: [R2 versus adjusted R2]
tags: [atlas/learning, subject/statistics, topic/regression]
connections:
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Cross-validation]]"
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Overfitting]]"
  - "[[Learning/Statistical computing & learning/Statistical learning & prediction/Likelihood and information criteria - AIC and BIC]]"
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared]]"
---

# R squared versus adjusted R squared

Statistical inference & modeling → Regression & linear models → Linear regression → Diagnostics & model building → R squared and adjusted R squared

**$R^2$ measures training fit; adjusted $R^2$ asks whether that fit is worth the number of fitted predictors. Neither guarantees good predictions on new data.**

## Formulas and intuition

Consider ordinary least squares **with an intercept**, $n$ observations, and $k$ predictor columns excluding the intercept. Assume a full-rank design, $n>k+1$, and nonconstant responses. Define

$$
\mathrm{SSE}=\sum_i(y_i-\hat y_i)^2,
\qquad \mathrm{SST}=\sum_i(y_i-\bar y)^2.
$$

$$
R^2=1-\frac{\mathrm{SSE}}{\mathrm{SST}},
\qquad
R^2_{\mathrm{adj}}=1-\frac{\mathrm{SSE}/(n-k-1)}{\mathrm{SST}/(n-1)}
=1-(1-R^2)\frac{n-1}{n-k-1}.
$$

- **$R^2$:** the fraction of training variation around $\bar y$ accounted for by the fitted model. For example, $0.60$ means a 60% reduction in squared error relative to predicting the sample mean—not “60% accurate.”
- **Adjusted $R^2$:** compares residual and total sums of squares **per degree of freedom**. Estimating the intercept and $k$ coefficients leaves $n-k-1$ residual degrees of freedom. It is a complexity-adjusted score, not literally a fraction of explained variation.

Adding predictors to a nested OLS model on the **same observations and response** cannot decrease training $R^2$: setting the new coefficients to zero reproduces the old fit, so the minimum SSE cannot increase. But adjusted $R^2$ rises only if SSE falls enough to compensate for the lost degrees of freedom—equivalently, if $\mathrm{SSE}/(n-k-1)$ decreases.

## A small example

Suppose $n=100$, $\mathrm{SST}=100$, and we add one predictor:

| Model | $k$ | SSE | $R^2$ | Adjusted $R^2$ |
| --- | ---: | ---: | ---: | ---: |
| Original | 2 | 40.0 | 0.600 | $1-0.400(99/97)=0.5918$ |
| One more predictor | 3 | 39.8 | 0.602 | $1-0.398(99/96)=0.5896$ |

**The training fit improves slightly, but not enough to justify the extra predictor by adjusted $R^2$.** Here adjusted $R^2$ would increase only if the new SSE were below $40(96/97)\approx39.588$.

With one added predictor, this is exactly [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared#4. One restriction can occur inside a many-predictor model|partial F > 1]].

Compare the [[Learning/Statistical computing & learning/Statistical learning & prediction/Likelihood and information criteria - AIC and BIC#6. Exactly how much improvement pays for another parameter?|AIC/BIC complexity penalties]].

## What to remember

- Under the stated setup, $0\le R^2\le1$ and $R^2_{\mathrm{adj}}\le R^2$; adjusted $R^2$ can be negative. Test-set $R^2$ can also be negative, and the training monotonicity argument does not apply there.
- Compare these scores using the same response and observations. Changing the response scale or the rows can make comparisons misleading.
- Adjusted $R^2$ penalizes complexity, but does not eliminate overfitting or replace held-out evaluation. High values do not establish causation or validate regression assumptions.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Cross-validation|Cross-validation]] — Evaluates performance on held-out observations rather than relying on a degrees-of-freedom correction to training fit.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Overfitting|Overfitting]] — Adding predictors can improve training $R^2$ without improving generalization; adjusted $R^2$ penalizes complexity but does not eliminate overfitting.

- [[Learning/Statistical computing & learning/Statistical learning & prediction/Likelihood and information criteria - AIC and BIC|Likelihood and information criteria - AIC and BIC]] — Both adjust regression fit for added parameters, but use different penalties and can rank the same models differently.

- [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared|Why one restriction gives F equals t squared]] — For nested OLS fits on the same data, adjusted R² increases after adding one predictor exactly when its partial F exceeds 1; this is not a fixed-significance-level rule.

## Origin

> [!info]- Source details
> Requested by the user on 2026-11-09 as a small comparison note. Explanation and numerical example are Codex synthesis, not a transcription of the user's derivation. Formulas and example arithmetic were independently checked under the stated OLS conditions. Reference: [Penn State STAT 501, Multiple Linear Regression](https://online.stat.psu.edu/stat501/Lesson05), “Coefficient of Determination, R-squared, and Adjusted R-squared”; its $p$ counts the intercept, so $p=k+1$ here.
