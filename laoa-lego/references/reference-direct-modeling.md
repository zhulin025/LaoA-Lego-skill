# Reference-Direct Micro-Brick Modeling

Use this workflow only when the deliverable is primarily planar or coordinate-exact and the front-view arrangement of colors carries more identity than volumetric construction: pixel art, mosaics, text, logos, shallow reliefs, or intentionally flat display sculptures.

Do not use this mode for a complete three-dimensional humanoid merely because its face, scars, or costume contain thin lines. Surface-shell sampling tends to smooth hands, feet, joints, and facial depth into rounded masses. Build the character with structured primitives and express small marks as thin add primitives instead.

1. Measure the reference in normalized subject coordinates: silhouette bounds, head/body ratio, limb pose, and feature centers.
2. Author analytic occupancy for the shallow relief or display volume. Avoid treating hands, feet, or other articulated anatomy as generic ellipsoids; if articulated anatomy is essential, switch to `primitives-v1`.
3. Sample occupancy on a regular grid. Target at least 70-100 cells across the most detail-critical region, usually the face.
4. Retain exterior cells by checking the six axial neighbors. Use a filled volume only when the user explicitly needs internal construction.
5. Assign base material by body region, then paint the visible front surface with ordered masks:
   - broad face/belly regions;
   - mouth cavity and tongue;
   - eyes and eyebrows;
   - whiskers, seams, text, or other thin lines;
   - nose, highlights, and final foreground marks.
6. Represent curves as distance-to-segment chains or signed-distance masks. Do not approximate a curved closed eye with one thick box.
7. Export the final cells as `explicit-bricks-v1`; never pass them through primitive resampling again.
8. Render the assembled front view and compare silhouette, pose, feature centers, line thickness, and color boundaries against the reference. Adjust masks or sampling resolution before changing lighting or camera styling.

Keep the grid only as dense as needed. Doubling linear resolution can increase surface bricks by about four times and filled-volume work by about eight times. Prefer a surface shell plus instanced rendering for interactive viewers.
