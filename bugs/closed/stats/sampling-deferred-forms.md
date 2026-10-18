# sampling deferred forms: draw-value parity (randi/randperm cascades), wswor algorithm, lhsnorm construction

- **Kind:** stub
- **Status:** ✅ FIXED (`6525be9`)
- **Component:** stats (randsample / datasample / lhsnorm)
- **Found:** 2026-09-19, stats argcheck campaign sampling portion
  (probe75; contracts landed as randsample_full / datasample_full in
  resample.cpp and the lhsnorm smooth plumbing in sampling/lhs.cpp).

## Deferred branches

1. **Draw-value parity** — randsample/datasample draws run on nk's
   MatlabMT19937 stream but through std::uniform_int_distribution /
   std::shuffle, which consume the stream differently from the
   reference's randi / randperm. Forms, classes, shapes and
   RNG-invariant quantities (permutation sums, positive-weight
   confinement) are parity-pinned; the exact draw sequences are not.
2. **Weighted sampling without replacement (datasample)** — nk's
   kernel uses rejection sampling where the reference uses
   internal.stats.wswor; distributionally equivalent, sequences differ.
   (randsample REFUSES weights without replacement — parity error,
   implemented.)
3. **lhsnorm construction** — nk builds a plain LHS design and maps it
   through the Cholesky factor (the reference ranks an mvnrnd sample);
   both are Latin-hypercube stratified with the target marginals, the
   exact draws differ. The DOSMOOTH on/off contract (any non-'on'
   value takes the off branch — the reference never validates it,
   probe75 L01) is implemented.

**Guard:** deferred (RNG-sequence approximations; every rejection
class and shape is probed-parity — see
tools/parity/specs/sampling_forms.json and
src/toolboxes/stats/tests/sampling_contract_test.cpp).
