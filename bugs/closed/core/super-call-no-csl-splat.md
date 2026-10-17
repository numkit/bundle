# core.vm — superclass calls never flatten CSL (`obj@Base(c{:})`, `m@Base(obj, c{:})`)

- **Status:** ✅ FIXED (45bbe77d6)
- **Kind:** bug
- **Severity:** P1 — hard error on a legal MATLAB call form
- **Found:** 2026-09-16 while fixing the dot-call splice bugs
  (bugs/opened/core/call-method-splice-arg-count-uint8-wrap.md) — same
  family, same probe session.

## Symptom

`compileSuperCall` compiles super-call args with plain `compileNode`,
which appends COLLAPSE to every brace-index arg — the runtime splice
`c{:}` is collapsed (thrown for n≠1) before the VM ever sees it. The VM
chains `CALL_SUPER_CTOR` / `CALL_SUPER_METHOD` also take the raw
registers with no flatten step.

## Repro

`B.m` / `D.m` on path (B: `properties nargs`, ctor `obj = B(varargin)
obj.nargs = nargin;`, method `r = bsum(obj, varargin) r = sum([varargin{:}]);`;
D < B: ctor `obj = D(c) obj@B(c{:});`, override
`r = bsum(obj, varargin) r = 100 + bsum@B(obj, varargin{:});`):

```matlab
clear;
c = num2cell(1:5);
dd = D(c);
dd.nargs
% nk:     error "Too many values: a comma-separated list expanded to
%         5 values where 1 is required"
% MATLAB R2025b (probed 2026-09-16): ans = 5
bsum(dd, c{:})
% nk:     same error (super-method leg)
% MATLAB R2025b (probed): ans = 115   (100 + sum(1..5) via bsum@B)
```

## Root cause

`Compiler::compileSuperCall` (compiler.cpp ~3897): plain `compileNode`
per arg (COLLAPSE on brace-index). VM `CALL_SUPER_CTOR`/`CALL_SUPER_METHOD`
pass `Span(&R[argBase], nargs)` with no splat.

## Suggested fix

Mirror the CALL_METHOD treatment: expand-compile brace args
(mAnyBrace → `compileNodeExpand`), splat in the VM via the shared
`splatCallArgs` helper (size_t count, zero-copy pure splice).

## References

- **Guard:** `DISABLED_SuperCallSpliceSplat` (src/core/tests/vm_test.cpp)
- Siblings (same probe session):
  bugs/opened/core/call-method-splice-arg-count-uint8-wrap.md,
  bugs/opened/core/call-method-multi-no-csl-splat.md,
  bugs/opened/core/qualified-call-no-csl-splat.md
