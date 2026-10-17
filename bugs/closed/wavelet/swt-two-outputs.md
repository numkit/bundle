# swt lacked the [SWA, SWD] = swt(x, n, wname) two-output form

- **Kind:** missing-output
- **Component:** wavelet (swt)
- **Found + Fixed:** 2026-09-18, bug-quartet portion (the canonical
  reference round-trip `[A,D] = swt(x,n,w); iswt(A,D,w)` was unwritable
  in nk — the reg ignored nargout and always returned the stacked SWC).

## Repro

```
clear;
[A, D] = swt(1:8, 2, 'haar');   % nk: "Too many output arguments"
```

## Fix

`swtAD(x, n, wname)` compute added (per-level approximation AND detail
matrices — n×N each, level 1 = finest row); the reg returns the pair
under nargout ≥ 2, the stacked matrix otherwise. Values cross-checked
against probe61 Q20/Q21/Q22 (SWA level-2 row `[5 7 9 11 13 11 9 7]`
etc.). iswt gained the matching `iswt(SWA, SWD, wname)` input form
(reference iswt.m dispatch; result class follows SWA).

**Guard:** round-trip + `[A,D]` cases in
`src/toolboxes/wavelet/tests/swt_modwt_test.cpp`.
