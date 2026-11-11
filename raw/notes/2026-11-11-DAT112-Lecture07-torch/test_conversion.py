"""Focused checks for lecture 7's layout, schedule, and trainable U-Net."""
import io
from pathlib import Path
import unittest
import numpy as np
import torch

from ddpm import ddpm_schedules
from diffusion_model import CatDataset, find_data
from unet import NaiveUnet


class ConversionTests(unittest.TestCase):
    def test_original_tensorflow_schedule(self):
        reference = Path(__file__).parent / 'runs' / 'tf_schedules.npz'
        if not reference.exists():
            self.skipTest('Export the original TensorFlow schedule first; see README.')
        with np.load(reference) as expected:
            for key, value in ddpm_schedules(1e-4, 0.02, 1000).items():
                # sqrt(1-alphabar) magnifies float32 cancellation near t=0.
                np.testing.assert_allclose(value.numpy(), expected[key], rtol=3e-6, atol=3e-6)

    def test_schedule_and_forward_noise_variance(self):
        schedules = ddpm_schedules(1e-4, 0.02, 1000)
        beta = np.linspace(1e-4, 0.02, 1001)
        alphabar = np.cumprod(1 - beta)
        np.testing.assert_allclose(schedules['alphabar_t'].numpy(), alphabar, rtol=3e-6)
        torch.testing.assert_close(schedules['sqrtab'] ** 2 + schedules['sqrtmab'] ** 2,
                                   torch.ones(1001))
        self.assertLess(schedules['alphabar_t'][-1], 0.0001)
        # The lecture includes beta[0] in its cumulative product.
        self.assertAlmostEqual(schedules['alphabar_t'][0].item(), 0.9999, places=6)

    def test_dataset_layout_and_normalization(self):
        dataset = CatDataset(find_data(), limit=2)
        original = np.load(find_data(), mmap_mode='r')[0]
        image = dataset[0]
        self.assertEqual(image.shape, (3, 64, 64))
        self.assertEqual(image.dtype, torch.float32)
        np.testing.assert_array_equal(image.permute(1, 2, 0).numpy(),
                                      (original / 255).astype('float32'))

    def test_shapes_gradients_and_weight_reload(self):
        torch.manual_seed(7)
        model = NaiveUnet((64, 64, 3), 8)
        images = torch.randn(2, 3, 64, 64)
        times = torch.tensor([0.1, 1.0])
        shapes = {}
        handles = []
        for name in ['init_conv', 'down1', 'down2', 'down3', 'to_vec', 'up0', 'up1', 'up2', 'up3']:
            handles.append(getattr(model, name).register_forward_hook(
                lambda module, inputs, output, name=name: shapes.__setitem__(name, tuple(output.shape))))
        output = model([images, times])
        for handle in handles:
            handle.remove()
        self.assertEqual([shapes[name][-1] for name in shapes], [64, 32, 16, 8, 2, 8, 16, 32, 64])
        self.assertEqual(output.shape, images.shape)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, eps=1e-7)
        before = model.out.weight.detach().clone()
        (output - images).square().mean().backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters()))
        optimizer.step()
        self.assertFalse(torch.equal(before, model.out.weight))
        buffer = io.BytesIO()
        torch.save(model.state_dict(), buffer)
        buffer.seek(0)
        reloaded = NaiveUnet((64, 64, 3), 8)
        reloaded.load_state_dict(torch.load(buffer, weights_only=True))
        with torch.no_grad():
            torch.testing.assert_close(model([images, times]), reloaded([images, times]), rtol=0, atol=0)


if __name__ == '__main__':
    torch.set_num_threads(2)
    unittest.main(verbosity=2)
