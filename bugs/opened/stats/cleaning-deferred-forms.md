# cleaning family: deferred reference forms (stub)

**Kind:** stub · **Status:** opened 2026-09-19 · **Found:** stats argcheck drain
(cleaning family portion)

## What

The 2026-09-19 cleaning-family contract migration (detrend / isoutlier /
rmoutliers / fillmissing / rmmissing / standardizeMissing — probe
batteries build/probe70{,b,c,d}.m, source reads of detrend.m,
parseIsOutlierInput.m, locateoutliers.m, rmMissingOutliers.m,
ismissingKernel.m, fillmissing.m) implemented the full ARRAY-path
contracts. The reference-engine forms below remain voiced nk stubs.

## Deferred branches

### detrend
* `SamplePoints` NV (custom abscissa) — `nk:detrend:samplePoints`.
* table / timetable inputs (`DataVariables`, `ReplaceValues`) —
  array-reject `nk:detrend:tableOnly` (needs the table engine feature,
  see bugs/opened/lang/table.md).
* The `PolyNotUnique` WARNING on rank-deficient designs: nk computes a
  basic solution (free variable = 0) matching the reference VALUES in
  the probed cases but emits no warning.
* single-precision detrend computes in double and narrows: residuals
  differ from the single-computed reference at single-eps scale
  (parity uses closeness predicates; same precedent as the wavelet
  single paths).

### isoutlier
* `SamplePoints` NV — `nk:isoutlier:samplePoints`.
* table inputs (`DataVariables`, `OutputFormat`) — array-reject
  `nk:isoutlier:dataVariables` / `nk:isoutlier:outputFormat`.

### rmoutliers
* table inputs (`DataVariables`) — array-reject; 3rd–6th outputs ARE
  implemented (mask + thresholds via the isoutlier outputs).

### fillmissing
* `'spline'` / `'pchip'` / `'makima'` / `'knn'` fill methods —
  `nk:fillmissing:methodDeferred`.
* function-handle fill methods — the parse rejects non-strings
  (`nk:fillmissing:methodInvalid`); the reference's ≥3-arg custom
  filler contract is not implemented.
* `SamplePoints` / `MaxGap` / `Distance` NVs —
  `nk:fillmissing:optionDeferred`.
* string / cell array inputs — `nk:fillmissing:firstInputInvalid`
  (reference accepts them; needs string-array missing support).
* complex fill constants for NON-complex inputs (the reference
  promotes the result to complex; nk requires a complex input).

### rmmissing / standardizeMissing
* string / cell / categorical / datetime inputs — voiced
  `nk:rmmissing:typeUnsupported` / indicator-compatibility errors
  (reference accepts them; same string/table dependency).
* `standardizeMissing` NV tail (`DataVariables`, `ReplaceValues`) —
  array-reject (table-only in the reference).

## Guard

**Guard:** deferred (voiced stubs; no wrong-value paths — every listed
branch errors with its nk identifier instead of computing).

## Repro

    clear;
    try, detrend(1:5, 1, 'SamplePoints', [0 1 2 3 4]); end   % ref: works, nk: nk:detrend:samplePoints
    try, fillmissing([1 NaN 3], 'spline'); end               % ref: works, nk: nk:fillmissing:methodDeferred
    try, isoutlier([1 2 3], 'SamplePoints', [1 2 3]); end    % ref: works, nk: nk:isoutlier:samplePoints
