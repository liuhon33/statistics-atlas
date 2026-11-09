"""Author the proposed statistics taxonomy and its typed cross-links. No vault writes."""
import json, math, re, unicodedata
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
sources = {
 'asa': ['ASA undergraduate curriculum guidelines', 'https://www.amstat.org/education/curriculum-guidelines-for-undergraduate-programs-in-statistical-science-', '2014 guidelines: theory, methods, mathematics, data, computation and practice'],
 'ms': ['Stanford Statistics MS', 'https://bulletin.stanford.edu/programs/STATS-MS', 'Terminal master\'s core and breadth requirements'],
 'ubc': ['UBC MSc Statistics', 'https://stat.ubc.ca/msc-program', 'Typical coursework and statistical consulting'],
 'psu': ['Penn State graduate statistics catalog', 'https://bulletins.psu.edu/university-course-descriptions/graduate/stat/', 'Course descriptions: applied models, design, sampling, multivariate analysis and time series'],
 'psumas': ['Penn State statistics degrees', 'https://bulletins.psu.edu/graduate/programs/majors/statistics/', 'MAS/MS core and elective breadth'],
 'prob': ['Harvard Stat 110 syllabus', 'https://stat110.hsites.harvard.edu/resource/syllabus', 'Probability topics and lecture sequence'],
 'process': ['Pishro-Nik: Probability, Statistics and Random Processes', 'https://probabilitycourse.com/', 'Undergraduate and first graduate probability; random processes'],
 'linear': ['MIT 18.06SC Linear Algebra', 'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/', 'Linear algebra course and units'],
 'math': ['UBC graduate preparation', 'https://www.grad.ubc.ca/prospective-students/graduate-degree-programs/master-of-science-statistics', 'Calculus, linear algebra, proof, probability and statistics preparation'],
 'estimate': ['Penn State STAT 415, Estimation I', 'https://online.stat.psu.edu/stat415/Lesson02', 'Unbiasedness, sufficiency, variance and mean squared error'],
 'theory': ['Stanford STATS 200', 'https://bulletin.stanford.edu/courses/1254161', 'Statistical inference course scope'],
 'asym': ['Penn State graduate course catalog via OR', 'https://www.or.psu.edu/or-program-course-catalog/', 'Statistics courses: convergence, Slutsky, delta method, likelihood and U-statistics'],
 'bda': ['Gelman et al.: Bayesian Data Analysis, 3rd ed.', 'https://statmodeling.stat.columbia.edu/wp-content/uploads/2013/08/bda3_contents.pdf', 'Contents: chapters 1–17 and 18–22; topic coverage, not a proof citation'],
 'isl': ['James et al.: An Introduction to Statistical Learning', 'https://www.statlearning.com/', 'Book topic list, regression through multiple testing'],
 'causal': ['Hernan and Robins: Causal Inference, What If', 'https://www.routledge.com/Causal-Inference/Hernan-Robins/p/book/9781420076165', 'Contents: effects, identification, diagrams, adjustment and longitudinal treatment'],
 'fpp': ['Hyndman and Athanasopoulos: Forecasting, 3rd ed.', 'https://otexts.com/fpp3/', 'Chapters 2–5 and 7–13'],
 'spatial': ['UBC STAT 547P Spatial Statistics', 'https://www.stat.ubc.ca/sites/default/files/course_outlines/STAT547P_Spatial_Statistics.pdf', 'Spatial data, random fields, covariance and kriging'],
 'biostat': ['UBC STAT 536E Biostatistics outline', 'https://www.stat.ubc.ca/sites/default/files/course_outlines/STAT536E_outline_2025W2-20260104.pdf', 'Survival analysis and biostatistical modeling'],
 'electives': ['UBC statistics course listing', 'https://www.stat.ubc.ca/lookup-courses', 'Graduate electives, ecological data and high-dimensional biology'],
 'genomics': ['Penn State STAT ONLINE course index', 'https://online.stat.psu.edu/statprogram/courses', 'STAT 555 Statistical Analysis of Genomics Data and applied courses'],
 'r4ds': ['Wickham, Cetinkaya-Rundel and Grolemund: R for Data Science', 'https://r4ds.hadley.nz/', 'Transform, tidy, visualize, import, program and communicate'],
 'compute': ['CMU 36-350 Statistical Computing', 'https://stat.cmu.edu/~ryantibs/statcomp-F15/', 'Statistical programming and databases'],
 'practice': ['CMU Applied Data Science handbook, 2025–26', 'https://www.cmu.edu/dietrich/statistics-datascience/resources/docs/mads-grad-handbook.pdf', 'Visualization, engineering, computing, modeling, time series and practice'],
 'optim': ['Boyd and Vandenberghe: Convex Optimization', 'https://web.stanford.edu/~boyd/cvxbook/', 'Convex functions, optimization, duality and numerical methods'],
 'vi': ['Blei, Kucukelbir and McAuliffe: Variational Inference', 'https://www.cs.columbia.edu/~blei/papers/BleiKucukelbirMcAuliffe2017.pdf', '2017 review: ELBO, mean-field and stochastic variational inference'],
 'mining': ['Shalizi: Statistical Data Mining', 'https://www.stat.cmu.edu/~cshalizi/350/', 'Information, clustering, PCA, factors, smoothing and learning'],
 'conformal': ['Angelopoulos and Bates: Conformal Prediction', 'https://people.eecs.berkeley.edu/~angelopoulos/publications/downloads/gentle_intro_conformal_dfuq.pdf', 'Gentle introduction: prediction sets, marginal coverage and exchangeability'],
 'vi-course': ['Helsinki Computational Statistics I', 'https://www.cs.helsinki.fi/u/ahonkela/teaching/compstats1/book/variational-inference.html', 'Chapter 12: variational inference, ELBO and approximations']
}
nodes=[]; edges=[]; by_id={}; current={}; current_sources=[]; current_stage='U'
def slug(s):
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def N(id,label,level,parent=None,stage=None,refs=None,description=''):
    assert id not in by_id, id
    core=id if level==1 else by_id[parent]['core']
    n=dict(id=id,label=label,level=level,parent=parent,core=core,stage=stage or current_stage,sources=refs or list(current_sources))
    if description:n['description']=description
    nodes.append(n);by_id[id]=n;current[level]=id
    if parent:edges.append(dict(source=parent,target=id,type='contains'))
    return n
