# linalg remainder: raw `Not a double array` diagnostics for non-double input

- **Kind:** bug
- **Namespace:** linalg
- **Status:** ✅ FIXED (2026-09-18, linalg remainder portion)
- **Reference:** MATLAB R2025b (probed 2026-09-18)
- **Found:** 2026-09-18, argcheck structural portion (linalg)
- **Fixed-By:** this commit — linalg remainder portion, 2026-09-18
  (`git log --grep 'linalg remainder'`)

## Resolution

Every census entry now takes `detail::requireDoubleInput(A, "<fn>")` as
the first statement of its compute entry (chol_reg's local [R,p]
implementation calls the same core at the marshalling site):
`nk:<fn>:inputType` / `nk:<fn>:singleUnsupported` instead of the raw
buffer error. The mldivide/mrdivide matrix path gained
`checkSolveOperandClass` (cell/string/struct → `nk:<op>:inputType`) and
the integer-matrix class (`nk:<op>:integerUnsupported` — the reference's
separate integerLinearAlgebra rejection). Per-entry probe-driven
exceptions: trace coerces numeric+logical to double, normest coerces
logical+char, gsvd coerces logical only, ordschur select accepts any
numeric class. Behaviour fixes landed with the portion: eigs-values on
nonsymmetric matrices, general sqrtm/logm/sylvester mounted (complex
included), ordeig complex branch, complex page solves. Guard
`DetCellDiagnostic` enabled live in
`src/toolboxes/linalg/tests/known_bugs_test.cpp`; full coverage in
`type_contract_test.cpp` (Remainder* suites). Remaining gaps tracked in
`single-float-inputs.md` and `complex-kernel-gaps.md`.


## What diverges

The 2026-09-18 portion wired the shared argcheck cores
(`detail::requireDoubleInput` / `requireFloatOrLogicalInput`,
`linalg_detail.hpp`) into the svd-route, norm, eig, page and predicate
families. The REST of the toolbox still answers a non-double input with
the raw buffer error — identifier `nk:error`, message
`Not a double array`, no function name, no received class:

```
clear;
det({1 2; 3 4});
% MATLAB: MATLAB:math:mustBeFloat "Invalid data type. Argument must be double or single."
% nk:     nk:error "Not a double array"
```

Same shape for every entry in the census below (nk column =
`nk:error / Not a double array` unless noted):

| Entry (cell input) | nk today | reference class |
|---|---|---|
| chol | raw | mustBeFloat |
| lu | raw | (LU family float contract) |
| qr | raw | float contract |
| det | raw | math:mustBeFloat |
| inv | raw | inv:inputType |
| trace | raw | diag:inputType — **coerces** numeric/char/logical (int32 trace returns a value!) |
| rcond | raw | float contract |
| condest | raw | float contract |
| condeig | raw | float contract |
| expm | raw | float contract |
| hess | raw | float contract |
| schur | raw | float contract |
| ldl | raw | float contract |
| gsvd | raw | float contract |
| ordschur | raw | float contract |
| balance | raw | float contract |
| rref | raw | float contract |
| linsolve | raw | float contract |
| expmv | raw | float contract |

Transitively fixed by the portion (route through a migrated entry, so
they now voice the ROUTE's identifier — still worth an own-voice pass
when their portions land): cond/normest (`nk:svd:inputType`),
sqrtm/logm/funm (`nk:eig:inputType`), lsqminnorm (`nk:pinv:inputType`).

## Fix direction

One line per entry: `detail::requireDoubleInput(A, "<fn>")` as the first
statement of the compute function (trace wants the coercing variant —
the reference accepts numeric/char/logical there; probe per entry before
rejecting). Direct-C++ calls then cross the same checks.

**Guard:** `DISABLED_DetCellDiagnostic` in
`src/toolboxes/linalg/tests/known_bugs_test.cpp` (asserts
`det(cell)` throws `nk::Error` with identifier `nk:det:inputType`).

## Repro

```
clear;
e = det({1 2; 3 4});
% MATLAB: error MATLAB:math:mustBeFloat (clean, blames det)
% nk:     nk:error "Not a double array" (raw, no function name)
```
