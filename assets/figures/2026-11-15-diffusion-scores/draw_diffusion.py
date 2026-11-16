"""Original diffusion illustrations and independent mathematical spot checks.

Run: D:/anaconda/python.exe assets/figures/2026-11-15-diffusion-scores/draw_diffusion.py
Requires numpy, scipy, matplotlib and Pillow. No model weights or source images.
"""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
from PIL import Image, ImageDraw
from scipy.integrate import quad
from scipy.special import logsumexp
from scipy.stats import norm

OUT = Path(__file__).resolve().parent
INK, BLUE, GREEN, ORANGE, PURPLE = "#26364a", "#2969a7", "#138d82", "#c16b32", "#8c61ae"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK,
    "axes.edgecolor": "#aeb9c4", "xtick.color": INK, "ytick.color": INK,
    "svg.fonttype": "none", "svg.hashsalt": "diffusion-scores-2026-11-15",
    "savefig.facecolor": "white",
})
MEANS = np.array([[-1.45, -0.8], [1.45, -0.8], [0.0, 1.35]])
WEIGHTS = np.array([0.35, 0.35, 0.30])
BASE_VAR = 0.12**2


def save(fig, name):
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", metadata={"Date": None})
    fig.savefig(OUT / (name + ".png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, xywh, title, detail="", color=BLUE):
    x, y, w, h = xywh
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.035,rounding_size=0.08",
        edgecolor=color, facecolor=color + "10", linewidth=1.4))
    ax.text(x + w/2, y + h*(0.66 if detail else 0.5), title,
            ha="center", va="center", weight="bold", fontsize=11, color=color)
    if detail:
        ax.text(x + w/2, y + h*0.29, detail, ha="center", va="center", fontsize=10)


def arrow(ax, start, end, color=INK, style="-", rad=0):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=12,
        color=color, linewidth=1.25, linestyle=style,
        connectionstyle=f"arc3,rad={rad}"))


def loss_routes():
    fig, ax = plt.subplots(figsize=(13.2, 4.1))
    ax.set(xlim=(0, 13.5), ylim=(0, 4.2))
    ax.axis("off")
    ax.text(.2, 3.95, "Two routes to a trainable noise predictor", fontsize=17, weight="bold")
    box(ax, (.25, 2.5, 2.5, .9), "Likelihood / ELBO", "compare reverse Gaussians", BLUE)
    box(ax, (3.25, 2.5, 2.6, .9), "Mean prediction", r"$\|\widetilde{\mu}_t-\mu_\theta\|^2$", BLUE)
    box(ax, (6.35, 2.5, 2.65, .9), "Reparameterize", r"$\mu_\theta=A_tx_t-B_t\epsilon_\theta$", BLUE)
    box(ax, (.25, .9, 2.5, .9), "Score matching", r"$s_t=\nabla\log p_t$", GREEN)
    box(ax, (3.25, .9, 2.6, .9), "Gaussian teacher", r"$\nabla\log q_t=-\epsilon/b_t$", GREEN)
    box(ax, (6.35, .9, 2.65, .9), "Reparameterize", r"$s_\theta=-\epsilon_\theta/b_t$", GREEN)
    for y in (2.95, 1.35):
        arrow(ax, (2.8, y), (3.2, y))
        arrow(ax, (5.9, y), (6.3, y))
    box(ax, (10.05, 1.65, 3.0, 1.05), "Noise MSE", r"$\mathbb{E}\|\epsilon-\epsilon_\theta(x_t,t)\|^2$", PURPLE)
    arrow(ax, (9.05, 2.95), (10.0, 2.35), BLUE)
    arrow(ax, (9.05, 1.35), (10.0, 1.98), GREEN)
    ax.text(.3, .28, "Same regression target; timestep weights must be accounted for separately.",
            fontsize=11)
    save(fig, "01-loss-routes")