def S(id,label,description):
    global current_sources,current_stage
    current_sources=['asa','ms','ubc'];current_stage='U–M'
    N(id,label,1,description=description)
def A(id,label,description):N(id,label,2,current[1],stage='U–M',refs=['asa','ms','ubc'],description=description)
def B(id,label,stage,refs,description=''):
    global current_stage,current_sources
    current_stage=stage;current_sources=refs.split()
    N(id,label,3,current[2],description=description)
def C(id,label,points,description=''):
    N(id,label,4,current[3],description=description)
    for point in points.split(';'):
        point=point.strip()
        if not point:continue
        if '=' in point:pid,title=point.split('=',1)
        else:pid,title=id+'-'+slug(point),point
        n=N(pid,title,5,id)
        n['kind']='suggested question' if title.endswith('?') else 'knowledge point'

S('probability','Probability & mathematical foundations','The language and mathematical tools for describing randomness; mathematics here is a supporting foundation.')
A('math-tools','Mathematical tools','Calculus, geometry and proof tools used throughout statistical reasoning.')
B('calculus','Calculus & analysis for statistics','Foundation','math')
C('calc','Differentiation & integration','Limits and continuity;Derivatives and partial derivatives;Multiple integrals;taylor=Taylor approximation;Jacobian matrices;Constrained extrema')
C('analysis','Proof & convergence tools','Sets and functions;Quantifiers and proof methods;Sequences and series;Continuity and compactness;Dominated convergence overview;Interchanging limits and integrals')
B('linalg','Linear algebra for statistics','Foundation','linear')
C('spaces','Vectors, spaces & projections','Vector spaces and bases;Rank and null spaces;Inner products and norms;projection=Orthogonal projection;Least squares geometry')
C('spectral','Matrices & decompositions','Positive semidefinite matrices;eigen=Eigenvalues and eigenvectors;svd=Singular value decomposition;Quadratic forms;Trace and determinant')
B('convex','Convexity & inequalities','U–M','optim prob')
C('convexity','Convex functions & bounds','Convex sets and functions;Gradients and Hessians;jensen=Jensen inequality;Cauchy–Schwarz inequality;Holder inequality')

A('prob-language','Probability foundations','Events, probability models and updating with information.')
B('prob-models','Probability models','U','prob')
C('events','Events & counting','Sample spaces and events;Probability axioms;Permutations and combinations;Inclusion–exclusion;Union bound')
C('cond-events','Conditional probability','Conditional probability;Total probability;bayesrule=Bayes rule;Event independence;Conditional independence')
B('prob-measure','Graduate probability language','M elective','process asym')
C('measure','Measure-based overview','Sigma-algebras;Probability measures;Measurable random variables;Almost sure statements;Lebesgue expectation overview')

A('random-variables','Random variables & distributions','Describe one quantity, its transformations and its average behavior.')
B('univariate','Univariate distribution theory','U','prob process')
C('rv','Random variables & distribution functions','Discrete and continuous laws;CDF, PMF and density;Quantiles and inverse CDF;Support and event regions;Mixed distributions')
C('moments','Expectation & moments','LOTUS expectation rule;Indicator expectations;Variance and standard deviation;Moment existence;MGFs and characteristic functions')
C('transforms','Transforming random variables','CDF transformation method;Change of variables;Jacobian density factor;Convolution of independent sums')
B('distribution-families','Useful distribution families','U','prob')
C('discrete','Discrete families','Bernoulli and binomial;Geometric and negative binomial;Hypergeometric;Poisson;Multinomial')
C('continuous','Continuous families','Uniform;Normal and lognormal;Exponential and gamma;Beta;Student t, chi-square and F;Weibull and heavy-tail examples')
C('sample-laws','Sample statistics & order','Sample mean and variance;Order statistics;Sample quantiles;Normal-sample pivots;Extreme order behavior')

A('dependence','Joint variation & conditioning','Build multivariate models and separate different meanings of dependence.')
B('joint-laws','Joint distributions','U','prob')
C('joint','Marginal & conditional laws','Joint CDF and density;Marginalization;Conditional density;independence=Independence versus zero covariance;Covariance matrices')
C('conditional-mean','Conditional expectation','ce=Conditional expectation;tower=Tower property;totalvar=Total variance;L2 conditional projection;Best mean-square prediction')
B('multivariate-prob','Multivariate probability','U–M','prob bda')
C('gaussian','Multivariate normal laws','Gaussian linear transformations;Gaussian conditioning;Gaussian zero-covariance independence;Chi-square quadratic forms')
C('dependence-models','Beyond Gaussian dependence','Exchangeability;Mixture distributions;Copulas overview;Tail dependence;Conditional-independence graphs')

