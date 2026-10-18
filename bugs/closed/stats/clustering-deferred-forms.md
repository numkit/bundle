# clustering deferred forms: pdist2 Smallest/Largest acceptance divergence

- **Status:** ✅ FIXED (2026-10-18 — `pdist2_full` requires the positional
  `Distance` argument before `'Smallest'`/`'Largest'`, so `pdist2(X, Y, 'Smallest', K)`
  rejects with `numkit:pdist2:unrecognizedDistance` per probe P09 while
  `pdist2(X, Y, Distance, 'Smallest', K)` computes top-k distances)
- **Kind:** cleanup
- **Component:** stats (pdist2)
- **Found:** 2026-09-19, stats argcheck campaign clustering portion
  (probe77 P09; contracts landed as the *_full entries in
  cluster/cluster_full.cpp — pdist / pdist2 / linkage / cluster /
  inconsistent / silhouette; mahal was already marshal-only).

## Resolution

In the reference engine, `'Smallest'` and `'Largest'` are name-value
options accepted AFTER the 3rd positional `Distance` argument
(`[D,I] = pdist2(X, Y, Distance, 'Smallest', K)`). Passing `'Smallest'`
as the 3rd argument (`pdist2(X, Y, 'Smallest', K)`, probe P09) puts it
in the `Distance` slot and rejects with `UnrecognizedDistance`.
`pdist2_full` now checks `'Smallest'`/`'Largest'` only at `tail` index
`>= 1`, matching both `[D,I] = pdist2(X, Y, 'euclidean', 'Smallest', K)`
and the P09 rejection of `pdist2(X, Y, 'Smallest', K)`.

**Guard:** `ClusterContractTest.Pdist2MahalFormsAndGates` (`modules/stats/tests/cluster_contract_test.cpp`).
