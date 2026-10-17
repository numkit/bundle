# signal: bandpower one-sided-PSD forms not implemented

**Kind:** stub
**Status:** ✅ FIXED (2026-10-17)
**Guard:** BandpowerPsdForm (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

The reference's power-spectrum forms — `bandpower(pxx, f, 'psd')` and
`bandpower(pxx, f, freqrange, 'psd')` — integrate a GIVEN one-sided
PSD instead of computing one from a time signal (probed: 'psd' is the
only supported 4th-input option). nk's reg rejects every 4-argument
bandpower call with `nk:bandpower:psdUnsupported` (non-'psd' strings
with `nk:bandpower:badOption`).

While tightening this, the fs/freqrange coupling was corrected to the
reference contract: `bandpower(x, fs)` WITHOUT freqrange is not a legal
reference call (probe: FreqRangeMissing) and nk now rejects it with
`nk:bandpower:freqRangeRequired`; freqrange must be exactly 2 elements
(`nk:bandpower:freqRange`).

## Repro

```matlab
clear;
[p, f] = periodogram(cos(0:0.1:2*pi), [], [], 100);
bp = bandpower(p, f, 'psd');
% MATLAB: 0.5013320412; nk: nk:bandpower:psdUnsupported
```

## Fix sketch

Detect the 'psd' flag in bandpower_reg, take (pxx, f) as the grid and
integrate `trapez(pxx .* (2 except DC/Nyquist), f)` over the (optional)
freqrange — the existing `integrate` helper in spectral_metrics.cpp
already does the trapezoid; only the halved end bins and the pxx-based
normalisation are new.
