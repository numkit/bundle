# Image complex kernels — reference computes, nk stubs

- **Kind:** stub
- **Found:** 2026-09-19, image argcheck portion (probe12/13 batteries vs
  MATLAB R2025b).

The reference's image toolbox COMPUTES complex results for a small set
of entries; nk's kernels are real-double, so those inputs are refused
with `nk:<fn>:complexUnsupported` (honest refusal beats silently
dropping imaginary parts through `elemAsDouble`).

| Entry | Complex argument | Reference result (probed) |
|---|---|---|
| `imfilter(I, h)` | I or kernel h | complex convolution, e.g. `imfilter(magic(5)/8+1i, ones(3)/9)` → `1.18056+0.444444i` at (1,1) |
| `roifilt2(h, I, BW)` | I | same kernel as imfilter |
| `imnoise(I, mode)` | I | pass-through for deterministic modes (`'salt & pepper'` density 0 → identity) |
| `imapplymatrix(M, X)` | M or X | complex linear combination, `imapplymatrix([0.3 0.6 0.1]+1i, RGB)` → `3.2 4.6 …` |
| `fsamp2(Hd)` | Hd | complex filter design |
| `fwind1(Hd, win)` | Hd or win | complex filter |
| `fwind2(Hd, win)` | Hd or win | complex filter |
| `axes2pix(n, extent, coord)` | extent | complex result (`axes2pix(5, [0 1]+1i, 0.5)` → `3-4i`) |

Everything else in the probed set (87 entries × 11 classes) rejects
complex input exactly like the reference (`expectedReal` class) — only
`im2col` (values preserved, implemented) and `immse` (|z|² error,
implemented) compute complex for real today.

## Repro (representative)

```matlab
clear;
J = imfilter(magic(5)/8 + 1i, ones(3)/9);   % MATLAB: complex double
                                             % nk: nk:imfilter:complexUnsupported
```

## Guards

`DISABLED_ImfilterComplexKernel`, `DISABLED_ImnoiseComplexIdentity`,
`DISABLED_ImapplymatrixComplexKernel`, `DISABLED_Axes2pixComplexExtent`
in `src/toolboxes/image/tests/known_bugs_test.cpp`.
