# spectral* family (non-flux) regs do not expose the shared Window/OverlapLength/FFTLength/Range options

- **Kind:** stub
- **Component:** audio (spectralCentroid / Spread / RolloffPoint /
  Decrease / Slope / Crest / Entropy / Flatness / Kurtosis / Skewness)
- **Found:** 2026-09-18, bug-quartet portion

## Repro

```
clear;
xc = cos(2*pi*(0:159)/40); xc = xc(:);
y = spectralCentroid(xc, 1600, 'Window', hann(64));
```

- MATLAB R2025b: computes — every descriptor shares the same
  signal.internal.spectraldescriptors preprocess surface as
  spectralFlux (same iGetWindow / iGetFFTLength / iGetRange rules).
- nk: the reg forwards only (x, f) — a trailing Name=Value pair is
  silently DROPPED (worse than refusing: the default geometry computes).

The shared computeStft port landed with the spectralFlux fix
(bugs/closed/audio/spectral-flux-stft-options.md); the compute side is
ready — what's missing is per-descriptor reg NV parsing + compute
signatures carrying StftOptions.

## Fix direction

Mechanical: extend each descriptor's compute signature with
`const StftOptions &opts = {}`, add the shared NV parse helper to each
reg, one parity spec per descriptor exercising Window/FFTLength/Range.

**Guard:** deferred (stub — options are ignored, not mis-computed;
flips live when the family wiring lands).
