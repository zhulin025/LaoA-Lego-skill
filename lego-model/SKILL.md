---
name: lego-model
description: Generate a high-recognition LEGO-style brick-built 3D model from a keyword, reference image, character, robot, vehicle, creature, building, or object, then deliver a ready-to-open interactive webpage with assembly, disassembly, scatter forms, orbit rotation, pan, and zoom. Use when Codex is asked to create a brick model such as Bumblebee, Gundam, Optimus Prime, a spaceship, a landmark, or a custom subject; also use to validate, repair, package, preview, or improve an existing BrickMorph model JSON.
---

# LEGO Model

Deliver an interactive 3D webpage, not only model JSON. Use Codex's current model to author the geometry; do not call another paid LLM API unless the user explicitly asks.

## Workflow

1. Create a dedicated output directory. Use the user's requested path; otherwise use `<safe-subject>-lego-model/` in the current workspace. Use `models/` only when the current repository requires generated artifacts there.
2. Read [references/model-schema.md](references/model-schema.md) before authoring or editing JSON.
3. Read [references/modeling-guide.md](references/modeling-guide.md) before creating a new subject or repairing weak visual identity.
4. Establish the canonical subject:
   - Prefer the version named by the user.
   - Treat supplied reference images as primary evidence.
   - Otherwise research front, side, and three-quarter references when image search is available.
   - Record silhouette, proportions, palette, and at least 8 unmistakable landmarks in a brief.
5. Author a complete compact JSON at `<output>/model.json`. Target 56-72 meaningful primitives and 16,000 requested bricks. Build in Boolean order: structural `add`, local `subtract`, then thin color/detail `add`.
6. Recompute and write the self-check:

   ```bash
   python3 <skill-dir>/scripts/brick_model.py check <output>/model.json --write-self-check
   ```

7. Repair every failed hard check and rerun it. Perform up to three focused repair passes. Never lower a threshold or claim that a failing model passed. If visual or numeric concerns remain, disclose them and still package the user's inspectable result.
8. Build the standalone webpage and ZIP:

   ```bash
   python3 <skill-dir>/scripts/build_viewer.py \
     <output>/model.json --output <output>/viewer --zip
   ```

9. Start the viewer and keep the process running:

   ```bash
   python3 <skill-dir>/scripts/serve_viewer.py <output>/viewer --port 0
   ```

   Return the printed URL as the primary deliverable. In an environment that exposes forwarded ports, return its preview URL. If serving is unavailable, return `viewer/index.html`, `model.json`, and the ZIP artifact explicitly.
10. Open the webpage when browser control is available. Verify model load, assembled form, disassembled form, drag rotation, zoom, and at least one alternate scatter shape. Fix the model or package if the page fails.

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
- Subject/version chosen, primitive count, and quality result.
- Any unresolved numeric or visual warning.

The generated viewer is self-contained and carries local Three.js files. It supports assembly, disassembly, ring/sphere/tornado scatter layouts, progress scrubbing, automatic rotation, pointer orbit, pan, zoom, and light/dark theme. It does not require the BrickMorph website or an API key.
