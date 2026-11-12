"""Reproduce the introductory Bayes GIF and its static keyframes, offline.

Run this file with Python, numpy, matplotlib and Pillow. Outputs stay beside it.
The supplied Steve model is illustrative, not an empirical population claim.
Unlike a morph into a normalized bar, this animation uses only translations and
a rigid 90-degree rotation after the evidence rectangles have been revealed.
Every screen area is preserved, and the camera never changes scale.
"""

from pathlib import Path
from fractions import Fraction as F
import json
import math
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
BG, INK, MUTED = "#f7f8fa", "#172b40", "#65758a"
BLUE, ORANGE, GRAY = "#307eae", "#d49b43", "#e6ebf0"
WIDTH, HEIGHT = 1120, 780
FPS = 12.5                     # GIF can encode an exact 80 ms frame duration.
TOTAL_SECONDS = 17.6
WHOLE = (140., 220., 840., 400.)
PIVOT = np.array([80., 495.])
BLUE_AREA, ORANGE_AREA = 6400., 32000.
PIXELS_PER_PERSON = 1600.
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13,
    "text.color": INK, "figure.facecolor": BG, "svg.fonttype": "none",
})


def ease(t):
    t = float(np.clip(t, 0., 1.))
    return t*t*(3.-2.*t)


def rectangle(x, y, w, h):
    return np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])


def phase(t):
    # Separate revealing, translating, rotating and joining; hold the endpoints.
    if t < 2.0:
        return "whole", 0.
    if t < 4.8:
        return "reveal", ease((t-2.)/1.5)
    if t < 7.2:
        return "extract", ease((t-4.8)/1.8)
    if t < 9.8:
        return "rotate", ease((t-7.2)/2.)
    if t < 11.6:
        return "join", ease((t-9.8)/1.2)
    return "ratio", 1.


def polygons(t):
    name, u = phase(t)
    original_b = rectangle(140., 460., 40., 160.)
    original_o = rectangle(180., 580., 800., 40.)
    lifted_b = rectangle(40., 335., 40., 160.)
    lifted_o = rectangle(280., 455., 800., 40.)
    if name == "whole":
        return name, u, rectangle(140., 620., 40., 0.), rectangle(180., 620., 800., 0.)
    if name == "reveal":
        return name, u, rectangle(140., 620.-160.*u, 40., 160.*u), rectangle(180., 620.-40.*u, 800., 40.*u)
    if name == "extract":
        return name, u, original_b + u*np.array([-100., -125.]), original_o + u*np.array([100., -125.])
    angle = (u if name == "rotate" else 1.)*math.pi/2.
    rotation = np.array([[math.cos(angle), -math.sin(angle)],
                         [math.sin(angle), math.cos(angle)]])
    blue = (lifted_b-PIVOT) @ rotation.T + PIVOT
    orange = lifted_o.copy()
    if name in ("join", "ratio"):
        orange += np.array([-40.*u, 0.])
    return name, u, blue, orange


def area(poly):
    x, y = poly.T
    return abs(float(x @ np.roll(y, 1)-y @ np.roll(x, 1)))/2.


def text(ax, x, y, s, size=15, color=INK, align="left", weight="normal", alpha=1.):
    return ax.text(x, y, s, fontsize=size, color=color, ha=align,
                   va="center", weight=weight, alpha=alpha)


def label_arrow(ax, label, xy, xytext, color, align="left", alpha=1.):
    ax.annotate(label, xy=xy, xytext=xytext, ha=align, va="center",
                fontsize=15, color=color, alpha=alpha,
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": color,
                            "alpha": alpha, "connectionstyle": "arc3,rad=0.04"})


HEADINGS = {
    "whole": ("1   Start with one big rectangle", "Its whole area represents 210 people: 10 librarians and 200 farmers."),
    "reveal": ("2   Color the people matching the description", "Retain 40% of the librarian column and 10% of the farmer column."),
    "extract": ("3   Keep only the two colored pieces", "Discard the gray remainder; the colored areas are still 4 and 20."),
    "rotate": ("4   Tip the blue piece onto its side", "Rotate 90 degrees: same area, now the same height as orange."),
    "join": ("4   Slide the pieces side by side", "Nothing is stretched: equal heights let widths show the area ratio."),
    "ratio": ("5   Compare blue with the combined colored area", "Among everyone matching the description, what fraction are librarians?"),
}


