"""Original Rao-Blackwell introductory diagram; run with Pillow installed.

Enumerate all 3-toss sequences to verify conditional averages exactly;
check unconditional means and variances on a probability grid.
Outputs are written beside this script, independent of the working directory.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
sequences = list(product((0, 1), repeat=3))
for t in range(4):
    group = [x for x in sequences if sum(x) == t]
    assert Fraction(sum(x[0] for x in group), len(group)) == Fraction(t, 3)
for p in map(lambda k: Fraction(k, 20), range(21)):
    weights = [p ** sum(x) * (1-p) ** (3-sum(x)) for x in sequences]
    old = [Fraction(x[0]) for x in sequences]
    new = [Fraction(sum(x), 3) for x in sequences]
    for vals, variance in [(old, p*(1-p)), (new, p*(1-p)/3)]:
        assert sum(w*v for w, v in zip(weights, vals)) == p
        assert sum(w*(v-p)**2 for w, v in zip(weights, vals)) == variance

im = Image.new("RGB", (1600, 700), "#f8fafc")
d = ImageDraw.Draw(im)
ink, blue, teal = "#182c43", "#285ea8", "#087e82"
def label(x, y, s, size=28, color=ink, bold=False, anchor="la"):
    font = ImageFont.truetype("C:/Windows/Fonts/" + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)
    d.text((x, y), s, font=font, fill=color, anchor=anchor)

label(50, 35, "Keep the heads count. Average away the order.", 45, bold=True)
label(50, 110, "Three independent tosses, same heads probability p; condition on T = 2 heads.", 29)
label(70, 205, "Possible order", 30, bold=True)
label(470, 205, "First-toss rule U", 30, blue, True)
for y, seq in zip((310, 430, 550), ((1, 1, 0), (1, 0, 1), (0, 1, 1))):
    for i, head in enumerate(seq):
        x = 120 + 100*i
        d.ellipse((x-38, y-38, x+38, y+38), fill=blue if head else "#e0e6ee",
                  outline=ink if i == 0 else None, width=3)
        label(x, y, "H" if head else "T", 34, "white" if head else ink, True, "mm")
    label(585, y, str(seq[0]), 46, blue, anchor="mm")
    d.line((670, y, 950, 430), fill=teal, width=4)
    d.polygon([(970, 430), (944, 417), (944, 443)], fill=teal)
d.rounded_rectangle((985, 285, 1535, 575), radius=24, fill="#e3f4f1", outline=teal, width=3)
label(1260, 340, "Conditional average", 32, teal, True, "mm")
label(1260, 430, "(1 + 1 + 0) / 3 = 2/3", 36, anchor="mm")
label(1260, 515, "New rule: U* = T / 3", 33, teal, anchor="mm")
label(70, 635, "Each order has conditional probability 1/3. H = heads; T on a coin = tails.", 27)
im.save(OUT / "conditional-average.png")
(OUT / "checks.json").write_text(json.dumps({
    "conditional_means": "Exact rational checks for all four heads counts passed",
    "mean_and_variance": "Exact rational checks for p=0, 0.05, ..., 1 passed",
    "old_variance": "p*(1-p)", "new_variance": "p*(1-p)/3",
    "scope": "Finite enumeration verifies this example, not a proof of the general theorem"
}, indent=2) + "\n", encoding="utf-8")
print("PASS: conditional averages, means, variances; PNG generated")
