# lang.datafun — base reductions reject the vecdim form

- **Status:** ✅ FIXED (2026-09-17, vecdim campaign — shared nk::vecdim parser + collapse path)
- **Severity:** P2 (documented R2018b+ argument form rejected with a
  mis-blaming diagnostic across the whole base reduction family)
- **Kind:** bug
- **Found:** 2026-09-17 while reviewing argcheck diagnostic output (probed
  against R2025b).

## Symptom

sum/mean/prod/max/min (datafun_reg.cpp) accept only a scalar dim; a
vecdim vector is rejected as "dimension argument must be a scalar
(argument is 1x2)". The reference accepts the vecdim form for all of
them. The rejection also mis-blames the input: the form is documented,
the value is legal — only our parser lacks the branch.

## Repro

```matlab
clear;
s = sum(1:5, [1 2]);
% nk:     Error: sum: dimension argument must be a scalar (argument is 1x2)
% MATLAB R2025b (probed 2026-09-17): s = 15

m = mean(magic(3), [1 2]);   % nk: error; MATLAB: m = 5
p = prod(magic(3), [1 2]);   % nk: error; MATLAB: p = 362880
mx = max(magic(3), [], [1 2]);  % nk: error; MATLAB: mx = 9
```

Negative probe (do NOT "fix" cumsum): `cumsum(1:5,[1 2])` is rejected by
the reference too ("Dimension argument must be a positive integer scalar
within indexing range", probed 2026-09-17) — nk's rejection there is
correct parity.

## Root cause

datafun_reg.cpp routes the dim argument straight through
`argcheck::dimArg(Value)` (scalar-only); there is no vecdim branch and no
dimension-set reduction path in the kernels.

## Suggested fix

Share the dimension-set reduction path added for
stats/vecdim-partial.md; parse vecdim in the datafun dim slot the same
way the stats descriptive regs do (post rank-model fix).

## References

- **Guard:** `DISABLED_SumVecdim`, `DISABLED_MeanVecdim`,
  `DISABLED_ProdVecdim`, `DISABLED_MaxVecdimEmptyFlag`
  (src/bundle/tests/known_bugs_test.cpp)
- Related: bugs/opened/stats/vecdim-rank-model.md,
  bugs/opened/stats/trimmean-vecdim.md.