def mixture(points, sigma):
    """Exact density and score of a 2-D spherical Gaussian mixture."""
    variance = BASE_VAR + sigma**2
    delta = points[..., None, :] - MEANS
    logc = np.log(WEIGHTS) - np.log(2*np.pi*variance) - np.sum(delta**2, axis=-1)/(2*variance)
    logp = logsumexp(logc, axis=-1)
    responsibility = np.exp(logc - logp[..., None])
    score = np.sum(responsibility[..., None] * (-delta/variance), axis=-2)
    return np.exp(logp), score


GRID = np.linspace(-3.5, 3.5, 170)
GX, GY = np.meshgrid(GRID, GRID)
GP = np.stack((GX, GY), axis=-1)
QX, QY = np.meshgrid(np.linspace(-3.1, 3.1, 15), np.linspace(-3.1, 3.1, 15))
QP = np.stack((QX, QY), axis=-1)


def scale_scene(ax, sigma, label):
    ax.clear()
    density, _ = mixture(GP, sigma)
    _, scores = mixture(QP, sigma)
    length = np.linalg.norm(scores, axis=-1, keepdims=True)
    direction = np.divide(scores, length, out=np.zeros_like(scores), where=length > 1e-12)
    # Relative-to-peak contours reveal the shape; absolute levels vary with sigma.
    ax.contourf(GX, GY, density / density.max(),
                levels=[.02, .08, .2, .4, .7, 1.001],
                colors=["#edf8f6", "#d2eee8", "#9cd8cb", "#58b5a2", "#188975"])
    ax.quiver(QX, QY, direction[..., 0], direction[..., 1],
              color=BLUE, angles="xy", scale_units="xy", scale=5.1, width=.0045, alpha=.8)
    ax.scatter(MEANS[:, 0], MEANS[:, 1], marker="x", c=ORANGE, s=48, linewidths=2, zorder=5)
    ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5), aspect="equal",
           xlabel="coordinate 1", ylabel="coordinate 2")
    ax.set_title(label + "\n" + r"$\sigma=$" + f"{sigma:.2f}", fontsize=12, pad=9)
    ax.set_xticks([-3, 0, 3])
    ax.set_yticks([-3, 0, 3])


