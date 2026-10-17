# stats.*rnd — size tails are 2-D only: [m n p …] flattens, 3+ scalar sizes reject

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (rarely used forms; [m n] and m/n forms are correct)
- **Kind:** bug
- **Found:** 2026-09-17 while migrating the *rnd size extraction to
  `nk::argcheck` (the shared `parse_rng_size` admitted the flattening in
  a comment). Same-day second symptom found by the max-arity probe:
  the reference accepts an unbounded SCALAR size tail.

## Symptom

Every toolbox `<dist>rnd` accepts trailing size arguments, but only the
2-element forms behave like the reference:

1. **vector form**: 3+ element size vectors are flattened to
   `first × product(rest)` instead of an N-D array;
2. **scalar-tail form**: a 3rd+ scalar size is REJECTED with
   `nk:<fn>:maxnargin` ("more than two size inputs"), while the
   reference computes an N-D draw.

## Repro

```matlab
clear;
s = size(geornd(0.5, [2 3 4]));
% nk:     s = [2 12]
% MATLAB R2025b (probed 2026-09-17): s = [2 3 4]

t = size(geornd(0.5, 2, 3, 4));
% nk:     Error nk:geornd:maxnargin (parse_rng_size caps at two sizes)
% MATLAB R2025b (probed 2026-09-17): t = [2 3 4] (also normrnd/poissrnd)
```

## Root cause

`parse_rng_size` (src/toolboxes/stats/src/distributions/dist_helpers.hpp)
multiplies the trailing dims into `cols` and throws `maxnargin` past two
scalar sizes, and the compute kernels all take `(rows, cols)` — the rnd
family has no N-D output path. NOTE: the helper's "more than two size
inputs is too many" comment and the `TooManySizeInputs` test in
argcheck_stats_test.cpp encode this nk cap; they are NOT the reference
contract (the 2026-09-17 arity probe disproved it) and must flip with
the fix.

## Suggested fix

Widen the shared kernel signatures to a dims vector (or rows/cols/pages)
for the rnd family — the dist broadcast helpers already allocate 3-D
(`Value::matrix3d`), so the pattern exists. Mechanical across the ~23
rnd adapters once the compute side accepts a shape. The 2026-09-17
arity migration deliberately left the rnd regs min-only (no max), so no
reg-side bound needs relaxing.

## References

- **Guard:** `RndSizeVectorND`, `RndNdSizeTails`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
- Correct forms pinned live in the same file (`RndSizeContract*`).
