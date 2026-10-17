# medfilt1([]) errored on the TreeWalker backend (empty-typed [] split)

- **Kind:** bug
- **Component:** signal (shared requireFloatInput gate), TreeWalker
- **Found:** 2026-09-18, engine-gap portion regression sweep
  (DspGapsTest.Medfilt1PreservesShape/TW failing; verified pre-existing
  on a clean tree — introduced by the signal argcheck portion).
- **Fixed:** 2026-09-18, same portion.

## Repro

```
clear;
y = medfilt1([]);
```

- MATLAB R2025b: `[]` (empty out).
- nk TreeWalker: `medfilt1: input 1 (x) must be a double or complex
  double array (got a 0x0 empty array)`.
- nk VM: works.

## Root cause

The backends materialize the `[]` literal differently — the VM as a
0×0 DOUBLE, the TreeWalker as an EMPTY-typed Value — and the shared
`requireFloatInput` class gate accepted DOUBLE but not EMPTY, so the
same call accepted on one backend and rejected on the other. The
kernel's own empty path (`if (total == 0) return r;`) was never reached
on TW.

## Fix

`requireFloatInput` accepts EMPTY (behaves as 0×0 double downstream,
the same rule the wavelet type_gates follow).

**Guard:** `DspGapsTest.Medfilt1PreservesShape` (live, dual-backend).
