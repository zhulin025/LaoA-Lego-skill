---
name: laoa-lego
description: Generate a high-recognition LEGO-style brick-built 3D model from a keyword or reference image through a concept-image-first workflow, including reference-faithful explicit micro-brick models for faces, mosaics, pixel sculptures, and thin painted details, then deliver an interactive webpage with assembly, disassembly, scatter, orbit, pan, and zoom. Use for characters, robots, vehicles, creatures, buildings, objects, exact image replication, or validation, repair, conversion, packaging, and preview of BrickMorph JSON.
---

# LaoA-Lego skill

Deliver an interactive 3D webpage, not only model JSON. Use Codex's current model to author the geometry; do not call another paid LLM API unless the user explicitly asks.

## Generate the modeling concept first

For a keyword-only request, do not jump directly from text to geometry. Read [references/concept-image-workflow.md](references/concept-image-workflow.md), use the built-in image generation tool to create a clean 3D brick-built concept image, and save the accepted image under `<output>/reference/`. This concept image becomes the visual contract for the model.

If the user supplies a non-brick reference, preserve it as the identity source and generate a normalized brick-built concept derived from it. If the supplied image is already a clear, full-subject brick-built 3D render, it may serve directly as the concept image. Never replace or contradict a user-supplied identity reference.

Do not author `model.json` until the concept passes the landmark and buildability checklist. If built-in image generation is unavailable, do not silently skip this step; disclose the limitation and continue with direct modeling only after the user approves.

## Choose the representation after the concept image

Select before modeling:

- Use `primitives-v1` for editable, compact, fully three-dimensional subjects whose identity comes from silhouette, volume, openings, armor, limbs, or mechanical parts. Read [references/model-schema.md](references/model-schema.md) and [references/modeling-guide.md](references/modeling-guide.md).
- Use `explicit-bricks-v1` when a supplied reference depends on small facial marks, pixel art, mosaic color boundaries, text, thin linework, or exact front-view color placement; also switch to it when a primitive model remains visibly coarse after one repair. Read [references/explicit-bricks-schema.md](references/explicit-bricks-schema.md) and [references/reference-direct-modeling.md](references/reference-direct-modeling.md).

Do not treat a larger requested count as a substitute for the correct representation. Primitive resampling can only refine geometry that already encodes the intended feature.

## Core workflow

1. Create a dedicated output directory. Use the user's requested path; otherwise use `<safe-subject>-laoa-lego-model/` in the current workspace. Use `models/` only when the current repository requires generated artifacts there.
2. Establish the canonical subject:
   - Prefer the version named by the user.
   - Treat supplied reference images as primary evidence.
   - Otherwise research front, side, and three-quarter references when image search is available.
   - Record silhouette, proportions, palette, and at least 8 unmistakable landmarks in a brief.
3. Create and accept the modeling concept:
   - Generate `<output>/reference/concept.png` from the brief with the built-in image generation tool.
   - Save the final structured prompt as `<output>/reference/concept-prompt.md`.
   - Reject concepts with the wrong version, missing landmarks, cropped silhouette, duplicated anatomy, smooth non-brick surfaces, or invented accessories. Make one targeted image repair and re-check it; never accept a concept that still fails a critical identity check.
   - Record any occluded or ambiguous geometry as explicit assumptions in the brief.
4. Choose the representation from the accepted concept, then author `<output>/model.json`:
   - For `primitives-v1`, target 56-72 meaningful primitives and `requestedBrickCount: 16000`; build in Boolean order: structural `add`, local `subtract`, then thin color/detail `add`.
   - For `explicit-bricks-v1`, generate a deterministic surface shell or volume, paint reference-critical regions directly at brick resolution, export unique `[x,y,z,material]` entries, and set `requestedBrickCount` to the exact array length. Keep the result at or below 150,000 bricks.
   - Map every landmark in the brief to one or more concrete `part` names or explicit-brick regions. Do not invent geometry that contradicts the accepted concept.
5. Recompute and write the self-check:

   ```bash
   python3 <skill-dir>/scripts/brick_model.py check <output>/model.json --write-self-check
   ```

6. Repair every failed hard check and rerun it. Perform up to three focused repair passes. Never lower a threshold or claim that a failing model passed. If visual or numeric concerns remain, disclose them and still package the user's inspectable result.
7. Build the standalone webpage and ZIP:

   ```bash
   python3 <skill-dir>/scripts/build_viewer.py \
     <output>/model.json --output <output>/viewer --zip
   ```

8. Start the viewer and keep the process running:

   ```bash
   python3 <skill-dir>/scripts/serve_viewer.py <output>/viewer --port 0
   ```

   Return the printed URL as the primary deliverable. In an environment that exposes forwarded ports, return its preview URL. If serving is unavailable, return `viewer/index.html`, `model.json`, and the ZIP artifact explicitly.
9. Open the webpage when browser control is available. Verify model load, assembled form, disassembled form, drag rotation, zoom, and at least one alternate scatter shape. Capture the assembled three-quarter view and compare it with the accepted concept. Require at least 80% landmark agreement and full agreement on critical silhouette landmarks; use remaining repair passes for the largest mismatches.

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
- Accepted concept image and concept prompt paths.
- Subject/version chosen, representation, primitive or explicit-brick count, and quality result.
- Landmark agreement result against the concept image.
- Any unresolved numeric or visual warning.

The generated viewer is self-contained and carries local Three.js files. It supports assembly, disassembly, ring/sphere/tornado scatter layouts, progress scrubbing, automatic rotation, pointer orbit, pan, zoom, and light/dark theme. It does not require the BrickMorph website or an API key.
