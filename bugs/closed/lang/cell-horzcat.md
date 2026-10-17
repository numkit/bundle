# [a, b] concatenation of cell arrays was unsupported

- **Kind:** bug
- **Component:** core value ops (Value::horzcat)
- **Found:** 2026-09-18, stats argcheck portion (a probe battery's
  `[forms extra]` cell concat failed; verified on a clean tree).
- **Fixed:** 2026-09-18, same portion.

## Repro

```
clear;
a = {1 2};
b = {3};
c = [a b];      % MATLAB: 1x3 cell {1, 2, 3}
```

- MATLAB R2025b: 1×3 cell.
- nk (before): `Concatenation not supported for type 'cell'` — horzcat
  had no cell branch (vertcat's cell path existed; horzcat fell through
  to numeric promotion).

## Fix

`Value::horzcat` gained a cell branch mirroring vertcat's: row dims
must match, columns append side by side (column-major copy).

**Guard:** `CellHorzcatConcatenates` in
`src/bundle/tests/struct_concat_test.cpp`.