A('limits','Limits & concentration','Connect random samples to stable averages and useful approximations.')
B('limit-theory','Probability limit theory','U–M','prob asym')
C('convergence','Modes of convergence','Convergence in probability;Convergence in distribution;Almost sure convergence;L2 convergence;Relations and counterexamples')
C('lln-clt','Laws of large numbers & CLT','lln=Weak and strong LLN;clt=Classical iid CLT;Multivariate CLT;Finite-variance conditions;Normal-approximation limits')
C('limit-tools','Transforming limits','Continuous mapping theorem;slutsky=Slutsky theorem;delta=Delta method;Stochastic order notation;Second-order delta examples')
B('bounds','Probability bounds','U–M','process asym')
C('concentration','Inequalities & finite-sample control','Markov inequality;Chebyshev inequality;Chernoff bounding method;Hoeffding inequality;Tail bounds versus asymptotics')

A('processes','Stochastic processes','Model sequences and indexed collections of random quantities.')
B('discrete-process','Discrete-time stochastic models','U–M','prob process')
C('markov','Markov chains','Transition matrices;Chapman–Kolmogorov equations;stationary=Stationary distributions;Irreducibility and aperiodicity;Detailed balance;Mixing and convergence')
C('martingale','Random walks & martingales','Random walks;Martingale definition;Conditional-mean innovations;Stopping times;Optional-stopping conditions')
B('continuous-process','Continuous-time models','M elective','process ms')
C('poisson-process','Counts, arrivals & renewal','Poisson process;Exponential waiting times;Renewal processes;Continuous-time Markov chains;Queueing overview')
C('gaussian-process','Gaussian processes & Brownian motion','Gaussian process definition;Covariance kernels;Brownian motion basics;Stationarity of a process;Sample paths versus distributions')

S('statistics','Statistical inference & modeling','Learn about populations and mechanisms, quantify uncertainty, design studies and build interpretable models.')
A('inference','Inference foundations','What is being estimated, how data arise and what uncertainty means.')
B('stat-thinking','Statistical reasoning','U','asa theory')
C('targets','Questions, populations & data','Target population and sampling frame;Estimands and parameters;estimator=Estimator versus estimate;Prediction versus explanation;Association versus causation;Measurement scales')
C('sampling','Sampling distributions','Repeated sampling;Bias and variance;mse=Mean squared error;Standard error;Consistency;Identifiability')
B('decision','Decision theory','M','bda theory')
C('risk','Loss, risk & actions','Loss functions;Frequentist risk;Bayes risk;Bayes actions;Minimax and admissibility overview')

A('frequentist','Frequentist & likelihood inference','Estimate and test using the sampling behavior of statistical procedures.')
B('estimation','Point estimation','U–M','estimate theory asym')
C('likelihood','Likelihood methods','likelihood-point=Likelihood function;Maximum likelihood estimation;Score and observed information;Fisher information;MLE invariance;Boundary and nonregular cases')
C('estimators','Constructing & improving estimators','Method of moments;Sufficient statistics;Factorization criterion;Rao–Blackwell theorem;Completeness and Lehmann–Scheffe;Cramer–Rao bound')
C('large-sample','Large-sample inference','MLE consistency under conditions;Asymptotic normality;M-estimation;Sandwich covariance;Efficiency;Misspecified-model targets')
B('testing','Tests & confidence sets','U–M','theory asym')
C('test-theory','Testing principles','Null and alternative;Type I and II errors;Power and sample size;Neyman–Pearson lemma;Likelihood-ratio tests;p-value interpretation')
C('intervals','Intervals & test inversion','Confidence coverage;Pivotal quantities;test-invert=Inverting a test;Wald, score and likelihood intervals;Prediction versus confidence intervals')
C('classic-tests','Classical comparisons','One- and two-sample t procedures;Paired data;Variance inference;Chi-square goodness of fit;Equivalence and noninferiority')
C('multiplicity','Multiple comparisons','Familywise error;Bonferroni and Holm;fdr=False discovery rate;Benjamini–Hochberg procedure;Selection-induced bias')

A('bayesian','Bayesian inference','Update uncertain quantities with data and examine the resulting model.')
B('bayes-foundations','Bayesian inference foundations','U–M','bda')
C('posterior','Prior, likelihood & posterior','Prior and posterior;Marginal likelihood / evidence;Conjugate updating;Posterior summaries;Credible intervals;Posterior predictive distribution')
C('prior-design','Choosing and examining priors','Weakly informative priors;Prior predictive checks;Jeffreys prior overview;Improper-prior cautions;Prior sensitivity')
B('bayes-modeling','Hierarchical Bayesian modeling','M','bda')
C('hierarchical','Hierarchies & pooling','Partial pooling;Exchangeable group effects;Hierarchical variance priors;Empirical Bayes;Bayesian shrinkage')
C('bayes-checking','Bayesian model assessment','Posterior predictive checks;Predictive cross-validation;WAIC and LOO overview;Bayes factors;Calibration and model criticism')

