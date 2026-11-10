"""Render the selected source PDF page without retouching it.

Run: python render_source_page.py --pdftoppm /path/to/pdftoppm
Requires Poppler. The PDF stays immutable; the PNG is a derived preview.
"""
from pathlib import Path
import argparse
import hashlib
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--pdftoppm',default='pdftoppm')
args=parser.parse_args()
out=Path(__file__).resolve().parent
vault=out.parents[2]
pdf=vault/'raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics.pdf'
assert hashlib.sha256(pdf.read_bytes()).hexdigest()=='e0d659f47f63bf99d9b196621aafe6a95ca5cfdd03a4105b24e7d24d0c8075ab'
subprocess.run([args.pdftoppm,'-f','4','-l','4','-scale-to','2200','-png','-singlefile',str(pdf),str(out/'source-pdf-page-04')],check=True)
