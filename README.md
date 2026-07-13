<p align="center">
  <img src="lego-model/assets/viewer/assets/brickmorph-icon-64.png" width="64" height="64" alt="LEGO Model Skill icon">
</p>

# LEGO Model Skill

\`$lego-model\` turns a keyword or reference image into a detailed brick-built
3D model and a ready-to-open interactive webpage.

Every run can produce:

- A validated BrickMorph-compatible \`model.json\`.
- A webpage with assembly, disassembly, ring/sphere/tornado scatter layouts,
  orbit, pan, zoom, progress scrubbing, automatic rotation, and theme switching.
- Local Three.js runtime files, so the viewer does not depend on a CDN.
- A ZIP archive for download, sharing, or static deployment.

The Skill uses Codex's current model and does not require a second paid LLM API call.

## Install

\`\`\`text
Use $skill-installer to install lego-model from
https://github.com/zhulin025/lego-model-skill
\`\`\`

Or clone and link it manually:

\`\`\`bash
git clone https://github.com/zhulin025/lego-model-skill.git
mkdir -p "\${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/lego-model-skill/lego-model" \
  "\${CODEX_HOME:-$HOME/.codex}/skills/lego-model"
\`\`\`

For Codex Cloud or repository-scoped use, place or link \`lego-model/\` under
\`.agents/skills/lego-model\`. Reload Codex after installation.

## Use

\`\`\`text
Use $lego-model to create a movie-style Bumblebee brick model and open its
interactive 3D assembly webpage.
\`\`\`

\`\`\`text
Use $lego-model with this reference image. Preserve the silhouette and iconic
parts, then give me the running viewer URL and ZIP.
\`\`\`

\`\`\`text
Use $lego-model to improve this existing model.json and package a new viewer.
\`\`\`

## Validate

\`\`\`bash
python3 lego-model/scripts/brick_model.py check model.json --write-self-check
python3 lego-model/scripts/build_viewer.py model.json --output viewer --zip
python3 lego-model/scripts/serve_viewer.py viewer --port 0
\`\`\`

The runtime uses only Python's standard library.

## License

MIT