def draw(fig, ax, t):
    ax.clear()
    ax.set(xlim=(0, WIDTH), ylim=(HEIGHT, 0))
    ax.set_aspect("equal")
    ax.axis("off")
    name, u, blue, orange = polygons(t)
    text(ax, 65, 51, "Bayes' rule, by moving areas", 26, weight="bold")
    text(ax, 65, 109, HEADINGS[name][0], 20, weight="bold")
    text(ax, 65, 151, HEADINGS[name][1], 13.5, MUTED)

    whole_alpha = 1. if name in ("whole", "reveal") else (1.-u if name == "extract" else 0.)
    if whole_alpha > 0.:
        x, y, w, h = WHOLE
        ax.add_patch(Rectangle((x, y), w, h, facecolor=GRAY,
                               edgecolor="#8796a8", lw=1.6, alpha=whole_alpha))
        ax.plot([180, 180], [220, 620], color="#aab7c7", lw=1.3, alpha=whole_alpha)
        label_arrow(ax, "10 librarians", (160, 220), (140, 190), BLUE, alpha=whole_alpha)
        text(ax, 580, 190, "200 farmers", 15, "#986411", "center", alpha=whole_alpha)
        if name == "whole":
            text(ax, 570, 385, "Whole population", 24, MUTED, "center")
            text(ax, 570, 430, "total area = 210 people", 17, MUTED, "center")
        if name == "reveal":
            label_arrow(ax, "40% of 10 = 4", (160, 500), (275, 365), BLUE, alpha=u)
            label_arrow(ax, "10% of 200 = 20", (700, 600), (570, 465), "#986411", alpha=u)

    if name != "whole":
        for poly, color, count, ink in [(blue, BLUE, "4", "white"), (orange, ORANGE, "20", INK)]:
            ax.add_patch(Polygon(poly, closed=True, facecolor=color, edgecolor=BG, lw=1.1))
            if name != "reveal" or u == 1.:
                center = poly.mean(axis=0)
                text(ax, *center, count, 18, ink, "center", "bold")

    if name in ("rotate", "join", "ratio"):
        ax.plot([40, 1080], [497, 497], color="#bcc6d2", lw=1., ls=(0, (4, 4)), zorder=0)
    if name in ("extract", "rotate", "join"):
        text(ax, 560, 630, "Moving and rotating preserve area", 20, align="center", weight="bold")
        text(ax, 560, 673, "Blue = 4 people     Orange = 20 people", 16, MUTED, "center")
    if name == "ratio":
        text(ax, 160, 420, "Librarians", 15, BLUE, "center")
        text(ax, 640, 420, "Farmers", 15, "#986411", "center")
        ax.plot([80, 80, 1040, 1040], [516, 531, 531, 516], color=MUTED, lw=1.4)
        text(ax, 560, 557, "All matching descriptions: 4 + 20 = 24", 16, align="center")
        text(ax, 223, 628, r"$P(H\mid E)=$", 24)
        text(ax, 592, 605, "blue area", 20, BLUE, "center")
        ax.plot([420, 765], [627, 627], color=INK, lw=1.8)
        text(ax, 430, 650, "blue area", 18, BLUE)
        text(ax, 566, 650, "+", 18)
        text(ax, 600, 650, "orange area", 18, "#986411")
        text(ax, 800, 628, r"$=\frac{1}{6}$", 25)
        text(ax, 560, 702, r"$\frac{4}{4+20}=\frac{1}{6}\approx 16.7\%$", 24, align="center", weight="bold")
    else:
        footer = "Column widths encode the 10 : 200 prior ratio." if name == "whole" else (
            "Area = column width x retained height." if name == "reveal" else "Same scale throughout; no resizing or normalization of the pieces.")
        text(ax, 560, 708, footer, 13, MUTED, "center")

    text(ax, 560, 756, "Illustrative Steve model   |   Blue: librarian   Orange: farmer   |   Fixed camera", 10.5, MUTED, "center")


def make_canvas():
    fig = plt.figure(figsize=(WIDTH/100., HEIGHT/100.), dpi=100, facecolor=BG)
    return fig, fig.add_axes([0, 0, 1, 1])