A('regression','Regression & linear models','Describe conditional responses, estimate effects and assess model assumptions.')
B('linear-models','Linear regression','U','psu isl')
C('ols','OLS estimation & geometry','Design matrices;ols-point=Normal equations and OLS;Hat matrix;Frisch–Waugh–Lovell theorem;Simple slope and correlation;Gauss–Markov theorem')
C('reg-inference','Regression uncertainty','Coefficient covariance;Residual variance and degrees of freedom;Coefficient t tests;Nested-model F tests;ft=One-restriction F equals t squared;Mean-response and prediction intervals')
C('reg-diagnostics','Diagnostics & model building','Residual plots;Heteroskedasticity;Collinearity and VIF;Leverage and influence;Interactions and transformations;R squared and adjusted R squared')
B('generalized-models','Generalized linear models','U–M','psu bda')
C('glm','Exponential families & GLMs','Exponential-family form;Link and mean–variance functions;Deviance;IRLS / Fisher scoring;Quasi-likelihood')
C('categorical','Binary, count & categorical responses','Logistic regression;Poisson regression;Overdispersion and negative binomial;Contingency tables;Log-linear models;Multinomial and ordinal models')
B('mixed-models','Multilevel & longitudinal models','M','psu bda')
C('mixed','Random effects & repeated measures','Random intercepts and slopes;Variance components;REML;BLUP and shrinkage;Within-person correlation;Generalized estimating equations')
C('nonlinear-model','Flexible regression','Nonlinear least squares;Polynomial and spline bases;Generalized additive models;Quantile regression;Measurement error models')

A('design','Design, sampling & causality','Create informative data and separate design-based claims from model assumptions.')
B('experiments','Design of experiments','U–M','psu psumas')
C('design-principles','Randomization & comparison','Randomization;Replication and experimental units;Blocking;Confounding;Blinding;Power planning')
C('anova','ANOVA & factorial design','One- and two-factor ANOVA;Contrasts and interactions;Factorial and fractional factorial designs;Split-plot designs;ANCOVA;Response surface methods')
B('survey','Survey sampling','U–M','psu')
C('survey-design','Finite-population sampling','Simple random sampling;Stratified sampling;Cluster and multistage samples;Inclusion probabilities;Horvitz–Thompson estimation;Finite-population correction')
C('survey-adjust','Survey weights & errors','Design effects;Calibration and poststratification;Nonresponse adjustment;Ratio and regression estimators;Weight-based variance estimation')
B('causal-course','Causal inference','M elective','causal')
C('causal-id','Effects & identification','Potential outcomes;Average treatment effects;Exchangeability, consistency and positivity;DAGs and backdoor paths;Confounders, colliders and mediators')
C('causal-est','Estimating causal effects','Randomized treatment comparisons;Standardization / g-formula;Propensity scores;Inverse-probability weighting;Doubly robust estimation;Instrumental variables overview')
C('quasi','Quasi-experiments & sensitivity','Difference in differences;Regression discontinuity;Sensitivity to unmeasured confounding;Target trial specification;Time-varying treatment overview')

A('nonparametric','Nonparametric & robust inference','Relax distributional assumptions and examine sensitivity.')
B('nonparam','Nonparametric inference','U–M','psumas isl asym')
C('rank-tests','Ranks & distribution-free procedures','Sign and signed-rank tests;Mann–Whitney and Kruskal–Wallis;Rank correlations;Permutation tests;Kolmogorov–Smirnov tests;Exchangeability requirements')
C('density','Distribution & density estimation','Empirical CDF;Histograms;Kernel density estimation;Bandwidth choice;Boundary bias;Nonparametric regression')
B('robust','Robust statistics','M elective','bda psumas')
C('robustness','Sensitivity & resistant estimation','Median and trimmed means;Median absolute deviation;Influence functions;Breakdown point;Huber M-estimators;Robust regression')
B('resampling-inference','Resampling inference','U–M','isl asa')
C('bootstrap','Bootstrap & jackknife','bootstrap-point=Nonparametric bootstrap;Parametric bootstrap;Bootstrap intervals;Jackknife;Dependent-data resampling;Conditional versus unconditional bootstrap variation')

A('multivariate','Multivariate analysis','Understand variation across several measured quantities.')
B('multivariate-course','Multivariate statistical analysis','U–M','psu mining')
C('multi-inference','Vector means & covariance','Sample covariance matrix;Hotelling T squared;MANOVA;Wishart distribution overview;Canonical correlation')
C('dimension','Linear dimension reduction','pca=Principal component analysis;PCA scores and loadings;Factor analysis;Rotation and identifiability;Latent-variable measurement')
C('multi-class','Discrimination & association','Linear discriminant analysis;Quadratic discriminant analysis;Mahalanobis distance;Covariance regularization')

A('temporal','Time series & forecasting','Analyze temporal dependence and predict future observations.')
B('time-series','Time series analysis','U–M','fpp psu')
C('ts-foundations','Temporal structure','Trend and seasonality;Weak stationarity;Autocorrelation and partial autocorrelation;White noise;Time-series decomposition;Spectral density overview')
C('arima','Time series models','AR and MA processes;ARMA / ARIMA;Seasonal ARIMA;Unit roots and differencing;Model residual diagnostics;Dynamic regression')
C('forecasting','Forecasts & evaluation','Exponential smoothing;Forecast distributions;Rolling-origin evaluation;Forecast accuracy metrics;Grouped forecast reconciliation')
B('state-space','State-space & dynamic models','M elective','fpp electives')
C('states','Latent dynamic states','State-space representation;Kalman filter;Hidden Markov models;Filtering versus smoothing;Particle filtering overview;Volatility models overview')

