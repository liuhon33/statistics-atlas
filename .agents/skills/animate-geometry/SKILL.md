---
name: animate-geometry
description: Create checked mathematical diagrams, GIFs, and offline interactive explorers for Obsidian notes. Use for sliders, linked plots, rotatable geometry, or animated mathematical transformations, including adapting a source diagram; not decorative image generation.
---

# Animate geometry for learning notes

The user explicitly liked the standardization GIF and asked to preserve its technique on 2026-11-09. Treat it as a useful example, not a requirement to animate every note. Follow the vault SOP for authorization, note placement, source preservation and review; making a figure does not authorize a digest or a commit.

## Choose the useful format

The user also requested reusable slider-based figures after the Fisher-information explorers on 2026-11-11. Keep one skill: the mathematical and visual checks are shared, while the output formats serve different reading tasks.

- **Static SVG:** a definition, comparison or geometry is clearest when all relevant states are visible together.
- **GIF with static keyframes:** a staged transformation has a useful order, such as center then normalize. Follow the generator guidance below.
- **Interactive HTML:** the reader should control a parameter, inspect a slice, rotate a view, or compare linked distributions. Read [references/interactive-explorers.md](references/interactive-explorers.md) for the existing Obsidian renderer, reusable builder, control design and integration checks.

Reuse an existing source figure when it already explains the relationship. If asked to find other suitable notes, inspect them and recommend specific controls and insights; discovery alone does not authorize changing the whole list. Existing note identities, approvals and source bytes stay intact during a visual-only update.

## Working GIF reference

Resolve these paths against the current vault root:

- `assets/figures/2026-11-09-standardization/draw_standardization.py`: complete tested generator, including `scene`, `centering_figure`, `scaling_figure`, `sphere_figure`, `animation`, and `checks`.
- `assets/figures/2026-11-09-standardization/05-center-then-normalize.gif`: user-liked result.
- `Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation.md`: captions, coordinate definitions and interpretation.

Inspect the relevant generator functions before adapting them. Write a new topic's generator and outputs into its own folder under `assets/figures/`; do not rerun the reference generator over approved figures just to make a new animation. Keep supplied screenshots unchanged in `raw/` and label generated geometry as an original reconstruction or illustrative example.

## Design the explanation before rendering

- Define what each axis, point, vector, plane and length represents. Changing from individuals-as-points to features-as-vectors must be explicit. Distinguish the mathematical object from its screen projection.
- Give each object a persistent color and label across all scenes. Use a few interpretable constructed examples rather than an unlabeled random cloud. Record their actual coordinates.
- Split transformations into phases so the viewer can tell what changes and what stays fixed. Translate, rotate and rescale separately when that distinction is the teaching point. Briefly hold the starting state, intermediate result and final state.
- Keep camera orientation and axis scales fixed during a phase. If a zoom is needed for legibility, separate or disclose it. Do not let camera motion masquerade as a data transformation.
- Supply labeled static SVG keyframes alongside the GIF. They let the reader inspect an equation or compare endpoints without racing the loop. Put the relevant explanation next to each embed.

## Exact construction, not plausible-looking motion

For scientific geometry, use deterministic plotting/code (the reference uses NumPy, Matplotlib and Pillow), not generative raster drawing. Check an available Python runtime and imports before use; `D:/anaconda/python.exe` worked for this example, but recheck availability rather than assuming it.

Compute every frame from the phase parameter, not by repeatedly updating the previous frame. Example for mean removal and radial unit normalization:

```python
# x, p, c are arrays with one feature vector per row.
# p_j = mean(x_j) * ones; c_j = x_j - p_j
# Exclude/handle constant features before division.
centered_motion = x - t * p                 # 0 <= t <= 1
radius = np.linalg.norm(c, axis=1)
q = c / radius[:, None]
radial_motion = ((1 - t)*radius + t)[:, None] * q
```

The first endpoint moves parallel to the all-ones direction. The second stays in the zero-mean subspace and preserves its direction. Small radii expand; large radii shrink. This second phase is **unit-length normalization**, not sample z-score standardization: the latter has Euclidean radius `sqrt(n-1)`.

Translate a residual arrow by moving both its tail and tip by the same amount. An arrow from the projection foot to the original endpoint is the same displacement as the centered arrow drawn from the origin. A plane/sphere intersection should be computed from the actual plane basis, not added as a decorative ellipse.

## Rendering choices from the successful example

- Dark background with bright, distinct feature colors; neutral wireframe and a translucent plane. Adapt the palette to the note rather than requiring this theme.
- `FuncAnimation` + `PillowWriter(fps=11)`; 8-inch square figure at 90 dpi produced a 720×720 GIF without FFmpeg. Four SVGs and PNG inspection previews accompany it. These are starting values, not fixed requirements.
- For the plane perpendicular to `(1,1,1)`, `view_init(elev=22, azim=-10)` made its area visible. The earlier `azim=-56` nearly hid it edge-on. Choose a view using the actual plane normal; include a face-on inset when the reader needs to compare angles.
- Keep labels away from arrows and from one another. Prefer short labels on the graphic and full coordinates in its caption. Perspective does not preserve angles; do not measure Pearson's angle from the oblique screen view.

## Verification and handover

1. Assert the mathematical invariants: endpoints, projection/orthogonality, preserved lengths or directions, plane constraints, normalization factors, and any claimed identity. Record maximum numerical errors; numerical checks support an analytic explanation, not a probabilistic proof.
2. Save the generator, constructed data and check results beside the artifacts. Include enough setup information to reproduce them without modifying originals.
3. Parse SVGs and inspect their rendered previews. Decode the GIF and inspect frames spanning **every phase**, including the endpoints. Pillow can merge identical hold frames: use the saved GIF's actual `n_frames`, not the animation's requested frame count, when selecting inspection frames.
4. Embed the GIF with `![[assets/figures/<topic>/<animation>.gif]]`; add a caption explaining phases, colors and any camera zoom. Link the reproducible source and embed static keyframes near their explanations.
5. Validate the note and vault when changing learning content. State whether visual review covered generated previews, sampled GIF frames or actual live Obsidian rendering; these are different checks. Leave work uncommitted unless approval was given.
