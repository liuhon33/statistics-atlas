# Offline interactive figures in Obsidian

Use this mode when moving a parameter reveals a relationship better than watching a fixed movie: linked density slices, score/likelihood views, a rejection threshold, a projection, or an optimization step. A useful control changes a named mathematical quantity and updates the related plots and numerical readouts together.

## Reuse the working infrastructure

The vault's existing `statistics-atlas` plugin renders `atlas-interactive` blocks. Its source is `_system/plugin-src/plugin.js` (`AtlasInteractiveBlock` and `renderInteractive`). It reads a local HTML file into a sandboxed iframe with scripts allowed and same-origin access disabled. Do not install another plugin or change the renderer for an ordinary new figure. Verify the renderer exists in a different vault before promising this behavior.

````markdown
```atlas-interactive
path: assets/figures/<topic>/explorer.html
title: A descriptive, accessible figure title
height: 1100
```

[[assets/figures/<topic>/explorer.html|Open the standalone explorer]]

> [!example]- Static view
> ![[assets/figures/<topic>/overview.svg]]
> *Original analytic illustration. State the model, parameter values and what to notice.*
````

The supported path contains ASCII letters, digits, `_`, `-`, `/`, and `.` under `assets/figures/`, ends in `.html`, and has no `..` segment. The height is a fallback. The bundled builder injects a `ResizeObserver` that sends `{type: 'atlas-interactive-ready', height}` to the parent; the renderer accepts only messages from that iframe. Reading view and rendered Live Preview blocks show the controls. Source mode shows the code block. Keep ordinary Markdown equations and a static fallback outside the iframe for reading/export without the plugin.

Send readiness/height directly after rendering and from `ResizeObserver`, not only through `requestAnimationFrame`: Chromium can suspend animation frames in an offscreen iframe. `ResizeObserver` already batches layout changes; send only when height changes. The builder handles this distinction.

## Build a portable artifact

Keep the model formulas separate from the drawing code, ideally as pure functions usable by Node or Python checks. Put the topic's HTML body, CSS, JS, generator and checks beside its generated files in `assets/figures/<topic>/`. Use deterministic SVG/canvas for mathematical graphics; no network, CDN, remote font, account, local server or external script should be needed to open the delivered HTML.

The reusable builder at `../scripts/build_explorer.py` packs local text inputs, supplies a restrictive CSP and the height handshake, and records input/output hashes:

```powershell
python .agents/skills/animate-geometry/scripts/build_explorer.py `
  --title 'Conditional distributions and their means' `
  --body assets/figures/example/body.html `
  --css assets/figures/example/explorer.css `
  --js assets/figures/example/math.js `
  --js assets/figures/example/explorer.js `
  --output assets/figures/example/explorer.html
```

Repeat `--css` or `--js` in load order. It refuses to overwrite an existing output that no longer matches its build manifest; inspect the changed file before using `--replace`. It does not write to `raw/`. The `.build.json` manifest belongs beside the generated HTML. `compile_html()` and `write_artifact()` are also importable for a topic-specific generator.

## Design the controls around the explanation