A('event-time','Event-time & reliability','Model time until an event while accounting for censoring and incomplete observation.')
B('survival','Survival & reliability','M elective','biostat isl')
C('time-to-event','Censoring & nonparametric survival','Censoring versus truncation;Survival and hazard functions;Kaplan–Meier estimator;Nelson–Aalen estimator;Log-rank test')
C('survival-models','Event-time regression','Cox proportional hazards;Partial likelihood;Proportional-hazards diagnostics;Accelerated failure time models;Competing risks;Frailty models')
A('spatial-data','Spatial statistics','Model observations whose locations create dependence and guide prediction.')
B('spatial-course','Spatial statistics','M elective','spatial')
C('spatial-structure','Random fields & spatial prediction','Spatial data types;Covariance and variogram;Stationarity and isotropy;Kriging;Spatial Gaussian process models')
C('spatial-models','Area & point data','Areal adjacency;CAR / SAR models overview;Spatial point patterns;Poisson point-process models;Spatial confounding')

A('applied-practice','Applied statistics & evidence','Connect general methods to incomplete data, scientific domains and responsible practice.')
B('missing','Missing data & measurement','M','bda electives')
C('missing-mechanisms','Missingness & incomplete likelihoods','MCAR, MAR and MNAR;Missing-data likelihood;Complete-case limitations;Multiple imputation;Rubin pooling rules;Sensitivity analysis')
B('biomedical','Biostatistics & evidence synthesis','U–M elective','psu biostat bda')
C('epi','Epidemiology & trials','Cohort and case-control studies;Risk ratio and odds ratio;Rates and person-time;Intention-to-treat analysis;Clinical-trial endpoints;Sequential monitoring overview')
C('meta-analysis','Combining studies','Fixed-effect and random-effects synthesis;Between-study heterogeneity;Forest plots;Publication bias;Meta-regression')
B('specializations','Selected application pathways','M elective','genomics electives practice')
C('bio-data','Genomics & high-dimensional biology','Count normalization;Batch effects;Differential expression;Genome-wide association;Multiple-testing in genomics;Association versus causal mediation')
C('other-domains','Additional statistical domains','Econometric panel models;Statistical quality control;Acceptance sampling;Extreme-value modeling;Functional data overview;Network data overview')
B('professional','Statistical practice','U–M','asa practice ubc')
C('consulting','Consulting & scientific communication','Translate questions into estimands;Analysis plans;Assumptions and sensitivity reporting;Communicate uncertainty;Statistical consulting;Reproducible case study')
C('ethics','Ethics & responsible evidence','Data provenance and consent;Privacy and disclosure;Selective reporting;Fairness and subgroup assessment;Replicability;Statistical versus practical significance')

S('computing','Statistical computing & learning','Implement statistical reasoning, fit complex models and assess prediction reliably.')
A('programming','Programming, data & visualization','Turn raw data and statistical algorithms into trustworthy analyses.')
B('stat-programming','Statistical programming','U','compute r4ds')
C('program-basics','Programming foundations','R and Python data structures;Functions and scope;Iteration and vectorization;Arrays and matrix operations;Debugging;Numerical precision')
C('reproducibility','Reliable computation','Random seeds and RNG streams;Unit checks for analysis code;Version control;Environments and dependencies;Profiling;Reproducible reports')
B('data-work','Data management & exploration','U','r4ds asa practice')
C('data-management','Data wrangling','Tidy data;Joins and keys;Group-wise transformations;SQL and databases;Dates, strings and categories;Data validation and provenance')
C('eda','Exploratory data analysis','Distribution summaries;Graphical comparisons;Missingness patterns;Outlier investigation;Simpson paradox;Exploration versus confirmation')
C('graphics','Statistical visualization','Visual encodings and scales;Distribution and uncertainty graphics;Multivariate graphics;Faceting and conditioning;Accessible color;Reporting analytical findings')

A('numerics','Numerical methods & optimization','Compute stable estimates and solve statistical objectives.')
B('numerical','Numerical analysis for statistics','U–M','ms optim')
C('stable-linear','Numerical linear algebra','QR least squares;Cholesky factorization;SVD for rank deficiency;Condition numbers;Sparse matrix methods;Solve systems without explicit inverses')
C('numeric-methods','Approximation & differentiation','Root finding;Numerical integration;Finite differences;Automatic differentiation;Log-sum-exp;Approximation error')
B('optimization','Optimization for statistics','U–M','optim')
C('opt-theory','Optimization structure','Convex objectives;First- and second-order conditions;Lagrange multipliers;KKT conditions;Duality;Constraints versus penalties')
C('opt-algorithms','Optimization algorithms','Gradient descent;Newton and quasi-Newton;Coordinate descent;Stochastic gradient descent;Proximal gradient;Convergence diagnostics')

A('simulation','Simulation & approximate inference','Approximate integrals, sampling distributions and posterior quantities.')
B('monte-carlo','Monte Carlo methods','U–M','bda process')
C('simulation-basics','Random generation & Monte Carlo','Inverse-transform sampling;Rejection sampling;Monte Carlo integration;Monte Carlo standard error;Simulation study design;Coverage experiments')
C('variance-reduction','Efficient integration','importance=Importance sampling;Self-normalized importance weights;Control variates;Antithetic variables;Stratified simulation')
B('mcmc','Markov chain Monte Carlo','M','bda')
C('mcmc-algorithms','Posterior simulation','Metropolis–Hastings;Gibbs sampling;Hamiltonian Monte Carlo;Parameter transformations;Posterior simulation targets')
C('mcmc-checks','Assessing simulation quality','Multiple chains;R-hat diagnostics;Effective sample size;Autocorrelation;Monte Carlo error versus posterior uncertainty;Divergences and geometry')
B('approx-inference','Approximate & latent-variable inference','M','bda vi vi-course')
C('laplace-em','Modes, curvature & latent variables','Laplace approximation;Expectation–maximization;E and M steps;Local optima;Observed versus complete-data likelihood')
C('variational','Variational inference','Variational family;elbo=Calculate the ELBO;Posterior KL gap;Mean-field factorization;Coordinate-ascent VI;Stochastic VI;Reparameterization gradient;Why do Jensen and KL give the same bound?','Approximate a posterior through optimization. ELBO derivations link this chapter to probability, Bayesian inference and optimization.')

