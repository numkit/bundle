# comm — silently-ignored documented option tails (consolidated)

- **Status:** 🔴 OPEN
- **Severity:** P3 (options accepted, parsed by the reference, dropped by nk)
- **Kind:** bug
- **Found:** 2026-09-17 during the comm arity migration — probing the
  reference walls exposed several option arguments that nk accepts
  (inside the wall) but never reads.

## Symptom

Several comm regs accept the reference's full arity range but silently
drop documented trailing options, so calls "succeed" with the option
ignored instead of changing behavior (or, in awgn's case, instead of
erroring where the reference errors).

| Function | Ignored args | Reference behaviour |
|---|---|---|
| awgn | 4th powertype ('db'/'linear'), seed | powertype must be the LAST input; a 5th arg after it errors |
| bsc | 3rd seed | reproducible seeding |
| biterr | 4th flg ('overall'/…) | aggregation changes count/ratio shape |
| huffmandict | 3rd expMinLength, 4th variance | minimum codeword length / variance tie-break |
| lloyds | 4th 'plot' | displays partition evolution |
| mskmod | 4th dataenc? (wall 4) | per R2025b doc |
| ofdmmod / ofdmdemod | 4th..8th name-value | pilot/null options |
| vitdec | 6th..11th name-value | termination / soft-decision options |

(Reference semantics of the unprobed rows were not distilled to
per-option repros yet — do that when picking this file up.)

## Repro

```matlab
clear;
awgn(ones(1, 4), 10, 1, 'db', 5);
% nk:     returns a noisy vector (5 silently ignored)
% MATLAB R2025b (probed 2026-09-17):
%   Error comm:awgn:InputAfterPowerType
%   ("The signal power type can only be specified once and must be the
%    last input.")
```

## Root cause

The regs were written against happy-path signatures; trailing options
inside the arity wall were never wired into the compute calls.

## Suggested fix

Per option: parse, either implement or throw a voiced nk deferral
(never accept-and-drop). Start with awgn/bsc (seed = engine rng
reseeding) and biterr (aggregation mirrors the symerr flag work).

## References

- **Guard:** `DISABLED_AwgnPowerTypeMustBeLast`
  (src/toolboxes/comm/tests/known_bugs_test.cpp)
