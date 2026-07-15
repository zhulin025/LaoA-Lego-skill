# BrickMorph Model Schema

## Root object

```json
{
  "version": "1.0",
  "name": "short display name",
  "description": "one-sentence visual description",
  "subjectClass": "humanoid_robot",
  "landmarks": ["at least 6 unmistakable features"],
  "qualitySelfCheck": {
    "primitiveCount": 0,
    "geometryTypeCount": 0,
    "boxRatio": 0,
    "rotatedCount": 0,
    "subtractCount": 0,
    "materialCount": 0,
    "topThreeVolumeRatio": 0,
    "dominantMaterialRatio": 0,
    "landmarkCount": 0,
    "namedPartRatio": 0,
    "uniquePartCount": 0,
    "passed": false
  },
  "palette": ["#RRGGBB"],
  "primitives": [],
  "requestedBrickCount": 16000,
  "keyword": "user subject",
  "generatedAt": "ISO-8601 timestamp",
  "generatorVersion": "codex-skill-v1"
}
```

Use 1-12 palette colors. `material` is a zero-based palette index. Use one of these `subjectClass` values: `humanoid_robot`, `vehicle`, `creature`, `building`, `object`.

Coordinates use `x` left/right, `y` down/up, and `z` back/front. Face the model toward `+z`, keep it centered, and keep a standing subject upright. A humanoid commonly fits a height of 70-100 units; a vehicle commonly fits a longest dimension of 70-110 units.

Every primitive requires:

- `type`: one supported type below.
- `op`: `add` or `subtract`.
- `material`: valid palette index. It is ignored visually for subtract operations but remains required.
- `part`: concise semantic name such as `head_crest`, `left_shoulder_armor`, or `chest_window`.

## Primitive forms

```json
{"type":"box","op":"add","center":[0,0,0],"size":[10,8,6],"rotation":[0,0,0],"material":0,"part":"torso_core"}
{"type":"ellipsoid","op":"add","center":[0,0,0],"size":[10,8,6],"rotation":[0,0,0],"material":0,"part":"helmet"}
{"type":"cylinder","op":"add","center":[0,0,0],"radius":4,"height":10,"axis":"y","rotation":[0,0,0],"material":0,"part":"joint"}
{"type":"cone","op":"add","center":[0,0,0],"radiusTop":2,"radiusBottom":5,"height":10,"axis":"y","rotation":[0,0,0],"material":0,"part":"calf_armor"}
{"type":"capsule","op":"add","start":[0,0,0],"end":[0,10,0],"radius":3,"material":0,"part":"upper_arm"}
{"type":"torus","op":"add","center":[0,0,0],"majorRadius":6,"minorRadius":2,"axis":"z","rotation":[0,0,0],"material":0,"part":"wheel"}
{"type":"frustum","op":"add","center":[0,0,0],"bottomSize":[12,8],"topSize":[8,5],"height":10,"rotation":[0,0,0],"material":0,"part":"chest_armor"}
```

`axis` must be `x`, `y`, or `z`. Sizes, radii, and heights must be positive. `cone.radiusTop` and each `frustum.topSize` component may be zero. For a torus, `minorRadius < majorRadius`. Rotation values are Euler degrees. Capsule orientation is defined by `start` and `end` and has no `rotation` field.

## Boolean and color order

The array order is the modeling order. Later operations affect earlier geometry:

1. Add the structural mass.
2. Subtract cavities, wheel arches, visor slits, intakes, joint gaps, or panel lines.
3. Add thin windows, eyes, lamps, emblems, trim, armor overlays, and other color details.

Do not add a large body primitive after eyes, windows, or trim if it would cover them. A late color overlay must be thin on at least one axis but thick enough to survive voxelization; use roughly 2-4% of the model's longest dimension as a practical minimum.

## Compatibility limits

- `version` is `1.0`.
- Use 1-80 primitives; aim for 56-72 in detailed mode.
- Use `requestedBrickCount: 16000` for current BrickMorph top-detail compatibility.
- Do not emit expressions, `NaN`, comments, JavaScript, Markdown fences, or unrecognized fields in primitive definitions.