A('stat-learning','Statistical learning & prediction','Learn predictive rules and judge performance on appropriate unseen data.')
B('learning-foundations','Learning objectives & evaluation','U–M','isl')
C('prediction-risk','Risk, fit & generalization','Population risk;Empirical risk minimization;Bias–variance tradeoff;Bayes optimal prediction;Overfitting;Regularization')
C('validation','Validation & model selection','Train / validation / test splits;Cross-validation;Nested cross-validation;Group and temporal splits;Data leakage;Hyperparameter tuning;Learning curves')
C('prediction-assessment','Evaluating predictions','Regression metrics;ROC and precision–recall;Probability calibration;Proper scoring rules;Class imbalance;Distribution shift')
B('supervised','Supervised learning methods','U–M','isl')
C('penalized','Penalized linear models','ridge=Ridge regression;Lasso;Elastic net;Shrinkage paths;Feature scaling;High-dimensional identifiability')
C('neighbors-kernels','Local methods & kernels','Nearest neighbors;Kernel regression;Support vector machines;Kernel trick;Gaussian process regression')
C('trees','Trees & ensembles','Regression and classification trees;Pruning;Bagging;Random forests;Gradient boosting;Feature importance caveats')
B('unsupervised','Unsupervised learning','U–M','isl mining')
C('clustering','Clustering & mixtures','K-means;Hierarchical clustering;Density-based clustering;Gaussian mixture models;Cluster validation;Label switching')
C('embeddings','Dimension reduction & embeddings','Multidimensional scaling;Spectral embeddings;Nonlinear manifold overview;PCA versus visualization embeddings;Distances and scaling')
B('modern-prediction','Modern predictive inference','M elective','conformal')
C('prediction-uncertainty','Prediction uncertainty','Conformal prediction overview;Exchangeability and coverage;Prediction sets;Marginal versus conditional coverage;Calibration under shift')

A('prob-learning','Probabilistic models & neural methods','Selected master\'s-level introductions linking latent variables, probability and learning.')
B('graphical','Probabilistic graphical models','M elective','bda mining')
C('graphs','Factorization & graphical models','Directed graphical models;Undirected graphical models;Graphical conditional independence;Variable elimination;Message passing overview;Latent-variable models')
B('neural','Neural statistical learning','M elective','isl practice vi')
C('neural-basics','Neural networks','Multilayer networks;Backpropagation;Activation functions;Minibatch optimization;Regularization and early stopping;Representation learning')
C('neural-models','Selected architectures & latent models','Convolutional networks overview;Sequence models overview;Autoencoders;Variational autoencoders;Generative-model evaluation;Predictive versus generative tasks')
B('information','Information for statistical learning','U–M elective','mining vi')
C('information-measures','Information measures','Entropy;Cross-entropy;kl=KL divergence;Mutual information;Log loss;Likelihood and compression')

# Each non-hierarchy link is authored: its role is explicit and its direction matters.
def X(a,b,kind,why):
    assert a in by_id and b in by_id,(a,b)
    assert a!=b
    edges.append(dict(source=a,target=b,type=kind,reason=why))

