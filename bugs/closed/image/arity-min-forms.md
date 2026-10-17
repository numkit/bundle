# image.arity-min-forms — reference short/0-arg forms rejected by the applied bounds

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (documented reference forms currently rejected with
  `nk:<fn>:nargin` / `nk:<fn>:maxnargin`)
- **Kind:** stub
- **Found:** 2026-09-17, image-domain max-arity migration
  (bugs/opened/lang/reg-max-arity.md): a dedicated 0-arg probe (k=0) plus
  valid-argument probes found forms the []-arity probe cannot see.

## Symptom

The reference engine accepts these forms; after the arity migration nk
rejects them at the first statement. The old nk regs rejected them too
(hand min-throws), so this is a **pre-existing implementation gap made
explicit**, not a regression: the bounds keep the crash-proof minimum
until the short form is actually implemented.

## Gaps (verified against R2025b, 2026-09-17)

| fn | reference form | nk today |
|---|---|---|
| gray, hot, cool, spring, summer, autumn, winter, copper, pink, hsv*, flag, prism, lines, bone, white | `gray()` etc. → default n (colormap fns accept 0 args) | requires 1 |
| checkerboard | `checkerboard()` → 8×8 default | requires 1 |
| phantom | `phantom()` → shepp-logan default | requires 1 |
| strel | `strel()` → default square strel | requires 1 |
| gabor | `gabor()` → default gabor object (0-arg form) | stub throws NotImpl regardless |
| whitepoint | `whitepoint()` → default D65? | requires 1 |
| imnoise | `imnoise(I)` → default gaussian noise | requires (I, type) |
| bwselect | 1–2-arg interactive figure forms | requires ≥3 (non-interactive) |
| roipoly | 1–2-arg interactive figure forms | requires ≥3 (non-interactive) |
| imcrop | `imcrop(I)` interactive crop UI | requires ≥2 (rect form) |

\* `hsv()` IS implemented in nk (hsv_cmap_reg defaults n=256, bound 0..1).

The three interactive forms (bwselect/roipoly/imcrop) need figure
infrastructure — track with the graphics work, not the argcheck campaign.

## Fix direction

Implement the defaults (n=64-ish colormap default, 8×8 checkerboard,
shepp-logan phantom, square strel, etc.) and lower the applied min in the
same commit; each function then gets its branch test per full_fidelity.md.

## References

- **Guard:** `ImageShortForms` (modules/image/tests/known_bugs_test.cpp)
- Applied bounds: `tools/arity_reference.json` ("image"), reg comments in
  `modules/image/src/register/**`.
- Probe evidence: 0-arg pass `image_arity_k0.tsv`, interactive probes
  `image_arity_interactive.tsv` (R2025b, 2026-09-17).

