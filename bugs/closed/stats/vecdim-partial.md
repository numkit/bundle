# stats.median — partial vecdim reduction not supported

- **Status:** ✅ FIXED (2026-09-17, vecdim campaign — shared nk::vecdim parser + collapse path)
- **Severity:** P3 (documented vecdim sub-form; full-cover form works)
- **Kind:** stub
- **Found:** 2026-09-17 while reviewing argcheck diagnostic output (probed
  against R2025b).

## Symptom

A vecdim that covers only SOME of the input's dimensions throws
"partial vecdim reduction not supported". The reference reduces over the
listed dimensions and keeps the rest as trailing shape.

## Repro

```matlab
clear;
m = median(ones(2,2,2), [1 3]);
% nk:     Error: median: partial vecdim reduction not supported
%         (nk:median:vecdim)
% MATLAB R2025b (probed 2026-09-17): m = [1 1]   (1x2; dim 2 kept)
```

## Root cause

The vecdim branch in descriptive_reg.cpp (median site ~:318) only wires
two outcomes: all-covered → 'all' flatten, partial → explicit throw. The
compute kernels have no reduce-over-dimension-set entry point.

## Suggested fix

Add a dimension-set reduction path (permute listed dims to the front,
reshape the remainder, reduce along dim 1) shared by the vecdim-capable
reductions; then the rank-model fix (vecdim-rank-model.md) and this
become one code path.

## References

- **Guard:** `DISABLED_MedianVecdimPartial`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Related: bugs/opened/stats/vecdim-rank-model.md.
