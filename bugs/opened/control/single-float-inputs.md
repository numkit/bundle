# control — single-float inputs: acker returns single in the reference

- **Status:** 🔴 OPEN
- **Severity:** P4 (stubbed honestly; single is rare in control scripts)
- **Kind:** stub
- **Found:** 2026-09-18 during the control argcheck portion (probe10).

## Symptom

`acker` with any single input returns a **single-class** result in the
reference (probed: `acker(single(A), B, p)` → class=single `[8 21]`,
`acker(A, B, single(p))` → class=single). nk's kernel is double-only,
so single is rejected with `nk:acker:singleUnsupported` instead of
returning a wrong-class double.

Every OTHER control entry in the portion was probed single-clean — the
reference itself coerces to double results there (lyap/dlyap/ctrb/
obsv/ss2ss/lsim return double; tf/filt/ss store double internally —
`class(tfdata(tf(single, single)){1})` is double in the reference
too), so nk's double behavior is reference-identical and no stub is
needed there.

## Repro

```matlab
clear;
K = acker(single([2 1; 1 3]), [1; 0], [-1 -2]);
% MATLAB R2025b (probed 2026-09-18): class=single, [8 21]
% nk: nk:acker:singleUnsupported — single inputs produce a single
%   result in the reference engine; convert with double()
```

## Root cause

The Ackermann kernel (phiOfA / solveInPlace in place.cpp) works on
`std::vector<double>`.

## Suggested fix

Either a single-buffer kernel pass or an explicit single storage class
for the result (compute double, store single) — the latter matches the
reference's observable contract.

## References

- **Guard:** `DISABLED_AckerSingleResult`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
- Family file for the rest of the repo:
  `bugs/opened/linalg/single-float-inputs.md` (linalg family)
