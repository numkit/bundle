# signal: decimate default filter is FIR, the reference uses an order-8 Chebyshev I

**Kind:** bug
**Status:** ✅ FIXED (1267adf) 
**Guard:** DecimateChebyDefault (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

The reference's `decimate(x, q)` default designs an **order-8 Chebyshev
type I** lowpass (rp = 0.05 dB) with filtfilt; nk designs a **Hamming
windowed-sinc FIR** of order 8·q. Both suppress aliasing but produce
DIFFERENT transient and passband values — every decimate(x, q) call
without an explicit filter diverges from the reference numerically.

Also note the reference rejects short signals for the default order
(probed: decimate(1:12, 3) → "Data length must be greater than 24…");
nk computes anyway.

## Repro

```matlab
clear;
d = decimate(1:100, 5);
% MATLAB R2025b: d(1)=4.902857522  d(2)=9.917302047
%                d(10)=49.41857222 d(20)=98.66579112
% nk: different values (FIR pipeline)
```

## Fix sketch

Design cheby1(8, 0.05, 1/q) + bilinear-free digital direct form (the
toolbox ships cheby1) and filtfilt it; keep the FIR path behind the
explicit `fir` filter-form branch. Add tools/parity/specs/decimate.json
after the fix.
