# linalg — complex inputs rejected by real-only kernels

- **Status:** ✅ FIXED (2026-10-17)
- **Kind:** stub
- **Namespace:** linalg
- **Found:** 2026-09-18, argcheck remainder portion (probe batteries vs
  MATLAB R2025b)

## What diverges

The reference engine computes these entries for complex input; nk's
kernels consume real buffers only, so the entries reject complex input
with a dedicated stub identifier (or the historical v1 id):

| Entry | nk identifier | note |
|---|---|---|
| expm | `nk:expm:complexUnsupported` | Padé scaling-and-squaring kernel is real-only |
| condest | `nk:condest:complexUnsupported` | 1-norm estimator consumes a real buffer |
| condeig | `nk:condeig:complexUnsupported` | eigenvector-based estimator is real-only |
| rcond | `nk:rcond:NoComplex` | v1 stub id (pre-existing) |
| rref | `nk:rref:NoComplex` | v1 stub id (pre-existing) |
| ldl | `nk:ldl:NoComplex` | complex Hermitian variant missing |
| balance | `nk:balance:NoComplex` | v1 stub id (pre-existing) |

Fixed in the same portion (complex routes mounted/unlocked):
schur, hess, eigs (values + VD), sqrtm, logm, sylvester, ordeig,
gsvd, qz, page solve family.

## Repro

```matlab
clear;
e = expm(complex([2 1; 1 3], 1));
% MATLAB R2025b: [-5.84268292+10.30999422i -9.425053187+15.72526185i; ...
% nk: nk:expm:complexUnsupported (kernel gap, honest stub)
```

## Fix direction

Complex kernel work per entry: Padé on complex buffers (expm), complex
1-norm + solve reuse (condest/rcond), complex eigenvectors (condeig),
complex Gauss-Jordan (rref), complex LDLᵀ / balance. Not a diagnostic
change — do not flip the stubs until the kernels land.

## References

- **Guard:** DISABLED_ExpmComplexKernel, DISABLED_CondestComplexKernel,
  DISABLED_CondeigComplexKernel
  (src/toolboxes/linalg/tests/known_bugs_test.cpp) — assert the
  reference-correct complex results; the live `RemainderComplexStubs`
  suite in type_contract_test.cpp pins the current stub identifiers.
