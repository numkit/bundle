# lang.mfilename — mfilename inside an anonymous function: caller's origin instead of the creating file

- **Status:** ✅ FIXED (2026-09-17 — capture-at-creation provenance)
- **Kind:** stub
- **Severity:** P3
- **Found:** 2026-09-17 as a follow-up gap of bugs/closed/lang/mfilename-in-function.md.

## Symptom

Anonymous functions carried no provenance, so mfilename() inside the
body observed whatever origin was active AT CALL TIME: a handle created
in script A and called from script B reported B (or '' at top level).

## Repro

`anon_host.m` (`h = @() mfilename;`), then at top level:

```matlab
clear;
addpath('<dir with anon_host.m>');
run('<dir>/anon_host.m');
r = h();
% nk (fixed): r = 'anon_host'
% MATLAB R2025b (probed 2026-09-17): r = 'anon_host'  (creation context
%   wins over call context; a command-window-born handle keeps '' even
%   when called from a script)
```

## Fix

Provenance captured at CREATION (`Engine::captureScriptOrigin`): TW
`execAnonFunc` at runtime; VM `compileAnonFunc` at compile time under
`Compiler::AnonOriginSentry` (the resolver passes the function file into
`registerFunctionAs` because it compiles before the origin frame is
active). `originKnown` + empty fields = "born with no executing file" →
an all-empty origin entry MASKS the caller's file ('' like the
reference's command window).

## References

- **Guard:** `MFilenameInAnonymousFromScript`,
  `MFilenameInAnonymousCreatedInFunction`,
  `MFilenameInAnonymousFromTopLevelMasksCaller` in
  src/core/tests/mfile_resolver_test.cpp (dual-engine TW/VM).
- Design: dev-docs/memory/script_origin_stack.md.
