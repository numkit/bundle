# lang.maxmin — 'linear' index option not supported (incl. vecdim form)

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (secondary-output option)
- **Kind:** stub
- **Found:** 2026-09-17 while implementing the vecdim reduction form
  (probed against R2025b).

## Symptom

`[M, I] = max(X, [], dim, 'linear')` (linear indices into the operating
dimension) is not parsed — nk has no 'linear' option for max/min at all.
With a vecdim the reference REQUIRES it for two outputs:

```matlab
clear;
A = reshape(1:24, [2 3 4]);
[v, i] = max(A, [], [1 3]);
% nk:     Error: max: returning two outputs with a dimension vector
%         requires the 'linear' option (nk:max:vecdimLinear)
% MATLAB R2025b (probed 2026-09-17): Error using max — Specify 'linear'
%         option when returning two outputs and the operating dimension
%         is a vector.
[v, i] = max(A, [], [1 3], 'linear');   % MATLAB: OK; nk: flag unknown
```

## Root cause

The max/min regs never parse a trailing 'linear' string flag; the index
semantics (linear index into the collapsed operating dims) has no kernel
path.

## Suggested fix

Parse 'linear' as a trailing flag in max_reg/min_reg; for the reduction
form return the column-major offset within the operating dims (the
collapse view already groups them contiguously, so the existing index
output of the collapsed reduction IS the linear index modulo its
last-dim stride — verify against probed reference values).

## References

- **Guard:** `MaxMinLinearOption`
  (src/bundle/tests/known_bugs_test.cpp)