def verify_geometry():
    priors = [F(10, 210), F(200, 210)]
    likelihoods = [F(2, 5), F(1, 10)]
    evidence = sum(p*l for p, l in zip(priors, likelihoods))
    posterior = priors[0]*likelihoods[0]/evidence
    assert posterior == F(1, 6)
    assert F(4, 210) == priors[0]*likelihoods[0]
    assert F(20, 210) == priors[1]*likelihoods[1]
    max_area_error, max_ratio_error, max_rigidity_error = 0., 0., 0.
    min_gap = float("inf")
    for t in np.linspace(4.8, TOTAL_SECONDS, 2001):
        name, u, b, o = polygons(float(t))
        ab, ao = area(b), area(o)
        max_area_error = max(max_area_error, abs(ab-BLUE_AREA), abs(ao-ORANGE_AREA))
        max_ratio_error = max(max_ratio_error, abs(ab/(ab+ao)-1/6))
        for poly, sides in [(b, [40., 160., 40., 160.]), (o, [800., 40., 800., 40.])]:
            lengths = np.linalg.norm(np.roll(poly, -1, axis=0)-poly, axis=1)
            max_rigidity_error = max(max_rigidity_error, float(np.max(np.abs(lengths-sides))))
        min_gap = min(min_gap, float(o[:, 0].min()-b[:, 0].max()))
        assert np.all(b[:, 0] >= 0) and np.all(o[:, 0] <= WIDTH)
    _, _, b, o = polygons(13.)
    assert np.allclose(b[:, 1].min(), o[:, 1].min())
    assert np.allclose(b[:, 1].max(), o[:, 1].max())
    assert np.allclose(b[:, 0].max(), o[:, 0].min())
    assert np.isclose(np.ptp(b[:, 0])/np.ptp(o[:, 0]), 1/5)
    assert max_area_error < 1e-7 and max_rigidity_error < 1e-9 and min_gap > -1e-9
    return {
        "model": {"population": [10, 200], "likelihoods": ["2/5", "1/10"],
                  "retained_counts": [4, 20], "posterior_librarian": str(posterior)},
        "geometry": {"whole_rectangle_xywh": WHOLE, "pixels_squared_per_person": PIXELS_PER_PERSON,
                     "blue_area": BLUE_AREA, "orange_area": ORANGE_AREA, "rotation_pivot_xy": PIVOT.tolist(),
                     "rotation_degrees": 90, "final_widths": [160, 800], "final_common_height": 40},
        "checks": {"samples": 2001, "maximum_area_error": max_area_error,
                   "maximum_ratio_error": max_ratio_error, "maximum_side_length_error": max_rigidity_error,
                   "minimum_horizontal_gap": min_gap, "equal_final_heights": True,
                   "pieces_touch_without_overlapping": True, "camera_fixed": True},
        "interpretation": "The retained area is 24/210 of the original area. The blue fraction within it is 4/24, not 24/4. No stretching or zoom occurs.",
    }


def main():
    report = verify_geometry()
    fig, ax = make_canvas()
    keyframes = [(1., "01a-whole-population"), (4.4, "01b-retained-areas"), (13., "01c-side-by-side-ratio")]
    for t, name in keyframes:
        draw(fig, ax, t)
        fig.savefig(HERE/f"{name}.svg", facecolor=BG)
        fig.savefig(HERE/f"{name}.png", dpi=100, facecolor=BG)
        ET.parse(HERE/f"{name}.svg")

    # Build one fixed palette from all important phases to avoid color flicker.
    samples = [1., 3., 4.4, 6., 7.5, 8.2, 9.5, 10.3, 13.]
    palette_sheet = Image.new("RGB", (WIDTH, HEIGHT*len(samples)), BG)
    for row, t in enumerate(samples):
        draw(fig, ax, t)
        fig.canvas.draw()
        rgb = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy())
        palette_sheet.paste(rgb, (0, row*HEIGHT))
    palette = palette_sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    frames = []
    requested = int(round(TOTAL_SECONDS*FPS))
    for k in range(requested):
        draw(fig, ax, k/FPS)
        fig.canvas.draw()
        frame = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy())
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))
    gif = HERE/"01-bayes-area-update.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=80,
                   loop=0, optimize=False, disposal=1)
    plt.close(fig)

    # Decode the actual saved GIF; identical hold frames may have been merged.
    decoded = Image.open(gif)
    durations, starts, elapsed = [], [], 0
    for k in range(decoded.n_frames):
        decoded.seek(k)
        starts.append(elapsed)
        duration = decoded.info.get("duration", 0)
        durations.append(duration)
        elapsed += duration
        assert decoded.size == (WIDTH, HEIGHT)
    assert elapsed == requested*80
    picks = []
    contact = Image.new("RGB", (WIDTH//2*3, (HEIGHT//2+30)*3), "white")
    for slot, t in enumerate(samples):
        idx = min(np.searchsorted(starts, int(t*1000), side="right")-1, decoded.n_frames-1)
        decoded.seek(int(idx))
        thumb = decoded.convert("RGB").resize((WIDTH//2, HEIGHT//2), Image.Resampling.LANCZOS)
        x, y = slot % 3*(WIDTH//2), slot//3*(HEIGHT//2+30)
        contact.paste(thumb, (x, y))
        ImageDraw.Draw(contact).text((x+12, y+HEIGHT//2+7), f"{t:.1f}s | saved frame {idx} | {phase(t)[0]}", fill="black")
        picks.append({"time_seconds": t, "saved_frame": int(idx), "phase": phase(t)[0]})
    contact.save(HERE/"intro-animation-contact-sheet.png")
    report["render"] = {"gif": gif.name, "requested_frames": requested, "saved_frames": decoded.n_frames,
                        "duration_ms": elapsed, "size": [WIDTH, HEIGHT], "loop": "infinite",
                        "keyframes": [name+".svg" for _, name in keyframes], "decoded_samples": picks,
                        "visual_review": "Pending inspection of decoded contact sheet and static previews; no live Obsidian claim."}
    (HERE/"intro-animation-checks.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
