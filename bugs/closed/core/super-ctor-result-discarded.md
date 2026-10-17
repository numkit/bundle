# core.classdef — statement-position super-ctor discards its result (`obj@B(7)` never mutates obj)

- **Status:** ✅ FIXED (02b24c563)
- **Kind:** bug
- **Severity:** P1 — inheritance correctness: base-ctor initialization is silently lost
- **Found:** 2026-09-16 while testing the super-call splice fix
  (bugs/opened/core/super-call-no-csl-splat.md): the spliced args DO
  reach the base ctor, but whatever the base ctor assigns never lands
  on the derived instance — and the same loss reproduces WITHOUT any
  splice, so it is an independent, older defect.

## Symptom

`obj@Base(args)` as a ctor statement compiles to CALL_SUPER_CTOR with
`dst = tempReg()` (statement position, `explicitOutBase = -1`) —
`R[dst] = superConstruct(...)` writes a throwaway temp; the derived
`obj` register is never updated, so properties assigned by the base
constructor read back empty.

## Repro

`B.m` (`classdef B / properties nargs / methods / function obj =
B(varargin) obj.nargs = nargin; end / ... end`) and `D4.m`
(`classdef D4 < B / methods / function obj = D4() obj@B(7); end /
end`) on path:

```matlab
clear;
d4 = D4();
d4.nargs
% nk:     []   (empty — the base ctor's assignment is discarded)
% MATLAB R2025b (probed 2026-09-16): 1   (nargin of B(7) — one argument)
```

## Root cause (suspected)

`Compiler::compileSuperCall` ctor leg: `uint8_t dst =
(explicitOutBase >= 0) ? ... : tempReg();` — statement-position
super-ctor gets a scratch destination and the result is dropped; or
`Engine::superConstruct` returns a fresh base instance that is never
merged into the derived seed. Needs a write-back to the obj register
(or an in-place merge in superConstruct).

## Suggested fix

For a statement-position ctor super-call, pass the LHS obj register as
the destination so `R[objReg] = superConstruct(...)` updates the
instance being constructed; add a classdef inheritance test asserting
base-assigned properties survive derived construction.

## References

- **Guard:** `DISABLED_SuperCtorResultDiscarded`
  (src/core/tests/vm_test.cpp)
- Discovered via: bugs/opened/core/super-call-no-csl-splat.md (its
  splice verification had to route around this defect)
