# linalg.funm — defective-matrix branch answers 0 instead of the matrix function

- **Status:** 🟡 OPEN
- **Severity:** P2 (silently wrong numeric result)
- **Kind:** bug
- **Namespace:** linalg
- **Found:** 2026-09-18, linalg remainder portion (funm parity spec
  MISMATCH; stash-verified pre-existing — unchanged by the portion)

## Repro

```matlab
clear;
B = [2 1; 0 2];               % defective: repeated eigenvalue 2
F = funm(B, @exp);
% MATLAB R2025b: F = [7.389056099 7.389056099; 0 7.389056099]  (== expm(B))
% nk:            F = [7.389056099 0; 0 7.389056099]  — F(1,2) is 0
```

## Notes

The registered funm is the embedded m-source
(`kFunmMSource` in `src/bundle/src/register/linalg/linalg_library.cpp`)
which builds F = V·diag(fun(D))·V⁻¹ from `[V, D] = eig(A)`. For a
defective matrix V is singular and the reconstruction degenerates
(here: an off-diagonal 0 instead of e²). The Schur–Parlett kernel that
handles confluent/defective matrices EXISTS as the C++ `funm_eval`
(`src/toolboxes/linalg/src/matrix_functions.cpp`,
funm_parlett_test.cpp is green) but is not mounted behind the builtin —
the m-source took over the registration and the parity spec's
defective-matrix fingerprint (Fb/err_b rows) regressed. Diagonalizable
inputs (@exp/@sin/@cos on [1 2; 3 4], symmetric matrices) still match.

## Fix direction

Route the builtin to the Schur–Parlett compute: an adapter marshalling
function handles (`@exp` → the named-overload fast paths; anonymous
handles need the FnHandle callback pattern from library_api.md §7) —
then the m-source fallback can go.

## References

- **Guard:** `DISABLED_FunmDefectiveBranch` in
  `src/toolboxes/linalg/tests/known_bugs_test.cpp`.
