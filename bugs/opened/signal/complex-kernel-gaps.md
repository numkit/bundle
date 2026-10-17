# signal: complex-input branches the double kernels cannot compute yet

**Kind:** stub
**Status:** ⬜ OPEN (2026-09-18)
**Guard:** DISABLED_Xcorr2Complex, DISABLED_SosfiltComplexX, DISABLED_PolystabComplex (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

The reference (probed R2025b) ACCEPTS complex inputs for the entries
below and computes genuine complex results. nk's kernels are
double-buffer only there, so each entry rejects complex with a dedicated
`nk:<fn>:complexUnsupported` identifier instead of silently dropping the
imaginary part or crashing raw.

Complex branches that ARE implemented (not on this list): conv
(complex×complex bilinear path), downsample / upsample (complex gather),
bitrevorder (permutation), extractsigroi (slice copy), goertzel (complex
recurrence), stft (framing), czt (chirp-z), bandpower 1-arg (mean |x|²),
polyscale (complex scale factors).

## Affected surface

- `xcorr2` — complex 2-D correlation / cross-correlation
- `conv2`, `convn`, `filter2` — complex 2-D / N-D convolution
- `sosfilt` — complex x through the biquad cascade (reference returns
  complex; guard asserts the probed values)
- `decimate`, `resample` — complex FIR pipeline
- `bandpower` (fs form) — complex periodogram path (the 1-arg form is
  implemented)
- `tf2sos` — complex (paired-conjugate) b/a coefficients
- `polystab` — complex polynomial coefficients (blocked on the
  real-coefficient root finder)

## Repro

```matlab
clear;
sos = [1 1 1 1 0.5 0.25];
y = sosfilt(sos, (1:8)+1i);
% MATLAB: [1+1i 2.5+1.5i 4.5+2i 6.125+1.625i 7.8125+1.6875i 9.5625+1.75i
%         11.265625+1.703125i 12.9765625+1.7109375i]
% nk: nk:sosfilt:complexUnsupported
```

## Fix sketch

The biquad cascade recurrence is type-generic if `applyCascade` /
`sosfiltfiltColumn` are templated over the element type (real coeffs,
complex signal/state — same shape as the goertzel rewrite in
transforms/goertzel.cpp). conv2/convn/filter2 need a complex
`ops::conv2Direct` variant (or an fft2-based path). decimate/resample
need a complex `applyFirDf2t`.
