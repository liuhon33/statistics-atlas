---
id: learning-diffusion-pytorch-unet
title: Diffusion in PyTorch - why U-Net and how the formulas become code
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Selected architectures & latent models]]"
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models
study_band: M elective
note_types:
  - topic-note
  - question
  - insight
question_roles:
  - mechanism
  - cross-topic-connection
source_format: lecture-slides-and-pytorch
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: unknown
aliases:
  - DAT112 Lecture 7 diffusion implementation
  - U-Net tensor shapes and DDPM code
tags:
  - atlas/learning
  - subject/computing
  - topic/diffusion
  - topic/pytorch
  - study/masters-elective
connections:
  - "[[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation]]"
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL]]"
sources:
  - "[[raw/notes/2025-05-13-DAT112-Lecture07-Diffusion-models.pdf]]"
  - "[[raw/assets/2025-05-13-DAT112-diffusion-I01-unet.png]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/unet.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/ddpm.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/diffusion_model.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/reverse_diffusion.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/sample_archive.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/show_samples.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/test_conversion.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/test_sample_archive.py]]"
  - "[[raw/notes/2026-11-11-DAT112-Lecture07-torch/2026-11-11-DAT112-Lecture07-source-README.md]]"
---

# Diffusion in PyTorch - why U-Net and how the formulas become code

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models

**The U-Net is the function $\epsilon_\theta(x_t,t)$ inside the diffusion equations—not the entire diffusion process.** One network call predicts an image-shaped noise tensor. Training teaches that function using noise we generated ourselves; sampling repeatedly calls it inside a Gaussian update.

We are we designing the UNet like this?

The earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation|Lecture 12 note]] already derives the forward marginal, Gaussian bridge, ELBO, noise loss and reverse update. This note adds the implementation: the supplied **PyTorch files**, which is different from the transcription of the PDF's TensorFlow snippets. The brief equations below identify what each block implements; they do not repeat those proofs.

> [!warning] Read the implementation, not an idealized replacement
> The supplied code preserves a nonstandard $T+1$ schedule and an extra, untrained $t=0$ sampling call. Section 6 separates these from the standard formulas. The lecture files and trained checkpoint have not been modified.

## 1. Why go down, come up, and connect across?

![[raw/assets/2025-05-13-DAT112-diffusion-I01-unet.png]]

*The supplied screenshot of DAT112 slide 23, preserved unchanged. It is a schematic: the actual bottleneck also pools from $8\times8$ to $2\times2$, then upsamples back to $8\times8$ before the first decoder concatenation.*

For one batch of RGB images, the task is

$$
\underbrace{(x_t,t)}_{\text{noisy image and noise level}}
\longmapsto
\underbrace{\epsilon_\theta(x_t,t)}_{\text{one predicted noise value per RGB coordinate}},
\qquad
\mathbb R^{B\times3\times64\times64}\longrightarrow
\mathbb R^{B\times3\times64\times64}.
$$

Think of a noisy cat: interpreting an eye benefits from surrounding facial structure, but correcting its boundary requires precise spatial information. These are complementary requirements:

| Part | What it contributes | Why it is there |
| --- | --- | --- |
| Initial convolutions | Learned local feature maps | Replace raw RGB coordinates with many useful feature channels |
| Down path | Coarser representations combining broader regions | Later local convolutions can combine information from a larger area of the input |
| Bottleneck | Strongly compressed features, conditioned on time | Process broad structure while being told the noise level |
| Up path | Learned return to a dense output grid | Predict a correction at each original pixel location |
| Skip connections | Encoder features at matching spatial resolutions | Fine spatial information need not survive the bottleneck alone |
| Final convolution | Three output channels | Convert features into an RGB-shaped noise prediction |

