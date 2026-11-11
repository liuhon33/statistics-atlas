# Lecture 07: diffusion models

The PyTorch version follows the supplied TensorFlow code, including the
129,329,667-parameter U-Net at `n_feat=512`. The TensorFlow source is unchanged.
This is a learning implementation of DDPM, not a pretrained cat model.

## Files

| TensorFlow reference | PyTorch translation | Purpose |
| --- | --- | --- |
| `tensorflow/ddpm.py` | `torch/ddpm.py` | Linear noise schedule |
| `tensorflow/unet.py` | `torch/unet.py` | Residual blocks, down/up blocks, sine time embedding, U-Net |
| `tensorflow/diffusion_model.py` | `torch/diffusion_model.py` | Cat loading, forward noising, noise-prediction training |
| `tensorflow/reverse_diffusion.py` | `torch/reverse_diffusion.py` | Reverse diffusion and image export |

`slides/7_DM.pdf` contains the lecture notes. `data/64x64_cats.npy` contains
29,843 RGB images, shape `(29843, 64, 64, 3)`, dtype `uint8`. The supplied file
was moved from `lecture06/` into this lecture and verified with SHA-256.

## Run on Windows

Run these commands from the repository root, `E:/DAT112`, using the existing
`pytorch_learn` environment. No packages or environments were installed or changed.

Continue the saved model for one **full** pass through all cat images:

```powershell
conda run --no-capture-output -n pytorch_learn python lecture07/torch/diffusion_model.py --epochs 1 --batch-size 8
```

Training automatically resumes model weights and Adam state if the checkpoint
exists. `--epochs` specifies additional passes, not a target total. A run limited
by `--max-batches` still increments the pass/epoch counter; the initial saved
counter of 2 represents two partial passes, not two full epochs. Each new pass
starts at the beginning of the data, as in the original unshuffled dataset.
CPU and CUDA RNG states are saved for same-device continuation.

To run from scratch without overwriting the supplied validation checkpoint,
choose a new checkpoint path:

```powershell
conda run --no-capture-output -n pytorch_learn python lecture07/torch/diffusion_model.py --epochs 1 --batch-size 8 --checkpoint lecture07/torch/runs/new_training/model.pt
```

With no arguments, the script preserves the source's defaults: 300 additional
epochs, batch size 64, 512 feature channels, 1,000 diffusion steps, Adam learning
rate 0.001. Batch size 64 has **not** been verified to fit this GPU. The verified
batch size 8 changes batch-level gradient estimates, not the architecture.

Generate images from the default checkpoint:

For an eight-image grid from the latest saved weights (and a Windows preview):

```powershell
conda run --no-capture-output -n pytorch_learn python lecture07/torch/show_samples.py --show
```

This uses the installed NumPy and Pillow packages. It saves `grid.png`, individual
images, raw samples, and the exact loaded checkpoint's epoch/configuration in a
new folder such as `torch/samples/model/epoch_000086/`. Omit `--show` for generation
without opening a window. `--seed` changes the random samples; `--output` selects
the archive root. A new epoch subfolder is always created, even with `--output`.
If that epoch folder already exists, the new folder has a UTC timestamp and
unique suffix. Previous images are never overwritten.

To use the original sampler entry point (also archives individual files and a grid):

```powershell
conda run --no-capture-output -n pytorch_learn python lecture07/torch/reverse_diffusion.py --n-sample 2
```

The sampler saves raw NHWC `int16` values in each epoch folder's `samples.npy` and
clipped 8-bit PNG previews alongside them. Both commands use the same archive rules.
An undertrained model's output is not evidence of learned cat-image quality.

Run focused checks:

```powershell
conda run --no-capture-output -n pytorch_learn python -m unittest discover -s lecture07/torch -p "test_*.py" -v
```

Default data, checkpoint, and output paths are resolved relative to the script.
Explicit relative CLI paths are resolved relative to your current directory.
`--data PATH` selects an alternative `.npy` file. `--limit`, `--max-batches`, and
`--n-feat` are explicit reduced-run options. A different model width or schedule
needs a separate checkpoint.

## Image history enabled on 2026-10-16

Training now automatically generates **eight images every 10 checkpoint epochs**
after saving that epoch's model. The existing checkpoint counter is 86, so the
next automatic set is epoch **90**, then **100**, **110**, and so on. This follows
the existing epoch counter, which includes the initial two partial passes.
There is no attempt to reconstruct lost images from earlier model weights.

