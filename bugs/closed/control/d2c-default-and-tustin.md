# control — d2c: default must be 'zoh'; tustin breaks on a plain stable pole

- **Status:** ✅ FIXED (0a50c4d) 
- **Severity:** P2 (default path errors on a textbook system)
- **Kind:** bug
- **Found:** 2026-09-17 during the control arity migration — the REPL
  smoke of the applied contracts called the documented default form
  `d2c(sysd)` and it errored.

## Symptom

Three stacked divergences in `d2c`:

1. The reference default discretization method is `'zoh'`; nk defaults
   to `'tustin'`.
2. nk's tustin path errors with "A_d + I is singular" on a plain
   stable first-order system.
3. `'zoh'` (the reference default) is rejected outright: "only
   'tustin' is supported".

## Repro

```matlab
clear;
d = d2c(tf([1], [1 1], 0.1));
% nk:     Error nk:d2c:singular — "d2c (tustin): A_d + I is singular"
% MATLAB R2025b (probed 2026-09-17): continuous model,
%   num = [0 1.170334e-6 493.4802], den = [1 -2.22e-13 986.9603]

d2 = d2c(tf([1], [1 1], 0.1), 'zoh');
% nk:     Error — "only 'tustin' is supported"
% MATLAB R2025b: same continuous model (zoh is the default method)

d3 = d2c(tf([1], [1 -0.5], 0.5));
% nk:     OK (tustin happens to work for this pole) — method still
%         diverges from the reference default numerics
```

## Root cause

discretize.cpp implements the tustin map only, selects it silently as
the default, and its matrix inversion `(A_d + I)^-1` is taken on a
companion-form realization where that sum is singular for this system;
the zoh inverse map (eigenvalue log path, matching the reference
default) is missing.

## Suggested fix

Implement the zoh inverse (eig of A_d, s = log(λ)/Ts) and make it the
default; fix or guard the tustin inversion on singular realizations
(solve instead of invert, or reorder the companion form).

## References

- **Guard:** `D2cDefaultZoh`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
