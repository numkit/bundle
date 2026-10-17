# correlation deferred forms: nearcorr weights/newton, corr rank+weights & pairwise, partialcorr pval & pairwise

- **Kind:** stub
- **Component:** stats (nearcorr / corr / partialcorr)
- **Found:** 2026-09-19, stats argcheck campaign correlation portion
  (probe71{,b} + probe72; contracts landed with corr_full /
  partialcorr_full / nearcorr_full in src/toolboxes/stats/src/
  descriptive/correlation.cpp + nearcorr.cpp).

## Deferred branches (all voiced, never silent)

1. **nearcorr `'Weights'`** — `nk:nearcorr:weightsUnsupported`. The
   reference's diagonal-W / H-form weighting changes the minimizer
   (alternating projections on a weighted norm). Needs the weighted
   projection kernel; the unweighted problem is complete.
2. **nearcorr `'Method','newton'`** — ACCEPTED but runs the alternating
   projections solver (same minimizer, different convergence route —
   deliberate divergence, documented in nearcorr.cpp). A true semismooth
   Newton iteration would converge in fewer iterations.
3. **nearcorr scalar single NV values** — the reference rejects
   `nearcorr(A, 'Tolerance', single(1e-6))` (validateattributes demands
   double); nk's engine marshalling promotes scalar single → double
   BEFORE the gate sees it, so the class is invisible (the array form
   `single([1e-6])` IS rejected). Engine-level promotion, not a
   nearcorr-layer decision.
4. **corr Weights + Kendall/Spearman** — `nk:corr:weightsRankUnsupported`.
   The reference's corrSpearman/corrKendall support weights; nk's rank
   kernels are unweighted.
5. **corr `'Rows','pairwise'` + rank types** — `nk:corr:PairwiseType`
   (pre-existing tag). The reference re-ranks per column pair on the
   non-NaN subset; nk's pairwise kernel is Pearson-only.
6. **corr complex + pairwise** — `nk:corr:complexPairwiseUnsupported`
   (all/complete compute complex rho fine).
7. **corr single-precision arithmetic** — single inputs compute in
   double and cast down (`asComputeDouble`); the reference runs the
   kernel in single, diverging by O(1e-7) in the last digits
   (parity spec guards these fingerprints with a 1e-6 closeness check).
8. **partialcorr 2nd output (p-values)** — missing-output: the reference
   returns [rho, pval] with df = n − rank(Z) − 2 and Tail-dependent
   one/two-sided forms; nk emits rho only. `'Tail'` parses and is inert
   until pval exists.
9. **partialcorr `'Rows','pairwise'` for (X, Z) / (X, Y, Z)** —
   `nk:partialcorr:pairwiseUnsupported`. The combinedXZ form
   (partialcorr(X)) treats pairwise == complete (reference parity,
   probe71b P15) and computes; the per-pair loop with varying dz is not
   implemented.

## Fix direction

1 needs weighted PSD projections; 2 is an optimization only; 3 is an
engine marshalling question (scalar class preservation); 4-5 need
weighted/per-pair rank kernels; 8 needs rank(Z) + the t-tail block;
9 is the per-pair residualisation loop with per-pair ranks.

**Guard:** deferred (voiced stubs on every listed path; no silently
wrong values — the computed paths are parity-pinned in
tools/parity/specs/correlation_forms.json).
