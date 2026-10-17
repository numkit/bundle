# stats.reductions — vecdim rank model rejects entries the reference accepts

- **Status:** ✅ FIXED (2026-09-17, vecdim campaign — shared nk::vecdim parser + collapse path)
- **Severity:** P2 (documented vecdim form rejected on every vector/scalar
  input and every rank-4+ array)
- **Kind:** bug
- **Found:** 2026-09-17 while reviewing argcheck diagnostic output (probed
  against R2025b).

## Symptom

The stats reduction regs compute the input's rank with the heuristic

```cpp
const int rank = args[0].dims().is3D() ? 3
                  : (args[0].dims().isVector() || args[0].isScalar() ? 1 : 2);
```

and reject any vecdim entry `d > rank` as "vecdim entries out of range".
The reference engine treats every array as rank ≥ 2 (a 1×5 row vector has
a dimension 2 of size 5) and supports rank-4+ arrays natively, so entries
that are legal there are rejected here. Affects every vecdim-capable
reduction sharing the copied heuristic: median, iqr, bounds, mode, moment
(sites: descriptive_reg.cpp:161/314/405, descriptive_extras_reg.cpp:176/
234/377).

## Repro

```matlab
clear;
m = median(1:5, [1 2]);
% nk:     Error: median: vecdim entries out of range (nk:median:vecdim)
% MATLAB R2025b (probed 2026-09-17): m = 3

m = median(3, [1 2]);
% nk:     same error
% MATLAB: m = 3

m = median(ones(2,3,4,5), [1 2 3 4]);
% nk:     same error (rank collapses to 2 for non-3D inputs)
% MATLAB: m = 1

r = iqr(1:5, [1 2]);      % nk: error; MATLAB: r = 2.5
b = bounds(1:5, [1 2]);   % nk: error; MATLAB: b = [1 5]
```

## Root cause

The rank heuristic models a vector/scalar as rank 1 and any non-3D array
as rank 2, instead of the input's real dimension count with the implicit
minimum rank 2. The full-cover branch then treats `[1 2]` on a vector as
out of range rather than "all elements".

## Suggested fix

Derive the rank from `args[0].dims().ndim()` clamped to a minimum of 2
(reference semantics), and let the existing full-cover check decide
all-vs-partial. Partial vecdim reduction is a separate filed gap
(vecdim-partial.md).

## References

- **Guard:** `DISABLED_MedianVecdimVector`, `DISABLED_MedianVecdimScalar`,
  `DISABLED_MedianVecdimRank4`, `DISABLED_IqrVecdimVector`,
  `DISABLED_BoundsVecdimVector`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Related: bugs/opened/stats/vecdim-partial.md (partial reduction stub),
  bugs/opened/lang/datafun-vecdim.md (base reductions lack the form).
