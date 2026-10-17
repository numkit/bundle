# stats — *_of compute helpers read doubleData() without a type contract

- **Status:** ✅ FIXED (routed through `*_full` cleaning contracts, 2026-10-17)
- **Severity:** P2 (raw memory read on non-numeric input)
- **Kind:** bug
- **Found:** 2026-09-18 during the stats structural _argcheck survey —
  the compute helpers behind the m-source dispatchers assume their
  Value inputs are double arrays.

## Symptom

`detrend_of` / `isoutlier_of` / `rmoutliers_of` / `fillmissing_of` /
`rmmissing_of` / `standardizeMissing_of`
(descriptive/descriptive_extras.cpp) call `x.doubleData()` with no type
check; a char/cell/struct Value reaching them reads raw heap bytes as
doubles. The m-source dispatchers usually validate first, but direct
C++ calls (and any dispatcher gap) reach the helpers unchecked.

## Repro

```matlab
clear;
d = detrend('ab');
% nk (via a dispatcher gap or direct C++ stats::detrend_of): reads the
%   char payload as doubles — garbage or crash, no nk-voiced error
% MATLAB R2025b: rejects non-numeric input with a type error
```

## Root cause

The helpers predate the func_argcheck pattern (dev-docs/todo/
argcheck_separation.md): no `<fn>_argcheck` guards the type contract at
the compute layer.

## Suggested fix

Add a shared numeric-contract argcheck at the top of each `_of` helper
(matching each function's reference rejection class — probe before
fixing: unlike the nan family, these reference functions REJECT char),
and route the dispatcher through the same checks.

## References

- **Guard:** `DetrendCharRejected`
  (modules/stats/tests/known_bugs_test.cpp)
