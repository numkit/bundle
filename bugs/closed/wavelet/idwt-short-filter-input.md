# idwt / idwt2 return an EMPTY result when the filter is longer than the data supports

- **Kind:** bug
- **Component:** wavelet (1-D idwt kernel; surfaces through idwt2)
- **Found:** 2026-09-19, wavelet argcheck portion (probe41 battery, `idwt2 db4 small`)
- **Fixed:** 2026-09-18, bug-quartet portion

## Repro

```
clear;
[cA,cH,cV,cD] = dwt2([1 2 3; 4 5 6; 7 8 9], 'haar');
y = idwt2(cA, cH, cV, cD, 'db4');   % 2x2 coefficients, db4 filter length 8
numel(y)
```

- nk (before): `0` (silently empty)
- MATLAB R2025b (re-probed, probe61 Q5-table + P13): `100` — a 10×10
  reconstruction (first row `[0.328209 1.018413 1.369993 1.422226 …]`).
  The initial bug-file text claimed "16 / 4x4"; that was a battery
  misread — ground truth is 10×10 = the full-convolution length
  `2·la + Lf − 2` per dimension.

The 1-D form has the same hole: `idwt(zeros(2,1), zeros(2,1), 'db4')`
returned `[]` where the reference reconstructs 10 samples.

## Root cause (reference sources: idwt.m → upsconv1.m → wkeep1.m)

The default keep length is `2·la − Lf + 2` and wkeep1 extracts the
CENTRAL run — but when the keep length is negative (or meets/exceeds
the full convolution), **wkeep1 returns the convolution uncropped**,
and when it is exactly 0 the result is empty. nk treated every
non-positive natural length as empty.

## Fix

`idwt_with_filters` now applies the wkeep1 rule: natural length
`2·la − Lf + 2`; `< 0` (or `≥` full length) → the full convolution
(offset 1 in nk's leading-zero-padded frame, length `2L + Lf − 2`);
`== 0` → empty. The central-crop offset is `(sx − s)/2 + 1` (wkeep1 'c'
side 'u'), which reproduces the old fixed `Lf − 1` offset for the
normal symmetric case. idwt2 inherits via its per-dimension natural
probe. Also fixed here: 1-D idwt result class now follows cA
(the reference's `isUnderlyingType(a,'single')` cast).

Verified: la ∈ {1,2,3,4,5} × {haar,db2..db6,sym8,coif2} length table
(Q51–Q510, 10/10) + la=2/db4 = literally the db4 Lo_R filter + the
idwt2 10×10 first row; `idwt(single(...))` → single.

**Guard:** `Idwt2Db4ShortCoefficients` in
`src/toolboxes/wavelet/tests/known_bugs_test.cpp` (live).
