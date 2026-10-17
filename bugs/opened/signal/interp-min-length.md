# signal.interp — no minimum data-length check (reference rejects short inputs)

- **Status:** 🔴 OPEN
- **Severity:** P3
- **Kind:** bug
- **Found:** 2026-09-17 during the argcheck signal sweep probes.

## Symptom

The reference requires the data length to exceed the interpolation
filter half-length (`n`, default 4 → length ≥ 2n+1 = 9); nk accepts any
length silently.

## Repro

```matlab
clear;
y = interp(1:8, 2);
% nk:     y = 1x16 result (no error)
% MATLAB R2025b (probed 2026-09-17): Error — "Length of data sequence
%   must be at least 9. You either need more data or a shorter filter (L)."
```

## Root cause

interp_reg validates r/n (positive integers, landed 2026-09-17) but no
`numel(x) >= 2*n+1` domain check.

## Suggested fix

Add the length check in the reg (nk-voiced: interp: input 1 (x) must
have at least 2*n+1 = <computed> samples (got <numel>) — mention
shortening the filter via the n argument).

## References

- **Guard:** `DISABLED_InterpMinLength`
  (src/toolboxes/signal/tests/known_bugs_test.cpp)
