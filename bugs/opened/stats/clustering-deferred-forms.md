# clustering deferred forms: pdist2 Smallest/Largest acceptance divergence

- **Kind:** cleanup
- **Component:** stats (pdist2)
- **Found:** 2026-09-19, stats argcheck campaign clustering portion
  (probe77 P09; contracts landed as the *_full entries in
  cluster/cluster_full.cpp — pdist / pdist2 / linkage / cluster /
  inconsistent / silhouette; mahal was already marshal-only).

## Divergence

The reference REMOVED the `'Smallest'`/`'Largest'` top-k options from
pdist2 (R2025b rejects them with UnrecognizedDistance, probed P09).
nk keeps the feature (the pdist2_topk kernel and its tests predate
this campaign and pin its behavior). This is an ACCEPTANCE
divergence: nk computes where the reference errors.

## Options (user decision at review)

1. Keep the extension (current state — the option is documented and
   tested; the parity spec excludes it).
2. Remove the extension for strict parity (delete pdist2_topk + the
   two gtests).

Everything else in the family is parity-pinned: metric/method/
criterion name tables (validatestring prefix semantics, canonicalized
before dispatch), the probed rejection classes
(DistanceFunctionNotFound / UnrecognizedDistance / the linkage METHOD
and cluster Criterion value-list classes), the 1×0 single-row pdist
empty, single contagion, and the cluster/clusterdata/silhouette
values (cluster labels asserted structurally — they are arbitrary
between engines).

**Guard:** deferred (an acceptance divergence, not a wrong value).
