# core.compiler — function definitions needing >255 registers die loudly instead of falling back to TreeWalker

- **Status:** ✅ FIXED (c9f05538d, 2026-09-15)
- **Kind:** bug
- **Severity:** P3 (a function with >255 named parameters is pathological in real code, but MATLAB runs it and nk errors)
- **Found:** 2026-09-15, follow-up probe while closing call-arg-count-uint8-wrap.md
- **Found-By:** manual probe (MATLAB R2025b cross-check)

## Symptom

A function whose declared named parameters alone exceed the VM's
255-register chunk ceiling fails script load with
"Compiler: register exhaustion" reaching the user. The documented
dual-engine contract (bugs/closed/core/register-exhaustion-no-fallback)
says oversized chunks execute on the TreeWalker — and it does hold for
top-level scripts and call sites (300 literal call args work via the
fallback), but NOT for function definitions.

## Repro

```
clear;
function s = f(p1, p2, ..., p300)   % 300 named params
  s = p1 + p300;
end
c = num2cell(1:300);
disp(f(c{:}));
% MATLAB R2025b: 301   (probed 2026-09-15)
% nk:            error "Compiler: register exhaustion (>255 registers needed in chunk)"
```

(300 LITERAL args at one call site DO work — the fallback fires there;
only the definition path is missing it.)

## Root cause

Function-def compilation (compileFunction / registerFunction at script
load) let RegisterExhaustionError propagate to the user instead of
registering the function as TreeWalker-only — and the VM's CALL chains
had no dispatch for a user function without a chunk (straight to
"undefined function").

## Fix (2026-09-15)

compileFunctionDef catches CompilerLimitError and registers the function
TW-only (chunk store skipped, UserFunction adopted as usual); resolveMFile_
does the same for .m files loaded from disk. The VM's seven user-function
chains (CALL / CALL_CSL / CALL_MULTI / CALL_MULTI_CSL / indirect single /
indirect multi / indirect flattened multi) dispatch chunk-less functions
inline on the TreeWalker via VM::callTwOnlySingle/Multi and the new public
Engine::callUserFunctionOnTreeWalker[Multi] re-entry points
(TreeWalker::callUserFunction went public for this).

Per-surface policy (deliberate): user script functions and user m-files
fall back to the TreeWalker (MATLAB semantics, any size); builtin
embedded m-source wrappers and classdef methods still fail LOUDLY — they
must run on the VM for callback pausability and debuggability
(registerBuiltinMSource / ensureClassMethodCompiled rethrow
CompilerLimitError). Known degradations of the TW-only path, documented
at the helpers: inputname(k) sees no caller arg names, and the body is
not step-debuggable under a debug observer (it can never run on the VM,
so rethrowing would just break the call).

## Suggested fix

Catch `CompilerLimitError` where script-local functions are
pre-compiled (Engine::beginScript / registerFunction path): register
the UserFunction TW-only (skip the chunk), mirroring the top-level
script fallback. VM-side calls already resolve TW-only functions via
lookupUserFunction + m-file dispatch.

## References

- Guard: `VMTest.FunctionDefManyParamsFallsBack` (src/core/tests/vm_test.cpp) — live
- Contract: bugs/closed/core/register-exhaustion-no-fallback.md
- Sibling (call side, FIXED): bugs/closed/core/call-arg-count-uint8-wrap.md
