# lang.regs — macro-generated regs silently drop documented option arguments

- **Status:** 🔴 OPEN
- **Severity:** P3 (options compute wrong results instead of erroring or
  being honored)
- **Kind:** bug
- **Found:** 2026-09-17 during the builtin max-arity sweep — bounding
  these macros would trade a silent wrong result for a wrong rejection,
  so they were left min-only and the option gaps filed here.

## Symptom

Macro-generated regs read a fixed number of arguments and silently DROP
the rest, so documented option forms compute with defaults instead of
the caller's values:

```matlab
clear;
% eraseBetween(str, startPat, endPat, 'Boundaries', 'inclusive')
r = eraseBetween("abcabc", "b", "b", "Boundaries", "inclusive");
% nk:     uses Boundaries='inclusive' default silently — option dropped
% MATLAB R2025b: honors the option

% paddata(A, k, 'FillValue', v) / trimdata(A, k, Name-Value)
p = paddata(1:4, 6, 'FillValue', -9);
% nk:     pads with 0 (default) — option dropped
% MATLAB: pads with -9
```

Affected families (src/bundle/src/register/builtin/):
- `NK_STR_TRI_REG` (lang_strings_reg.cpp) — eraseBetween 4th+ args
  ('Boundaries'); insertAfter/insertBefore take none, bounded 2..2/3..3.
- `NK_RESIZE_REG` (lang_manip_reg.cpp) — paddata/trimdata/resize
  Name-Value tails.

## Root cause

The macros marshal a fixed arity (`FN(args[0], n, mr)`); no option
parsing exists behind them. issortedrows was split out of its macro for
the same reason (variadic, now min-only 1).

## Suggested fix

Parse the option tails in the macros (or split the affected fns out into
hand regs with `argcheck::expectedChoice`-based option parsers), then
bound the arity or leave unbounded per the reference
(nargin('eraseBetween') = -4, paddata/trimdata = -3).

## References

- **Guard:** deferred until pickup (assert option-honoring values, e.g.
  paddata fill and eraseBetween bounds, probed against the reference).
- Arity bounds landed without maxing these macros:
  bugs/opened/lang/reg-max-arity.md (builtin domain note).

## Signal domain additions (2026-09-17, max-arity sweep)

The signal migration bounded zp2sos/tf2sos at the reference's arity, which
exposes previously REJECTED-and-now-ACCEPTED-but-ignored option positions
(the old code threw on any extra argument, so these were not silent before):

- `zp2sos(z, p, k, dir_flag, order, scale)` — args 4..6 now pass arity and
  are dropped (old code rejected >3). Reference: `zp2sos(___,dir_flag,order)`
  + scale handling.
- `tf2sos(b, a, dir_flag, order)` — args 3..4 now pass arity and are
  dropped (old code required exactly 2). Reference: `tf2sos(___,dir_flag,order)`.

Same class, pre-existing (min-only before and after — documented in reg
comments during the sweep): `resample` n/beta/method + name-value tail
(bound 3..3, honest rejection of the unimplemented forms),
`tsa` numerical-3 + name-value (args 4..5 serve the legacy nk continuous-rpm
form), `tachorpm` name-value past arg 4 (bound 2..4),
`sigrangebinmask` option-string tail (bound 2..2), `hann`/`hanning` third
argument (bound 1..3).

## Image domain additions (2026-09-17, max-arity sweep)

The image migration bounded the four reg macros at the reference arity;
within those bounds the macros still marshal a fixed prefix and DROP the
rest (pre-existing: the old hand-throws only enforced minimums, so extra
args were silently dropped before too):

- `NK_BIN_REG` (arithmetic_reg.cpp): `imadd(I, J, scale)` — 3rd positional
  (scale / output-class string) accepted (bound 2..3) and dropped; the
  2-arg result is returned silently.
- `NK_COLOR_REG` (color_reg.cpp): channel/space-parameter forms accepted
  per the probed bounds and dropped — worst cases compute WRONG results,
  not just defaults: `hsv2rgb(H, S, V)` computes `hsv2rgb(H)` (bound
  1..3); `rgb2xyz/rgb2lab` whitepoint args (bound 1..5);
  `xyz2rgb/lab2rgb` whitepoint args (bound 1..7); `rgb2hsv` extra
  channel args (min-only, custom-parser reference). Converter pairs
  bounded 1..1 (`rgb2ycbcr`, `ycbcr2rgb`, `rgb2ntsc`, `ntsc2rgb`,
  `lab2double`, `lab2uint8`, `lab2uint16`) are exact.
- `NK_IM_UNARY_REG` (type_convert_reg.cpp): `im2double/im2single/
  im2uint8/im2uint16(X, 'indexed')` — the `'indexed'` flag (bound 1..2)
  is dropped: indexed images convert with the same code path as
  intensity images (wrong scaling for indexed inputs).
- `NK_MORPH_REG` (morph_reg.cpp): `imerode/imdilate(I, SE, n, packopt,
  shape)` — args 3..5 (bound 2..5) are dropped; the single-iteration
  result is returned.
- Direct regs, same class: `imlincomb` trailing output-class string is
  honored, but `entropy`'s nbins 2-arg extension is now REJECTED per the
  reference (`entropy(I)` only, bound 1..1) — the nbins body code is now
  unreachable dead code, to clean when picked up.
