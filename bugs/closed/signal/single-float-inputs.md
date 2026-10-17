# signal: single-precision inputs are a capability gap across the toolbox

**Kind:** stub
**Status:** ✅ FIXED (2026-10-17) — single-precision inputs accepted across the signal toolbox, returning single-class outputs matching MATLAB R2025b.
**Guard:** ConvSingleResultClass (modules/signal/tests/known_bugs_test.cpp)

## Problem

The reference engine (R2025b, probed 2026-09-18 —
build/probe_signal_classes.m) ACCEPTS single-precision inputs across the
signal toolbox and returns **single-classed results** computed in single
precision. nk's signal kernels consume double / complex-double buffers
only, so every entry below rejects single with a dedicated
`nk:<fn>:singleUnsupported` identifier (with a `double()` hint) instead
of silently returning a double-classed result or crashing with a raw
buffer error.

Implementing this means either single-precision kernel variants (true
parity — results differ from double-compute-then-cast at the 1e-7 level)
or an accepted double-compute→float-cast approximation. The pure
gather/permutation entries (downsample, upsample, convmtx, bitrevorder)
already preserve single exactly — they are NOT on this list.

## Affected surface (identifier per entry)

- `conv`, `conv2`, `convn`, `filter2`, `xcorr2` — `nk:<fn>:singleUnsupported`
- `polyscale`, `polystab` — same id
- `sosfilt` (x and sos matrix), `sosfiltfilt` (x and sos matrix) — same id
- `zp2sos` (zeros/poles), `tf2sos` (b/a) — reference returns a
  single-classed SOS matrix
- `decimate`, `resample` — same id
- `medfilt1` — reference returns single
- `bandpower` — same id
- `stft` — reference returns single spectra
- `czt`, `goertzel` — reference returns single
- `modulate`, `demod` — same id
- `extractsigroi` — reference returns a cell of single vectors
- sigroi family (`sigroi2binmask`, `extendsigroi`, `shortensigroi`,
  `mergesigroi`, `removesigroi`) — single roi accepted by the reference

## Repro

```matlab
clear;
y = conv(single([1 2]), [1 1]);
% MATLAB: single [1 3 2]; nk: nk:conv:singleUnsupported
```

## Fix sketch

Shared `singleDataMut()` gather paths exist (see convmtx / bitrevorder /
downsample in this toolbox). For computed kernels the honest options are
(a) float kernel variants per family, or (b) double-compute + float cast
with a documented tolerance divergence — decide once for the whole
toolbox and apply uniformly.