X('probability','statistics','connection','Probability supplies sampling models; inference reasons from observed data about their unknown features.')
X('statistics','computing','connection','Statistical models define objectives and uncertainty; computation fits and checks the procedures.')
X('computing','probability','connection','Simulation implements probability models and uses probabilistic error analysis.')
X('projection','ols','prerequisite','OLS fits the projection of the response onto the design column space.')
X('spectral','dimension','prerequisite','Eigenvectors and singular values describe principal directions of variation.')
X('linalg','numerical','prerequisite','Stable matrix algorithms implement linear-algebra operations in statistical fitting.')
X('taylor','delta','prerequisite','Taylor linearization transfers a limiting distribution through a smooth function.')
X('calc','transforms','prerequisite','Integration and Jacobians transform density-weighted probability regions.')
X('convexity','opt-theory','prerequisite','Convexity gives useful global optimality conditions for statistical objectives.')
X('jensen','elbo','prerequisite','Concavity of log bounds the log of an expectation; support and integrability conditions matter.')
X('kl','elbo','prerequisite','The ELBO gap is KL from the variational distribution to the posterior when the identity is well-defined.')
X('bayesrule','posterior','prerequisite','Bayes rule updates the prior using the likelihood and its normalizing evidence.')
X('cond-events','causal-id','connection','Causal identification adds assumptions linking observational conditionals to interventions.')
X('rv','sampling','prerequisite','An estimator is a random variable or vector because its input sample is random.')
X('sample-laws','classic-tests','prerequisite','Exact normal-sample laws provide t, chi-square and F reference distributions.')
X('ce','ols','connection','The conditional mean minimizes square loss; OLS restricts prediction to a linear class.')
X('ce','risk','application','Conditional expected loss determines optimal actions for a given loss.')
X('totalvar','bootstrap','application','Total variance distinguishes within-resample variation from variation across original datasets.')
X('tower','hierarchical','application','Hierarchical predictions average over latent parameters and groups.')
X('gaussian','reg-inference','prerequisite','Gaussian errors yield exact normal coefficient laws and independent residual quadratic forms.')
X('gaussian','states','application','Linear Gaussian conditioning is the update behind the Kalman filter.')
X('independence','graphs','prerequisite','Graphical models encode particular conditional-independence statements.')
X('lln','sampling','application','Sample averages provide elementary consistent estimators when LLN conditions hold.')
X('clt','large-sample','prerequisite','Asymptotic normal inference combines suitable CLTs with estimator-specific arguments.')
X('slutsky','intervals','application','Replacing a population scale by a consistent estimate supports asymptotic pivots.')
X('delta','intervals','application','Delta-method uncertainty yields approximate intervals for transformed parameters.')
X('lln','simulation-basics','prerequisite','Monte Carlo averages converge under applicable LLN conditions.')
X('clt','simulation-basics','application','A suitable CLT supplies a Monte Carlo error approximation.')
X('concentration','prediction-risk','connection','Finite-sample bounds help control deviations between empirical and population quantities.')
X('markov','mcmc-algorithms','prerequisite','MCMC constructs a Markov chain with the desired invariant distribution.')
X('stationary','mcmc-checks','connection','Having an invariant target alone does not establish that a finite simulation has mixed.')
X('poisson-process','time-to-event','connection','Arrival times supply elementary examples of survival and hazard modeling.')
X('gaussian-process','spatial-structure','application','Covariance kernels describe correlated random fields for spatial prediction.')
X('martingale','states','connection','Forecast innovations connect conditional-mean reasoning to dynamic modeling.')
X('targets','consulting','prerequisite','A precise estimand and population are needed before selecting an analysis.')
X('estimator','bootstrap','prerequisite','Bootstrap simulation approximates how a statistic varies across samples.')
X('mse','prediction-risk','connection','Bias–variance decompositions relate estimation error to predictive risk; prediction can add outcome noise.')
X('likelihood-point','glm','prerequisite','GLMs use an exponential-family likelihood and a link for the conditional mean.')
X('likelihood','survival-models','application','Event-time inference must incorporate censoring or use an appropriate partial likelihood.')
X('large-sample','robustness','connection','M-estimation and sandwich uncertainty connect robust fitting with asymptotic inference.')
X('test-invert','reg-inference','application','Inverting coefficient tests gives matching confidence intervals.')
X('ft','anova','connection','A one-degree-of-freedom Gaussian linear-model comparison has F equal to the matching t statistic squared.')
X('multiplicity','bio-data','application','Genome-wide comparisons need a stated error-rate control strategy.')
X('fdr','validation','connection','Repeated selection and reuse of data affect inferential claims as well as prediction estimates.')
X('posterior','mcmc','prerequisite','Posterior expectations define the quantities that MCMC approximates.')
X('posterior','approx-inference','prerequisite','Intractable posterior integrals motivate deterministic approximations.')
X('prior-design','penalized','connection','Certain MAP objectives match penalties; full posterior inference retains uncertainty beyond the optimum.')
X('ridge','hierarchical','connection','Gaussian-prior shrinkage connects ridge-style penalties with partial-pooling models.')
X('hierarchical','mixed','connection','Group-level latent effects connect hierarchical Bayes and mixed-effects models.')
X('bayes-checking','validation','connection','Both assess predictive behavior beyond the observations used to fit a model.')
X('ols','anova','connection','ANOVA and contrasts can be expressed as linear-model comparisons.')
X('reg-diagnostics','robustness','connection','Diagnostics reveal influential observations and motivate sensitivity analyses.')
X('glm','categorical','application','Logistic and Poisson regression instantiate GLMs for different response distributions.')
X('mixed','survey-design','connection','Clustering affects dependence and uncertainty; model-based and sampling-design routes differ.')
X('nonlinear-model','neighbors-kernels','connection','Smoothing and basis methods connect flexible regression to predictive learning.')
X('design-principles','causal-id','application','Randomization supports treatment exchangeability under the study design.')
X('design-principles','rank-tests','application','Randomization can justify permutation reference distributions; arbitrary shuffling cannot.')
X('survey-adjust','causal-est','connection','Both use weights, but inclusion probabilities and treatment propensities answer different questions.')
X('causal-id','missing-mechanisms','connection','Selection and missingness assumptions determine what observed data can identify.')
X('density','neighbors-kernels','connection','Kernel weighting is shared by density estimation and local prediction.')
X('bootstrap','simulation-basics','application','Bootstrap inference uses a fitted or empirical law as a simulation model.')
X('bootstrap','validation','connection','Both resample data, but uncertainty estimation and generalization assessment have different targets.')
X('pca','svd','connection','PCA can be computed using an SVD of an appropriately centered data matrix.')
X('dimension','embeddings','connection','Linear variance-preserving summaries contrast with nonlinear neighborhood displays.')
X('multi-class','supervised','application','Discriminant analysis is a model-based approach to supervised classification.')
X('processes','ts-foundations','prerequisite','Temporal modeling uses stochastic-process notions such as stationarity and covariance.')
X('forecasting','validation','application','Forecast evaluation preserves time order rather than training on the future.')
X('states','graphs','connection','Hidden Markov models are structured graphical latent-state models.')
X('survival-models','epi','application','Event-time regression models time-to-outcome data in clinical studies.')
X('time-to-event','missing-mechanisms','connection','Censoring and missing data both require explicit observation-process assumptions.')
X('spatial-structure','neighbors-kernels','connection','Gaussian process regression and kriging share conditional Gaussian prediction.')
X('missing-mechanisms','laplace-em','application','EM integrates missing or latent quantities in its expectation step.')
X('hierarchical','meta-analysis','application','Random-effects synthesis models study-specific effects within a hierarchy.')
X('ethics','validation','connection','Honest reporting requires separating model selection from final evaluation.')
X('data-management','targets','connection','Data definitions and joins must preserve the intended units and target population.')
X('graphics','reg-diagnostics','application','Residual and influence displays reveal model failures and unusual observations.')
X('reproducibility','simulation-basics','prerequisite','Documented RNG streams and repeatable code make simulation studies auditable.')
X('numeric-methods','neural-basics','application','Automatic differentiation computes gradients used in neural training.')
X('stable-linear','ols','application','QR or SVD solve regression problems more stably than explicitly inverting a Gram matrix.')
X('opt-algorithms','penalized','application','Coordinate and proximal methods solve common penalized objectives.')
X('opt-algorithms','variational','application','VI turns approximate posterior fitting into an optimization problem.')
X('importance','elbo','connection','Both involve density ratios; the log-expectation distinction leads to Jensen\'s bound.')
X('mcmc-checks','bayes-checking','connection','Computation diagnostics and model criticism examine different possible failures.')
X('laplace-em','clustering','application','EM is a common fitting algorithm for finite mixture models.')
X('elbo','neural-models','application','Variational autoencoders train a latent-variable model with an ELBO objective.')
X('validation','trees','prerequisite','Ensemble complexity and tuning must be evaluated on appropriate held-out data.')
X('prediction-assessment','ethics','application','Aggregate predictive accuracy can hide poor subgroup performance.')
X('prediction-uncertainty','convergence','connection','Exchangeability-based conformal guarantees use a different route from asymptotic normal intervals.')
X('kl','likelihood-point','connection','Expected log likelihood and KL relate model fit to distributional discrepancy.')
X('information-measures','trees','application','Entropy-based criteria can be used to select classification-tree splits.')

