"""Focused SVG viewports of the existing, unchanged four-view illustration.

Run with Python 3 (standard library only). No source figure is regenerated.
Each output changes the outer SVG viewport and display dimensions and trims
line-end whitespace. Descendant geometry, labels and definitions are retained.
"""
from pathlib import Path
from statistics import NormalDist
from fractions import Fraction
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / "2026-11-10-testing-power" / "roc-error-rates.svg"
PANELS = {
    "roc-operating-point.svg": (615, 70, 485, 365),
    "two-error-areas.svg": (48, 70, 470, 333),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def svg_signature(node, root=False):
    """Ignore only outer viewport fields and XML/SVG whitespace formatting."""
    attrs = {key: " ".join(value.split()) for key, value in node.attrib.items()
             if not (root and key in ("width", "height", "viewBox"))}
    return (node.tag, attrs, " ".join((node.text or "").split()),
            " ".join((node.tail or "").split()),
            [svg_signature(child) for child in node])


def main():
    original = SOURCE.read_bytes()
    text = original.decode("utf-8")
    root = re.search(r"<svg\b[^>]*>", text)
    assert root is not None
    original_tag = root.group()
    manifest = {}
    for name, (x, y, width, height) in PANELS.items():
        assert 0 <= x < x + width <= 1152
        assert 0 <= y < y + height <= 792
        tag = re.sub(r'\bwidth="[^"]+"', f'width="{width}pt"', original_tag)
        tag = re.sub(r'\bheight="[^"]+"', f'height="{height}pt"', tag)
        tag = re.sub(r'\bviewBox="[^"]+"', f'viewBox="{x} {y} {width} {height}"', tag)
        output = text[:root.start()] + tag + text[root.end():]
        # Substituting the old root tag back must recover every original byte.
        assert output.replace(tag, original_tag, 1).encode("utf-8") == original
        output = "\n".join(line.rstrip() for line in output.splitlines()) + "\n"
        assert svg_signature(ET.fromstring(output), root=True) == svg_signature(ET.fromstring(text), root=True)
        path = OUT / name
        path.write_bytes(output.encode("utf-8"))
        manifest[name] = {"viewBox": [x, y, width, height], "sha256": digest(path.read_bytes())}
    assert SOURCE.read_bytes() == original

    normal = NormalDist()
    cutoff = normal.inv_cdf(.95)
    separation = cutoff + normal.inv_cdf(.8)
    fpr = 1 - normal.cdf(cutoff)
    power = 1 - normal.cdf(cutoff - separation)
    assert math.isclose(fpr, .05, abs_tol=1e-14)
    assert math.isclose(power, .8, abs_tol=1e-14)
    tp, fn, fp, tn = map(Fraction, (80, 20, 45, 855))
    rates = {
        "recall_power": tp / (tp + fn),
        "false_positive_rate": fp / (fp + tn),
        "type_II": fn / (tp + fn),
        "specificity": tn / (tn + fp),
        "precision": tp / (tp + fp),
        "accuracy": (tp + tn) / (tp + fn + fp + tn),
    }
    assert list(rates.values()) == list(map(Fraction, (".8", ".05", ".2", ".95", ".64", ".935")))
    prevalence = Fraction(1, 100)
    rare_precision = prevalence * rates["recall_power"] / (
        prevalence * rates["recall_power"] + (1 - prevalence) * rates["false_positive_rate"]
    )
    assert rare_precision == Fraction(16, 115)
    auc = normal.cdf(separation / math.sqrt(2))
    assert math.isclose(auc, .9606435325062272, abs_tol=1e-14)
    # Independent finite-score check of interpolated AUC's half-tie convention.
    positives, negatives = [3, 2, 1], [2, 1, 0]
    pair_auc = sum(Fraction(int(p > n)) + Fraction(int(p == n), 2)
                   for p in positives for n in negatives) / (len(positives) * len(negatives))
    empirical = [(Fraction(0), Fraction(0))]
    for threshold in sorted(set(positives + negatives), reverse=True):
        empirical.append((Fraction(sum(n >= threshold for n in negatives), len(negatives)),
                          Fraction(sum(p >= threshold for p in positives), len(positives))))
    strip_auc = sum((x1-x0)*(y1+y0)/2 for (x0,y0),(x1,y1) in zip(empirical, empirical[1:]))
    assert strip_auc == pair_auc == Fraction(7, 9)
    previous = (0, 0)
    for threshold in [8 - i * 13 / 2000 for i in range(2001)]:
        point = (1 - normal.cdf(threshold), 1 - normal.cdf(threshold - separation))
        assert point[0] >= previous[0] and point[1] >= previous[1]
        previous = point
    result = {
        "source": "assets/figures/2026-11-10-testing-power/roc-error-rates.svg",
        "source_sha256": digest(original),
        "method": "Outer SVG viewport/dimensions changed; line-end whitespace trimmed; descendant geometry/labels unchanged",
        "panels": manifest,
        "exact_rates": {key: str(value) for key, value in rates.items()},
        "precision_at_one_percent_prevalence": str(rare_precision),
        "normal_model": {"cutoff": cutoff, "separation": separation, "FPR": fpr, "power": power, "AUC": auc},
        "empirical_AUC_with_ties": {"pair_counting": str(pair_auc), "ROC_trapezoids": str(strip_auc)},
        "checks": "PASS: XML; crop bounds; unchanged source/geometry; exact count fractions; complements; Bayes; AUC with ties; 2001 monotone ROC points",
    }
    (OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["checks"])


if __name__ == "__main__":
    main()
