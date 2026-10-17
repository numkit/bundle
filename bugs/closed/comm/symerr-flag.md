# comm — symerr: 'row-wise'/'column-wise'/'overall' flag deferred

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (documented 3rd argument of a common metric)
- **Kind:** stub
- **Found:** 2026-09-17 during the comm arity migration — R2025b probe
  showed symerr walls at (2,3) with a functional 3rd flag argument.

## Symptom

`symerr` accepts the documented flag argument in the reference and
changes the output aggregation; nk's compute has only the element-wise
default, so the 2026-09-17 arity migration accepts the 3-arg call but
throws a voiced deferral (`nk:symerr:flg`) instead of computing.

## Repro

```matlab
clear;
[n, r] = symerr([1 0; 0 1], [0 1; 1 0], 'overall');
% nk:     Error nk:symerr:flg ("flag is not supported yet")
% MATLAB R2025b (probed 2026-09-17): n = 4 (scalar), r = 1

n2 = symerr([1 0; 0 1], [0 1; 1 0]);
% both: n2 = 4 — the 2-arg default already matches
```

## Root cause

`comm::symerr` (engine-free compute) returns the element-wise count and
ratio only; the flag aggregation modes were never implemented.

## Suggested fix

Extend the compute with the three documented aggregations: 'overall'
(scalar total), 'column-wise' (row vector), 'row-wise' (column vector);
parse the flag in `symerr_reg` and drop the deferral throw.

## References

- **Guard:** `SymerrOverallFlag`
  (src/toolboxes/comm/tests/known_bugs_test.cpp)
