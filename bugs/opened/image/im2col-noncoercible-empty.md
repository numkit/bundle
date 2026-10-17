# im2col accepts non-coercible inputs only via the reference's empty path

- **Kind:** stub (deliberate divergence, documented)
- **Found:** 2026-09-19, image argcheck portion (probe12 battery).

## Repro

```matlab
clear;
B = im2col({magic(5)}, [3 3]);   % 1×1 cell, 3×3 blocks
```

**MATLAB R2025b:** `OK`, `zeros(9,0)` — the block is larger than the
1×1 image, so the reference returns an EMPTY result before its (loose)
class validation ever reads a value. Same for `'ab'` (char), `"s"`
(string) and struct inputs: each is smaller than the block and the empty
result short-circuits.

**nk:** `nk:im2col:inputType` — cell / char / string / struct are
rejected outright.

## Decision

Deliberate divergence: nk voices the class instead of silently emitting
an empty matrix for a `{cell}` "image". The numeric/logical/complex
contract is full parity (values preserved, class-preserving, block >
image → empty double — probed). Revisit only if real corpus code relies
on the empty-path acceptance.

**Guard:** deferred (documented divergence, no wrong value is returned).
