# Concept-Image-First Modeling

Use this workflow for every keyword-only request and for any supplied reference that is not already a clear brick-built 3D render.

## 1. Lock the canonical subject

Before generating an image, write down:

- exact subject and named version, era, form, or trim;
- intended pose and viewing direction;
- front, side, and overall proportions;
- canonical palette and color-block locations;
- at least 8 unmistakable landmarks;
- forbidden substitutions, transformations, accessories, and redesigns.

For a known character or vehicle, research authoritative front, side, and three-quarter references when available. The concept may translate the subject into bricks, but it must not redesign the identity.

## 2. Generate one canonical concept image

Use the built-in image generation tool in `stylized-concept` mode. Default to one full-subject three-quarter view because it exposes front, side, silhouette, depth, and pose in a single image. Generate a second rear or opposite-side view only when a critical landmark is otherwise hidden.

Use this prompt scaffold, replacing bracketed fields with the brief:

```text
Use case: stylized-concept
Asset type: canonical 3D brick-modeling reference
Primary request: Create a highly recognizable brick-built 3D sculpture of [exact subject and version].
Scene/backdrop: clean neutral light-gray studio, unobtrusive ground plane, no environment or props.
Subject: full body/object fully inside frame, centered, three-quarter front view, facing slightly toward camera.
Identity locks: [8-12 concrete silhouette, proportion, palette, costume/bodywork, face/front-fascia, and accessory landmarks].
Construction: visibly assembled from interlocking toy bricks, plates, slopes, wedges, cylinders, and studs; readable brick scale; plausible connected construction; layered depth at the face/front and signature details.
Composition/framing: long-lens or orthographic-like product view with low perspective distortion; all extremities visible; critical landmarks unobstructed.
Lighting/mood: soft studio lighting that separates every major plane and color block.
Constraints: preserve the named version, canonical proportions, pose, and color placement; use only accessories explicitly listed.
Avoid: smooth plastic character render, generic minifigure, action figure, costume, voxel cube style, chibi redesign unless canonical, invented armor or weapons, transformed variants not requested, cropped extremities, duplicate limbs, text, captions, logos, watermark, busy background.
```

For a user-supplied non-brick image, label it as the identity reference and add: `Preserve the reference's identity, silhouette, pose, proportions, color blocking, and signature details; change only the construction into visible interlocking bricks.`

Save the selected project-bound image as `<output>/reference/concept.png` and the exact final prompt as `<output>/reference/concept-prompt.md`. Do not leave the only copy under the image tool's default output directory.

## 3. Accept or repair the concept

Accept only when all of these are true:

1. The named version or form is correct.
2. The complete silhouette is visible and not cropped.
3. At least 80% of listed landmarks are clearly present, including every critical silhouette landmark.
4. Canonical color blocks are in the correct regions.
5. The subject is visibly brick-built rather than a smooth toy or generic minifigure.
6. The pose exposes the parts needed for modeling without severe self-occlusion.
7. Anatomy or mechanical structure is coherent with no duplicate or missing major parts.
8. No unrequested accessory, transformation, text, logo, or environment has been invented.

If one or two checks fail, make one targeted image edit that changes only those defects and preserves the accepted identity features. If the second image still fails a critical identity check, disclose the mismatch instead of treating it as ground truth.

## 4. Convert the concept into a modeling map

In the brief, record:

- normalized subject bounds and head/body or cabin/body ratio;
- centers and spans of every landmark;
- at least 10 semantic part groups;
- sampled palette colors and their approximate volume share;
- visible connections, overlaps, gaps, openings, and depth order;
- assumptions for occluded rear or underside geometry;
- the chosen representation and why it fits this concept.

Map each landmark to concrete primitive `part` names or explicit-brick coordinate regions before adding generic detail.

## 5. Compare the built model back to the concept

Capture an assembled viewer screenshot at a matching three-quarter camera angle. Compare in this order:

1. black silhouette and overall proportions;
2. pose and landmark centers;
3. large canonical color blocks;
4. depth layering, openings, and overlaps;
5. face/front-fascia and small signature details.

Count a landmark as matched only when its shape, position, scale, and color role agree with the concept. Require at least 80% total landmark agreement and 100% agreement for critical silhouette landmarks. Spend repair passes on the largest identity mismatch first; extra bricks cannot compensate for a wrong silhouette.
