# lang — reshape size args unvalidated (silent truncation) + all error texts/IDs diverge

- **Status:** ✅ FIXED (2026-09-16 — `nk::argcheck` portion)
- **Severity:** P1 (fractional size silently truncated — wrong result,
  no error at all)
- **Kind:** bug
- **Found:** 2026-09-16 (MATLAB R2025b probe while designing
  `nk::argcheck` — dev-docs/todo/argcheck_separation.md)

## Symptom

`reshape_reg` converted every scalar size argument with a bare
`static_cast<size_t>(args[i + 1].toScalar())` — no integer check, no
negative check, no identifier — and every hand-written error diverged
from MATLAB:

```matlab
clear;
reshape(1:6, 2.5, 3)   % nk:    OK — 2.5 silently truncated to 2, returns 2x3 (!)
                       % MATLAB: ERROR id=MATLAB:getReshapeDims:notRealInt
                       %         "Size arguments must be real integers."
reshape(1:6, 2, -3)    % nk:    id=nk:reshape:elementCountMismatch (wrap-around
                       %        lands on the numel check by accident)
                       % MATLAB: id=MATLAB:checkDimCommon:nonnegativeSize
                       %         "Size vector elements should be nonnegative."
reshape(1:6)           % nk:    id=nk:reshape:nargin "reshape: requires at least 2 arguments"
                       % MATLAB: id=MATLAB:minrhs "Not enough input arguments."
reshape(1:6, [], 2, [])% nk:    id=nk:reshape:tooManyInferred "only one dimension may be inferred via []"
                       % MATLAB: id=MATLAB:getReshapeDims:unknownDim
                       %         "Size can only have one unknown dimension."
reshape(1:6, 7, [])    % nk:    id=nk:reshape:indivisible "divisible by product of known dims"
                       % MATLAB: id=MATLAB:getReshapeDims:notDivisible
                       %         "Product of known dimensions, 7, not divisible into total number of elements, 6."
reshape(1:6, 2, 4)     % nk:    id=nk:reshape:elementCountMismatch "…must not change in reshape"
                       % MATLAB: id=MATLAB:getReshapeDims:notSameNumel
                       %         "Number of elements must not change. Use [] as one of the size inputs…"
reshape(1:6, 2+3i, 3)  % nk:    raw converter leak "Cannot convert complex … to double scalar"
                       % MATLAB: id=MATLAB:checkDimCommon:complexSize
                       %         "Size argument cannot be complex."
```

## Root cause

Validation lived in the reg adapter as ad-hoc checks around an unguarded
cast; nothing enforced the size-input contract, and none of the messages
had been probed against MATLAB. The compute-side numel check (matrix.cpp)
also carried an invented text/ID.

## Fix

reshape's size contract moves onto `nk::argcheck` primitives
(`reshapeSizeArg` for the Value-level scalar/real checks,
`reshapeSize` for the numeric nonnegative/integer chain — R2025b probe
table in argcheck.hpp, including the check ORDER: negative fires before
non-integer). Adapter errors carry the probed texts/IDs
(minrhs/unknownDim/notDivisible); the numel check in matrix.cpp keeps its
first-line position with the notSameNumel text/ID.


**Re-voiced 2026-09-17** (user rule, later same day): the shipped strings are nk-voiced — `nk:<fn>:<tag>` identifiers and richer messages with got-clauses; the probed reference diagnostics above remain the rejection-behavior contract (same inputs fail, same argument blamed).

## Guard

Live gtests `ReshapeSizeArgValidation` + `ReshapeErrorParity`
(src/builtin/tests/argcheck_test.cpp) — silent-truncation case asserts a
THROW, all branches assert identifier + text.
