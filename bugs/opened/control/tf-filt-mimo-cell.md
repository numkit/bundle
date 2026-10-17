# control — tf/filt MIMO (cell) coefficient form unsupported

- **Status:** 🔴 OPEN
- **Severity:** P4 (SISO covered; MIMO is a model-representation feature)
- **Kind:** stub
- **Found:** 2026-09-18 during the control argcheck portion — cell
  coefficients used to CRASH with the raw buffer error ("Cannot read
  element as double from type 'cell'"); now the 1x1 SISO-in-cell form
  unwraps and larger cells stub with `nk:<fn>:mimoUnsupported`.

## Symptom

The reference treats cell arrays as the MIMO coefficient form
(`tf({1 2; 5 6}, {1 3; 1 4})` builds a 2x2 model, `filt({1}, [1 3])`
is the SISO-in-cell form). nk's LTI struct represents one SISO
transfer function, so:

- `tf({1}, [1 3])`, `filt({[1 2]}, [1 3])` — 1x1 cells UNWRAP and
  build the SISO model (reference-identical acceptance, done
  2026-09-18);
- any other cell shape → `nk:tf:mimoUnsupported` /
  `nk:filt:mimoUnsupported` (the reference builds a MIMO model here).

## Repro

```matlab
clear;
sys = tf({1 2; 5 6}, {1 3; 1 4});
% MATLAB R2025b (probed 2026-09-18): builds a 2x2 tf model
%   (issiso(sys) == false)
% nk: nk:tf:mimoUnsupported — only SISO models are supported in
%   this build

s2 = tf({1}, [1 3]);
% MATLAB: SISO tf — nk: same (unwrapped, num = 1)
```

## Root cause

`nk::control::tf`/`filt` construct a struct with scalar `num`/`den`
row vectors (kind='tf'); there is no cell-array (Ny×Nu) representation
in the struct model, and none of the consumers (tfdata/step/pole/…)
are MIMO-aware.

## Suggested fix

Extend the tf struct to hold cell `num`/`den` grids + wire the
consumers' MIMO paths (a model-layer feature, not an argcheck fix).

## References

- **Guard:** `DISABLED_TfMimoCellForm`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
- Live guards for the 1x1 unwrap + MIMO stub: `TfCoefficientContract` /
  `FiltBroadNumeratorContract`
  (src/toolboxes/control/tests/type_contract_test.cpp)
