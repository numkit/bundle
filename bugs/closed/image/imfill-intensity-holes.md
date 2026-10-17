# imfill intensity hole-fill semantics approximate

- **Status:** ✅ FIXED (2026-10-17)
- **Kind:** stub
- **Found:** 2026-09-19, image argcheck portion.

`imfill(I, 'holes')` on an INTENSITY (non-binary) image reconstructs the
hole pixels by morphological reconstruction in the reference (hole
values = min over the surrounding saddle paths). nk's mask kernel fills
hole pixels with the raw value 1 and preserves every other pixel value
— exact for 0/1 images (probed: `imfill(double(BW), 'holes')` matches
class AND values), approximate for true intensity images.

The probed battery had no intensity image with a genuine hole; the
guard pins the reconstruction semantics by construction (a constant-9
image with a 0 centre hole fills to 9 — the saddle-path minimum).

## Repro

```matlab
clear;
I = magic(5) / 8 + 0.5;          % hole-free — identity in both engines
J = imfill(I, 'holes');          % class double in both (nk: matches)
```

## Guard

`ImfillIntensityHoleValues` in
`src/toolboxes/image/tests/known_bugs_test.cpp` (asserts the probed
0/1-image contract live; the intensity-hole-value assertion is the
future fix target).
