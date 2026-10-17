# control — hinfnorm: discrete-time models unsupported

- **Status:** 🔴 OPEN
- **Severity:** P3 (feature gap; honest stub with its own identifier)
- **Kind:** stub
- **Found:** 2026-09-18 during the control argcheck portion (probe9) —
  the stub voice existed before; filing the gap explicitly with a
  guard so it is tracked.

## Symptom

`hinfnorm(sys)` for a discrete model (Ts > 0) answers `Inf` (or a
finite value) in the reference; nk stubs with
`nk:hinfnorm:discrete` (continuous-time Hamiltonian bisection only).

## Repro

```matlab
clear;
g = hinfnorm(ss([2 1; 1 3], [1; 0], [1 0], 0, 0.1));
% MATLAB R2025b (probed 2026-09-18): Inf  (|λ|>1 → unbounded)
% nk: nk:hinfnorm:discrete — discrete-time systems are not yet
%   supported (continuous-time only)
```

## Documented divergence (deliberate)

For untyped garbage the reference's hinfnorm returns
`[Inf Inf 0]` + a warning (`hinfnorm(struct('a',1))`, `hinfnorm({})`,
probed) — a dispatch accident of its lti coercion. nk rejects those
with `nk:hinfnorm:inputType` instead of mirroring Inf-for-garbage.
Numeric SCALARS are the real static-gain form and are mirrored
exactly (`hinfnorm(1)` → `[1 1 0]`, `hinfnorm(-3)` → `[3 3 0]`,
`hinfnorm(2i)` → `[2 2 0]`, probed).

## Root cause

The Bruinsma–Steinbuch Hamiltonian test is built for the s-plane;
the discrete version needs the unit-circle bicriteria form
(γ²I − AᵀA -like blocks with the sample-time mapping).

## Suggested fix

Add the discrete Hamiltonian test (H = [Aᵀ (γ²I−…)A …] per Zhou/
Doyle, or map poles via z→ln(z)/Ts and reuse the continuous kernel).

## References

- **Guard:** `DISABLED_HinfnormDiscrete`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
- Live guards for the scalar + garbage forms: `HinfnormContracts`
  (src/toolboxes/control/tests/type_contract_test.cpp)
