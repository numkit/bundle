# signal.findpeaks — 'WidthReference' option unsupported

- **Status:** ✅ FIXED (2026-09-17 — both references, full rule reverse-engineered)
- **Severity:** P2 (missing option)
- **Kind:** stub
- **Found:** 2026-06 via signal.* DEEP-PROBE sweep (previously known gap)

## Symptom
`findpeaks(..., 'WidthReference', 'halfheight'|'halfprom')` throws. nk
always measures the width `w` at the half-prominence reference; the
`'halfheight'` reference (and explicit `'halfprom'`) are rejected.

## Repro
```matlab
clear;
findpeaks([1 3 2 5 1 6 1], 'WidthReference', 'halfheight')
% nk (fixed): peaks; widths [1.75 1.45833 1.2]
% MATLAB R2025b: same (probed 2026-09-17)
```

## Fix

`'halfprom'` (default) keeps the existing machinery; `'halfheight'`
added (`PeakOpts::widthRef`, `peakWidth` branch, reg parser accepting
exactly `'halfprom'`/`'halfheight'`, bad value →
`nk:findpeaks:badWidthReference`).

## The halfheight rule (R2025b, probed 2026-09-17 — 3 batteries, ~50 signals)

Two earlier sessions (2026-06-03, 2026-06-05) were blocked on the
pedestal widths {6,5,6,4,4} fitting no closed form. The rule that fits
ALL probes:

Each side independently, walking OUTWARD from the peak through
NON-INCREASING samples (stop at the first strict rise or the array end):

1. **Crossing:** the first sample `x[k] <= h/2` interpolates on the
   segment `[k, inner-neighbor]` — a sample exactly EQUAL to ref lands
   exactly on that sample (f = 0), and a touch BEFORE a deeper dip wins
   over the dip (`[5 5 5 6 10 6 5 5 4]` → 4, not 5.5).
2. **No crossing** (reference below the whole descent — the pedestal):
   the bound is the LEFTMOST index of the first floor plateau: on the
   right the first flat sample, on the LEFT the FAR end of the flat.
   This asymmetry is what the old sessions could not fit — it is
   leftmost-in-index-order on both sides, not a per-side edge rule.
   `[5 5 5 6 9 6 5 5 5]` → bounds (1,7) → 6, not the naive span 8.

Notable discriminators that pinned it:
- `[5 6 5 5 5 6 9 6 5]` → w(9)=6: left bound 3 (far end of flat
  [3..5], NOT the interval-min first occurrence 1).
- `[5 5 5 6 9 6 5 7 4.7]` → w(9)=6: the deeper 4.7 beyond the rise is
  ignored; bound stays at the first flat sample 7.
- `[1 3 2 5 1 6 1]` peak 3 → 1.75: right bound 3 — the walk stops at
  the rise to 5 BEFORE the later 1 (a crossing below ref beyond a rise
  is NOT used).
- `[7.5 8 9 8.5 8.6 2]`: halfprom w=2.803 (crossing searched across the
  FULL prominence interval — a rise does NOT stop it there), while
  halfheight w=3 (walk stops at the rise, plateau bound). The two
  references genuinely use different search scopes.
- X/Fs forms measure in location units (bounds map through the
  location array): `[5 5 5 6 9 6 5]` with X=0:0.5:3 → 3.

## References

- **Guard:** `FindpeaksHalfHeightWidth` (enabled; known_bugs_test.cpp) +
  10 dual-engine TEST_P suites in
  `src/toolboxes/signal/tests/findpeaks_width_test.cpp` — every expected
  value reference-validated.
- Parity: tools/parity/specs/findpeaks.json (WidthReference branches
  fingerprinted; correctness=OK 2026-09-17).
- Follow-up stub (unpicked): bugs/opened/signal/findpeaks-width-options.md
  (MinPeakWidth / MaxPeakWidth / Annotate / DoubleSided).
