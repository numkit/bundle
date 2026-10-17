# stats.trimmean — vecdim form rejected

- **Status:** ✅ FIXED (2026-09-17, vecdim campaign — shared nk::vecdim parser + collapse path)
- **Severity:** P3 (single function, documented argument form)
- **Kind:** bug
- **Found:** 2026-09-17 while reviewing argcheck diagnostic output (probed
  against R2025b).

## Symptom

trimmean's dim slot accepts only a scalar; a vecdim vector is rejected as
"dimension argument must be a scalar (argument is 1x2)". The reference
accepts it.

## Repro

```matlab
clear;
t = trimmean(1:5, 10, [1 2]);
% nk:     Error: trimmean: dimension argument must be a scalar
%         (argument is 1x2)
% MATLAB R2025b (probed 2026-09-17): t = 3
```

## Root cause

The trimmean reg routes the dim argument through
`argcheck::dimArg(Value)` (scalar-only) — no vecdim branch.

## Suggested fix

Same dimension-set reduction path as the other vecdim gaps
(vecdim-partial.md / datafun-vecdim.md).

## References

- **Guard:** `DISABLED_TrimmeanVecdim`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Related: bugs/opened/lang/datafun-vecdim.md.
