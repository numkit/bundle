# lang.mfilename — mfilename inside a function m-file returns the calling script's file, not the function's

- **Status:** ✅ FIXED (2026-09-17 — per-function origin frames)
- **Kind:** stub
- **Severity:** P3 (script-level mfilename works; only the in-function form diverges)
- **Found:** 2026-09-16 while implementing mfilename (parity gap surfaced by the MATLAB probes).

## Symptom

mfilename() reads the engine's script-origin stack, which only `run()`,
the REPL and the IDE push. A FUNCTION m-file executed by name (resolved
via the m-file resolver) does not push its own origin, so a mfilename()
call inside it observes the CALLING script's file (or '' at top level).

## Repro

`mf_fn.m` on path (`function out = mf_fn() / out = mfilename; / end`):

```matlab
clear;
addpath('<dir with mf_fn.m>');
r = mf_fn();
% nk (fixed):     r = 'mf_fn'
% MATLAB R2025b (probed 2026-09-16): r = 'mf_fn'
```

## Root cause

UserFunction carried no source-file info, and neither the VM frame
lifecycle nor TreeWalker::callUserFunction pushes an origin around a
m-file function body.

## Fix (landed 2026-09-17)

Provenance plumbed end to end and the origin push made unwind-safe:

- `UserFunction::{sourceFs,sourceDir,sourceFile}` +
  `BytecodeChunk::{originFs,originDir,originFile}`, stamped by the
  m-file resolver for the primary function AND its subfunctions
  (`Compiler::setChunkOrigin` for the compiled chunk).
- VM: `CallFrame::originDepth` (stack depth at entry); entering a chunk
  with a non-empty `originFile` pushes its origin; EVERY frame-removal
  path (`popCallFrame`, `dispatchTryCatch` unwind, `ExecuteGuard`,
  `restorePausedState`, `startExecution`, `resumeExecution` error-pause)
  truncates back to that depth — no exit path can leak an entry.
- TreeWalker: `FsContext::OriginFrame` RAII guard around the body in
  `callUserFunction` / `callUserFunctionMulti`.
- Side effect (intended): sibling .m lookup inside a function body now
  sees the function's own directory first (consistent with the
  script-dir sibling design); `resolvePath`'s implicit FS during the
  body is the function file's FS.

## References

- **Guard:** `MFilenameInsideFunctionFile` + 6 more mfilename tests
  (`MFilenameInsideFunctionFullpath`, `...CalledFromScript`,
  `...SubfunctionReportsFileName`, `NestedFunctionOriginsRestore`,
  `FunctionOriginPoppedOnError`, `MFilenameInCatchAfterCalleeError`)
  in src/core/tests/mfile_resolver_test.cpp, dual-engine (TW/VM).
- Script-level behavior (working): `MFilenameInRunScript`,
  `MFilenameFullpathAndNoFile` in the same file.
- Design notes: dev-docs/memory/script_origin_stack.md.