The context-versus-localization motivation is the original U-Net design principle. Here it is adapted from segmentation to noise regression; the example features are intuition, not a claim that individual trained channels were inspected. U-Net is a useful architecture choice, **not something the ELBO mathematically requires**. [Ronneberger et al., U-Net abstract and architecture](https://arxiv.org/abs/1505.04597).

**Two different axes:** $t$ counts diffusion noise levels; depth counts layers within one U-Net call. During that call, $t$ stays fixed. The down layers do not add successive diffusion noise, and the up layers are not successive reverse timesteps.

### 1.1 Follow the actual tensor shapes

PyTorch uses **NCHW**: batch, channels, height, width. Let $F=\texttt{n\_feat}$; the training default is $512$, while the lightweight checks use $8$ without changing the spatial architecture.

| Code value | Shape | Operation |
| --- | --- | --- |
| `img_input` | `[B, 3, 64, 64]` | Noisy image $x_t$ |
| `x = init_conv(img_input)` | `[B, F, 64, 64]` | Two padded $3\times3$ convolutions; local residual |
| `down1` | `[B, F, 32, 32]` | Convolution block, then $2\times2$ max pooling |
| `down2` | `[B, 2F, 16, 16]` | Same pattern, more channels |
| `down3` | `[B, 2F, 8, 8]` | Same pattern |
| `to_vec(down3)` | `[B, 2F, 2, 2]` | $4\times4$ average pooling; despite its name, not a flat vector |
| `timeemb` after reshape | `[B, 2F, 1, 1]` | Broadcast over the $2\times2$ bottleneck |
| `up0(thro + timeemb)` | `[B, 2F, 8, 8]` | Transposed convolution: kernel 4, stride 4 |
| `up1([thro, down3])` | `[B, 2F, 16, 16]` | Concatenate at $8\times8$, then upsample |
| `up2([up1, down2])` | `[B, F, 32, 32]` | Concatenate at $16\times16$, then upsample |
| `up3([up2, down1])` | `[B, F, 64, 64]` | Concatenate at $32\times32$, then upsample |
| `out(cat([up3, x]))` | `[B, 3, 64, 64]` | Concatenate at $64\times64$, predict noise |

This is the checked source-specific order: **concatenate first, upsample second** inside each `UnetUpLayer`. Not every U-Net implementation uses that order. Source: [[raw/notes/2026-11-11-DAT112-Lecture07-torch/unet.py|unet.py, NaiveUnet and UnetUpLayer]].

### 1.2 What does a skip connection actually do?

Verbatim `UnetUpLayer.forward` body:

```python
img_input, skip = inputs
x = torch.cat([img_input, skip], dim=1)
x = torch.relu(self.Conv2DTranspose(x))
x = self.Conv3_1(x)
return self.Conv3_2(x)
```

For `up1`, concatenation does this:

```text
main: [B, 2F, 8, 8] ─┐
                     ├─ cat(dim=1) → [B, 4F, 8, 8]
skip: [B, 2F, 8, 8] ─┘
                     → transpose convolution → [B, 2F, 16, 16]
```

It **stacks channels**, not pixels along width, and does not average or add the two feature tensors. Following learned layers decide how to combine them. A transposed convolution is a learned upsampling operator here, not an inverse that recovers the exact information removed by pooling. [PyTorch ConvTranspose2d documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.ConvTranspose2d.html).

The skip comes from the same **noisy input**. It supplies neither $x_0$ nor target noise. Without skips, fine detail must pass through a severe bottleneck; without the coarse path, local detail has less broad context. Neither path alone is the complete rationale.

### 1.3 What the smaller blocks mean

- **`Conv3Layer` means $3\times3$ kernels, not three convolution layers:** it contains two Conv2d → GroupNorm → ReLU sequences. Padding 1 with stride 1 preserves height and width.
- **GroupNorm** normalizes within each image's channel groups and spatial positions. The code uses 8 groups, so $F$ must be divisible by 8. It does not estimate statistics across other images in the batch; the same kind of input statistics is used in train and eval modes. [PyTorch GroupNorm documentation](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GroupNorm.html).
- The initial block's **local residual** is `x1 + x`, where `x1` is the first activated convolution output—not the raw RGB input. This addition preserves channel count. It differs from the long U-shaped concatenation skips.
- The final `nn.Conv2d(2*F, 3, 3, padding=1)` has **no sigmoid, softmax or ReLU afterwards**. Its target is Gaussian noise, which may be negative or greater than one, not a bounded clean-pixel value or class probability.

## 2. Why does time need its own branch?

The same noisy pixel pattern can call for different predictions at different noise levels. The network must know which conditional regression problem it is solving. One shared model handles all levels rather than training $T$ independent networks.

The input is $\tau=t/T$. The learned time map is

$$
e(\tau)=W_2\sin(W_1\tau+b_1)+b_2\in\mathbb R^{2F}.
$$

Verbatim `TimeSirenLayer.forward` body:

```python
x = self.Dense_1(inputs)
x = torch.sin(x)
return self.Dense_2(x)
```

The scalar becomes multiple nonlinear features of noise level. The sine is an embedding choice; diffusion time itself is **not physically periodic**, and this is not the usual fixed sinusoidal positional-encoding table.

In `NaiveUnet.forward`:

```python
thro = torch.relu(self.to_vec(down3))
timeemb = self.timeemb(t_input.reshape(-1, 1)).reshape(
    -1, 2 * self.n_feat, 1, 1
)
thro = torch.relu(self.up0_norm(self.up0(thro + timeemb)))
```

The last two singleton dimensions make broadcasting explicit:

$$
(h+e)_{b,c,u,v}=h_{b,c,u,v}+e_{b,c}.
$$

Each image receives its own time vector, shared over its four bottleneck locations. It adds a channel-dependent condition without changing the tensor shape. In **this** network time is injected only at the bottleneck; do not assume every convolution block contains another time injection.

This branch supplies the second argument of [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#6.2 Let the network predict noise|the previously derived $\epsilon_\theta(x_t,t)$ parameterization]]. In code the argument is normalized to $t/T$; training and sampling use the same normalization.

## 3. Precompute the scalar coefficients, not noisy images

Source: [[raw/notes/2026-11-11-DAT112-Lecture07-torch/ddpm.py|ddpm.py, ddpm_schedules]]. Core excerpt:

```python
beta_t = (beta2 - beta1) * torch.arange(T + 1, dtype=torch.float32) / T + beta1
alpha_t = 1 - beta_t
log_alpha_t = torch.log(alpha_t)
alphabar_t = torch.exp(torch.cumsum(log_alpha_t, dim=0))
sqrtab = torch.sqrt(alphabar_t)
sqrtmab = torch.sqrt(1 - alphabar_t)
```

The cumulative sum implements $\exp(\sum\log\alpha)=\prod\alpha$. These are fixed lookup arrays, not trainable parameters. The code moves them to the same device as the model.

| Lookup key | Mathematical coefficient | Used for |
| --- | --- | --- |
| `sqrtab` | $\sqrt{\bar\alpha_t}$ | Signal scale in the forward marginal |
| `sqrtmab` | $\sqrt{1-\bar\alpha_t}$ | Aggregate-noise scale |
| `oneover_sqrta` | $1/\sqrt{\alpha_t}$ | Reverse-mean outer scale |
| `mab_over_sqrtmab` | $\beta_t/\sqrt{1-\bar\alpha_t}$ | Scale of predicted noise in the reverse mean |
| `sqrt_beta_t` | $\sqrt{\beta_t}$ | Standard deviation of fresh sampling noise |

**Indexing caveat:** in this table, interpreting the code's `alphabar_t` literally means $\prod_{s=0}^t\alpha_s$, not the earlier notes' $\prod_{s=1}^t\alpha_s$. The algebraic role is the same; the discrete schedule is not identical. Section 6 gives the exact difference.

## 4. One training batch is one Monte Carlo estimate

### 4.1 Put the clean image in the right shape

The supplied cat array is NHWC with values in $[0,255]$. `CatDataset.__getitem__` uses:

```python
image = (self.data[index] / 255).astype('float32')
return torch.from_numpy(image.transpose(2, 0, 1).copy())
```

This creates one `[3,64,64]` image in $[0,1]$; the DataLoader stacks images into `[B,3,64,64]`. **Transpose permutes axes; reshape alone would scramble their meaning.** The code does not use $[-1,1]$ scaling. Once Gaussian noise is added, $x_t$ is not confined to $[0,1]$.

### 4.2 Generate the supervised pair

Core excerpt from [[raw/notes/2026-11-11-DAT112-Lecture07-torch/diffusion_model.py|diffusion_model.py, train, lines 111–120]]:

```python
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
```

**This implements the [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#2.3 Extend to an arbitrary timestep|direct forward-marginal formula]]**

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon
$$

**and the [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#8. From local Gaussian KL to the noise-prediction loss|noise-prediction objective derived from local Gaussian KL]], subject to the code's indexing convention.**

Read the dimensions literally:

- `eps`: `[B,3,64,64]`, sampled standard Gaussian noise; it is the known target.
- `t_index`: `[B]`; each image gets a randomly sampled integer in $\{1,\ldots,T\}$. The upper limit of `randint` is exclusive.
- Indexed schedules: initially `[B]`, then `[B,1,1,1]` so one scalar multiplies every coordinate of its own image. A bare `[B]` tensor would align with the last dimension, not automatically with the batch.
- `x_t` and `predicted_eps`: both `[B,3,64,64]`.
- `batch_loss`: scalar.

There is **no forward loop through all $T$ states** and **no reverse chain in this training batch**. The exact marginal law supplies the noisy training input directly. Fresh time/noise draws create new corruptions on subsequent visits to an image. The actual DataLoader has `shuffle=False`: time and noise are random, while clean images are traversed in stored order, rather than independently resampled as in the textbook pseudocode.

### 4.3 What exactly is minimized?

The code sets `nn.MSELoss(reduction='mean')`, so with $C=3$ and $H=W=64$:

$$
\widehat L
=\frac{1}{BCHW}\sum_{b,c,h,w}
\left(\epsilon_{\theta,bchw}-\epsilon_{bchw}\right)^2.
$$

The dimension-averaged loss differs from a batch average of squared Euclidean norms by the fixed factor $1/(CHW)$. It contains **no timestep weights $\lambda_t$** and does not evaluate the full likelihood bound or a separate KL. That distinction is already established in [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#6.2 Let the network predict noise|the earlier mean-to-noise loss derivation]].

Training then runs:

```python
batch_loss.backward()
nn.utils.clip_grad_norm_(
    model.parameters(), float('inf'), error_if_nonfinite=True
)
optimizer.step()
```

`zero_grad` clears prior gradients; `backward` differentiates the loss through the U-Net, including its time branch; `step` updates weights. Here an infinite clipping threshold is a finite-gradient check, **not effective magnitude clipping**.

The optimal squared-error predictor is a conditional mean, $\mathbb E[\epsilon\mid x_t,t]$, not an oracle that always identifies the exact training draw. The noise is independent of $x_0$, but **not independent of $x_t$**, which contains it. See [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9.4 Connect the score identity to the noise network|the existing conditional-mean proof]] and [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#7.5 Why the teacher can use the clean image when the model cannot|why the training teacher can know more than the network input]].

## 5. Sampling turns the noise prediction into a reverse step

Source: [[raw/notes/2026-11-11-DAT112-Lecture07-torch/reverse_diffusion.py|reverse_diffusion.py, sample_from_model]]. Core excerpt, with progress printing omitted:

```python
x_t = torch.randn(this_size, device=device, generator=generator)
for i in range(T, -1, -1):
    z = torch.randn(this_size, device=device, generator=generator) if i > 0 else 0
    t = torch.full((n_sample, 1), i / T, device=device)
    eps = model([x_t, t])
    x_t = schedules['oneover_sqrta'][i] * (
        x_t - eps * schedules['mab_over_sqrtmab'][i]
    ) + schedules['sqrt_beta_t'][i] * z
```

**The arithmetic implements the [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#7.2 Sampling starts from noise|previously derived reverse update]], with $\sigma_t^2=\beta_t$:**

$$
x_{\text{next}}
=
\underbrace{\frac{1}{\sqrt{\alpha_i}}
\left(x_{\text{current}}-\frac{\beta_i}{\sqrt{1-\bar\alpha_i}}
\epsilon_\theta(x_{\text{current}},i)\right)}_{\mu_\theta}
+\underbrace{\sqrt{\beta_i}z}_{\text{fresh reverse-transition noise}}.
$$

Here the network actually receives $i/T$; the mathematical notation suppresses that input rescaling. “Current/next” avoids silently labeling the source's extra endpoint update as a standard $x_1\to x_0$ step.

Three different quantities must not be confused:

| Name | During training | During sampling |
| --- | --- | --- |
| Aggregate $\epsilon$ | Known random tensor used to create $x_t$ | Unknown; no original clean image is supplied |
| $\epsilon_\theta$ | Prediction compared against that target | Returned by the U-Net; confusingly stored in the variable `eps` |
| Fresh $z$ | Not needed for this noise-MSE batch | Samples the Gaussian reverse transition around its predicted mean |

**Why add noise while denoising?** The learned transition is a distribution, not just its mean. The mean update provides the systematic correction; the $z$ term samples remaining uncertainty. It is not reusing or restoring the training noise. Simply removing every $z$ produces a different procedure, not automatically a correctly derived accelerated sampler.

Nor is the update simply `x_t - eps`: the scale of aggregate noise and retained signal matters, and one reverse transition is not the same operation as estimating the final clean image.

Practical code details:

- `@torch.no_grad()` avoids constructing a gradient graph during generation; `model.eval()` sets evaluation mode. These are different controls. This particular U-Net has no dropout or BatchNorm; GroupNorm still uses input statistics.
- The sampler creates a private seeded `torch.Generator` and restores the prior model mode in `finally`. Preview generation therefore need not consume the training RNG stream or leave a training model in eval mode.
- Its returned array is NHWC `int16`, after multiplying by 255. `sample_archive.py` keeps that raw array and clips to $[0,255]$ only for PNG display. Display clipping is not part of the learned reverse equation.
- `mean_mse` in training history weights batch losses by their image counts; `loss_sum` is merely a sum of batch means. Neither by itself is a measurement of generated-image quality.

## 6. Where the source and the standard formulas differ

### 6.1 The extra schedule entry is mathematically consequential

The earlier notes use $\bar\alpha_0=1$ and $\bar\alpha_t=\prod_{s=1}^t\alpha_s$. The source instead has

$$
\beta_i=10^{-4}+(0.02-10^{-4})\,i/1000,\quad i=0,\ldots,1000,
\qquad A_i=\prod_{s=0}^i(1-\beta_s).
$$

Call its stored cumulative product $A_i$ here to make the difference visible:

| Quantity | Supplied code convention |
| --- | --- |
| `beta[0]` | $0.0001$ |
| `beta[1]` | $0.0001199$ |
| `alphabar[0]` | $A_0=0.9999$, **not 1** |
| `alphabar[1]` | $A_1\approx0.999780112$ |
| `alphabar[1000]` | $A_{1000}\approx3.99520\times10^{-5}$ |
| Training calls | indices $1,\ldots,1000$ |
| Sampling calls | indices $1000,\ldots,0$: **1001 calls** |

These numerical values are float64 evaluations of the source formula; the float32 arrays agree within rounding tolerance.

Thus the state associated with array index zero is already slightly noised. The sampler's last call uses a time value never sampled during training. A shifted indexing interpretation can explain the extra schedule entry, but it **does not fix the missing training level**.

Standard DDPM Algorithm 2 instead visits $T,\ldots,1$ and suppresses $z$ at $t=1$. The source visits $T,\ldots,0$ and suppresses $z$ only at zero. Repairing this coherently would require aligning the schedule, training levels, time labels and sampler together—not just changing one `range`. Existing weights were trained under the source convention, so a schedule change must not be silently applied to them. [Ho et al., Algorithms 1–2](https://arxiv.org/html/2006.11239v2#S3).

### 6.2 Slide shortcuts that should not be copied literally

| Source location | Careful reading |
| --- | --- |
| PDF p. 8, $\epsilon_t=\epsilon_{t-1}=\cdots$ | Forward increments must be independent. Their weighted sum can be replaced **in distribution** by one scaled standard Gaussian; the draws are not literally equal. See [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#2.2 Combine two independent Gaussian increments\|the existing derivation]]. |
| PDF p. 17, terminal KL “can be taken to be zero” | For a fixed schedule/prior it is independent of $\theta$, not generally exactly zero at finite $T$. No need to redigest the [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.3 Separate the loss into endpoints and intermediate terms\|already derived endpoint decomposition]]. |
| PDF pp. 18–19, KL is just a quadratic | The displayed equality uses matching fixed covariance $\tilde\beta_t I$ for $t\ge2$. Other fixed reverse variances give the corresponding weight plus a $\theta$-independent covariance term; see [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.5 Calculate the Gaussian KL instead of sampling its inner variable\|the full Gaussian KL]]. |
| PDF pp. 25–26, transposed convolutions and widths | The printed snippets do not show the same upsampling strides/decoder widths as the supplied PyTorch files. Follow the actual shape trace in §1, not a literal slide transcription. |
| PDF p. 29, reverse-mean prefactor | The printed $1/\sqrt{\bar\alpha_t}$ is inconsistent with pp. 13–14 and with `oneover_sqrta`. The reverse mean requires $1/\sqrt{\alpha_t}$. The same slide's $p_\theta(x_{t-1},x_t)$ should be a **conditional** transition. |
| PDF p. 29, replace posterior variance by $\beta_t$ | The code chooses reverse variance $\beta_t$ rather than $\tilde\beta_t=\beta_t(1-\bar\alpha_{t-1})/(1-\bar\alpha_t)$. These are not identical, and the ratio need not be near one at low noise levels. Under standard indexing it is zero at $t=1$. |

These are explanatory corrections and scope boundaries, not edits to the source PDF or code.

## 7. The small amount of additional lecture material

Most of pp. 5–21 is already covered by the earlier derivations, and the category-guidance ideas on p. 33 are developed much further in [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9. Conditional generation and guidance|the existing guidance sections]]. The present code is **unconditional**: there is no class/text input, classifier or guidance-scale argument.

Three brief additions are enough:

1. **GAN-training contrast (p. 4).** This implementation minimizes one denoising-regression objective, rather than alternating a generator/discriminator game. That avoids adversarial coupling; it does not make the neural optimization convex or guarantee convergence.
2. **Cosine scheduling (pp. 9, 33).** The schedule controls how signal is destroyed across time. The commonly referenced improved-DDPM cosine construction specifies a smooth cosine-squared $\bar\alpha_t$ curve, then obtains $\beta_t=1-\bar\alpha_t/\bar\alpha_{t-1}$; it is not simply “take the cosine of $\beta_t$.” It is absent from `ddpm.py`. This is a primary-source clarification of the slide's shorthand. [Nichol–Dhariwal, §3.2](https://arxiv.org/html/2102.09672v1#S3.S2).
3. **Strided sampling (p. 33).** Skipping timesteps requires transitions suitable for the larger jump. For retained levels $s<t$, the corresponding forward variance is $1-\bar\alpha_t/\bar\alpha_s$, not the original single-step $\beta_t$. Reverse coefficients must change consistently while conditioning on the original noise level. Changing only `range(..., -1)` to a larger stride is insufficient. No accelerated sampler is implemented here. [Nichol–Dhariwal, §4, equation (19)](https://arxiv.org/html/2102.09672v1#S4).

## Connections

- [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation|Diffusion models - Lecture 12 derivations and guided generation]] — The schedule lookup, noisy-batch construction and reverse sampler implement the forward-marginal, noise-parameterized mean and sampling formulas derived there; section links beside the code identify the exact correspondences and the source's indexing exceptions.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL|VAE and diffusion ELBO - images, hidden paths, and Gaussian KL]] — The PyTorch noise-MSE loop is the simplified objective reached from its local Gaussian-KL derivation, not a numerical evaluation of the full path KL; its teacher/model distinction explains why the target can use information unavailable to the U-Net.

## Origin

> [!info]- Source details
> Requested as one new code-focused learning note, separate from the earlier theory digests. Main sources: Erik Spence, SciNet, *Neural network programming: diffusion models*, 13 May 2025, all 34 PDF pages; the supplied p. 23 screenshot; and the current PyTorch source snapshot from `E:\DAT112\lecture07\torch`, with its parent README. The PDF was read as text and visually inspected; mathematical and architecture discrepancies were checked against the rendered pages and actual source.
>
> The screenshot and PDF are unchanged originals. All eight Python files and the README were copied byte-for-byte. Four core modules receive detailed explanation; preview/archive helpers and the two test modules supply implementation and verification context. Dataset bytes, trained weights, run history and generated cat archives were not copied or digested. The README's older training claims are not presented as newly verified training results.
>
> Code excerpts are from the archived PyTorch files, with indentation/line wrapping adjusted and omissions identified. Tensor shapes, design explanations, comparison with previous notes and source corrections are assistant synthesis prompted by the quoted user question, not user-authored derivations. The original U-Net paper, DDPM Algorithms 1–2, official PyTorch operator documentation and Improved DDPM §§3.2/4 were consulted only for the specific inline clarifications; the lecture bibliography was not separately ingested.
>
> Verification: [[assets/figures/2026-11-11-diffusion-pytorch/check_code.py|reproducible check script]] and [[assets/figures/2026-11-11-diffusion-pytorch/checks.json|results and source hashes]]. Small-model CPU forward shapes, skip concatenations, per-image broadcasting, normalization, finite gradients (including the time branch), an optimizer update, schedule values and mean/noise-loss algebra passed. All eight supplied tests passed with no skips, including a CUDA RNG/mode-isolation check on the available RTX 4090. The supplied TensorFlow-schedule fixture matched; full TensorFlow/PyTorch forward parity was not tested.
>
> “Checked” concerns the explanations and documented behavior, not an endorsement of the source indexing as standard DDPM. No real checkpoint was loaded or changed, no full training or sample-quality assessment was performed, and live Obsidian rendering was not verified. Coverage and immutable-file hashes are recorded in [[_system/Digest Checkpoints]]; the remaining source-indexing issue is in [[_system/Review Queue]].
