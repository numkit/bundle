# runtime.mldivide — exactly singular square solve must WARN and return Inf, not throw

- **Status:** 🟡 OPEN
- **Severity:** P2 (user code relying on warn-and-continue breaks)
- **Kind:** bug
- **Namespace:** runtime (binary_ops matrixSolve path)
- **Found:** 2026-09-18, linalg remainder type-contract probes

## Repro

```matlab
clear;
x = true(2) \ eye(2);
% MATLAB R2025b: Warning: Matrix is singular to working precision.
%                x = [Inf -Inf; -Inf Inf]
% nk:            throws nk:mldivide:singular
y = eye(2) / true(2);
% MATLAB R2025b: same warning + Inf-filled y
% nk:            throws nk:mldivide:singular (via the transpose identity)
```

## Notes

The reference distinguishes "singular to working precision" (warn +
Inf-filled result, la_solve's NaN/Inf propagation) from hard rank
failures. nk's matrixSolve throws on any la_solve failure. The fix
needs the LAPACK-style distinction: near-zero pivots → warn + Inf
result; genuinely inconsistent systems still error.

## References

- **Guard:** `DISABLED_MldivideSingularWarns` in
  `src/bundle/tests/known_bugs_test.cpp`.
