"""Unretouched full-page renders of the preserved four-page original, pages 2 and 3.
Requires Poppler's pdftoppm on PATH; no cropping, annotations or source modification.
"""
from pathlib import Path
import shutil,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
exe=shutil.which('pdftoppm')
if not exe:raise SystemExit('Install/configure Poppler pdftoppm on PATH before rendering.')
subprocess.run([exe,'-f','2','-l','3','-scale-to','2400','-png',str(ROOT/'raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics-four-page-original.pdf'),str(HERE/'handwriting-page')],check=True)