- Say what is held fixed: the data-generating law, observations/noise, evaluation parameter, coordinate frame, sample size, or model family. In the Fisher example, changing the evaluation mean does not regenerate the data. Label sample estimates separately from exact population values.
- Use a small set of controls, a reset/reference preset, visible current values, semantic labels and keyboard-operable inputs. Use fixed seeded draws across parameter changes when comparing the same sample; make resampling an explicit separate action if useful.
- Give linked objects persistent colors. Keep axes and scales fixed while a comparison relies on widths/heights. Disclose adaptive ranges, histogram normalization and omitted tails. Equal-looking screen lengths need not represent equal units across panels.
- Keep different spaces explicit: observation vs parameter vs score coordinates; raw slice vs normalized conditional density; a contour slice vs a projected random variable; camera rotation vs changing the model. A density value is not a point probability. A point mass should be drawn as a stem, not a fake narrow density.
- Set meaningful finite parameter ranges. Explain excluded singular cases (for example `|rho| = 1` for a nonsingular bivariate normal). Handle boundaries, zero denominators and tiny variances in the mathematics rather than letting `NaN` reach the plot.
- Use responsive layouts at actual note widths, including a narrow column. Avoid `height:100vh` or a body minimum height tied to the iframe; auto-height can otherwise feed back on itself. Put a high-DPI canvas inside a wrapper with a fixed CSS aspect ratio, then size its pixel buffer inside that box; changing intrinsic canvas dimensions must not change the layout being measured. Check that embed height stabilizes after another resize, rather than merely reaching the renderer's 5000 px cap. Long figures should remain scrollable or be split into useful blocks.
- Animation starts paused and has Play/Pause/Reset controls. Stop it when the document is hidden; keep its button state consistent. Respect reduced-motion preferences. A camera drag should have a reset and a keyboard alternative; it must not change the mathematical parameters.
- Add a short “try this” prompt beside the embed: change one control, predict a visible effect, then compare a numerical readout. Do not put build instructions or plugin internals into the learning flow.

## Adapting an existing screenshot or animation

First locate all notes embedding the actual asset with `rg`. Inspect the source image and any available original implementation. A screenshot containing sliders is still only an image: if source code was not supplied, build and label an original reconstruction rather than implying recovered interactivity. Preserve original bytes and attribution. Reuse one generated explorer in the notes that explain the same object, with a different short prompt where their purposes differ; do not silently add it to unrelated notes.

When only asked to find candidates, inspect the notes and recommend a short ranked list: exact note, mathematical control, linked views, and insight gained. Prefer a controllable relationship over decorative motion. Do not batch-modify the list or rewrite approved relationships without authorization.

## Verify the mathematics and the actual controls

1. Check the formulas analytically and use independent numerical checks for relevant invariants: density integrals/moments, derivative finite differences, covariance inverses, projection orthogonality, endpoint behavior, probability bounds, etc. Test reference values and boundary cases across the allowed control ranges. Shared code agreeing with itself is not an independent check.
2. Build the self-contained HTML, then use an available browser skill for a temporary local preview. Exercise meaningful controls and presets, Play/Pause if present, and camera controls. Check numerical readouts and visible curves at matching/nonmatching parameters or other conceptually distinct states. Inspect wide and note-width layouts. Close temporary servers/tabs afterwards; the delivered HTML must work offline.
3. Generate and visually inspect static SVG/PNG alternatives. Retain axes, normalization and essential qualifications. Source screenshots do not replace inspection of newly generated output.
4. Test the actual Obsidian component when available without repeatedly moving the user's active pane. `assets/figures/2026-11-11-fisher/check_obsidian.js` is a working offscreen integration example: load `plugin.renderInteractive(...)` into a temporary container, wait for readiness, inspect height/sandbox, and unload/remove everything in `finally`. This proves the iframe executed, not that every note formula or slider was visually tested inside Obsidian. Browser interaction tests complement it. Do not weaken sandboxing to inspect the child DOM.
5. Validate affected notes and links using the vault's existing tools. Only if plugin source changes, rebuild its bundle and run the map model/refresh tests required by AGENTS. Report numerical, browser, static-image and live-app checks distinctly; append concise maintenance records and leave work uncommitted unless a commit is authorized.

## Concrete examples to adapt selectively

- `assets/figures/2026-11-11-fisher/`: six linked scalar likelihood/score/curvature plots and a 2D covariance explorer. `math.js` supplies pure formulas; `explorer.js` supplies UI; `test_math.cjs` and `build_visuals.py` supply checks and static views. This older builder embeds its own resize handshake; avoid duplicating it when migrating to the reusable packer.
- `assets/figures/2026-11-11-joint-density/`: reconstruction of the user's density-slice image, with two conditional curves, marginals, weighted conditional means and a rotatable joint surface. It uses the reusable packer and retains the original PNG separately in the notes.

Read only the relevant example files. Treat their colors, dimensions and panel counts as examples, not a mandatory template.
