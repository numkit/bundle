# stats.mvnrnd — explicit n = 0 / negative n derives from mu instead of an empty draw

- **Status:** ✅ FIXED (2026-09-19, stats argcheck campaign distributions portion: mvnrnd_full takes the raw cases value, so zero/negative counts produce the 0×d empty directly — commit follows)
- **Severity:** P3 (edge; validation of n landed 2026-09-17, this is the
  clamp-through)
- **Kind:** bug
- **Found:** 2026-09-17 while migrating multivariate count extraction to
  `nk::argcheck` (probed alongside).

## Symptom

`mvnrnd(rng, mu, Sigma, n)` uses `n == 0` as the "derive from mu"
sentinel (public default). A PRESENT zero-or-negative n therefore takes
the derive path and returns a draw, where the reference returns a 0×d
empty.

## Repro

```matlab
clear;
s = size(mvnrnd(0, 1, -2));
% nk:     s = [1 1]  (derive path)
% MATLAB R2025b (probed 2026-09-17): s = [0 1]  (empty; the size-input
%   clamp -2 → 0 rows)
```

## Root cause

The sentinel and the literal count share the value 0; the reg cannot
express "explicitly zero" through the current public signature.

## Suggested fix

Change the public sentinel to a distinguishable form per library_api
(e.g. an overload taking the count WITHOUT a default, or default =
"derive" sentinel `SIZE_MAX`), then let the reg pass the validated
count literally (0 → empty). mvtrnd/mnrnd already treat their counts
literally and clamp correctly.

## References

- **Guard:** `DISABLED_MvnrndZeroN`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Size-contract validation (fractional/NaN/complex) landed 2026-09-17 —
  see `ArgcheckStatsRnd` tests.