# Clarify selected leaves without turning the atlas into a textbook.
by_id['elbo']['description']='For observed x, latent z and a trial density q, assemble expected log joint minus expected log q. The posterior-KL identity and Jensen give the same bound under suitable support and finiteness conditions.'
by_id['ft']['description']='For a single linear restriction in the same Gaussian linear model, the matching F statistic equals t squared; joint restrictions need not reduce to one t statistic.'
by_id['independence']['description']='Independence implies zero covariance when moments exist. The reverse needs additional structure, such as joint Gaussianity.'
by_id['prediction-uncertainty']['description']='Elective introduction. Standard split conformal provides marginal coverage under exchangeability, not arbitrary conditional coverage or protection from distribution shift.'

meta={
 'title':'Statistics backbone', 'version':1, 'created':'2026-11-08',
 'scope':'A broad proposed map from mathematical preparation through undergraduate statistics and selected master\'s electives; not an exhaustive or official curriculum.',
 'level_names':{'1':'Core subject','2':'Area','3':'Course / book-sized unit','4':'Chapter / theme','5':'Knowledge point / theorem / suggested question'},
 'stages':'Foundation, U (undergraduate), M (master\'s), U–M and elective are approximate study bands, independent of hierarchy levels. Every master\'s program selects a subset.',
 'organization':'Each concept has one display parent. Cross-links express prerequisites, applications or comparisons, not additional duplicate nodes. The three roots and exact hierarchy are an authored synthesis.',
 'evidence':'Sources support topic coverage and study scope. Course/book-sized units and chapters are proposed groupings, not claims about the exact tables of contents. Cross-link explanations are authored conceptual synthesis, not a complete formal prerequisite graph.',
 'questions':'Question-form leaves are suggested study prompts unless explicitly mapped to a supplied question. No learning mastery is inferred.',
 'obsidian':'External planning artifact. No vault pages, settings, logs or digest checkpoints were edited.'
}

def finish():
    assert len({n['id'] for n in nodes})==len(nodes)
    assert Counter(n['level'] for n in nodes)[1]==3
    for n in nodes:
        assert 1<=n['level']<=5
        assert all(s in sources for s in n['sources'])
        if n['parent']:assert by_id[n['parent']]['level']==n['level']-1
    triples=[(e['source'],e['target'],e['type']) for e in edges]
    assert len(triples)==len(set(triples))
    assert all(e['source'] in by_id and e['target'] in by_id for e in edges)
    payload=dict(meta=meta,sources={k:dict(title=v[0],url=v[1],scope=v[2]) for k,v in sources.items()},nodes=nodes,edges=edges)
    raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'))
    (ROOT/'statistics-backbone.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    template=ROOT/'atlas-template.html'
    if template.exists():
        (ROOT/'statistics-backbone.html').write_text(template.read_text(encoding='utf-8').replace('/*ATLAS_DATA*/',raw),encoding='utf-8')
    print(json.dumps({'nodes':len(nodes),'levels':dict(Counter(n['level'] for n in nodes)),'edges':len(edges),'crosslinks':sum(e['type']!='contains' for e in edges),'sources':len(sources),'stages':dict(Counter(n['stage'] for n in nodes))}))
if __name__=='__main__':finish()
