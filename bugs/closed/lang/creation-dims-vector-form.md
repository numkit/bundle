# lang — size-VECTOR form of the creation family assumes a double array (complex leaks, int8 rejected)

- **Status:** open
- **Severity:** P3 (error-path parity + one rejected legal form)
- **Kind:** bug
- **Found:** 2026-09-17 (self-evaluation probe of the argcheck Phase-1
  landing — the residual edge deliberately deferred in
  bugs/closed/lang/creation-dims-error-parity.md)

## Symptom

The vector form of the shared size parser (`parseDimsArgs` /
`parseDimsArgsND`, `src/ops/include/nk/ops/helpers.hpp`) calls
`doubleData()` unconditionally, so a size vector that is not a plain
double array never reaches `nk::argcheck`:

```matlab
clear;
zeros([2 3+4i])     % nk:   id=nk:error  "Not a double array"  (raw doubleData leak)
                    % MATLAB: id=MATLAB:obsoleteComplexInput  "Size inputs must be real."
zeros(int8([2 3]))  % nk:   id=nk:error  "Not a double array"  (legal form rejected)
                    % MATLAB: OK — 2x3 array
```

## Root cause

Scalar size positions were routed through `argcheck::arrayDim(Value)`
(fixed in the argcheck portion), but the `[m n p ...]` vector form still
reads `args[0].doubleData()` directly — no complex check, no integer-type
support.

## Fix direction

Route vector elements through `argcheck::arrayDim` semantics too: an
`isComplex()` guard first (obsoleteComplexInput), then read elements via
the type-aware accessor so integer-typed size vectors work (MATLAB
accepts them). Probe single/int vector forms while at it.


**Re-voiced 2026-09-17** (user rule, later same day): the shipped strings are nk-voiced — `nk:<fn>:<tag>` identifiers and richer messages with got-clauses; the probed reference diagnostics above remain the rejection-behavior contract (same inputs fail, same argument blamed).

## Guard

`DISABLED_CreationDimsVectorForm` in src/bundle/tests/known_bugs_test.cpp
(asserts the MATLAB-correct diagnostic for complex and the 2x3 result for
int8; fails today, becomes a live guard when fixed).
