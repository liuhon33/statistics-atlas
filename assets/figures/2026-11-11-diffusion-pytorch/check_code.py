"""Reproduce the digest's source, shape, algebra and small-model checks.

Run with pytorch_learn Python, -s -B. No lecture checkpoint is loaded or changed.
The digest checks run on CPU; the supplied archive-isolation test also checks
CUDA if it is available. Temporary test files stay under D:/CodexStorage/temp.
"""
from pathlib import Path
import hashlib
import importlib
import io
import json
import os
import sys
import tempfile
import unittest

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "raw/notes/2026-11-11-DAT112-Lecture07-torch"
LIVE = Path(r"E:\DAT112\lecture07\torch")
TEMP = Path(r"D:\CodexStorage\temp\dat112-digest")
TEMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = os.environ["TMP"] = str(TEMP)
tempfile.tempdir = str(TEMP)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ARCHIVE))
from unet import NaiveUnet
from ddpm import ddpm_schedules
from diffusion_model import CatDataset
from reverse_diffusion import sample_from_model

torch.set_num_threads(2)
torch.manual_seed(1126)
report = {
    "runtime": {"python": sys.executable, "torch": torch.__version__,
                "digest_check_device": "cpu",
                "cuda_available": torch.cuda.is_available(),
                "cuda_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None},
    "limits": [
        "Small n_feat=8 model, not the n_feat=512 training run.",
        "No pretrained checkpoint loaded, no full training, no image-quality claim.",
        "No TensorFlow forward-output parity or live Obsidian-render claim.",
        "Known schedule/indexing and slide discrepancies are documented, not repaired."
    ]
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pairs = [(p, LIVE / p.name) for p in sorted(ARCHIVE.glob("*.py"))]
pairs += [(ARCHIVE / "2026-11-11-DAT112-Lecture07-source-README.md", LIVE.parent / "README.md"),
          (ROOT / "raw/notes/2025-05-13-DAT112-Lecture07-Diffusion-models.pdf",
           LIVE.parent / "slides/7_DM.pdf"),
          (ROOT / "raw/assets/2025-05-13-DAT112-diffusion-I01-unet.png",
           Path(r"D:\CODEXS~1\temp\claudian-codex-images-m3qWzc\1-image.png"))]
sources = []
for preserved, source in pairs:
    digest = sha(preserved)
    original_exists = source.is_file()
    if original_exists:
        assert digest == sha(source), (preserved, source)
    sources.append({"path": preserved.relative_to(ROOT).as_posix(),
                    "source_path": str(source), "sha256": digest,
                    "bytes": preserved.stat().st_size,
                    "source_exists_on_rerun": original_exists,
                    "byte_identity_verified": original_exists})
report["sources"] = sources

# Trace every image resolution and every skip concatenation.
F, B = 8, 2
model = NaiveUnet((64, 64, 3), F).cpu()
x0 = torch.rand(B, 3, 64, 64)
shapes, skip_shapes = {}, {}
handles = []
for name in ["init_conv", "down1", "down2", "down3", "to_vec", "timeemb",
             "up0", "up1", "up2", "up3", "out"]:
    def capture(module, inputs, output, name=name):
        shapes[name] = list(output.shape)
    handles.append(getattr(model, name).register_forward_hook(capture))
for name in ["up1", "up2", "up3"]:
    def capture_skip(module, inputs, name=name):
        main, skip = inputs[0]
        assert main.shape[0] == skip.shape[0] and main.shape[2:] == skip.shape[2:]
        skip_shapes[name] = {"main": list(main.shape), "skip": list(skip.shape),
                             "cat": list(torch.cat([main, skip], dim=1).shape)}
    handles.append(getattr(model, name).register_forward_pre_hook(capture_skip))
s = ddpm_schedules(1e-4, 0.02, 1000)
t = torch.tensor([1, 1000])
eps = torch.randn_like(x0)
a = s["sqrtab"][t].reshape(B, 1, 1, 1)
b = s["sqrtmab"][t].reshape(B, 1, 1, 1)
xt = a * x0 + b * eps
predicted = model([xt, t.float()/1000])
for handle in handles:
    handle.remove()
expected = {
    "init_conv": [B,F,64,64], "down1": [B,F,32,32],
    "down2": [B,2*F,16,16], "down3": [B,2*F,8,8],
    "to_vec": [B,2*F,2,2], "timeemb": [B,2*F],
    "up0": [B,2*F,8,8], "up1": [B,2*F,16,16],
    "up2": [B,F,32,32], "up3": [B,F,64,64], "out": [B,3,64,64]
}
assert shapes == expected, shapes
assert list(predicted.shape) == [B,3,64,64]
report["shapes"] = shapes
report["skip_shapes"] = skip_shapes
report["small_model_parameters"] = sum(p.numel() for p in model.parameters())

# Exact algebraic shape/normalization correspondences, up to float rounding.
torch.testing.assert_close(a*a + b*b, torch.ones_like(a))
loss = torch.nn.functional.mse_loss(predicted, eps)
explicit = ((predicted-eps)**2).sum()/(B*3*64*64)
torch.testing.assert_close(loss, explicit)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, eps=1e-7)
optimizer.zero_grad(set_to_none=True)
before = model.out.weight.detach().clone()
loss.backward()
assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
assert model.timeemb.Dense_1.weight.grad.abs().sum().item() > 0
optimizer.step()
assert not torch.equal(before, model.out.weight)
report["training"] = {"mse": loss.item(), "all_gradients_finite": True,
                      "time_embedding_nonzero_gradient": True, "optimizer_changed_weights": True,
                      "broadcast_shapes": [list(a.shape), list(b.shape)],
                      "loss_denominator": B*3*64*64}

beta_np = np.linspace(1e-4, 0.02, 1001, dtype=np.float64)
abar_np = np.cumprod(1-beta_np)
np.testing.assert_allclose(s["alphabar_t"].numpy(), abar_np, rtol=3e-6)
torch.testing.assert_close(s["sqrtab"]**2+s["sqrtmab"]**2, torch.ones(1001))
report["schedule"] = {
    "length": len(beta_np), "beta0": float(beta_np[0]), "beta1": float(beta_np[1]),
    "alphabar0": float(abar_np[0]), "alphabar1": float(abar_np[1]),
    "alphabar1000": float(abar_np[-1]),
    "training_indices": [1,1000], "sampling_indices": [1000,0],
    "standard_baralpha0": 1.0
}

# The source recurrence equals its written mean, not simple x_t - epsilon.
i = 375
state, ehat = torch.randn(3,4, dtype=torch.float64), torch.randn(3,4, dtype=torch.float64)
alpha, abar = s["alpha_t"][i].double(), s["alphabar_t"][i].double()
mu_formula = (state-(1-alpha)/torch.sqrt(1-abar)*ehat)/torch.sqrt(alpha)
mu_code = s["oneover_sqrta"][i].double()*(state-s["mab_over_sqrtmab"][i].double()*ehat)
torch.testing.assert_close(mu_code, mu_formula, rtol=1e-6, atol=1e-7)

# Fixed-variance Gaussian-mean loss and weighted epsilon loss agree.
beta = torch.tensor(0.02, dtype=torch.float64)
alpha = 1-beta
abar_prev = torch.tensor(0.72, dtype=torch.float64)
abar = alpha*abar_prev
clean, noise, estimate = [torch.randn(7, dtype=torch.float64) for _ in range(3)]
state = torch.sqrt(abar)*clean+torch.sqrt(1-abar)*noise
teacher = (state-beta/torch.sqrt(1-abar)*noise)/torch.sqrt(alpha)
mu = (state-beta/torch.sqrt(1-abar)*estimate)/torch.sqrt(alpha)
variance = beta
lhs = (teacher-mu).square().sum()/(2*variance)
rhs = beta.square()/(2*variance*alpha*(1-abar))*(noise-estimate).square().sum()
torch.testing.assert_close(lhs, rhs, rtol=1e-12, atol=1e-12)
report["algebra"] = {"mean_recurrence_pass": True, "weighted_loss_abs_error": abs(lhs-rhs).item()}

# Dataset layout is permutation, not reshaping or a range change to [-1,1].
with tempfile.TemporaryDirectory(dir=TEMP) as tmp:
    path = Path(tmp)/"synthetic.npy"
    raw = np.arange(2*64*64*3).reshape(2,64,64,3).astype(np.uint8)
    np.save(path, raw)
    data = CatDataset(path)
    torch.testing.assert_close(data[0], torch.from_numpy((raw[0]/255).astype("float32").transpose(2,0,1).copy()))
    data.data._mmap.close()  # Release the Windows file mapping before temp cleanup.
    del data
report["dataset"] = {"synthetic_layout": [3,64,64], "range": [0,1], "pass": True}

# Instrument the actual sampler to prove the extra untrained endpoint call.
class RecordingModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.dummy = torch.nn.Parameter(torch.zeros(()))
        self.times = []
    def forward(self, inputs):
        x, time = inputs
        self.times.append(float(time[0,0]))
        return torch.zeros_like(x)+self.dummy

recorder = RecordingModel().train()
random_before = torch.get_rng_state().clone()
config = {"image_shape": (64,64,3), "beta1": 1e-4, "beta2": 0.02, "T": 2, "n_feat": 8}
samples = sample_from_model(recorder, config, n_sample=1, seed=42, verbose=False)
assert recorder.times == [1.0,0.5,0.0]
assert recorder.training and torch.equal(random_before, torch.get_rng_state())
assert samples.shape == (1,64,64,3)
report["sampler_trace"] = {"T": 2, "calls": recorder.times, "mode_restored": True, "rng_preserved": True}

# Run all 8 existing lecture tests without editing their source/checkpoints.
# Rebind only the modules' __file__ for fixture and data lookup; code is from
# the byte-verified archive. All writes by these tests are temporary fixtures.
import diffusion_model as dm
dm.HERE = LIVE
suite = unittest.TestSuite()
for name in ["test_conversion", "test_sample_archive"]:
    module = importlib.import_module(name)
    module.__file__ = str(LIVE/(name+".py"))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
report["supplied_tests"] = {"run": result.testsRun, "skipped": len(result.skipped),
                          "failures": len(result.failures), "errors": len(result.errors),
                          "output": stream.getvalue()}
assert result.wasSuccessful(), stream.getvalue()
report["result"] = "PASS"
(OUT/"checks.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k not in ["sources"]}, indent=2))
