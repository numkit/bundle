# lang.mfilename — mfilename inside a classdef method reports the caller's file, not the class file

- **Status:** ✅ FIXED (2026-09-17 — classdef provenance)
- **Kind:** stub
- **Severity:** P3
- **Found:** 2026-09-17 as a follow-up gap of bugs/closed/lang/mfilename-in-function.md.

## Symptom

Classdef method UserFunctions carried no provenance, so mfilename()
inside a method body observed the caller's origin (a calling script's
file, or '' at top level).

## Repro

`Point.m` on path with `methods` containing
`function s = where(obj) / s = mfilename; / end`:

```matlab
clear;
addpath('<dir with Point.m>');
p = Point();
r = p.where();
% nk (fixed): r = 'Point'
% MATLAB R2025b (probed 2026-09-17): r = 'Point' (ctor, ordinary and
%   Static methods all report the classdef file's base name)
```

## Fix

`registerClassDef` (inline classdefs: captures the executing script's
origin) and the new `registerClassDefFrom` (m-file resolver: takes the
matched file explicitly — resolution can happen while an unrelated
script runs) stamp the provenance onto every method / constructor /
get/set accessor / Static UserFunction. Inherited methods keep their
DECLARING class's file (the inheritance merge reuses the base ufs).
`Compiler::ensureClassMethodCompiled` copies uf → chunk so the VM path
pushes the same origin; the TreeWalker covers ctor/method bodies via
the existing OriginFrame guards (runClassCtor gained its own).

## References

- **Guard:** `MFilenameInClassdefMembers` (ctor tag, instance method,
  Static method) in src/core/tests/mfile_resolver_test.cpp
  (dual-engine TW/VM).
- Design: dev-docs/memory/script_origin_stack.md.
