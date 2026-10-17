# corrcoef deferred branches: complex R, pairwise p-values, 1-obs p-values

- **Kind:** stub
- **Component:** stats (corrcoef)
- **Found:** 2026-09-18, stats descriptive argcheck portion (probe68).

## Deferred branches (all probed R2025b, all reject-or-diverge in nk today)

1. **Complex R**: `r = corrcoef(complex(X, X))` computes in the reference
   (R via |cov|-style complex correlation); nk's kernel routes through the
   cov complex stub (`nk:cov:complex`). The 2-output form correctly
   rejects with the ComplexInputs class already.
2. **`[R, P]` with `'Rows','pairwise'`**: per-pair degrees of freedom —
   currently `nk:corrcoef:PairwisePValue` stub (the R alone computes).
3. **1-observation p-values**: `[r, p] = corrcoef([1 2 NaN])` errors with
   the reference's internal badsubscript; nk returns R/P for the single
   observation.

## Fix direction

1 needs the cov complex kernel (tracked with the stats complex-kernel
stubs); 2 is a per-pair-n Fisher transform in corrcoefPValues; 3 is an
n ≥ 2 guard on the p-value path.

**Guard:** deferred (stubs, not wrong values on computed paths).
