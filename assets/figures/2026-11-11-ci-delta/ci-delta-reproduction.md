# CI inversion and the squared-mean delta method

Original Codex analytic illustrations, added 2026-11-11 with the vault's `animate-geometry` skill. These extend the existing CI/p-value and CLT/delta-method learning notes. The examples come from those notes; no new source experiment or recovered lecturer animation is claimed.

## Use

Open `ci-explorer.html` or `delta-explorer.html` directly in a browser, or use their `atlas-interactive` blocks in Obsidian Reading view / rendered Live Preview. Each HTML file is self-contained and needs no network or server. A temporary local server was used only for QA. The notes also embed static SVG fallbacks.

- **CI:** change observation, candidate null and significance. Normal location uses known standard error 0.1; the uniform-scale example uses one observation from Uniform(θ/2, 3θ/2). All tests are equal-tailed. Reject strictly when p < α, so confidence sets include their boundaries. At floating-point boundaries the implementation uses a 1e-12 comparison tolerance. The square band has equal axis scales. Plot windows stay fixed within a model, while tail probabilities use the full distributions.
- **Delta:** iid N(μ,1) observations, estimating μ² with the squared sample mean. Change μ, n, and one standardized draw z; choose raw, √n or n scaling for the CDF. The decomposition panel always uses √n scaling and fixed axes. The CDF's horizontal range adapts; pinning retains an earlier exact distribution in the same coordinate system. Changing scale clears the pin. At μ = 0 the first-order approximation is a point mass, drawn as a CDF jump; nX̄² has the exact χ²₁ law for every n.

Both animations start paused, stop when hidden, and have keyboard-operable controls. Presets reset the principal comparison; there is no random data regeneration. Holding z fixed as n changes is a coupling of marginal examples, not a nested growing sample.

## Reproduce

From this folder, with Python packages NumPy, SciPy and Matplotlib, plus Node:

```powershell
& 'D:\anaconda\python.exe' build.py
node check_math.cjs
```

`build.py` imports the shared `.agents/skills/animate-geometry/scripts/build_explorer.py`. It packs the body fragments, CSS, pure formulas in `math.js`, SVG helper in `plot.js` and topic UI scripts. Build manifests record input/output hashes; the helper refuses to overwrite manually changed HTML. Static figures are computed independently with SciPy and Matplotlib; PNGs are inspection previews. No files in `raw/` are modified.

## Mathematical checks

`reference-values.json` contains independent SciPy normal and noncentral chi-square CDF values. For V = a(X̄² − μ²), the exact law follows from nX̄² having noncentral χ² with one degree of freedom and noncentrality nμ². This independently checks the normal-interval formula used by JavaScript, across positive, negative and zero μ, five sample sizes and all three scales. Gaussian quadrature also checks the exact first two moments.

`check_math.cjs` records results in `math-checks.json`: 801 normal CDF values, 13 normal quantiles, 630 transformed CDF values, 15,606 CI/test/p-value decision comparisons, exact and neighbouring boundaries, coverage probabilities, square-expansion identities and the zero-mean scaling identities. Numerical agreement supports the analytic derivations; it is not a proof of a general asymptotic theorem.

`check_obsidian.js` exercises the actual installed renderer in temporary offscreen components at 760 and 420 CSS pixels. It checks execution, readiness, initial sizing, stability and sandboxing without opening or rearranging the user's active note. Offscreen Chromium frames can defer later viewport relayout, so interactive resizing is tested separately in a visible browser preview. Browser control/visual checks and static image inspection are separate; results are recorded in `ui-checks.json` and `obsidian-checks.json`.