The normal training command enables this behavior without additional flags:

```powershell
conda run --no-capture-output -n pytorch_learn python lecture07/torch/diffusion_model.py --epochs 300 --batch-size 8
```

`--epochs 300` still means 300 additional epochs. To finish at checkpoint counter
302 when resuming from 86, use `--epochs 216`. This code change does not start a
training job. An already-running Python process must be restarted from its last
saved checkpoint to use the updated code; edits cannot change its loaded loop.

Default output layout (90 and 100 are future examples):

```text
torch/samples/model/
    epoch_000086/             # current-checkpoint baseline, generated manually
        sample_000.png        # eight individual 64x64 images
        ...
        sample_007.png
        grid.png              # all eight enlarged for viewing
        samples.npy           # raw generated pixels before display clipping
        metadata.json         # epoch, loss, configuration, seed, device, UTC time
    epoch_000090/
    epoch_000100/
```

- The fixed sampling seed is **42**, independent of the training seed. It uses
  the same starting noise and reverse-step noise at each checkpoint so changes
  in weights can be compared. Keep device, batch size, and seed the same for
  consistent comparisons. Sampling uses the same 1,001 reverse steps as before.
- Sampling uses the current model directly, without loading a second large
  model, and restores training mode. Its private generator leaves the training
  random-number streams unchanged. The next training epoch starts after images
  are saved; this adds sampling time every 10 epochs.
- `--sample-every N` changes the interval; `--sample-every 0` disables automatic
  previews. `--sample-seed` changes the fixed preview seed. `--sample-dir PATH`
  changes the archive root. The default root is beside the checkpoint at
  `samples/<checkpoint stem>/`, keeping different checkpoint names separate.
- A repeated epoch creates a new timestamped directory; automatic and manual
  previews both retain previous results. `metadata.json` is written last and
  marks a complete set. An interrupted write leaves an incomplete folder for
  inspection; reruns create a separate folder.
- Metadata records whether the source was `training` or `manual`, the checkpoint
  path and counter, the last training loss record (including partial-pass status),
  model/schedule settings, seed, device, image count, and creation time in UTC.
- Model checkpoints still use the existing rolling `model.pt`. This feature
  retains **images and metadata**, not a full 1.55 GB checkpoint every 10 epochs.
  Existing legacy `samples/current/` and other older files are left in place.
- The model is saved before automatic sampling. If sampling or writing fails,
  the error stops the run with that epoch's checkpoint already saved. You can
  rerun `show_samples.py` to archive those saved weights before continuing.

Validation: all eight tests passed in `pytorch_learn`, including resumed 9-to-11
training with an archive only at 10, eight-image output and repeat-write retention,
CPU/CUDA random-state preservation, mode restoration after failure, and identical
CPU training weights with automatic sampling enabled versus disabled. The tiny
test model uses two diffusion steps; it does not modify the real checkpoint.

## Mathematics and correspondence

For a clean image `x_0` with pixel values divided by 255, training samples a
time index `t` uniformly from 1 through `T`, and independent standard Gaussian
noise `epsilon` with the same shape as the image. The schedules are

```text
beta_t     = beta1 + (beta2 - beta1) * t / T
alpha_t    = 1 - beta_t
alphabar_t = product(alpha_s, s=0..t)       # the supplied code's convention
x_t        = sqrt(alphabar_t) * x_0 + sqrt(1 - alphabar_t) * epsilon
loss       = mean((epsilon_theta(x_t, t/T) - epsilon)^2)
```

`beta_t` sets the per-step noise variance. The cumulative product `alphabar_t`
measures how much original signal remains. The signal and noise coefficients
have squared magnitudes adding to one. At small `t`, most of the clean image
remains; at large `t`, the noise dominates. The network receives the noisy image
and normalized time and learns to predict the **added noise**, not the clean
image directly. The loss averages over batch, channels, height, and width.

Sampling starts from standard Gaussian noise and applies the original recurrence:

```text
x_(t-1) = (x_t - (1-alpha_t)/sqrt(1-alphabar_t) * epsilon_theta(x_t,t/T))
          / sqrt(alpha_t) + sqrt(beta_t) * z
```

Here `z` is fresh standard Gaussian noise except at the last loop iteration,
where it is zero. The supplied sampler visits `T, T-1, ..., 0`, and its schedule
includes `beta_0` in the cumulative product. Both details are retained for
comparison. This evaluates the network at an untrained `t=0` and performs `T+1`
updates; it differs from the usual DDPM `T..1` indexing. Changing only the sampling
endpoint would not by itself reconcile the schedule conventions.

