# struct() rejects cell-array values whose elements have mixed shapes

- **Kind:** bug
- **Component:** builtin `struct` (cell-value expansion)
- **Found:** 2026-09-18, engine-gap portion (struct-concat verification
  battery — the probe62 R10 case could not be built in nk).

## Repro

```
clear;
sn = struct('m', {magic(2), 1}, 't', {{1, 'x'}});
```

- MATLAB R2025b: 1×2 struct array — a 1×N cell VALUE spreads across N
  elements, and each element may hold whatever that cell slot contains
  (a 2×2 matrix for element 1, the scalar 1 for element 2).
- nk: `nk:struct:cellShape` — "cell-array values must all have the same
  shape" (every field's cell is required to be a uniform-shape grid).

## Fix direction

The cell-expansion rule is: a 1×N or N×1 cell (or N×M grid) of values
defines the struct-array SHAPE; non-cell scalars broadcast; the per-
slot VALUES may differ in shape freely — only the OUTER cell's shape
participates in the size unification, not the shapes of the values it
contains. The current cellShape check conflates the two.

**Guard:** `DISABLED_StructMixedCellShapes` in
`src/bundle/tests/known_bugs_test.cpp`.
