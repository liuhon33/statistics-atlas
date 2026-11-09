"""Reproduce the p. 5 diagram extraction; preserve the archived PDF unchanged.

Usage: python extract_diagram.py --pdftoppm /path/to/pdftoppm
Coordinates are in the 1,600-pixel-high Poppler page rendering.
This renders a rectangular excerpt of the PDF; it does not reconstruct its art.
"""

from pathlib import Path
import argparse
import hashlib
import subprocess
import tempfile

SOURCE_SHA256 = "f1f23310c8264ab64d4199c5d9178a91b07786d29de985ea35f97f58418509cf"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdftoppm", default="pdftoppm")
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    vault = folder.parents[2]
    source = vault / "raw/conversations/2026-10-18-Clarify-Probability-Error.pdf"
    source_bytes = source.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256
    destination = folder / "pdf-p05-corrected-event-region.png"
    with tempfile.TemporaryDirectory(prefix="probability-pdf-extract-") as temp:
        prefix = Path(temp) / "diagram"
        subprocess.run(
            [args.pdftoppm, "-f", "5", "-l", "5", "-singlefile",
             "-scale-to", "1600", "-x", "110", "-y", "680",
             "-W", "640", "-H", "510", "-png", str(source), str(prefix)],
            check=True,
        )
        data = prefix.with_suffix(".png").read_bytes()
    if destination.exists():
        if destination.read_bytes() != data:
            raise FileExistsError(f"Refusing to overwrite a different extraction: {destination}")
    else:
        with destination.open("xb") as stream:
            stream.write(data)
    assert source.read_bytes() == source_bytes
    print(f"{destination.name}: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
