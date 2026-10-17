# lang.types — complex values report class 'complex' instead of 'double' (class/isa/isfloat)

- **Status:** ✅ FIXED (4b23381d4)
- **Kind:** bug
- **Severity:** P2 — reflection surface diverges from MATLAB for every complex value
- **Found:** 2026-09-16, bug-hunt battery on the splice family
  (class(varargin{end}) after splicing `{Inf, -Inf, NaN, 0, -0, eps, 1i}`).

## Symptom

nk models complexity as a ValueType (COMPLEX); MATLAB models it as an
ATTRIBUTE of double/single. The reflection layer exposes the internal
name, so every complex value misreports its class:

| expression | nk | MATLAB R2025b (probed 2026-09-16) |
|---|---|---|
| `class(1i)` | `complex` | `double` |
| `class([1i 2i])` | `complex` | `double` |
| `isa(1i,'double')` | 0 | 1 |
| `isfloat(1i)` | 0 | 1 |
| `isa(1i,'numeric')` / `isnumeric` / `isreal` | ✓ correct | ✓ |

Root: `mtypeName(ValueType::COMPLEX)` returns `"complex"`
(src/value/src/value_type.cpp) and `isFloatType` omits COMPLEX; class(),
isa() and cast('like', …) all route through them (cast(1,'like',1i)
dispatches on the bogus "complex" class name).

## Repro

```matlab
clear;
fprintf('%s\n', class(1i));
% nk:     complex
% MATLAB R2025b: double
```

## Suggested fix

Map COMPLEX to "double" in mtypeName (audit: every consumer — error
messages, cast 'like', matfun casts, classOf — either improves or is
neutral; nothing parses the string back) and add COMPLEX to
isFloatType. class/isa/isfloat/cast('like') then align for free.

## References

- **Guard (live):** `ComplexReportsDoubleClass`
  (src/builtin/tests/types_public_api_test.cpp)
