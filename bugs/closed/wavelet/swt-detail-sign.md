# swt detail rows carried the OPPOSITE SIGN vs the reference (masked by abs() parity fingerprints)

- **Kind:** bug
- **Component:** wavelet (swt)
- **Found + Fixed:** 2026-09-18, bug-quartet portion (surfaced by the
  iswt integer port — iswt(swt(x)) stopped round-tripping when iswt
  moved to the reference's filter convention)

## Repro

```
clear;
w = swt(1:8, 1, 'haar');
w(1, 1:2)          % detail row
```

- MATLAB R2025b: `[-0.70711 -0.70711]`
- nk (before): `[+0.70711 +0.70711]` — the whole detail row negated
  (last entry −4.94975 where the reference has +4.94975).

The approximation row matched (Lo_R is palindromic for haar, hiding the
convention there); the divergence was DOCUMENTED in swt.json's comment
and papered over with `abs(...)` fingerprints — a masked silent-wrong
for every consumer of swt detail rows.

## Root cause (reference source: swt.m)

The reference CONVOLVES the per-extended signal with the analysis
filters (upsampled between taps per level) and keeps the central N
samples from offset lf — a circular CONVOLUTION. nk computed a forward
CORRELATION (`y[i] = Σ h[j]·x[(i+j·step) mod N]`), which mirrors every
non-palindromic filter.

## Fix

swtAD/swt rewritten as a verbatim swt.m port (per-extend by lf/2 → conv
→ wkeep from 0-based lf → filters dyadup'd between taps per level).
Detail rows now sign-exact; round-trips through the new phase-based
iswt are exact (haar/db2, levels 1–3). swt.json fingerprints made
sign-aware.

**Guard:** round-trip + value cases in
`src/toolboxes/wavelet/tests/swt_modwt_test.cpp` (live, was passing
only via the mirrored-convention pair) and the parity spec.
