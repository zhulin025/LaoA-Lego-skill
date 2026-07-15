<p align="center">
  <img src="laoa-lego/assets/viewer/assets/brickmorph-icon-64.png" width="64" height="64" alt="LaoA-Lego skill icon">
</p>

# LaoA-Lego skill

**Version 0.4**

`$laoa-lego` turns a keyword or reference image into a high-recognition
brick-built 3D model and a self-contained interactive webpage.

Version 0.4 uses a concept-image-first workflow: keyword requests first produce
and validate a canonical 3D brick-built concept image, then author the model
against that visual contract and compare the assembled viewer back to it.

Every run can produce:

- An accepted `reference/concept.png` and its exact generation prompt.
- A validated BrickMorph-compatible `model.json`.
- Compact `primitives-v1` geometry or exact `explicit-bricks-v1` coordinates.
- A local webpage with assembly, disassembly, ring/sphere/tornado scatter,
  orbit, pan, zoom, progress scrubbing, automatic rotation, and theme switching.
- A portable ZIP with local Three.js runtime files and no CDN dependency.

The skill uses Codex's current model and built-in image generation. It does not
require a second paid LLM API call.

## Install

```text
Use $skill-installer to install laoa-lego from
https://github.com/zhulin025/lego-model-skill
```

Or clone and link it manually:

```bash
git clone https://github.com/zhulin025/lego-model-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/lego-model-skill/laoa-lego" \
  "${CODEX_HOME:-$HOME/.codex}/skills/laoa-lego"
```

For Codex Cloud or repository-scoped use, place or link `laoa-lego/` under
`.agents/skills/laoa-lego`. Reload Codex after installation.

## Use

```text
Use $laoa-lego to create a classic black-haired Son Goku brick model. Generate
and validate the canonical concept image first, then open the interactive viewer.
```

```text
Use $laoa-lego with this reference image. Preserve its identity, silhouette,
pose, proportions, and color blocking while translating it into visible bricks.
```

```text
Use $laoa-lego to reproduce this character as an explicit high-detail
micro-brick model and preserve small facial marks and color boundaries.
```

```text
Use $laoa-lego to improve this existing model.json and package a new viewer.
```

## Model formats

Use `primitives-v1` for editable 3D subjects whose identity comes from volumes,
limbs, armor, openings, or mechanical parts. Use `explicit-bricks-v1` when the
reference needs direct brick-level control for a face, text, mosaic, pixel
sculpture, or thin decorative lines.

## Validate

```bash
python3 laoa-lego/scripts/brick_model.py check model.json --write-self-check
python3 laoa-lego/scripts/build_viewer.py model.json --output viewer --zip
python3 laoa-lego/scripts/serve_viewer.py viewer --port 0
```

The runtime uses only Python's standard library.

## License

MIT
