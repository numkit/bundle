# core.vm — call argument count wraps at 256 for runtime-spliced lists (f(c{:}))

- **Status:** ✅ FIXED (eadcd8080, 2026-09-15)
- **Kind:** bug
- **Severity:** P2 (silent wrong result on legal MATLAB code; needs a >255-element splice)
- **Found:** 2026-09-15, PVS audit follow-up (V1029 8-bit family, `src/core/src/vm.cpp:2202` etc.)
- **Found-By:** PVS-Studio (V1029, CWE-190)

## Symptom

The VM's call convention carries the argument count in a `uint8_t`
(`NF`/`pushCallFrame`). Direct call sites are register-bounded (255 max,
guarded by `RegisterExhaustionError`), but the **runtime comma-list
splice** path flattens `c{:}` into a `std::vector` with no bound — so a
cell with >255 elements wraps the count silently and the callee sees a
wrong `nargin` (and wrong argument tail).

## Repro

```
clear;
function r = f(varargin)
  r = nargin;
end
c = num2cell(1:300);
disp(f(c{:}));
% MATLAB R2025b: 300   (probed 2026-09-15; a 256-cell also gives 256)
% nk:            44    (= 300 - 256, the uint8_t wrap)
```

## Root cause

`src/core/src/vm.cpp:2202` and `:2419` (named/indirect call flattening)
and `:2670` (indirect span): `NF = static_cast<uint8_t>(flatArgs.size())`
with no check. Cousins on the compile side: `compiler.cpp:3892`
(register-bounded, unreachable — 255-register ceiling fires first) and
`compiler.cpp:4085/4086` (`numParams`/`numReturns` from the parser — a
function DECLARED with >255 params would wrap; pathological but cheap to
guard the same way).

## Suggested fix

Two tiers:

1. **Minimal (stop the silent corruption):** throw a loud runtime error
   at the three flattening sites when `flatArgs.size() > 255` (and a
   compile-time error for >255 declared params/returns) — the
   register-exhaustion contract.
2. **Full (right fix):** the splice is ALREADY a first-class CSL value
   (`ValueType::CSL`, one register, see dev-docs/memory/csl_first_class.md)
   — the bug is purely the `uint8_t` count at the call ABI. Keep spliced
   tails as ONE CSL value in the call frame and expand only where the
   parts are consumed (nargin/varargin indexing); named params stay in
   registers (≤255 by function-schema construction). This preserves
   MATLAB semantics for any count and removes the flatArgs copy.

## References

- Guard: `VMTest.CallSpliceArgCountNoWrap` + `CallSpliceMixedPositions` / `CallSpliceVararginTailSizes` / `CallSpliceIndirectHandle` / `CallTooManyArgumentsStillThrows` (src/core/tests/vm_test.cpp) — live
- Prior art in the same operand-space family: bugs/closed/core/compiler-int16-pool-overflow.md
- PVS report: [bugs/pvs/modules/core.md](../../pvs/modules/core.md) (V1029, prod)
