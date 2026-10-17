# core.vm — qualified/package calls never flatten CSL (`pkg.fn(c{:})`)

- **Status:** ✅ FIXED (45bbe77d6)
- **Kind:** bug
- **Severity:** P1 — hard error on a legal MATLAB call form
- **Found:** 2026-09-16 while fixing the dot-call splice bugs — same
  family, same probe session.

## Symptom

Plain-name calls gate on "any brace-index arg → CALL_FLATTEN"
(compiler.cpp ~3495), but the qualified-name branch (`pkg.fn(x)`,
`pkg.sub.fn(x)`) always emits plain `CALL` (single output) or
`CALL_MULTI` (multi output) with COLLAPSEd args, and neither VM chain
flattens. So a runtime splice in a package-qualified call dies.

## Repro

`+qp/qf1.m` (`function n = qf1(varargin) n = nargin; end`) and
`+qp/qf.m` (`function [n,s] = qf(varargin) n = nargin; s =
sum([varargin{:}]); end`) on path:

```matlab
clear;
c = num2cell(1:5);
r = qp.qf1(c{:});
% nk:     error "Too many values: a comma-separated list expanded to
%         5 values where 1 is required"
% MATLAB R2025b (probed 2026-09-16): r = 5
[n, s] = qp.qf(c{:});
% nk:     same error (CALL_MULTI leg)
% MATLAB R2025b (probed): n = 5, s = 15
```

## Root cause

compiler.cpp ~3127 (qualified single-output branch): no anyBraceArg
gate — always plain CALL. compiler.cpp ~984 (qualified multi-output):
`compileArgsBlock` with plain `compileNode`. VM `CALL`/`CALL_MULTI`
chains take raw registers with no splat (by design for CALL — the fix
is to route brace-arg calls to CALL_FLATTEN; CALL_MULTI needs the
splat).

## Suggested fix

Single output: add the same anyBraceArg gate as plain names → emit
CALL_FLATTEN with the qualified name (identical full dispatch). Multi
output: expand-compile brace args + splat in the VM CALL_MULTI chain
via the shared `splatCallArgs` helper.

## References

- **Guard:** `DISABLED_QualifiedCallSpliceSplat` (src/core/tests/vm_test.cpp)
- Siblings (same probe session):
  bugs/opened/core/call-method-splice-arg-count-uint8-wrap.md,
  bugs/opened/core/call-method-multi-no-csl-splat.md,
  bugs/opened/core/super-call-no-csl-splat.md
