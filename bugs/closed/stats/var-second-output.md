# var / std second output (the weight vector) is not emitted

- **Status:** ✅ FIXED (2026-10-17)
- **Kind:** missing-output
- **Component:** stats (var, std)
- **Found:** 2026-09-18, stats descriptive argcheck portion (probe68 V21).

## Repro

```
clear;
[v, w] = var([1 2 3; 4 5 6; 7 8 9]);   % w = ones(1,3) (or the weight vector)
```

- MATLAB R2025b: v per column, w = the normalization weight vector in
  effect (ones for the plain w=0/w=1 forms, the user weights otherwise).
- nk: "Too many output arguments".

## Fix direction

varStdDispatch computes the effective weights already (normFlag /
wVec); emit them as outs[1] under nargout ≥ 2.

**Guard:** `VarSecondOutput` (src/toolboxes/stats/tests/known_bugs_test.cpp)
