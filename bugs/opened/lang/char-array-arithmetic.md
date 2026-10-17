# Char-array arithmetic with scalars throws raw errors

- **Kind:** bug
- **Found:** 2026-09-19, image argcheck portion (probe12 battery rows
  `imreducehaze:char`, `deconvwnr:char`, `tonemap:char/cell/str` — the
  failures were in the probe EXPRESSIONS, before any image function
  ran).

## Repro

```matlab
clear;
x = 'ab' / 10;          % MATLAB: double [9.7 9.8] (char codes / 10)
y = abs('ab') + 0.1;    % MATLAB: double [97.1 98.1]
z = abs({1 2});         % MATLAB: errors (cell) — nk: raw too, ok
```

**nk:** `'ab' / 10` and `abs('ab') + 0.1` both die with the raw
`nk:error | Not a double array` instead of computing the elementwise
double result over char code values. (Cell/string operands SHOULD keep
erroring — they only need a voiced identifier.)

Element-wise scalar arithmetic on char arrays follows the numeric-class
promotion rules in the reference engine; nk's elementwise dispatch
treats char as unsupported.

## Guard

`DISABLED_CharArrayScalarDivision` in
`src/bundle/tests/known_bugs_test.cpp`.
