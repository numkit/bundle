# core.vm — CALL_METHOD splice arg count wraps at 256 (`o.m(c{:})`, `s.fh(c{:})`)

- **Status:** ✅ FIXED (45bbe77d6)
- **Kind:** bug
- **Severity:** P1 silent wrong result
- **Found:** 2026-09-15, follow-up PVS scan (V1029 residual at `src/core/src/vm.cpp:2521`) after the CSL call-args ABI portion (eadcd8080) — the dot-call chain was missed.

## Symptom

The `CALL_METHOD` opcode flattens runtime CSL splices (`c{:}`) into
`flatBuf`, then stores the count in a `uint8_t`:

```cpp
uint8_t argN = I.e;
...
argN = static_cast<uint8_t>(flatBuf.size());   // wraps at 256
```

Every consumer downstream (`pushCallFrame` classdef path, builtin-class
method `Span`, `execCallIndirectSpan` struct-field-handle path) then sees
the wrapped count. 300 spliced args arrive as 44. Same defect class as the
fixed `f(c{:})` wrap (bugs/closed/core/call-arg-count-uint8-wrap.md), but
in the dot-indexing dispatch.

## Repro

```matlab
clear;
s = struct('fh', @(varargin) nargin);
c = num2cell(1:300);
r = s.fh(c{:});
% nk:     r = 44   (uint8 wrap: 300 & 0xFF)
% MATLAB R2025b (probed 2026-09-15): r = 300
```

Classdef-method variant (needs `C.m` on path — `classdef C / methods /
function r = m(obj, varargin) / r = nargin; end`):

```matlab
clear;
o = C();
c = num2cell(1:300);
r = o.m(c{:});
% nk:     r = 45   (obj + 44 wrapped args)
% MATLAB R2025b (probed): r = 301
```

Small splices (≤255) are correct, which makes the wrap easy to miss.

## Root cause

`case OpCode::CALL_METHOD:` in the VM dispatch flattens into a local
`std::vector<Value> flatBuf` but keeps the count in `uint8_t argN`
(vm.cpp ~2521), unlike the main call chains which were widened to
`size_t` in eadcd8080.

## Suggested fix

Widen the chain to `size_t` like the fixed ABI: `size_t argN = I.e;`,
drop the cast (or flatten via the same zero-copy pure-splice fast path
`na==1 && R[argBase].isCsl()` used by CALL/CALL_INDIRECT_FLATTEN), and
pass `flatBuf.size()` as `size_t` into `pushCallFrame` /
`execCallIndirectSpan` (both already take `size_t`).

## References

- **Guard:** `DISABLED_CallMethodSpliceArgCountNoWrap`
  (src/core/tests/vm_test.cpp)
- Sibling (fixed): bugs/closed/core/call-arg-count-uint8-wrap.md
- PVS: V1029 vm.cpp:2521 (residual after the core-fix portion)
