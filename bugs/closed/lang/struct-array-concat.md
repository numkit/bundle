# Struct-array concatenation ([s1 s2] / [s1; s2]) was unsupported

- **Kind:** bug
- **Component:** core value ops (Value::horzcat / Value::vertcat)
- **Found:** 2026-09-19 (wavelet portion battery preamble — odeget
  struct-array setup needed `[o1 o1]` and failed; worked around then).
- **Fixed:** 2026-09-18, engine-gap portion.

## Repro

```
clear;
o1 = odeset('RelTol', 1e-9);
oa = [o1 o1];        % 1x2 struct array
```

- MATLAB R2025b: 1×2 struct array.
- nk (before): `Concatenation not supported for type 'struct'` (structs
  fell through to the numeric promotion path).

## Contract (probed R2025b, probe62)

- Same field SET required, ORDER-INSENSITIVE — the result keeps the
  FIRST operand's field order and values follow the field
  ([struct('a',1,'b',2), struct('b',5,'a',6)] → a=[1 6], b=[2 5]).
- Different field sets → `MATLAB:catenate:structFieldBad` ("Names of
  fields ... same set of fields").
- Struct mixed with a non-struct non-empty → conversion error
  ("Conversion to struct from double/cell is not possible").
- Empties neutral; struct arrays concatenate element-wise with the
  usual dimension rules.

## Fix

`Value::concatStructs` (shared by horzcat/vertcat, dispatched before
the numeric/string/char paths): field-set check via sorted
`fieldNamesInOrder` comparison, element-wise copy through `setField`
(insertion order preserved), dimension mismatch via the shared rule.

**Guard:** `src/bundle/tests/struct_concat_test.cpp` (6 live TEST_F).
