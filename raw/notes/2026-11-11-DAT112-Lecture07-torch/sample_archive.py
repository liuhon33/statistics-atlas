"""Save generated images in separate, never-overwritten epoch folders."""
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def make_grid(samples, metadata):
    """Enlarge actual 64x64 pixels with nearest-neighbor interpolation."""
    columns = min(4, len(samples))
    rows = (len(samples) + columns - 1) // columns
    size, margin, caption, header = 256, 20, 32, 96
    width = max(900, margin + columns * (size + margin))
    height = header + rows * (size + caption + margin)
    grid = Image.new('RGB', (width, height), '#f4f5f7')
    draw = ImageDraw.Draw(grid)
    try:
        title_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 26)
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
    except OSError:
        title_font = font = ImageFont.load_default()
    draw.text((margin, 16), 'Lecture 7: diffusion model samples', fill='#17202a', font=title_font)
    draw.text((margin, 54),
              f"Checkpoint epoch {metadata['epoch']} | seed {metadata['seed']} | 64 x 64 RGB | {metadata['config']['T'] + 1:,} reverse steps",
              fill='#465362', font=font)
    for i, sample in enumerate(samples):
        x = margin + (i % columns) * (size + margin)
        y = header + (i // columns) * (size + caption + margin)
        image = Image.fromarray(np.clip(sample, 0, 255).astype('uint8'))
        grid.paste(image.resize((size, size), Image.Resampling.NEAREST), (x, y))
        draw.text((x, y + size + 5), f'Sample {i + 1}', fill='#17202a', font=font)
    return grid


def save_sample_set(samples, metadata, root):
    """Reserve a fresh directory, then save pixels, previews, grid and provenance.

    Repeating an epoch (or two processes saving it together) creates a timestamped
    sibling. An incomplete directory is retained on failure, never overwritten.
    metadata.json is written last and marks a complete sample set.
    """
    samples = np.asarray(samples)
    if samples.ndim != 4 or samples.shape[1:] != (64, 64, 3) or len(samples) < 1:
        raise ValueError('Expected nonempty (N, 64, 64, 3) samples.')
    if not np.isfinite(samples).all():
        raise ValueError('Samples must be finite.')
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    name = f"epoch_{metadata['epoch']:06d}"
    output = root / name
    try:
        output.mkdir()  # Atomic reservation: never reuse an existing directory.
    except FileExistsError:
        prefix = f'{name}_{now:%Y%m%dT%H%M%SZ}_'
        output = Path(tempfile.mkdtemp(prefix=prefix, dir=root))
    np.save(output / 'samples.npy', samples)
    for i, sample in enumerate(samples):
        Image.fromarray(np.clip(sample, 0, 255).astype('uint8')).save(output / f'sample_{i:03d}.png')
    make_grid(samples, metadata).save(output / 'grid.png')
    record = {**metadata, 'n_sample': len(samples), 'created_at_utc': now.isoformat(),
              'raw_shape': list(samples.shape), 'raw_dtype': str(samples.dtype),
              'display': 'clip to [0,255], uint8, nearest-neighbor enlargement',
              'status': 'complete'}
    (output / 'metadata.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    return output
