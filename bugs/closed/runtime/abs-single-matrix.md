# abs() rejects single matrices ("Not a double array")

- **Kind:** bug
- **Component:** builtin `abs` (single-class dispatch).
- **Found:** 2026-09-19, image argcheck portion probe battery.
- **Fixed:** 2026-09-18, engine-gap portion.

## Repro

```
clear;
x = abs(single([1 -2 3]));   % expect single [1 2 3]
```

- MATLAB R2025b: single `[1 2 3]`.
- nk (before): `nk:error | Not a double array` (matrix path called
  `doubleData()` on a single buffer; the scalar path silently returned
  DOUBLE instead of single too).

## Fix

Both abs backends (highway + portable) gained a SINGLE branch (single
result, fabs loop) placed before the scalar shortcut, plus
logical/char widening to double (abs('ab') = [97 98]) which shared the
same `doubleData()` crash.

**Guard:** `AbsSingleMatrix` in `src/bundle/tests/known_bugs_test.cpp`
(live).
