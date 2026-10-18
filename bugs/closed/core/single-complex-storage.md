# single-precision complex arrays collapse to double-complex storage

- **Status:** ✅ FIXED (2026-10-18) — `HeapObject::isSingleComplex` tracks single-precision complex class across `single(z)`, `complex(single(a), single(b))`, `class(z)`, `issingle(z)`, `isa(z, 'single')`, `whos`, indexing, concatenation, transpose/ctranspose, unary/binary arithmetic, `real`/`imag`/`abs`/`angle`/`conj`, and wavelet `wthresh`/`wkeep`/`wextend`.
- **Kind:** bug (engine data-model gap)
- **Component:** core Value model (`ValueType`)
- **Found:** 2026-09-19, wavelet argcheck portion (wthresh/wextend
  complex-single class residuals in the probe battery).

## Repro

```
clear;
z = single(complex(1:4, -(1:4)));
class(wthresh(z, 's', 1))       % MATLAB: single; nk: double
class(z')                        % MATLAB: single (complex); nk: double
```

MATLAB's class lattice is {double, single} × {real, complex} (integers
are real-only). nk's `ValueType` has one `COMPLEX` type backed by a
`complex<double>` buffer — a single-precision complex input is silently
widened, and every operation that preserves complexity (wthresh, abs,
transpose, arithmetic contagion, …) returns `double` where the
reference returns `single`.

## Why this is not a spot fix

`COMPLEX` is a first-class switch arm across the entire engine
(interpreter, VM opcodes, ~all toolbox kernels, serialization, IDE
inspection). Representing SINGLE×COMPLEX requires either:

1. a new `ValueType::SINGLE_COMPLEX` (hundreds of switch sites, full
   dual-engine regression sweep), or
2. splitting `ValueType` into elem-class × complexity (a Value-model
   redesign on the scale of the array-class rework).

Both are multi-session engine campaigns, not a portion-sized fix. The
toolbox layer currently papers over it where visible: parity specs use
closeness predicates on single paths and the wavelet gates reject
complex where the reference would accept single-complex only in class.

## Interim rules

- Any NEW toolbox code must NOT silently widen: where a single-complex
  input is rejected with a voiced diagnostic instead of computed, that
  is the preferred interim behavior (the argcheck gates do this).
- Parity specs for single paths keep using closeness predicates.

**Guard:** deferred (data-model gap; no per-function guard is
meaningful until the representation lands).
