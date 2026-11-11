# SciNet's DAT112, Neural Network Programming.
# Lecture 7, 13 May 2025. Original code: Erik Spence.
# PyTorch translation; originally inspired by cloneofsimo/minDiffusion.

import argparse
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from unet import NaiveUnet
from ddpm import ddpm_schedules
from reverse_diffusion import sample_from_model
from sample_archive import save_sample_set

HERE = Path(__file__).resolve().parent


class CatDataset(Dataset):
    """Read the lecture's NHWC, 0..255 array without loading it all into RAM."""
    def __init__(self, path, limit=None):
        self.data = np.load(path, mmap_mode='r', allow_pickle=False)
        if self.data.ndim != 4 or self.data.shape[1:] != (64, 64, 3):
            raise ValueError(f'Expected (N, 64, 64, 3), got {self.data.shape}.')
        self.length = len(self.data) if limit is None else min(limit, len(self.data))
        if self.length < 1:
            raise ValueError('Dataset must contain at least one image.')

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        # Preserve (data / 255).astype(float32), then NHWC -> NCHW.
        image = (self.data[index] / 255).astype('float32')
        if not np.isfinite(image).all() or image.min() < 0 or image.max() > 1:
            raise ValueError('Expected finite image values in the range 0..255.')
        return torch.from_numpy(image.transpose(2, 0, 1).copy())


def find_data():
    candidates = sorted(HERE.parent.rglob('64x64_cats.npy'))
    candidates += [HERE.parents[1] / '64x64_cats.npy']
    candidates = list(dict.fromkeys(p.resolve() for p in candidates if p.is_file()))
    if len(candidates) != 1:
        raise FileNotFoundError('Specify --data PATH to the lecture 64x64_cats.npy file.')
    return candidates[0]


