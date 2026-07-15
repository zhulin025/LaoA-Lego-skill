# High-Recognition Brick Modeling Guide

## Recognition plan

Write a brief before JSON:

1. Name the canonical version or design era.
2. Estimate front, side, and overall proportions.
3. List at least 8 landmarks that distinguish this exact subject from its category.
4. Define the canonical palette and where each color appears by volume.
5. Divide the subject into 10 or more semantic part groups.
6. Allocate a primitive budget before detailing.

For humanoid robots, a useful 56-72 primitive allocation is: head 8-12, chest/back 12-18, both arms 12-18, waist/hips 4-8, both legs 14-20, and weapons or signature accessories 4-10. Adjust rather than mechanically applying this split.

## Shape strategy

- Start with 6-12 medium structural masses that establish the exact silhouette. Avoid one huge torso or hull primitive.
- Build each major region from 2-4 intersecting forms that create taper, armor overlap, depth, and directional planes.
- Prefer `frustum` for chest plates, shoulder armor, skirts, hoods, noses, and engine covers.
- Prefer `capsule` for angled limbs, struts, tails, and organic connectors.
- Prefer `ellipsoid` for helmets, canopies, creature bodies, and rounded shells.
- Prefer `torus` for wheels, ring thrusters, turbines, and circular framing.
- Use rotated `box` forms for mechanical armor, fins, wings, and panels; do not let axis-aligned boxes define the entire subject.
- Use `subtract` for openings that change identity: visor slit, grille, intake, wheel arch, cannon bore, joint gap, cockpit recess, or signature groove.

A proven rich mix at 64 primitives was 27 box, 17 cylinder, 9 frustum, 4 torus, 4 capsule, 2 cone, and 1 ellipsoid, with 35 oriented forms and 3 subtract operations. Treat this as a diversity reference, not a template to copy.

## Landmark fidelity

Map every landmark string to explicit `part` names. Examples:

- A Gundam-like subject needs a distinctive head crest, face/visor arrangement, chest vents, shoulder silhouette, forearm shape, waist skirts, backpack, knee armor, and feet—not merely a white humanoid robot.
- An automotive robot needs its actual front fascia or windows on the chest, correctly placed wheels, door wings or vehicle panels, characteristic face, layered mechanical limbs, and canonical color blocking—not merely a colored humanoid.
- A spacecraft needs the actual planform, cockpit position, engine layout, asymmetry, gaps, and surface color zones—not merely a flattened oval.

Review in this order: black silhouette and proportions; landmark placement; depth layering; canonical color blocks; small trim. If the subject is unrecognizable without the filename, revise the silhouette and landmarks before adding decoration.

## Numeric gate

The bundled checker requires:

- 48-80 primitives and at least 5 geometry types.
- Box count / all primitives <= 0.62. Aim for <= 0.55.
- Rotated forms >= `max(10, ceil(primitiveCount * 0.22))`.
- At least 2 subtract forms. Aim for at least 3 meaningful cuts.
- At least 4 materials used by add forms.
- Largest 3 add-form volumes / total add volume <= 0.58.
- Largest same-material add volume / total add volume <= 0.72.
- At least 6 landmarks; use 8-12 for stronger identity.
- At least 90% of primitives have `part`; aim for 100%.
- At least 10 unique semantic part groups.

Do not satisfy ratios by splitting identical overlapping boxes. Reduce oversized masses and replace them with meaningful tapered armor, joints, structural gaps, recesses, mechanical internals, and signature parts.

## Connectivity and symmetry

- Make adjacent structural parts intersect slightly so voxelization connects them.
- Connect eyes, weapons, wheels, wing roots, and trim to a supporting surface.
- Mirror left/right centers, dimensions, and opposite rotations for genuinely symmetric features.
- Preserve real asymmetry when it is iconic; do not mirror an asymmetric cockpit, weapon, antenna, or damaged region.
- Keep thin details at roughly 2-4% of the longest model dimension so they survive brick sampling.

## Repair order

When validation fails, fix the underlying form:

1. Oversized top-three volume: break major masses into tapered, overlapping structural regions and open real gaps.
2. High box ratio: replace appropriate boxes with frustums, capsules, cylinders, ellipsoids, or cones.
3. Low rotation: orient armor, limbs, panels, wings, and accessories according to the subject.
4. Low geometry diversity: choose types that match actual anatomy or industrial form.
5. Dominant material: expose joints, internals, windows, lights, trim, and secondary armor in canonical colors.
6. Weak semantic coverage: rename parts by function and implement missing landmarks; do not add empty metadata alone.