def scales():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.8))
    for ax, sigma, label in zip(axes, [2.0, .8, .15],
                                ["Broad structure", "Separate possibilities", "Resolve local structure"]):
        scale_scene(ax, sigma, label)
    fig.suptitle("Less noise reveals a more detailed score field", fontsize=17, weight="bold", y=.99)
    fig.text(.5, .02, "Exact toy density: 3 Gaussian clusters. Arrows show direction only; axes stay fixed.",
             ha="center", fontsize=10)
    fig.subplots_adjust(left=.06, right=.99, bottom=.13, top=.82, wspace=.27)
    save(fig, "02-score-scales")

    fig, ax = plt.subplots(figsize=(6.2, 6.5))
    fig.subplots_adjust(left=.13, right=.96, bottom=.16, top=.82)
    fig.suptitle("From broad to fine", fontsize=17, weight="bold", y=.98)
    fig.text(.5, .055, "Direction field at each noise level; no particle trajectory.\n"
             "Orange crosses = clean component centers. Colors scale to each peak.",
             ha="center", fontsize=9)
    sigmas = np.r_[np.repeat(2., 7), np.geomspace(2., .8, 18)[1:],
                   np.repeat(.8, 7), np.geomspace(.8, .15, 23)[1:], np.repeat(.15, 12)]

    def frame(i):
        sigma = sigmas[i]
        label = "Broad structure" if sigma > 1.2 else (
            "Separate possibilities" if sigma > .45 else "Resolve local structure")
        scale_scene(ax, sigma, label)

    animation = FuncAnimation(fig, frame, frames=len(sigmas), interval=125, repeat=True)
    animation.save(OUT / "03-score-scales.gif", writer=PillowWriter(fps=8), dpi=100)
    plt.close(fig)
    with Image.open(OUT / "03-score-scales.gif") as gif:
        frame_ids = sorted(set([0, gif.n_frames//4, gif.n_frames//2,
                                3*gif.n_frames//4, gif.n_frames-1]))
        contact = Image.new("RGB", (310*len(frame_ids), 350), "white")
        draw = ImageDraw.Draw(contact)
        for j, i in enumerate(frame_ids):
            gif.seek(i)
            thumb = gif.convert("RGB")
            thumb.thumbnail((310, 325))
            contact.paste(thumb, (310*j, 18))
            draw.text((310*j+8, 3), f"Decoded GIF frame {i}", fill=INK)
        contact.save(OUT / "03-gif-inspection.png")
        return {"decoded_frames": gif.n_frames, "inspected_frame_ids": frame_ids}


def conditioning():
    fig, ax = plt.subplots(figsize=(14.4, 6.6))
    ax.set(xlim=(0, 14.5), ylim=(0, 6.7))
    ax.axis("off")
    ax.text(.25, 6.35, "Text changes the prediction; guidance combines two predictions", fontsize=17, weight="bold")
    box(ax, (.25, 4.5, 2.35, .8), "Negative / empty", "baseline prompt", ORANGE)
    box(ax, (.25, 2.9, 2.35, .8), "Positive prompt", "requested content", GREEN)
    box(ax, (3.2, 3.6, 1.85, 1.05), "Text encoder", "token embeddings", PURPLE)
    arrow(ax, (2.65, 4.9), (3.15, 4.35), ORANGE)
    arrow(ax, (2.65, 3.3), (3.15, 3.9), GREEN)
    box(ax, (6., 4.6, 2.4, .85), "Denoiser call 1", r"$\epsilon_-=\epsilon_\theta(z_t,t,c_-)$", ORANGE)
    box(ax, (6., 2.95, 2.4, .85), "Denoiser call 2", r"$\epsilon_+=\epsilon_\theta(z_t,t,c_+)$", GREEN)
    arrow(ax, (5.1, 4.35), (5.95, 5.0), ORANGE)
    arrow(ax, (5.1, 3.9), (5.95, 3.4), GREEN)
    ax.text(7.2, 4.12, "shared model weights", ha="center", fontsize=9)
    box(ax, (9.1, 3.75, 2.35, .95), "Guidance", r"$\epsilon_-+w(\epsilon_+-\epsilon_-)$", PURPLE)
    arrow(ax, (8.45, 5.0), (9.05, 4.45), ORANGE)
    arrow(ax, (8.45, 3.4), (9.05, 3.98), GREEN)
    box(ax, (12.0, 3.75, 1.9, .95), "Sampler step", r"$z_t\ \longrightarrow\ z_s$", BLUE)
    arrow(ax, (11.5, 4.22), (11.95, 4.22))
    box(ax, (6.05, 1.12, 2.3, .9), "Same inputs", r"noisy latent $z_t$, time $t$", BLUE)
    arrow(ax, (7.2, 2.06), (7.2, 2.9), BLUE)
    # Route the second shared-input branch around the denoiser boxes.
    ax.plot([6.1, 5.55, 5.55], [1.57, 1.57, 4.73], color=BLUE, linewidth=1.2)
    arrow(ax, (5.55, 4.73), (5.95, 4.73), BLUE)
    box(ax, (11.95, 1.12, 2.0, .9), "Random draw", "stochastic samplers", ORANGE)
    arrow(ax, (12.95, 2.07), (12.95, 3.7), ORANGE)
    ax.plot([8.4, 8.8, 11.15], [1.57, 2.53, 2.53], color=BLUE, linewidth=1.2)
    arrow(ax, (11.15, 2.53), (12.15, 3.7), BLUE)
    ax.text(9.4, 2.69, "state + schedule", fontsize=9, color=BLUE)
    ax.plot([12.1, 11.7, 11.7, 7.2, 7.2], [3.78, 3.22, .5, .5, .75],
            color=BLUE, linewidth=1.2, linestyle="--")
    arrow(ax, (7.2, .75), (7.2, 1.06), BLUE, "--")
    ax.text(9.2, .69, "update latent + time; repeat", ha="center", fontsize=9, color=BLUE)
    box(ax, (11.95, 5.35, 2.0, .65), "VAE decoder", color=GREEN)
    arrow(ax, (12.95, 4.75), (12.95, 5.3), GREEN)
    ax.text(12.12, 5.03, "at the end", fontsize=9)
    ax.text(.25, 1.25, "Conditioning enters each model call.\n"
            "Guidance happens after the calls.\n"
            "No text-vector subtraction is required.", fontsize=11, linespacing=1.7)
    save(fig, "04-conditioning-flow")


def math_checks():
    errors = {}
    rng = np.random.default_rng(20261115)
    points = rng.normal(size=(80, 2))
    sigma, h = .7, 1e-5
    p, score = mixture(points, sigma)
    numerical = np.empty_like(points)
    for j in range(2):
        delta = np.eye(2)[j]*h
        numerical[:, j] = (np.log(mixture(points+delta, sigma)[0])
                            - np.log(mixture(points-delta, sigma)[0]))/(2*h)
    errors["mixture_score_finite_difference"] = float(np.max(abs(score-numerical)))

    # 1-D mixture: check DSM equality by independent Gaussian quadrature over
    # the latent component, clean data, and noisy observation.
    means, weights, v0, b = np.array([-1.2, .9]), np.array([.4, .6]), .16, .7
    v = v0 + b*b
    def p1(y):
        return np.dot(weights, norm.pdf(y, means, np.sqrt(v)))
    def score1(y):
        responsibility = weights*norm.pdf(y, means, np.sqrt(v))
        return np.dot(responsibility, (means-y)/v)/responsibility.sum()
    def expectation(fun):
        return quad(lambda y: p1(y)*fun(y), -12, 12, epsabs=1e-10)[0]
    marginal = []
    conditional = []
    for k in [.3, .9, 1.5]:
        marginal.append(.5*expectation(lambda y: (-k*y-score1(y))**2))
        # r=-epsilon/b; E[epsilon^2]=1 and E[y*epsilon]=b exactly.
        ey2 = v + np.dot(weights, means**2)
        conditional.append(.5*(k*k*ey2 - 2*k + 1/(b*b)))
    gaps = np.array(conditional)-marginal
    errors["DSM_objective_constant_across_predictors"] = float(np.ptp(gaps))
    # Fisher identity by direct integration over clean x (no score1 formula).
    identity_errors = []
    for y in [-2.1, -.2, .6, 2.]:
        def p0(x):
            return np.dot(weights, norm.pdf(x, means, np.sqrt(v0)))
        numerator = quad(lambda x: p0(x)*norm.pdf(y, x, b)*(x-y)/(b*b),
                         -12, 12, epsabs=1e-11)[0]
        identity_errors.append(abs(numerator/p1(y)-score1(y)))
    errors["conditional_score_integral"] = max(identity_errors)
    # Integration by parts sign under N(0,1), s=-k*x+c*x^3.
    k, c = .6, .05
    implicit = quad(lambda x: norm.pdf(x)*(.5*(-k*x+c*x**3)**2-k+3*c*x*x),
                    -12, 12)[0]
    direct = .5*quad(lambda x: norm.pdf(x)*(-k*x+c*x**3+x)**2, -12, 12)[0]
    errors["implicit_score_matching_constant"] = abs(direct-implicit-.5)

    betas = np.linspace(.001, .02, 40)
    alphas = 1-betas
    bars = np.r_[1., np.cumprod(alphas)]
    mu_errors, ddim_errors = [], []
    for t in [2, 14, 40]:
        s = t-1
        posterior_variance = betas[t-1]*(1-bars[s])/(1-bars[t])
        rho2 = betas[t-1]
        x, eps, pred = rng.normal(size=(3, 8))
        coefficient = betas[t-1]/np.sqrt(alphas[t-1]*(1-bars[t]))
        mu_true = x/np.sqrt(alphas[t-1])-coefficient*eps
        mu_model = x/np.sqrt(alphas[t-1])-coefficient*pred
        actual = np.sum((mu_true-mu_model)**2)/(2*rho2)
        predicted = betas[t-1]**2/(2*rho2*alphas[t-1]*(1-bars[t]))*np.sum((eps-pred)**2)
        mu_errors.append(abs(actual-predicted))
        sigma2 = (1-bars[s])/(1-bars[t])*(1-bars[t]/bars[s])
        ddim_errors.append(abs(sigma2-posterior_variance))
        x0hat = (x-np.sqrt(1-bars[t])*pred)/np.sqrt(bars[t])
        ddim_mean = np.sqrt(bars[s])*x0hat + np.sqrt(1-bars[s]-sigma2)*pred
        ddim_errors.append(float(np.max(abs(ddim_mean-mu_model))))
    errors["ELBO_noise_MSE_weight"] = max(mu_errors)
    errors["DDIM_eta1_adjacent_posterior"] = max(ddim_errors)

    # Exact Gaussian class conditionals: Bayes, CFG and negative-prompt scores.
    var, mplus, mminus = 1.2, 1., -1.
    def densities(x):
        return norm.pdf(x, mplus, np.sqrt(var)), norm.pdf(x, mminus, np.sqrt(var))
    def log_class_posterior(x):
        plus, minus = densities(x)
        return np.log(plus/(plus+minus))
    x = np.linspace(-3, 3, 31)
    plus, minus = densities(x)
    sp, sm = (mplus-x)/var, (mminus-x)/var
    su = (plus*sp+minus*sm)/(plus+minus)
    derivative = (log_class_posterior(x+h)-log_class_posterior(x-h))/(2*h)
    errors["classifier_Bayes_score"] = float(np.max(abs((sp-su)-derivative)))
    w = 2.5
    def tilted_log_density(y):
        pp, pm = densities(y)
        return w*np.log(pp)+(1-w)*np.log(pm)
    tilted_diff = (tilted_log_density(x+h)-tilted_log_density(x-h))/(2*h)
    errors["negative_prompt_tilt_score"] = float(np.max(abs(sm+w*(sp-sm)-tilted_diff)))
    epsp, epsm = -b*sp, -b*sm
    errors["guidance_epsilon_score_sign"] = float(np.max(abs(
        -(epsm+w*(epsp-epsm))/b-(sm+w*(sp-sm)))))

    # Flow matching reindexed t=0 data, t=1 noise.
    t, var0, mean0 = .37, .5, .8
    vart = (1-t)**2*var0+t*t
    scoret = -(x-(1-t)*mean0)/vart
    clean_mean = mean0+(1-t)*var0/vart*(x-(1-t)*mean0)
    eps_mean = t/vart*(x-(1-t)*mean0)
    errors["flow_velocity_score_conversion"] = float(np.max(abs(
        eps_mean-clean_mean+(x+t*scoret)/(1-t))))
    # Brownian example: at the target marginal, reverse SDE and ODE both
    # shrink variance at rate -1; deleting SDE noise gives rate -2.
    errors["reverse_SDE_variance_rate"] = abs((-2+1)-(-1))
    errors["probability_flow_ODE_variance_rate"] = abs(-1-(-1))
    assert all(e < 2e-8 for e in errors.values()), errors
    return {"status": "PASS", "maximum_absolute_errors": errors,
            "mean_only_deleted_noise_variance_rate": -2,
            "analytic_assumptions": [
                "Differentiation under the integral and finite squared scores for DSM",
                "Vanishing p*s boundary flux for integration by parts",
                "Exact scores and continuous time for shared SDE/ODE marginals",
                "Guidance density interpretation at fixed time, when normalizable",
                "DDIM eta=1 comparison uses adjacent times and posterior variance",
            ]}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    results = math_checks()
    loss_routes()
    results["gif"] = scales()
    conditioning()
    for path in OUT.glob("*.svg"):
        ET.parse(path)
    (OUT / "constructed-data.json").write_text(json.dumps({
        "means": MEANS.tolist(), "weights": WEIGHTS.tolist(),
        "clean_component_variance": BASE_VAR, "shown_noise_sd": [2., .8, .15],
        "axes": [-3.5, 3.5], "arrow_lengths": "normalized; directions only",
        "color_scale": "density divided by frame-specific peak",
        "source": "original constructed example; not recovered video data"
    }, indent=2)+"\n", encoding="utf-8")
    results["sha256"] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OUT.iterdir()) if p.name != "checks.json" and p.is_file()
    }
    (OUT / "checks.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
