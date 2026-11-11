# SciNet's DAT112, Neural Network Programming.
# Lecture 7, 13 May 2025. Original code: Erik Spence.
# PyTorch translation of the lecture's reverse-diffusion recurrence.

import argparse
from pathlib import Path
import numpy as np
import torch

from unet import NaiveUnet
from ddpm import ddpm_schedules

HERE = Path(__file__).resolve().parent


@torch.no_grad()
def sample_from_model(model, config, n_sample=8, seed=42, verbose=True):
    """Sample existing weights without changing training RNG state or model mode."""
    if n_sample < 1:
        raise ValueError('n_sample must be positive.')
    device = next(model.parameters()).device
    generator = torch.Generator(device=device).manual_seed(seed)
    image_shape = config['image_shape']
    beta1, beta2, T = config['beta1'], config['beta2'], config['T']
    schedules = {k: v.to(device) for k, v in ddpm_schedules(beta1, beta2, T).items()}
    this_size = (n_sample, image_shape[2], image_shape[0], image_shape[1])
    x_t = torch.randn(this_size, device=device, generator=generator)
    # Deliberately retain the original T..0 loop, including the untrained t=0
    # evaluation. This is a lecture convention, not the usual DDPM T..1 loop.
    was_training = model.training
    model.eval()
    try:
        for i in range(T, -1, -1):
            if verbose and (i == T or i % 100 == 0):
                print(f'Denoising step {i}', flush=True)
            z = torch.randn(this_size, device=device, generator=generator) if i > 0 else 0
            t = torch.full((n_sample, 1), i / T, device=device)
            eps = model([x_t, t])
            x_t = schedules['oneover_sqrta'][i] * (
                x_t - eps * schedules['mab_over_sqrtmab'][i]
            ) + schedules['sqrt_beta_t'][i] * z
    finally:
        model.train(was_training)
    if not torch.isfinite(x_t).all():
        raise RuntimeError('Nonfinite generated image.')
    # As in the lecture, return NHWC int16 values; clip only when displaying.
    return (x_t.permute(0, 2, 3, 1).cpu().numpy() * 255).astype('int16')


@torch.no_grad()
def my_sample(image_shape=(64, 64, 3), n_sample=1, checkpoint=HERE / 'model.pt',
              device=None, seed=42, verbose=True, return_metadata=False):
    device = torch.device(device or ('cuda' if torch.cuda.is_available() else 'cpu'))
    saved = torch.load(checkpoint, map_location='cpu', weights_only=True)
    config = saved['config']
    metadata = {'epoch': saved['epoch'], 'config': config,
                'last_training_record': saved['history'][-1] if saved['history'] else None,
                'seed': seed, 'n_sample': n_sample, 'device': str(device),
                'checkpoint': str(Path(checkpoint).resolve()), 'source': 'manual'}
    if tuple(image_shape) != tuple(config['image_shape']):
        raise ValueError('image_shape does not match the checkpoint.')
    # Initializing a temporary CPU model must not advance the caller's RNG.
    with torch.random.fork_rng(devices=[]):
        model = NaiveUnet(image_shape, config['n_feat'])
    model.load_state_dict(saved['model_state_dict'])
    model = model.to(device)
    del saved  # Do not retain the training optimizer state during sampling.
    samples = sample_from_model(model, config, n_sample, seed, verbose)
    return (samples, metadata) if return_metadata else samples


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate images from a lecture 7 checkpoint.')
    parser.add_argument('--checkpoint', type=Path, default=HERE / 'model.pt')
    parser.add_argument('--output', type=Path, help='Archive root; each run creates a new epoch folder.')
    parser.add_argument('--n-sample', type=int, default=1)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--device', default=None)
    args = parser.parse_args()
    from sample_archive import save_sample_set
    samples, metadata = my_sample(n_sample=args.n_sample, checkpoint=args.checkpoint,
                                  device=args.device, seed=args.seed, return_metadata=True)
    root = args.output or args.checkpoint.resolve().parent / 'samples' / args.checkpoint.stem
    output = save_sample_set(samples, metadata, root)
    print(f'Saved {len(samples)} sample(s) to {output}', flush=True)
