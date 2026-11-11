"""Check retention, resumed cadence, and sampling isolation from training."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image
import torch

from diffusion_model import parse_args, train
from reverse_diffusion import sample_from_model
from sample_archive import save_sample_set
from unet import NaiveUnet

CONFIG = {'image_shape': (64, 64, 3), 'n_feat': 8,
          'beta1': 1e-4, 'beta2': 0.02, 'T': 2}


class SampleArchiveTests(unittest.TestCase):
    def test_repeated_epoch_never_overwrites_and_saves_eight_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            samples = np.full((8, 64, 64, 3), 128, dtype=np.int16)
            metadata = {'epoch': 90, 'seed': 42, 'config': CONFIG, 'source': 'training'}
            first = save_sample_set(samples, metadata, tmp)
            original = {p.name: p.read_bytes() for p in first.iterdir()}
            second = save_sample_set(samples + 1, metadata, tmp)
            self.assertNotEqual(first, second)
            self.assertEqual(original, {p.name: p.read_bytes() for p in first.iterdir()})
            self.assertEqual(len(list(first.glob('sample_*.png'))), 8)
            with Image.open(first / 'grid.png') as grid:
                grid.verify()
            np.testing.assert_array_equal(np.load(first / 'samples.npy'), samples)
            info = json.loads((first / 'metadata.json').read_text())
            self.assertEqual(info['status'], 'complete')
            self.assertEqual(info['epoch'], 90)
            self.assertEqual(info['n_sample'], 8)
            self.assertIn('created_at_utc', info)

    def test_sampling_preserves_rng_mode_weights_and_is_repeatable(self):
        devices = ['cpu'] + (['cuda'] if torch.cuda.is_available() else [])
        for device in devices:
            with self.subTest(device=device):
                model = NaiveUnet((64, 64, 3), 8).to(device).train()
                before = {k: v.clone() for k, v in model.state_dict().items()}
                cpu_rng = torch.get_rng_state().clone()
                cuda_rng = torch.cuda.get_rng_state().clone() if device == 'cuda' else None
                samples = sample_from_model(model, CONFIG, n_sample=2, verbose=False)
                again = sample_from_model(model, CONFIG, n_sample=2, verbose=False)
                np.testing.assert_array_equal(samples, again)
                self.assertTrue(model.training)
                self.assertTrue(torch.equal(cpu_rng, torch.get_rng_state()))
                if cuda_rng is not None:
                    self.assertTrue(torch.equal(cuda_rng, torch.cuda.get_rng_state()))
                for key, value in model.state_dict().items():
                    torch.testing.assert_close(value, before[key], rtol=0, atol=0)
                model.eval()
                sample_from_model(model, CONFIG, n_sample=1, verbose=False)
                self.assertFalse(model.training)

    def test_sampling_restores_training_mode_on_failure(self):
        model = NaiveUnet((64, 64, 3), 8).train()
        with patch.object(model, 'forward', side_effect=RuntimeError('simulated failure')):
            with self.assertRaisesRegex(RuntimeError, 'simulated failure'):
                sample_from_model(model, CONFIG, n_sample=1, verbose=False)
        self.assertTrue(model.training)

    def test_resume_at_nine_archives_ten_only_without_changing_training(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / 'cats.npy'
            np.save(data, np.full((2, 64, 64, 3), 128, dtype=np.uint8))
            model = NaiveUnet((64, 64, 3), 8)
            optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, eps=1e-7)
            initial = {'config': CONFIG, 'model_state_dict': model.state_dict(),
                       'optimizer_state_dict': optimizer.state_dict(), 'epoch': 9, 'history': []}
            results = []
            for name, frequency in [('enabled', 10), ('disabled', 0)]:
                checkpoint = root / name / 'model.pt'
                checkpoint.parent.mkdir()
                torch.save(initial, checkpoint)
                args = parse_args(['--checkpoint', str(checkpoint), '--data', str(data),
                                   '--epochs', '2', '--n-feat', '8', '--batch-size', '1',
                                   '--timesteps', '2', '--device', 'cpu',
                                   '--sample-every', str(frequency)])
                with contextlib.redirect_stdout(io.StringIO()):
                    train(args)
                results.append(torch.load(checkpoint, weights_only=True))
            enabled, disabled = results
            self.assertEqual(enabled['epoch'], 11)
            for key, value in enabled['model_state_dict'].items():
                torch.testing.assert_close(value, disabled['model_state_dict'][key], rtol=0, atol=0)
            self.assertTrue(torch.equal(enabled['rng_state'], disabled['rng_state']))
            sets = list((root / 'enabled' / 'samples' / 'model').iterdir())
            self.assertEqual([p.name for p in sets], ['epoch_000010'])
            self.assertEqual(len(list(sets[0].glob('sample_*.png'))), 8)
            metadata = json.loads((sets[0] / 'metadata.json').read_text())
            self.assertEqual(metadata['epoch'], 10)
            self.assertEqual(metadata['last_training_record']['epoch'], 10)
            self.assertEqual(metadata['source'], 'training')
            self.assertFalse((root / 'disabled' / 'samples').exists())


if __name__ == '__main__':
    torch.set_num_threads(2)
    unittest.main(verbosity=2)
