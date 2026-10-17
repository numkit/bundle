# stats.nanstdev — reference-absent extension (R2025b does not ship it)

- **Status:** 🔴 OPEN (user decision)
- **Severity:** P3
- **Kind:** cleanup
- **Found:** 2026-09-19, stats argcheck campaign final sweep
  (memory: stats_arity_probe_method; runbook decision).

## Situation

`nanstdev` is NOT part of MATLAB R2025b (the reference engine) — the
modern spelling is `std(x, 'omitnan')`, which nk implements. nk ships
`nanstdev` as an extension.

## Options (user decision at review)

1. **REMOVE** (full_fidelity reading: ship exactly the reference
   surface) — delete the function + reg + tests, note in the ledger.
2. **KEEP** as a documented nk extension (current state) — it is
   tested and harmless, but it is acceptance the reference does not
   have.

The argcheck campaign's classification entry for nanstdev is closed
either way: its value contract (normFlag/dim) already lives in
compute with the shared std machinery.

**Guard:** deferred (no wrong values; a surface-area decision).
