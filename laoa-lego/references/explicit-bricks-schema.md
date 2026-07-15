# Explicit Bricks Schema

Use this format when individual brick coordinates and colors must survive loading without re-voxelization.

```json
{
  "version": "1.0",
  "format": "explicit-bricks-v1",
  "name": "display name",
  "description": "one sentence",
  "subjectClass": "humanoid_robot",
  "landmarks": ["at least 6 visible features"],
  "palette": ["#RRGGBB"],
  "bricks": [[0, 0, 0, 0], [1, 0, 0, 1]],
  "requestedBrickCount": 2,
  "keyword": "subject",
  "generatedAt": "ISO-8601 timestamp",
  "generatorVersion": "codex-direct-voxel-v1"
}
```

Each brick entry is `[x, y, z, material]`. Coordinates are finite numbers with absolute value at most 240. `material` is a zero-based palette index. Coordinates must be unique. Use 1-12 colors, 1-150,000 bricks, and make `requestedBrickCount` equal the exact `bricks` length.

Prefer a compact JSON serialization for large files. Preserve the common metadata fields so BrickMorph/lego-falcon can display names, descriptions, landmarks, palette swatches, history, and download filenames consistently.

