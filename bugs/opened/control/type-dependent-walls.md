# control — type-dependent walls: sys-arg paths are stricter than the catalog walls

- **Status:** 🔴 OPEN
- **Severity:** P4 (extra-arg acceptance only; no wrong numerics)
- **Kind:** bug
- **Found:** 2026-09-17 during the control arity migration — walls probed
  with numeric dummies can be LOOSER than what the reference accepts
  for real model arguments (the reference dispatches on the first
  argument's class: model path vs obsolete matrix path).

## Symptom

For some functions the reference accepts extra positional arguments on
the obsolete numeric path but rejects them for model arguments, so the
catalog wall (probed with numeric dummies) lets nk accept calls the
reference refuses in practice.

| Function | nk wall (numeric-dummy probe) | model-arg path |
|---|---|---|
| covar | 5 | rejects 3+ (probed: TooManyInputs at 3 with an ss model) |
| ss2ss | 5 | rejects 3+ (probed: TooManyInputs at 5 with an ss model) |
| gram | 2 | model path accepts name-value tails (OptionHelper domain error at 3) — nk is stricter here |

## Repro

```matlab
clear;
sm = ss([0 1; -1 -2], [1; 0], [1 0], 0);
covar(sm, 1, 1);
% nk:     returns P (3rd argument silently ignored)
% MATLAB R2025b (probed 2026-09-17):
%   Error MATLAB:TooManyInputs — the model path accepts (sys, W) only

ss2ss(sm, eye(2), 1, 1, 1);
% nk:     returns the transformed model (3rd..5th ignored)
% MATLAB R2025b: Error MATLAB:TooManyInputs
```

## Root cause

The 2026-09-17 catalog walls come from dual-pass numeric probes; the
reference's class dispatch makes the effective wall depend on the first
argument's type, which a single (min, max) contract cannot express.

## Suggested fix

When the first argument parses as a model struct, apply the stricter
model-path bound (a reg-side check after checkNargin), or document the
looseness per function.

## References

- **Guard:** `DISABLED_CovarModelPathStrict`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
