# signal: integer-class inputs need integer-class outputs the Value layer cannot allocate

**Kind:** stub
**Status:** ⬜ OPEN (2026-09-18)
**Guard:** DISABLED_ConvmtxIntResultClass, DISABLED_DownsampleIntResultClass (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

The reference (probed R2025b) ACCEPTS integer-class inputs for the
gather/permutation entries and returns **integer-class results**:

- `convmtx(int8([1 1]), 3)` → 3×4 **int8** matrix
- `downsample(int8(1:8), 2)` → 1×4 **int8** row
- `upsample(int8(1:3), 2)` → 1×6 **int8** row
- `bitrevorder(int8(1:8))` → **int8** permutation

nk's `Value` exposes mutators for double / complex / single / logical
storage only (`doubleDataMut`, `complexDataMut`, `singleDataMut`,
`logicalDataMut`) — there is no public element-write path into an
INT8/UINT8/… matrix, so these entries reject integer classes with a
dedicated `nk:<fn>:integerUnsupported` identifier instead of silently
returning a double-classed result.

NOTE: where the reference COERCES integers to double (conv, conv2,
convn, filter2, xcorr2 — result double, probed), nk implements the
coercion and is NOT on this list. Where the reference REJECTS integers
(polyscale, medfilt1, bandpower, czt, goertzel, stft, modulate, demod,
sosfilt, decimate, resample), nk rejects with `nk:<fn>:inputType` and is
also not on this list.

## Repro

```matlab
clear;
y = convmtx(int8([1 1]), 3);
% MATLAB: int8 matrix; nk: nk:convmtx:integerUnsupported
```

## Fix sketch

Either add a typed element setter for integer matrices to the Value
layer, or a `Value::fromDoubles(dims, type, span)` factory; the four
call sites above are then trivial gather rewrites mirroring the
single/logical branches already shipped.
