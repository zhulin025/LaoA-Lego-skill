---
name: lego-model
description: Generate a high-recognition LEGO-style brick-built 3D model from a keyword or reference image, including reference-faithful explicit micro-brick models for faces, mosaics, pixel sculptures, and thin painted details, then deliver an interactive webpage with assembly, disassembly, scatter, orbit, pan, and zoom. Use for characters, robots, vehicles, creatures, buildings, objects, exact image replication, or validation, repair, conversion, packaging, and preview of BrickMorph JSON.
---

# LEGO Model

Deliver an interactive 3D webpage, not only model JSON. Use Codex's current model to author the geometry; do not call another paid LLM API unless the user explicitly asks.

## Choose the representation

Select before modeling:

- Use `primitives-v1` for editable, compact, fully three-dimensional subjects whose identity comes from silhouette, volume, openings, armor, limbs, or mechanical parts. Read [references/model-schema.md](references/model-schema.md) and [references/modeling-guide.md](references/modeling-guide.md).
- Use `explicit-bricks-v1` when a supplied reference depends on small facial marks, pixel art, mosaic color boundaries, text, thin linework, or exact front-view color placement; also switch to it when a primitive model remains visibly coarse after one repair. Read [references/explicit-bricks-schema.md](references/explicit-bricks-schema.md) and [references/reference-direct-modeling.md](references/reference-direct-modeling.md).

Do not treat a larger requested count as a substitute for the correct representation. Primitive resampling can only refine geometry that already encodes the intended feature.

## Core workflow

1. Create a dedicated output directory. Use the user's requested path; otherwise use `<safe-subject>-lego-model/` in the current workspace. Use `models/` only when the current repository requires generated artifacts there.
2. Establish the canonical subject:
   - Prefer the version named by the user.
   - Treat supplied reference images as primary evidence.
   - Otherwise research front, side, and three-quarter references when image search is available.
   - Record silhouette, proportions, palette, and at least 8 unmistakable landmarks in a brief.
3. Author `<output>/model.json` in the selected representation:
   - For `primitives-v1`, target 56-72 meaningful primitives and `requestedBrickCount: 16000`; build in Boolean order: structural `add`, local `subtract`, then thin color/detail `add`.
   - For `explicit-bricks-v1`, generate a deterministic surface shell or volume, paint reference-critical regions directly at brick resolution, export unique `[x,y,z,material]` entries, and set `requestedBrickCount` to the exact array length. Keep the result at or below 150,000 bricks.
4. Recompute and write the self-check:

   ```bash
   python3 <skill-dir>/scripts/brick_model.py check <output>/model.json --write-self-check
   ```

5. Repair every failed hard check and rerun it. Perform up to three focused repair passes. Never lower a threshold or claim that a failing model passed. If visual or numeric concerns remain, disclose them and still package the user's inspectable result.
6. Build the standalone webpage and ZIP:

   ```bash
   python3 <skill-dir>/scripts/build_viewer.py \
     <output>/model.json --output <output>/viewer --zip
   ```

7. Start the viewer and keep the process running:

   ```bash
   python3 <skill-dir>/scripts/serve_viewer.py <output>/viewer --port 0
   ```

   Return the printed URL as the primary deliverable. In an environment that exposes forwarded ports, return its preview URL. If serving is unavailable, return `viewer/index.html`, `model.json`, and the ZIP artifact explicitly.
8. Open the webpage when browser control is available. Verify model load, assembled form, disassembled form, drag rotation, zoom, and at least one alternate scatter shape. For a reference-driven result, capture the assembled front view and compare feature placement against the reference before handoff.

## Existing Models

Preserve an existing file unless the user requests in-place editing. Save a new revision, run the checker, then build a fresh viewer directory.

```bash
python3 <skill-dir>/scripts/brick_model.py check <model.json> --json
```

## Handoff

Always report:

- Clickable running viewer URL when available.
- Viewer directory and ZIP path.
- Source `model.json` path.
- Subject/version chosen, representation, primitive or explicit-brick count, and quality result.
- Any unresolved numeric or visual warning.

The generated viewer is self-contained and carries local Three.js files. It supports assembly, disassembly, ring/sphere/tornado scatter layouts, progress scrubbing, automatic rotation, pointer orbit, pan, zoom, and light/dark theme. It does not require the BrickMorph website or an API key.
