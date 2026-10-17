# stats.splines — pp-struct coefs layout diverges from the reference (pieces-major rows vs dim-major rows)

- **Status:** 🔴 OPEN
- **Severity:** P2 (cross-engine data-model divergence for every pp consumer)
- **Kind:** bug
- **Found:** 2026-09-19, stats argcheck campaign splines portion
  (probe78 S01-S17; MATLAB R2025b curvefit/splines).

## Symptom

nk's `ppmak(breaks, coefs[, d])` stores `coefs` as a **(d·L) × K**
matrix (rows = dim·pieces, columns = order), while the reference
stores **L × (k·d)** (rows = pieces, columns = order·dim). The two
layouts are transposes of each other for k = 1 and cannot both
satisfy the same input contract:

```matlab
clear;
br = 0:4; co = [1 0.5 0.2 1; -1 2 0 0.5];
% MATLAB R2025b (probe78 S01): pieces=4, order=1, dim=2 and
%   fnval(ppmak(br, co), 2.5) = [0.2; 0]   (piece 3 = co(:,3))
% nk:      ppmak reads rows as d·L → 2×4 coefs REJECT with
%          nk:ppmak:coefs (expects 4 rows for d=1)
```

Every pp consumer (fnval / fnder / fnint / fncmb / fnbrk / csapi)
agrees on the nk layout internally — nk results are self-consistent —
but pp structs are not interoperable with the reference, and the
ppmak input contract differs.

## Fix direction

Migrate the pp struct to the reference layout in one sweep
(ppmak + fnval + fnder + fnint + fncmb + fnbrk + csapi + their
tests), or provide a layout flag. Until then the splines portion of
the argcheck campaign pinned only the gates that do not depend on
the layout (break monotonicity, piece-count classes) and filed:

- fncmb's op-string form (`fncmb(f, '+', g)`) — unimplemented;
- fncmb's scalar-first form (`fncmb(c, f)`) — nk accepts, the
  reference rejects with unknownfrstfn (probe78 S16) — acceptance
  divergence;
- fnval's matrix-x output shape (d × size(x)) for d > 1.

## Repro

See the block above (copy-paste runnable in both engines).

**Guard:** `DISABLED_SplinePpLayout` (known_bugs_test.cpp) asserts
the reference reading of the S01 case.
