# comm — convertSNR: argument semantics diverge (positional modes vs keyword names)

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (silent wrong result on the reference-documented form)
- **Kind:** bug
- **Found:** 2026-09-17 during the comm arity migration — R2025b probes
  (`convertSNR(1,'esno')` legal, `convertSNR(1,'InputMode','ebno',...)`
  rejected) showed the reference parses positional mode VALUES, not
  keyword names.

## Symptom

The reference signature is `convertSNR(x, inputmode[, outputmode[,
name-value...]])` — arg 2 is the input-mode VALUE, arg 3 the output-mode
VALUE, and name-value pairs (e.g. `'BitsPerSymbol'`) follow. nk's reg
instead scans args 2..end for the keyword NAMES `'From'` / `'To'` /
`'BitsPerSymbol'` and ignores every other string, so the
reference-documented positional form silently computes a DIFFERENT
conversion (defaults ebno→esno with k=1).

## Repro

```matlab
clear;
v = convertSNR(10, 'esno', 'snr', 'BitsPerSymbol', 2);
% nk:     v = 13.0103  (From/To ignored -> defaults ebno->esno, k=2)
% MATLAB R2025b (probed 2026-09-17): v = 10  (esno and snr are the same
%                                  quantity; k never enters this pair)

v2 = convertSNR(0, 'ebno', 'esno', 'BitsPerSymbol', 2);
% MATLAB R2025b: v2 = 3.0103  (ebno + 10*log10(k))

v3 = convertSNR(1, 'InputMode', 'ebno');
% MATLAB R2025b: Error convertSNR:unrecognizedStringChoice
%              ('InputMode' is not a mode value); nk: accepts silently
```

## Root cause

`convertSNR_reg` parses a keyword-name dialect that nk invented; the
reference uses positional mode values plus real name-value pairs.
The positional From/To coincidence (nk's loop happens to pass
`'ebno'`,`'snr'` through as ignored strings while defaults compute the
same number for the ebno→esno/snr family) masked the divergence in the
existing suite.

## Suggested fix

Reparse per the reference contract: arg 2 = input mode value, arg 3 =
optional output mode value, then name-value pairs. Update the
channel_smoke.m name-form demo at the same time.

## References

- **Guard:** `ConvertSNRPositionalModes`
  (src/toolboxes/comm/tests/known_bugs_test.cpp)
