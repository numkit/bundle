# signal: conv2 separable form conv2(u, v, A) not implemented

**Kind:** stub
**Status:** ✅ FIXED (2026-10-17)
**Guard:** Conv2SeparableForm (src/toolboxes/signal/tests/known_bugs_test.cpp)

## Problem

`conv2(u, v, A)` — two vectors plus a matrix — is the reference's
SEPARABLE convolution form (probed R2025b: conv2([1 2],[3 4],ones(2))
== conv2([3 4;6 8],ones(2))). Before this portion nk SILENTLY IGNORED a
non-string third argument and computed the plain 2-arg convolution —
silently wrong for every separable call. The reg now rejects a numeric
third argument with `nk:conv2:separableUnsupported` (and a numeric shape
argument for conv / convn / filter2 with `nk:<fn>:badShape`, matching
the reference's unknownShapeParameter rejection class).

## Repro

```matlab
clear;
y = conv2([1 2], [3 4], ones(2));
% MATLAB: conv2(outer([1 2],[3 4]), ones(2)); nk: nk:conv2:separableUnsupported
```

## Fix sketch

Marshal: vectors u (col) and v (row) → kernel outer(u,v) → delegate to
the existing conv2(A, kernel, shape). The 4-arg form
conv2(u, v, A, shape) follows the same path with the shape string.
