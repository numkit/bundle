# iswt on integer-class input diverges from the reference's integer wavelet arithmetic

- **Kind:** bug
- **Component:** wavelet (iswt)
- **Found:** 2026-09-19, wavelet argcheck portion (probe41/probe52 batteries)
- **Fixed:** 2026-09-18, bug-quartet portion

## Repro

```
clear;
swq = uint8([repmat([100 50 200 25],1,16); repmat([10 20 30 40],1,16); repmat([60 70 80 90],1,16)]);
y = iswt(swq, 'haar');
y(1:4)
```

- MATLAB R2025b (probe52): `[64 14 91 0]` (repeating every 4)
- nk (before): `[0 0 0 0]`

## Root cause (reference source: iswt.m)

The reference's inverse is PHASE-DECOMPOSED: at each level k (coarsest
first) each of the `2^(k-1)` stride phases reconstructs via two
'per'-mode sub-reconstructions (even/odd positions), averaged with
`a(ind) = 0.5*(x1+x2)` — an ARRAY ASSIGNMENT whose target carries the
input's class. For integer classes that store rounds half-away-from-zero
and saturates PER PHASE — true integer wavelet arithmetic. nk's kernel
(a single transpose-operator pass in double + one final saturating cast)
matches level 1 but diverges from level 2 on.

## Fix

iswt rewritten as an exact port of the phase algorithm (dyadup(x,0,1) →
'per' extend by lf/2 → conv → wkeep from lf → even/odd average →
class-carrying store via storeElem, which now rounds half-away-from-zero
before the saturating cast). Also added while porting:
- `iswt(SWA, SWD, wname)` two-matrix form (result class follows SWA;
  only SWA's last row participates — probed Q31–Q42 crafted cases);
- `[SWA, SWD] = swt(x, n, wname)` two-output form.

Verified: crafted uint8/int8/uint16 level-1 and level-2 cases
([17 11 18 25], [0 5 5 6], [69 65 70 75], [37 35 22 0]) + the filed
repro [64 14 91 0] all bit-match; double/single round-trips exact.

**Guard:** `IswtUint8HaarValues` in
`src/toolboxes/wavelet/tests/known_bugs_test.cpp` (live).
