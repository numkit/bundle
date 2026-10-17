# signal: N-D and multi-channel branches not implemented

**Kind:** stub
**Status:** ⬜ OPEN (2026-09-18)
**Guard:** DISABLED_ConvnRank4, DISABLED_StftMatrixChannels (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

Reference-accepted (probed R2025b) input forms the nk kernels cannot
compute yet; each is rejected with a dedicated identifier instead of
silently computing over the flattened buffer (which produced WRONG
shapes/values before this was tightened):

- `convn` with rank > 3 — the reference supports arbitrary-rank
  convolution (probed: convn(ones(2,2,2,2), ones(2)) → 3×3×2×2); nk
  caps at 3-D with `nk:convn:nd`.
- `czt` with 3-D input — the reference accepts it (probed OK); nk
  rejects with `nk:czt:unsupportedNd`.
- `stft` with a matrix input — the reference treats each column as an
  independent channel (output is N×K×frames); nk rejects with
  `nk:stft:matrixUnsupported`. Before this portion nk framed the FLAT
  buffer — silently wrong shape for every matrix input.
- `downsample` / `upsample` with N-D (ndim > 2) input — the reference
  accepts (probed); nk rejects with `nk:<fn>:ndUnsupported`. (Matrix
  input IS implemented column-wise as of this portion.)

## Repro

```matlab
clear;
y = stft(ones(64, 2));
% MATLAB: 65×2×1 complex (two channels); nk: nk:stft:matrixUnsupported
```

## Fix sketch

stft channels: loop the existing framing per column, stack along dim 3
(mirrors the sosfilt per-column wrapper). downsample/upsample N-D:
page-loop the shipped column gather. convn rank>3: extend the nested
loop depth or factor into consecutive 1-D passes.