## Framework differences and source issues

- Inputs change from NHWC to NCHW: `(N,64,64,3)` becomes `(N,3,64,64)`.
  Concatenation uses dimension 1, and time embeddings broadcast as `(N,2F,1,1)`.
  `input_shape=(64,64,3)` remains the constructor's public shape description.
- The U-Net retains the source's `64 -> 32 -> 16 -> 8 -> 2 -> 8 -> 16 -> 32 -> 64`
  spatial progression, residual sum `x1+x`, skip connections, and sine embedding.
  Convolution blocks need explicit input channel counts in PyTorch.
- The `.py` source is authoritative where slide snippets differ, including the
  bottleneck transpose-convolution size and decoder widths on slide 26.
- GroupNorm uses 8 groups and `eps=0.001` to match
  [Keras GroupNormalization](https://keras.io/api/layers/normalization_layers/group_normalization/),
  rather than [PyTorch's default `1e-5`](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.normalization.GroupNorm.html).
  Convolution and dense kernels use Glorot/Xavier uniform initialization and zero
  biases, matching Keras' initialization distribution but not its random draws.
- Adam uses learning rate 0.001, betas `(0.9,0.999)`, and epsilon `1e-7` from the
  installed Keras configuration. TensorFlow and PyTorch place epsilon differently
  relative to bias correction, so their optimizer steps are not exactly identical.
- The data remain in `[0,1]`; there is no added `[-1,1]` normalization or shuffling.
  Memory-mapped loading normalizes one image at a time instead of allocating the
  entire normalized dataset in RAM.
- PyTorch uses an explicit backward/optimizer loop and `.pt` state dictionaries.
  It saves after each pass using a temporary file plus replacement, including
  optimizer/configuration/history. JSON history records summed batch MSE and
  image-weighted mean MSE, rather than Keras' potentially accumulated metrics.
- `tf-win` contains TensorFlow 2.10.1 and detects the RTX 4090, but the original
  U-Net cannot import: `tensorflow.keras.saving` and `GroupNormalization` are
  unavailable. The reference sampler also calls `km.load`, rather than
  `km.load_model`. No TensorFlow source or environment changes were made.
  Full TensorFlow/PyTorch forward-output parity is therefore **not verified**.

## Initial conversion validation (2026-10-03)

- PyTorch `2.10.0+cu130`, NumPy `2.3.5`, CUDA on NVIDIA GeForce RTX 4090 (24 GB).
- Original-width GPU training: 2 batches of 2 images, followed by 100 batches of
  8 images, using the original 1,000-step schedule. Total: 102 optimizer steps,
  804 image presentations (some images repeat), **not** 804 distinct images.
- The 100-batch continuation took about 23 seconds for its training loop. Last
  batch MSE was `0.078609`; mean MSE across that pass was `1.879752`, including
  the large early losses. Different times/noise/images make successive batch
  losses unsuitable as a controlled evaluation of generative quality.
- At initial validation, `torch/model.pt` contained the briefly trained model
  and `torch/model.history.json` contained the two partial-pass records. Subsequent
  user training has advanced these files; the image-history section records the
  checkpoint found when automatic archival was added.
- Checkpoint reload and GPU sampling completed all 1,001 reverse updates for two
  images, with finite outputs, saved in `torch/samples/`.
- Focused checks cover actual cat normalization/channel layout, schedule
  identities, encoder/decoder spatial sizes, finite gradients to every parameter,
  an optimizer update, and exact state-dictionary reload output on a small CPU model.
- `torch/runs/tf_schedules.npz` was exported by the original TensorFlow `ddpm.py`.
  Comparison uses `rtol=3e-6, atol=3e-6`: float32 rounding in `1-alphabar` is
  amplified by the square root near `t=0` (about `2e-6` absolute difference).
  The independent NumPy cumulative-product comparison is checked separately.

To regenerate the TensorFlow schedule fixture from the repository root:

```powershell
conda run --no-capture-output -n tf-win python -c "import sys,numpy as np,tensorflow as tf; tf.config.set_visible_devices([], 'GPU'); sys.path.insert(0,'lecture07/tensorflow'); from ddpm import ddpm_schedules; s=ddpm_schedules(1e-4,0.02,1000); np.savez('lecture07/torch/runs/tf_schedules.npz',**{k:v.numpy() for k,v in s.items()})"
```
