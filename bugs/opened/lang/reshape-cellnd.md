# lang — reshape: CELL/STRING arrays reject >3 dimensions (ND constructors missing)

- **Status:** 🔴 OPEN
- **Severity:** P3 (documented N-D reshape form)
- **Kind:** stub
- **Found:** 2026-09-18 during the reshape_argcheck boundary redesign —
  the >3-D path exists for numeric and object arrays but cell/string
  arrays hit a voiced deferral.

## Symptom

`reshape` of a cell or string array into more than 3 dimensions throws
`nk:reshape:cellND` ("ND CELL/STRING (>3) not yet supported"). The
reference reshapes cell/string arrays into any dimensionality
(element-wise copy, like the numeric path). 2-D/3-D cell/string forms
work.

## Repro

```matlab
clear;
c = reshape(num2cell(1:16), 2, 2, 2, 2);
% nk:     Error nk:reshape:cellND ("ND CELL/STRING (>3) not yet
%         supported")
% MATLAB R2025b (probed 2026-09-18): 2x2x2x2 cell, elements 1..16 in
%         column-major order

s = reshape(repmat("a", 1, 16), 2, 2, 2, 2);
% MATLAB R2025b: 2x2x2x2 string array
```

## Root cause

`Value` has no `cellND` / `stringArrayND` constructors: the cell/string
branch in `reshapeND` (src/builtin/src/elmat/matrix.cpp) only handles
2-D/3-D via `cell3D`/`stringArray3D` and defers nd > 3, then falls
back to the legacy path.

## Suggested fix

Add N-D cell/string construction (`Value::cellND(Span<const size_t>)`
/ `stringArrayND`, or generalize the cellDataVec path to arbitrary
Dims); drop the deferral and copy element-wise like the 2-D/3-D branch.

## References

- **Guard:** `DISABLED_ReshapeCellND`
  (src/bundle/tests/known_bugs_test.cpp)
