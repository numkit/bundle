# lang — array-creation size-arg errors diverge from MATLAB (text + identifier)

- **Status:** ✅ FIXED (2026-09-16 — `nk::argcheck` portion)
- **Severity:** P2 (silent wrong messages/IDs; complex size inputs leak a
  raw converter message)
- **Kind:** bug
- **Found:** 2026-09-16 (MATLAB R2025b probe while designing
  `nk::argcheck` — dev-docs/todo/argcheck_separation.md)

## Symptom

The shared size-arg validation for the array-creation family
(`zeros`/`ones`/`eye`/`true`/`false`/`inf`/`nan`/`rand`/`randn`/`randi`/
`strings`) — `toDim()` in `src/ops/include/nk/ops/helpers.hpp` — matched
MATLAB's *branching* (frac→error, negative→empty, huge→error) but every
error text/identifier diverged, and Inf/NaN had no branch of their own:

```matlab
clear;
zeros(inf)        % nk:   id=nk:error  "Size inputs must be integers."
                  % MATLAB: id=MATLAB:nonaninf  "NaN and Inf not allowed."
zeros(1e30)       % nk:   id=nk:error  "Requested array size is too large."
                  % MATLAB: id=MATLAB:pmaxsize  "Requested array exceeds the maximum possible variable size."
zeros([2 3], 4)   % nk:   id=nk:error  "Cannot convert double to scalar"   (raw toScalar leak)
                  % MATLAB: id=MATLAB:NonScalarInput  "Size inputs must be scalar."
zeros(2+3i)       % nk:   id=nk:error  "Cannot convert complex with nonzero imaginary part to double scalar"
                  % MATLAB: id=MATLAB:obsoleteComplexInput  "Size inputs must be real."
```

(`zeros(2.5)` text matched, but the identifier MATLAB:NonIntegerInput was
never attached.)

## Root cause

`toDim(double)` threw bare `std::runtime_error` (no `nk::Error`, no
identifier, no function name) and folded Inf/NaN into the non-integer
branch; `parseDimsArgs*` called raw `Value::toScalar()` before any
type/shape check, so non-scalar and complex size inputs leaked the
converter's message instead of MATLAB's size-input diagnostics.

## Fix

New engine-free primitives `nk::argcheck` (`src/value/include/nk/value/
argcheck.hpp`), texts/IDs probed against R2025b (probe table in the
header): `arrayDim(const Value&, fn)` does scalar→real→numeric checks
with NonScalarInput / obsoleteComplexInput / nonaninf /
NonIntegerInput / pmaxsize; `toDim` is deleted and
`parseDimsArgs`/`parseDimsArgsND` take an `fn` name for error
attribution.


**Re-voiced 2026-09-17** (user rule, later same day): the shipped strings are nk-voiced — `nk:<fn>:<tag>` identifiers and richer messages with got-clauses; the probed reference diagnostics above remain the rejection-behavior contract (same inputs fail, same argument blamed).

## Guard

Live gtest `CreationDimsErrorParity` (src/builtin/tests/argcheck_test.cpp)
asserts identifier + text for all four branches through the engine.

**Residual edge:** a complex element *inside* a size vector
(`zeros([2 3+4i])`) was left to a follow-up — fixed the next day in
`bugs/closed/lang/creation-dims-vector-form.md` (realness guard +
type-aware element reads in the vector branches).
