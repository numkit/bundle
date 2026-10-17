# signal: bandpower(x, fs, freqrange) integrates the PSD wrong (~163× off)

**Kind:** bug
**Status:** ✅ FIXED (1267adf) 
**Guard:** BandpowerFsIntegration (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

The fs-form bandpower integrates a periodogram PSD whose normalization
does not match the reference: for a unit sine at 100 Hz (1 s, fs=1000)

- MATLAB R2025b: `bandpower(x, 1000, [10 200])` = **0.499999998264**
  (essentially all the signal power, matching `bandpower(x)` = 0.5)
- nk: **81.4685** — 163× larger, i.e. the `computePsd` →
  `integrate(Pxx, F, fLo, fHi)` path is missing the 1/N (or 1/(N·df))
  normalization somewhere.

Found by extending tools/parity/specs/bandpower.json with the fs form
during the 2026-09-18 structural portion (the arity/type tightening is
correct; the VALUES were always wrong — nothing regression-tested the
fs path before).

`bandpower(x)` (1-arg, Parseval path) and the complex 1-arg form are
exact.

## Repro

```matlab
clear;
x = sin(2*pi*100*(0:999)/1000);
r2 = bandpower(x, 1000, [10 200]);
% MATLAB: 0.499999998264; nk: 81.4685
```

## Fix sketch

Compare `computePsd`'s Pxx against the reference periodogram output
(periodogram.json parity passes, so the PSD itself may be fine — suspect
`integrate`'s df handling or an fs-scaling factor in spectral_metrics).
meanfreq / medfreq / obw / powerbw share `computePsd` — re-run their
parity specs after the fix.
