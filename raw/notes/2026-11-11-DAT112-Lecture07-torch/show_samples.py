"""Generate and display a grid from the latest saved lecture 7 checkpoint.

Uses NumPy and Pillow, already installed in pytorch_learn. No Matplotlib or
Jupyter installation is needed. Run with --show to open the PNG on Windows.
"""
import argparse
from pathlib import Path

from PIL import Image

from reverse_diffusion import my_sample
from sample_archive import make_grid, save_sample_set

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, default=HERE / 'model.pt')
    parser.add_argument('--output', type=Path, help='Archive root; each run creates a fresh epoch folder.')
    parser.add_argument('--n-sample', type=int, default=8)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--device', default=None)
    parser.add_argument('--show', action='store_true', help='Open the grid in the system image viewer.')
    args = parser.parse_args()
    samples, metadata = my_sample(n_sample=args.n_sample, checkpoint=args.checkpoint,
                                  device=args.device, seed=args.seed, return_metadata=True)
    root = args.output or args.checkpoint.resolve().parent / 'samples' / args.checkpoint.stem
    output = save_sample_set(samples, metadata, root)
    print(f"Checkpoint epoch: {metadata['epoch']}", flush=True)
    print(f'Saved grid: {output / "grid.png"}', flush=True)
    if args.show:
        with Image.open(output / 'grid.png') as grid:
            grid.show()



if __name__ == '__main__':
    main()
