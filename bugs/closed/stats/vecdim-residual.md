# stats.reductions — residual scalar-only dim slots (zscore/range/mad/geomean/harmmean/nan* family)

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (family follow-up; the parser + collapse machinery now exists)
- **Kind:** bug
- **Found:** 2026-09-17 while fixing the vecdim rank model — the sweep
  covered the six sites that already parsed vecdim plus trimmean/moment/
  datafun; these slots still accept only a scalar dim.

## Symptom

The dim slot of these functions rejects the documented vecdim form with
"dimension argument must be a scalar (argument is 1x2)":

- `zscore` (normalize_reg.cpp, args[2])
- `range` (descriptive_extras_reg.cpp, args[1])
- `mad` (descriptive_extras_reg.cpp, args[2])
- `geomean` / `harmmean` (descriptive_extras_reg.cpp, args[1])
- `nanmedian` / `nanmean` / `nanvar` / `nanstd` … (nan_aware_reg.cpp —
  probe first: the legacy nan* family may legitimately be dim-only in
  the reference)

## Repro

```matlab
clear;
r = range(ones(2,3,4), [1 3]);
% nk:     Error: range: dimension argument must be a scalar
% MATLAB R2025b: range over dims [1 3] → 1x1x4 of zeros
```

(Verify each function's reference contract before wiring — probe
`fn(x, vecdim)` per function; any that the reference rejects stay as-is
with a comment.)

## Suggested fix

Route each dim slot through `vecdim::parseDimSet` +
`vecdim::collapseDims`/`expandReduced` (support/reduce_vecdim.hpp) —
the same three-line pattern the descriptive regs now use.

## References

- **Guard:** `VecdimResidual`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Fixed in the same campaign: vecdim-rank-model.md, vecdim-partial.md,
  trimmean-vecdim.md, lang/datafun-vecdim.md (all closed 2026-09-17).
