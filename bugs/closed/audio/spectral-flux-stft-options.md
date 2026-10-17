# spectralFlux Window / OverlapLength / FFTLength / Range name-value options are documented but refused

- **Kind:** stub
- **Component:** audio (spectralFlux)
- **Found:** 2026-09-19, audio argcheck portion (R2025b help dump + probe48)
- **Fixed:** 2026-09-18, bug-quartet portion

## Repro

```
clear;
xc = cos(2*pi*(0:159)/40); xc = xc(:);
y = spectralFlux(xc, 1600, 'FFTLength', 128);
```

- MATLAB R2025b: computes (the option re-shapes the internal STFT).
- nk (before): `nk:spectralFlux:optionUnsupported`.

## Implemented surface (exact port of the reference's
signal.internal.spectraldescriptors preprocess/stft)

- `Window` — real finite single/double COLUMN of length 3..xLen
  (defaults: rectwin geometry, see below).
- `OverlapLength` — single/double scalar integer ≥ 0, < window length.
- `FFTLength` — scalar integer ≥ 2, ≥ window length
  (`FFTLengthLessThanWindowLength` below that).
- `Range` — 1×2 increasing nonneg row ≤ fs/2; spectrum bins
  `ceil(R(1)·nfft/fs+1) .. floor(R(2)·nfft/fs+1)`.
- Default window geometry CORRECTED from the reference source (the
  earlier probed rule matched the fs grid but not the mechanism):
  `round(0.03·fs) > 120` → rectwin(round(0.03·fs)) (must fit the
  signal); else with no OverlapLength → rectwin(min(64, xLen)); WITH an
  OverlapLength → rectwin(fix((xLen + 7·ovl)/8)) — the "8 segments"
  geometry. Default overlap: `round(0.02·fs) > 80` → that, else half
  the window. Power |Y|²/(0.5·sum(win)²), magnitude |Y|/(0.5·sum(win)),
  DC/Nyquist halving on the selected bins.
- SpectrumType now validatestring (unambiguous prefixes: 'mag' works).
- previousSpectrum / second output are time-form syntax errors
  (InvalidFluxSyntax / nargoutchk — probed from the reference source).

Verified bit-matched: FFTLength=128 → [0 0.12891 0.02852 0.082768];
OverlapLength=10 → 8 frames [0 0.065114 …]; Window=hann(64); Range
[100 700]; the combined case; error classes for FFTLength<window,
reversed Range, window > signal, non-integer overlap.

**Guard:** live cases in `AudioTypeContract.SpectralFluxSignatureAndState`
(src/toolboxes/audio/tests/type_contract_test.cpp).

Residual (filed separately): the OTHER spectral* descriptors share this
computeStft surface but their regs do not expose the options yet —
bugs/opened/audio/spectral-family-stft-options.md.
