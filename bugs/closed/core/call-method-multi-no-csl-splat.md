# core.vm — CALL_METHOD_MULTI never flattens CSL (`[a,b] = o.mm(c{:})` errors)

- **Status:** ✅ FIXED (45bbe77d6)
- **Kind:** bug
- **Severity:** P1 — hard error on a legal MATLAB call form
- **Found:** 2026-09-15 while probing the CALL_METHOD splice wrap
  (bugs/opened/core/call-method-splice-arg-count-uint8-wrap.md) —
  neighbouring chain, opposite failure.

## Symptom

`CALL_METHOD` (single-output `o.m(c{:})`) flattens runtime CSL splices at
the top of the dispatch (per bugs/closed/lang/handle-call-csl-splat),
but `CALL_METHOD_MULTI` (`[a, b] = o.mm(args)`) does not flatten at all:
it packs the raw registers (`R[argBase + k]`) into `frameArgs`, so a
spliced `c{:}` reaches the callee as ONE argument holding the whole CSL.
The binder then rejects it with a "Too many values" error instead of
splatting.

## Repro

`MM.m` on path (classdef MM / methods / `function [r1, r2] = mm(obj,
varargin)` / `r1 = nargin; r2 = class(varargin{end});`):

```matlab
clear;
o = MM();
d = num2cell(1:5);
[a, b] = o.mm(d{:});
% nk:     error "Too many values: a comma-separated list expanded to
%         5 values where 1 is required"
% MATLAB R2025b (probed 2026-09-15): a = 6, b = 'double'
```

Literal args work fine (`[a,b] = o.mm(10,20,30)` → `4 'double'`), so only
the splice form diverges.

## Root cause

`case OpCode::CALL_METHOD_MULTI:` (vm.cpp ~2588) has no CSL-flatten step
before packing `frameArgs` / the builtin-method `Span` — the flatten
block exists only in the single-output CALL_METHOD case.

## Suggested fix

Factor the CALL_METHOD flatten (including the zero-copy pure-splice fast
path) into a helper and run it at the top of CALL_METHOD_MULTI too; count
in `size_t` from the start so the multi chain doesn't inherit the uint8
wrap as well.

## References

- **Guard:** `DISABLED_CallMethodMultiSpliceSplat`
  (src/core/tests/vm_test.cpp)
- Sibling (same probe session):
  bugs/opened/core/call-method-splice-arg-count-uint8-wrap.md
- Splat precedent: bugs/closed/lang/handle-call-csl-splat.md
