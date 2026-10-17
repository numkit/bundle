# spectral* time-domain form treats a matrix/row signal as one flat channel; the reference treats columns as channels

- **Kind:** bug
- **Component:** audio (shared computeStft behind the spectral* family)
- **Found:** 2026-09-19, audio argcheck portion (probe45 battery; shape probe round 8)
- **Fixed:** 2026-09-18, bug-quartet portion

## Repro

```
clear;
xv = cos(2*pi*(0:159)/40);            % 1x160 ROW
y = spectralFlux(xv, 1600);           % row input, time form
```

- MATLAB R2025b: error (`signal:utilities:utilities:insufficientSignalLength`)
  — a 1x160 signal is 160 channels of 1 sample.
- nk (before): OK, `[0; 0.121637; 0.02691; 0.0780958]` — the kernel
  flattened `numel(x)` into ONE channel.

## Root cause (reference sources: signal.internal.spectraldescriptors
## preprocess/stft/buffer)

`[xLen, numChannels] = size(x)` — the time form frames EACH COLUMN as a
channel (buffer is channel-major; metrics reshape to F×C); xLen < 2
rejects (so row inputs are 1-sample channels); 3-D rejects ('2d').

## Fix

computeStft reframed per-channel (one metric column per channel,
F×C outputs); the whole spectral* family inherits via the shared
prepareInput/perFrameChannel path. Also hardened per the reference's
shared contract: x single/double real 2-D nonempty finite; f nonempty
real nonnegative finite for both forms; freq form ≤ 3-D with L×M×C
channel semantics.

Verified: `spectralFlux([xc xc·0.5+0.25], 1600)` → 4×2 with per-channel
columns bit-matching probe P51; row input / 3-D input / short-channel
rejections match; `spectralCentroid([xc xc], 1600)` → 4×2.

**Guard:** `SpectralFluxRowTimeFormRejects` in
`src/toolboxes/audio/tests/known_bugs_test.cpp` (live).
