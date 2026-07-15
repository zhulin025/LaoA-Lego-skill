# Structured Humanoid and Character Modeling

Use this guide for complete characters, humanoids, robots, and creatures with readable limbs. Default to `primitives-v1`.

## Structural priority

Review the model in this order:

1. overall silhouette and body proportions;
2. head, torso, pelvis, and limb mass hierarchy;
3. shoulders, elbows, wrists, hips, knees, and ankles;
4. hands, feet, hair, clothing, armor, and signature accessories;
5. face and thin color details.

Do not trade stages 1-4 for a denser surface or a more detailed face. A model with fewer bricks and clear anatomy reads better than a smooth shell with collapsed joints.

## Hand construction gate

Never use one sphere, ellipsoid, capsule, or cylinder as a complete hand, fist, paw, or gripper.

For each visible hand, use side-prefixed semantic parts:

- `left_palm` or `left_fist_core`: block, frustum, or short beveled stack;
- `left_thumb`: a distinct angled block, capsule, cone, or frustum attached to the side/front;
- `left_finger_block_*` or `left_knuckle_*`: at least two visible groups that establish finger direction;
- `left_wrist`: a smaller connector that separates the hand from the forearm.

Mirror the naming for the right side. A clenched fist normally needs 4-7 primitives. An open hand normally needs 5-8. A mechanical gripper may use palm, thumb/jaw, opposing jaw, hinge, and wrist parts.

Make the thumb asymmetry visible in the silhouette. Offset the knuckle line and taper the wrist so the hand cannot be mistaken for a ball.

## Feet and shoes

Build each foot from at least a sole, upper/toe mass, and ankle transition. Add canonical straps, toe caps, heels, armor plates, or color bands as separate parts. Keep the sole wider and flatter than the lower leg. Do not end a leg in an ellipsoid or capsule without a readable sole.

## Limbs and joints

- Split upper arm and forearm at the elbow; split thigh and shin at the knee.
- Use overlap or a small joint primitive rather than one continuous capsule from shoulder to hand.
- Let adjacent structural parts intersect slightly so voxelization connects them.
- Use rotated boxes and frustums for cloth folds, boots, bracers, armor, and stylized anatomy.
- Reserve ellipsoids for craniums, helmets, rounded shells, and local muscles—not complete extremities.

## Face and costume details

Use thin boxes, small cylinders, short capsules, or shallow frustums as late add operations for eyes, brows, scars, lapels, belts, emblems, and trims. Keep the depth around 2-4% of the longest model dimension so details survive sampling without floating.

If a mark is too small for `primitives-v1`, preserve structural anatomy and disclose the mark as a limitation. Do not convert the entire character into an explicit surface shell for one thin line.

## Visual acceptance

Inspect front, three-quarter, and side views plus close views of both hands and feet. Reject the model when any of these are true:

- a hand or foot reads as a featureless round mass;
- fingers, thumb, sole, or wrist/ankle transition disappear at normal viewing distance;
- limbs merge into the torso or each other;
- the concept shows articulated construction but the model replaces it with a smooth organic shell;
- surface detail is high while the silhouette, joints, or pose remain wrong.
