# lang — domain validation lives in *_reg adapters (marshal-only rule violation)

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (diagnostic divergence between call paths; C++ API
  bypass on sites without compute-side checks)
- **Kind:** bug
- **Found:** 2026-09-18 — self-audit after the stats/comm/control arity
  migrations: the argcheck rule (`*_reg` adapters marshal only; domain
  checks live in a compute-side `<fn>_argcheck`) is violated across the
  migrated domains, and the 2026-09-17 migrations walked past the sites
  without filing them.

## Symptom

Domain validation is split between the reg layer and the compute layer
(anti-patterns 1–2 in dev-docs/todo/argcheck_separation.md):

1. **Duplicated checks with DIVERGING identifiers.** mil188qammod
   validates M in the reg (`nk:mil188qammod:MNotChoice` via
   expectedOneOf) AND in the compute (`nk:mil188qam:UnsupportedM` via
   constellationFor's switch). The eval path answers one id, a direct
   C++ call the other — and the compute id names a different function
   ("mil188qam").
2. **Reg-only checks = C++ public API bypass.** Where only the reg
   validates, direct C++ callers skip the checks entirely.

### Site census (reg-layer domain logic walked past in 2026-09-17)

| Domain | Sites | Status |
|---|---|---|
| comm | mil188qammod/demod M-set (`expectedOneOf` in regs, diverging compute id) | ✅ FIXED 2026-09-18 — compute-side `mil188MSetArgcheck`, one identifier, guard live |
| comm | bi2de base>=2 in reg | ✅ FIXED 2026-09-18 — compute-side `bi2de_argcheck` |
| comm | vitdec / syndtable multi-check prologues inline in compute | ✅ shaped 2026-09-18 into named `vitdec_argcheck` / `syndtable_argcheck` |
| comm | remaining `argcheck::expected*` in regs (pulse, base_conversions, analog, errors, arithcoding, dpcmopt) | extraction-with-validation for native-taking computes — accepted as marshalling (boundary decision, see memory); string-flag content checks stay reg-side per the compand precedent |
| stats | fit_reg.cpp like-family `params.numel() < 2` checks in the shared emit helper | resolved 2026-09-18 as marshalling (the C++ API takes mu/sigma natives — the numel check is vector-params extraction) |
| stats | rescale compute accepted non-numeric input the reference rejects | ✅ FIXED 2026-09-18 — compute-side rescale_argcheck (live guard RescaleTypeContract) |
| stats | *_of helpers read doubleData() without a type contract (direct C++ path) | ✅ FIXED 2026-10-17 — bugs/closed/stats/of-helpers-raw-doubledata.md |
| control | feedback sign ±1 content check in reg (compute takes any int) | ✅ FIXED 2026-10-17 — guard `FeedbackSignCppPathUnified` live |

The full per-function plan is `tools/argcheck_classification.json`
(267 `value-contract-in-compute` functions repo-wide; pilots + the comm
18 done; reshape / filter / fir1 remain the signal pilots) — this bug is
the enforcement hook for it.

## Repro

```matlab
clear;
mil188qammod(0, 128);
% nk (eval path, reg validates): Error nk:mil188qammod:MNotChoice
%   "input 2 (M) must be one of: 16, 32, 64, 256 (got 128)"
% MATLAB R2025b: Error comm:mil188qamshared:UnsupportedM
%   "The supported constellation sizes are 16, 32, 64 and 256."
```

Direct C++ call (bypasses the reg):

```cpp
nk::Value y = nk::comm::mil188qammod(nk::Value::scalar(0.0, mr), 128, mr);
// nk: throws nk:mil188qam:UnsupportedM — a THIRD spelling, from the
//     compute's own switch. One bad argument, two nk identifiers.
```

## Root cause

The 2026-09-17 arity migrations replaced arity handling only (their
recorded scope, bugs/opened/lang/reg-max-arity.md) and left the
pre-existing reg-side domain checks in place; some hand edits added new
defaults/validation to regs. The structural `func_argcheck` phase
(todo doc Phase 4, opportunistic) was not applied to the touched
functions.

## Suggested fix

Per the classification, migrate domain checks into file-internal
`<fn>_argcheck` functions at the top of each compute entry so the
interpreter and direct C++ calls cross the same checks with one
identifier; regs reduce to arity + Value→native marshalling. Start with
the sites above (the domains are fresh in memory), then follow the
classification order.

## References

- **Guard:** `Mil188CppApiDiagnosticUnified` (LIVE since 2026-09-18;
  src/toolboxes/comm/tests/known_bugs_test.cpp) — asserts the eval and
  direct C++ paths answer `mil188qammod(0, 128)` with the one
  identifier `nk:mil188qammod:MNotChoice`
- **Guard:** `DISABLED_FeedbackSignCppPathUnified`
  (src/toolboxes/control/tests/known_bugs_test.cpp) — the open control
  site
- dev-docs/todo/argcheck_separation.md (design, phases, audit gate)
- tools/argcheck_classification.json (backlog; comm's 18 migrated
  2026-09-18)
