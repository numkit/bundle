# linalg factorizations reject single inputs (reference computes them)

- **Kind:** stub
- **Namespace:** linalg
- **Functions:** svd, pinv, orth, null, rank, subspace, norm, eig, pagesvd,
  pagesvd (decompose form), pagepinv, pagenorm, pageinv, pageeig, det, inv,
  cond, normest, condest, condeig, expm, sqrtm, logm, funm; remainder
  portion 2026-09-18 added: chol, lu, qr, trace, rcond, hess, schur,
  ldl, gsvd, ordschur, qz, balance, rref, linsolve, lsqminnorm,
  sylvester, expmv, eigs, svds, ordeig, cholupdate,
  pagemldivide/pagemrdivide/pagelsqminnorm
- **Status:** ✅ FIXED (2026-10-17) — single-precision inputs accepted across all linalg factorizations, solvers, matrix functions, norms, and page operations, returning single-class outputs matching MATLAB R2025b.
- **Reference:** MATLAB R2025b (probed 2026-09-18)
- **Found:** 2026-09-18, argcheck structural portion (linalg); list
  extended by the remainder portion same day

## What diverges

The reference engine **accepts single-precision inputs across the whole
linalg factorization/norm family** and answers in single class:

```
clear;
s = pinv(single([1 2; 3 4]));   % MATLAB: 2x2 single, values ≈ double path
d = det(single([1 2; 3 4]));    % MATLAB: -1.99999988079071 (single)
n = norm(single([3 4]));        % MATLAB: 5 (single)
```

nk computes the family on double/complex-double buffers only, so single
inputs are rejected at the shared argcheck with a dedicated identifier
(`nk:<fn>:singleUnsupported`, message suggests `double()`), or — for
entries not yet migrated — leak the raw buffer error. `vecnorm` and the
matrix predicates (`istril`, `isbanded`, …) DO coerce single via
`elemAsDouble`: accepted, but `vecnorm(single(...))` answers in double
class where the reference answers single (result-class gap, values equal).
The remainder portion (2026-09-18) added three more coercing entries
with the same double-class gap: `trace(single(A))`, `normest(single(A))`
and `A \ B` / `A / B` with single operands (values match R2025b, class
is double). `funm(single(A))` is accepted-and-computed by its embedded
m-source via `eig`, so it voices `nk:eig:singleUnsupported` (transitive
identifier — acceptable per the route rule).

Rejection classes for everything EXCEPT single are parity-correct
(reference rejects logical / integer classes / char / string / cell for
the factorization family — probed, guarded in
`src/toolboxes/linalg/tests/type_contract_test.cpp`).

## Fix direction

Route single through the kernels: either compute in single throughout
(matching the reference's result class), or coerce to double at the
kernel boundary and document the double-class answers. The dedicated
`singleUnsupported` identifiers make every rejection site greppable.

**Guard:** `DISABLED_PinvSingleAccepted` in
`src/toolboxes/linalg/tests/known_bugs_test.cpp` (asserts the
reference-correct behaviour: `pinv(single(...))` returns a value).

## Repro

```
clear;
y = pinv(single([1 2; 3 4]));
% MATLAB: y = 2x2 single (-2.0000 1.0000; 1.5000 -0.5000)
% nk:     nk:pinv:singleUnsupported "single inputs are not supported yet"
```
