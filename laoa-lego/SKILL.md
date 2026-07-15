---
name: laoa-lego
description: Generate a high-recognition LEGO-style 3D model from a keyword or reference image through a concept-image-first, structure-first workflow, then deliver an interactive webpage with assembly, disassembly, scatter, orbit, pan, and zoom. Use for characters, robots, vehicles, creatures, buildings, objects, pixel art, mosaics, exact image replication, or validation, repair, conversion, packaging, and preview of BrickMorph JSON.
---

# LaoA-Lego skill

Deliver an interactive 3D webpage, not only model JSON. Use Codex's current model to author the geometry; do not call another paid LLM API unless the user explicitly asks.

## Generate the modeling concept first

For a keyword-only request, read [references/concept-image-workflow.md](references/concept-image-workflow.md), generate a clean brick-built concept image with the built-in image tool, and save the accepted image under `<output>/reference/`. Treat it as the visual contract.

Preserve a supplied identity reference under `<output>/reference/` and record its relative path as `identityReference` in `model.json`. A clear, full-subject brick-built render may serve directly as the concept. Do not author `model.json` until the concept passes the identity, buildability, articulation, and framing checks.

If built-in image generation is unavailable, disclose the limitation and continue with direct modeling only after the user approves; never silently skip the concept gate.

## Choose structure before surface detail

Choose the representation after accepting the concept:

- Default to `primitives-v1` for every fully three-dimensional subject, especially characters, humanoids, robots, vehicles, creatures, and objects with limbs, joints, armor, layered hulls, or readable construction seams. Read [references/model-schema.md](references/model-schema.md) and [references/modeling-guide.md](references/modeling-guide.md).
- For a character or humanoid, also read [references/articulated-character-modeling.md](references/articulated-character-modeling.md). Build hands, feet, joints, hair, clothing, and facial depth as semantic parts. A single sphere, ellipsoid, or capsule is never an acceptable hand, fist, or foot.
- Use `explicit-bricks-v1` only when the deliverable is primarily planar or coordinate-exact: pixel art, mosaics, text, logos, shallow reliefs, or front-view color maps. Read [references/explicit-bricks-schema.md](references/explicit-bricks-schema.md) and [references/reference-direct-modeling.md](references/reference-direct-modeling.md).

Do not switch an entire 3D character to `explicit-bricks-v1` merely for scars, eyes, costume lines, or higher brick count. Express those details as thin add primitives on a structured base. If the format cannot reproduce a tiny mark without destroying anatomy, preserve the anatomy and disclose the tiny-detail limitation.

## Core workflow

1. Create a dedicated output directory. Use the requested path; otherwise use `<safe-subject>-laoa-lego-model/` in the workspace.
2. Establish the canonical subject:
   - prefer the named version and supplied references;
   - otherwise research authoritative front, side, and three-quarter references when available;
   - record silhouette, proportions, palette, at least 8 identity landmarks, and 10 or more semantic part groups;
   - for humanoids, explicitly allocate parts for both palms/fists, thumbs, finger or knuckle blocks, wrists, feet, and shoes.
3. Generate and accept `<output>/reference/concept.png`:
   - save the exact prompt as `<output>/reference/concept-prompt.md`;
   - reject wrong versions, cropped silhouettes, duplicate anatomy, smooth action-figure surfaces, invented accessories, featureless ball hands, fused feet, or joints without readable segmentation;
   - make one targeted image repair when needed and re-check.
   - record `conceptReference: "reference/concept.png"` in `model.json`; when the user supplied an image, also record `identityReference` so the viewer can prefer the original user reference.
4. Author `<output>/model.json` from the accepted concept:
   - for `primitives-v1`, target 56-72 meaningful primitives and `requestedBrickCount: 16000`; complex articulated characters may use up to 80;
   - build in Boolean order: structural `add`, identity-changing `subtract`, then thin color/detail `add`;
   - map every landmark to concrete `part` names; use side-prefixed English part names such as `left_palm`, `left_thumb`, and `left_finger_block` so the checker can verify articulation;
   - for `explicit-bricks-v1`, export unique coordinates and keep the result at or below 150,000 bricks.
5. Recompute the self-check:

   ```bash
   python3 <skill-dir>/scripts/brick_model.py check <output>/model.json --write-self-check
   ```

6. Repair every failed hard check and rerun it. Perform up to three focused repair passes. Never lower thresholds or claim a failing model passed.
7. Build the standalone webpage and ZIP:

   ```bash
   python3 <skill-dir>/scripts/build_viewer.py \
     <output>/model.json --output <output>/viewer --zip
   ```

   The builder automatically packages the user reference when `identityReference`, `userReference`, or `referenceImage` is present; otherwise it packages `conceptReference`. For an older model without metadata, pass `--reference-image <path>` explicitly. The viewer shows the selected image as a bottom-right comparison thumbnail and opens the original image in a closable lightbox.

8. Start the viewer and keep it running:

   ```bash
   python3 <skill-dir>/scripts/serve_viewer.py <output>/viewer --port 0
   ```

9. Validate in the browser:
   - verify load, assembly, disassembly, rotation, zoom, and one alternate scatter layout;
   - compare a matching three-quarter view against the concept;
   - inspect close views of both hands, both feet, the face, and the major joints;
   - require at least 80% landmark agreement, 100% critical silhouette agreement, and zero featureless ball hands or feet;
   - spend repair passes on anatomy and structural readability before surface decoration.

## Existing models

Preserve the existing file unless the user requests in-place editing. Save a new revision, run the checker, and build a fresh viewer directory.

```bash
python3 <skill-dir>/scripts/brick_model.py check <model.json> --json
```

## Handoff

Report the running viewer URL, viewer directory, ZIP, source `model.json`, the comparison image displayed in the viewer, concept prompt, chosen subject/version, representation, count, quality result, landmark agreement, hand/foot articulation result, and unresolved warnings.

The generated viewer carries local Three.js files and supports assembly, disassembly, ring/sphere/tornado scatter, progress scrubbing, automatic rotation, orbit, pan, zoom, and light/dark theme. It needs no BrickMorph website or API key.
