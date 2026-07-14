# Reference-Direct Micro-Brick Modeling

Use this workflow when the front-view arrangement of colors carries more identity than the volumetric primitive decomposition.

1. Measure the reference in normalized subject coordinates: silhouette bounds, head/body ratio, limb pose, and feature centers.
2. Author analytic 3D occupancy for the major masses: ellipsoids for head/body/hands/feet, capsules for limbs, and small dedicated masses for accessories.
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
