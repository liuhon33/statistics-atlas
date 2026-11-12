"""Original checked illustrations for the Feature Map and Kernel chat extension.

Run this file with Python 3, NumPy and Matplotlib. Outputs go beside this file.
The examples are new illustrations, not recovered slide figures or attachments.
Exponential kernel convention: exp(-abs(x-z)/ell), not the slide's scale symbol.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
SEED = 20261112
JITTER = 1e-10  # Sampling-factor stabilization, NOT observation variance.
COLORS = ["#008a8a", "#396fc2", "#9c5ba8", "#c7781c", "#6b8c3c"]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.fonttype": "none",
                     "svg.hashsalt": "kernel-chat-20261112"})


def kernel(a, b, kind="rbf", ell=0.55):
    """Unit signal variance; a and b are one-dimensional input arrays."""
    d = np.asarray(a)[:, None] - np.asarray(b)[None, :]
    if kind == "rbf":
        return np.exp(-d**2 / (2 * ell**2))
    if kind == "exponential":
        return np.exp(-np.abs(d) / ell)
    raise ValueError(kind)


def draw(mean, cov, rng, n=5):
    """Each COLUMN is one joint grid draw; covariance is cov + JITTER*I."""
    cov = (cov + cov.T) / 2
    L = np.linalg.cholesky(cov + JITTER * np.eye(len(mean)))
    return mean[:, None] + L @ rng.standard_normal((len(mean), n)), L


def posterior(x, X, y, noise_sd, kind):
    C = kernel(X, X, kind) + noise_sd**2 * np.eye(len(X))
    B = kernel(X, x, kind)
    L = np.linalg.cholesky(C)
    beta = np.linalg.solve(L.T, np.linalg.solve(L, y))
    V = np.linalg.solve(L, B)
    mean = B.T @ beta
    cov = kernel(x, x, kind) - V.T @ V
    return mean, (cov + cov.T) / 2, C, B


def save_figure(fig, stem):
    fig.savefig(OUT / (stem + ".svg"), bbox_inches="tight",
                metadata={"Date": None})
    fig.savefig(OUT / (stem + ".png"), dpi=150, bbox_inches="tight")
    plt.close(fig)
    ET.parse(OUT / (stem + ".svg"))


def periodic_figure():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8),
                             gridspec_kw={"width_ratios": [1, 1.5]})
    t = np.linspace(0, 2 * np.pi, 400)
    ax = axes[0]
    ax.plot(np.cos(t), np.sin(t), color="#bcc8cf", lw=2)
    for phase, label, color in zip([0, .25, .5, .75],
                                   ["0 or p", "p/4", "p/2", "3p/4"], COLORS):
        point = np.array([np.cos(2*np.pi*phase), np.sin(2*np.pi*phase)])
        ax.annotate("", xy=point, xytext=(0, 0),
                    arrowprops={"arrowstyle": "->", "color": color, "lw": 2})
        ax.scatter(*point, s=35, color=color, zorder=3)
        ax.text(*(1.24 * point), label, ha="center", va="center", color=color)
    ax.set(xlim=(-1.6, 1.6), ylim=(-1.4, 1.4), aspect="equal",
           xlabel=r"$\cos(2\pi x/p)$", ylabel=r"$\sin(2\pi x/p)$",
           title="Same phase = same point on the circle")
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    ax = axes[1]
    delta = np.linspace(-1.1, 1.1, 600)
    ax.plot(delta, np.cos(2*np.pi*delta), color=COLORS[0], lw=2,
            label="Dot product: cosine kernel")
    ax.plot(delta, np.exp(-2*np.sin(np.pi*delta)**2/.7**2), color=COLORS[1],
            lw=2, label="RBF on the circle: periodic kernel")
    ax.axhline(0, color="#9babb5", lw=.8)
    ax.set(xlabel=r"Input separation $(x-z)/p$", ylabel=r"$k(x,z)$",
           title="Two different kernels on the same circle", ylim=(-1.1, 1.1))
    ax.legend(loc="lower center", fontsize=8.5)
    ax.grid(alpha=.15)
    fig.tight_layout(pad=1.5)
    save_figure(fig, "circle-kernels")


def gp_figure_and_checks():
    x = np.linspace(-2, 2, 201)
    X = np.array([-1.2, -.4, .5, 1.3])
    y = np.array([-.8, .65, .35, -.55])
    noise_sd = .15
    rng = np.random.default_rng(SEED)
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), sharex=True, sharey=True)
    records = {}
    arrays = {"x": x, "X_train": X, "y_train": y}
    for col, kind in enumerate(["rbf", "exponential"]):
        K = kernel(x, x, kind)
        mean, cov, C, B = posterior(x, X, y, noise_sd, kind)
        prior, L0 = draw(np.zeros(len(x)), K, rng)
        post, L1 = draw(mean, cov, rng)
        # Independent algebraic routes to the posterior; no matrix inverse needed.
        direct_mean = B.T @ np.linalg.solve(C, y)
        direct_cov = K - B.T @ np.linalg.solve(C, B)
        mean_error = float(np.max(np.abs(mean-direct_mean)))
        cov_error = float(np.max(np.abs(cov-direct_cov)))
        factor_error = max(float(np.max(np.abs(L @ L.T - A - JITTER*np.eye(len(x)))))
                           for L, A in [(L0, K), (L1, cov)])
        min_eig = float(np.linalg.eigvalsh(cov).min())
        reduction_min_eig = float(np.linalg.eigvalsh(K-cov).min())
        assert mean_error < 1e-12 and cov_error < 1e-12
        assert factor_error < 1e-12
        assert min_eig > -1e-10 and reduction_min_eig > -1e-10
        assert np.all(np.diag(cov) <= np.diag(K)+1e-12)
        assert prior.shape == post.shape == (len(x), 5)
        records[kind] = {"mean_formula_max_error": mean_error,
                         "covariance_formula_max_error": cov_error,
                         "cholesky_reconstruction_max_error": factor_error,
                         "posterior_min_eigenvalue": min_eig,
                         "variance_reduction_min_eigenvalue": reduction_min_eig,
                         "posterior_variance_range": [float(np.diag(cov).min()),
                                                       float(np.diag(cov).max())]}
        arrays.update({kind+"_prior_samples": prior, kind+"_posterior_samples": post,
                       kind+"_mean": mean, kind+"_covariance": cov})
        for row, samples, center, covariance, label in [
                (0, prior, np.zeros(len(x)), K, "PRIOR: no observations"),
                (1, post, mean, cov, "POSTERIOR: condition on four observations")]:
            ax = axes[row, col]
            sd = np.sqrt(np.maximum(np.diag(covariance), 0))
            ax.fill_between(x, center-2*sd, center+2*sd, color="#d6e7f3",
                            alpha=.7, label="Pointwise mean +/- 2 SD")
            for i, color in enumerate(COLORS):
                ax.plot(x, samples[:, i], color=color, lw=1, alpha=.85)
            ax.plot(x, center, color="#152b3a", lw=2, ls="--", label="Mean")
            if row:
                ax.scatter(X, y, c="#b54c26", edgecolors="white", s=50,
                           zorder=5, label="Noisy observations")
            ax.set_title(("RBF" if kind == "rbf" else "Exponential")+" | "+label,
                         fontsize=10)
            ax.set(xlabel="Fixed input x", ylabel="Latent f(x)", xlim=(-2, 2))
            ax.grid(alpha=.15)
    max_abs = max(float(np.abs(a).max()) for k,a in arrays.items() if k.endswith("samples"))
    bound = max(3.0, np.ceil((max_abs+.1)*2)/2)
    for ax in axes.flat:
        ax.set_ylim(-bound, bound)
    axes[1, 0].legend(loc="lower left", fontsize=8)
    fig.suptitle("One curve = one joint draw of all grid values", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, .96), pad=1.8)
    save_figure(fig, "gp-prior-posterior")
    np.savez_compressed(OUT / "example-data.npz", **arrays)
    return {"seed": SEED, "sampling_jitter_variance": JITTER,
            "grid_size": len(x), "length_scale": .55, "signal_variance": 1.0,
            "noise_sd": noise_sd, "training_inputs": X.tolist(),
            "training_outputs": y.tolist(), "common_y_limits": [-bound, bound],
            "kernels": records}


def algebra_checks():
    a = np.array([1., 2., 4.]); b = np.array([1., 3., 9.])
    assert a @ b == 43
    a[1] *= np.sqrt(2); b[1] *= np.sqrt(2)
    assert np.isclose(a @ b, 49)
    rng = np.random.default_rng(1729)
    x = rng.uniform(-4, 4, 24); p = 2.4; ell = .7
    u = np.column_stack([np.cos(2*np.pi*x/p), np.sin(2*np.pi*x/p)])
    d = x[:, None]-x[None, :]
    cosine = np.cos(2*np.pi*d/p)
    circle_d2 = ((u[:, None, :]-u[None, :, :])**2).sum(axis=2)
    periodic = np.exp(-2*np.sin(np.pi*d/p)**2/ell**2)
    cosine_error = float(np.max(np.abs(u @ u.T-cosine)))
    periodic_error = float(np.max(np.abs(np.exp(-circle_d2/(2*ell**2))-periodic)))
    assert cosine_error < 1e-13 and periodic_error < 1e-13
    assert np.linalg.eigvalsh(cosine).min() > -1e-12
    assert np.linalg.eigvalsh(periodic).min() > -1e-12
    Psi = np.array([[1., 1.], [1., 2.]])
    K = Psi @ Psi.T
    np.testing.assert_array_equal(K, [[2., 3.], [3., 5.]])
    # The all-linear-combinations variance in coefficient and function coordinates.
    q = np.array([.3, -.8])
    noise_var = .25
    lhs = q @ (K+noise_var*np.eye(2)) @ q
    rhs = np.sum((Psi.T @ q)**2) + noise_var*np.sum(q**2)
    assert abs(lhs-rhs) < 1e-14
    return {"polynomial_values": [43, 49], "cosine_identity_max_error": cosine_error,
            "periodic_identity_max_error": periodic_error,
            "linear_combination_variance_error": float(abs(lhs-rhs)),
            "shared_weight_covariance": K.tolist(),
            "noisy_covariance": (K+noise_var*np.eye(2)).tolist(),
            "random_sign_counterexample": {"Var(U+V)": 2, "P(U+V=0)": .5}}


if __name__ == "__main__":
    periodic_figure()
    result = {"algebra": algebra_checks(), "gp": gp_figure_and_checks(),
              "numpy": np.__version__, "matplotlib": matplotlib.__version__,
              "limits": "Numerical algebra/PSD checks are not proofs or a live Obsidian rendering test."}
    (OUT / "checks.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
