"""Run with Python + NumPy + statsmodels. All observations below are invented."""
import numpy as np
import statsmodels.api as sm

# 100 independent toy observations at each study-hour value.
hours = np.repeat(np.arange(1, 10), 100)
counts = [4, 8, 17, 31, 50, 69, 83, 92, 96]
passed = np.concatenate([
    np.r_[np.ones(k), np.zeros(100 - k)] for k in counts
])
X = sm.add_constant(hours)  # columns: intercept, hours
fit = sm.Logit(passed, X).fit(disp=False)

new_hours = np.array([3., 6., 7.])
p = fit.predict(sm.add_constant(new_hours))
print("Intercept, slope:", fit.params.round(6))
print("Hours, P(pass), class at threshold 0.5:")
print(np.column_stack([new_hours, p, (p >= 0.5).astype(int)]))
print("Odds multiplier per extra hour:", np.exp(fit.params[1]))

# Separate, invented test observations; not used to fit or choose the threshold.
test_hours = np.repeat(np.arange(1, 10), 20)
test_counts = [1, 2, 4, 6, 10, 14, 16, 18, 19]
test_y = np.concatenate([
    np.r_[np.ones(k), np.zeros(20 - k)] for k in test_counts
])
test_p = fit.predict(sm.add_constant(test_hours))
q = np.clip(test_p, 1e-12, 1 - 1e-12)  # only for numerical safety in log
log_loss = -np.mean(test_y * np.log(q) + (1-test_y) * np.log1p(-q))
print("Test log loss:", log_loss)
