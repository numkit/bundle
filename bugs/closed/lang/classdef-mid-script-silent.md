# lang.parser — classdef in the middle of a script is silently accepted (MATLAB rejects)

- **Status:** ✅ FIXED (df4130b0f)
- **Kind:** bug
- **Severity:** P3 — malformed scripts run with confusing downstream behavior instead of a clear parse error
- **Found:** 2026-09-16, bug-hunt battery (an intermediate probe script accidentally embedded a classdef after statements).

## Symptom

A script with statements followed by a `classdef` block runs to
completion with exit 0 — the classdef neither defines a class nor
errors. Worse, subsequent statements' errors get MISLOCATED (observed
"line 7, column 62" on a 30-column line) because the parser consumed
the classdef differently than intended.

## Repro

```matlab
clear;
x = 1;
classdef Foo
end
y = 2;
% nk:     runs silently, exit 0, no class Foo registered
% MATLAB R2025b (probed 2026-09-16):
%   Error: Line 2 Column 1: Illegal use of reserved keyword "classdef".
```

## Root cause

The parser accepts a classdef block as an ordinary statement in a
script/body context; MATLAB only allows classdef as the FIRST
non-comment construct of a file (and never inside a script).

## Suggested fix

Reject `classdef` at parse time when it is not the first non-comment
statement of the compilation unit, with MATLAB's message. Eval strings
that are a single classdef (first statement) keep working — the engine
tests rely on that form.

## References

- **Guard (live):** `ClassdefMidScriptRejected`
  (src/core/tests/parser_test.cpp)