def train(args):
    if args.epochs < 1 or args.batch_size < 1 or args.timesteps < 1:
        raise ValueError('epochs, batch-size, and timesteps must be positive.')
    if args.max_batches is not None and args.max_batches < 1:
        raise ValueError('max-batches must be positive.')
    if args.sample_every < 0:
        raise ValueError('sample-every must be nonnegative (0 disables sampling).')
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA was requested but is unavailable.')
    print('Device:', device, torch.cuda.get_device_name(device) if device.type == 'cuda' else '', flush=True)
    data_path = args.data.resolve() if args.data else find_data()
    dataset = CatDataset(data_path, args.limit)
    # The TF source does not shuffle or drop its last batch.
    train_dataset = DataLoader(dataset, batch_size=args.batch_size, shuffle=False,
                               num_workers=0, pin_memory=device.type == 'cuda')
    print(f'Data: {data_path}; images: {len(dataset)}; batch size: {args.batch_size}; n_feat: {args.n_feat}', flush=True)
    image_shape = (64, 64, 3)
    beta1, beta2, T = 1e-4, 0.02, args.timesteps
    model = NaiveUnet(image_shape, args.n_feat).to(device)
    # Match Keras defaults where possible. Adam's epsilon placement differs
    # between frameworks; equal eps values do not imply identical updates.
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999), eps=1e-7)
    loss_function = nn.MSELoss(reduction='mean')
    checkpoint = args.checkpoint.resolve()
    config = {'image_shape': image_shape, 'n_feat': args.n_feat,
              'beta1': beta1, 'beta2': beta2, 'T': T}
    start_epoch = 0
    history = []
    if checkpoint.exists():
        saved = torch.load(checkpoint, map_location=device, weights_only=True)
        if saved['config'] != config:
            raise ValueError('Checkpoint configuration differs; use a separate --checkpoint path.')
        model.load_state_dict(saved['model_state_dict'])
        optimizer.load_state_dict(saved['optimizer_state_dict'])
        start_epoch = saved['epoch']
        history = saved['history']
        if 'rng_state' in saved:
            torch.set_rng_state(saved['rng_state'].cpu())
        if device.type == 'cuda' and saved.get('cuda_rng_state') is not None:
            torch.cuda.set_rng_state(saved['cuda_rng_state'].cpu(), device)
        del saved
        print(f'Resuming after {start_epoch} epochs.', flush=True)
    print(f'Parameters: {sum(p.numel() for p in model.parameters()):,}', flush=True)
    schedules = {k: v.to(device) for k, v in ddpm_schedules(beta1, beta2, T).items()}
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    sample_root = args.sample_dir or checkpoint.parent / 'samples' / checkpoint.stem
    if args.sample_every:
        next_sample_epoch = (start_epoch // args.sample_every + 1) * args.sample_every
        print(f'Archive 8 samples every {args.sample_every} epochs; next: {next_sample_epoch}; '
              f'folder: {sample_root.resolve()}', flush=True)
    model.train()
    for i in range(start_epoch, start_epoch + args.epochs):
        start = time.perf_counter()
        loss, total_mse, count, batches = 0.0, 0.0, 0, 0
        for image_batch in train_dataset:
            image_batch = image_batch.to(device, non_blocking=True)
            this_batch_size = image_batch.shape[0]
            eps = torch.randn_like(image_batch)
            t_index = torch.randint(1, T + 1, (this_batch_size,), device=device)
            this_sqrtab = schedules['sqrtab'][t_index].reshape(this_batch_size, 1, 1, 1)
            this_sqrtmab = schedules['sqrtmab'][t_index].reshape(this_batch_size, 1, 1, 1)
            x_t = this_sqrtab * image_batch + this_sqrtmab * eps
            t_input = t_index.float() / T
            optimizer.zero_grad(set_to_none=True)
            predicted_eps = model([x_t, t_input])
            batch_loss = loss_function(predicted_eps, eps)
            if not torch.isfinite(batch_loss):
                raise RuntimeError('Nonfinite training loss.')
            batch_loss.backward()
            # Detect invalid gradients without modifying their magnitudes.
            nn.utils.clip_grad_norm_(model.parameters(), float('inf'), error_if_nonfinite=True)
            optimizer.step()
            value = batch_loss.item()
            loss += value
            total_mse += value * this_batch_size
            count += this_batch_size
            batches += 1
            if batches == 1 or batches % args.log_every == 0:
                print(f'Epoch {i + 1}, batch {batches}/{len(train_dataset)}, MSE {value:.6f}', flush=True)
            if args.max_batches is not None and batches >= args.max_batches:
                break
        row = {'epoch': i + 1, 'loss_sum': loss, 'mean_mse': total_mse / count,
               'last_batch_mse': value, 'images': count, 'batches': batches,
               'partial_epoch': batches < len(train_dataset),
               'seconds': time.perf_counter() - start}
        history.append(row)
        print(json.dumps(row), flush=True)
        saved = {'config': config, 'model_state_dict': model.state_dict(),
                 'optimizer_state_dict': optimizer.state_dict(), 'epoch': i + 1,
                 'history': history, 'data_path': str(data_path),
                 'run_options': {'batch_size': args.batch_size, 'limit': args.limit,
                                 'max_batches': args.max_batches, 'seed': args.seed,
                                 'sample_every': args.sample_every, 'sample_seed': args.sample_seed,
                                 'sample_dir': str(sample_root.resolve())},
                 'rng_state': torch.get_rng_state(),
                 'cuda_rng_state': torch.cuda.get_rng_state(device) if device.type == 'cuda' else None}
        temporary = checkpoint.with_suffix(checkpoint.suffix + '.tmp')
        torch.save(saved, temporary)
        temporary.replace(checkpoint)
        checkpoint.with_suffix('.history.json').write_text(json.dumps(history, indent=2), encoding='utf-8')
        if args.sample_every and (i + 1) % args.sample_every == 0:
            # Use the trained weights directly; checkpoint is already safe on disk.
            # Sampling has its own RNG and restores model.train() afterwards.
            print(f'Archiving 8 samples for epoch {i + 1}.', flush=True)
            optimizer.zero_grad(set_to_none=True)
            samples = sample_from_model(model, config, n_sample=8, seed=args.sample_seed)
            metadata = {'epoch': i + 1, 'config': config, 'last_training_record': row,
                        'seed': args.sample_seed, 'device': str(device), 'source': 'training',
                        'checkpoint': str(checkpoint), 'sample_every': args.sample_every}
            output = save_sample_set(samples, metadata, sample_root)
            print(f'Saved sample archive: {output}', flush=True)
    print(f'Saved checkpoint: {checkpoint}', flush=True)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Train the lecture 7 DDPM on cat images.')
    parser.add_argument('--data', type=Path)
    parser.add_argument('--epochs', type=int, default=300)
    parser.add_argument('--n-feat', type=int, default=512)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--timesteps', type=int, default=1000)
    parser.add_argument('--checkpoint', type=Path, default=HERE / 'model.pt')
    parser.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--limit', type=int, help='Use only the first N images for a reduced run.')
    parser.add_argument('--max-batches', type=int, help='Limit batches per epoch for a smoke test.')
    parser.add_argument('--log-every', type=int, default=20)
    parser.add_argument('--sample-every', type=int, default=10,
                        help='Archive 8 samples every N checkpoint epochs; 0 disables.')
    parser.add_argument('--sample-seed', type=int, default=42,
                        help='Fixed seed for comparable images across epochs.')
    parser.add_argument('--sample-dir', type=Path,
                        help='Archive root (default: checkpoint directory/samples/checkpoint stem).')
    args = parser.parse_args(argv)
    if args.log_every < 1:
        parser.error('--log-every must be positive')
    return args


if __name__ == '__main__':
    train(parse_args())
