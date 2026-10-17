# signal.findpeaks — MinPeakWidth / MaxPeakWidth / Annotate / DoubleSided options unsupported

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (missing options)
- **Kind:** stub
- **Found:** 2026-06 via signal.* DEEP-PROBE sweep; re-confirmed 2026-09-17
  while closing findpeaks-widthreference.md (the loud-throw list there
  shrank by exactly WidthReference).

## Symptom

`findpeaks(..., 'MinPeakWidth'|'MaxPeakWidth'|'Annotate'|'DoubleSided', ...)`
throws "option not supported". Width-reference machinery itself now works
('WidthReference' landed 2026-09-17), so the width FILTERS are the natural
follow-up; Annotate (plot extents) and DoubleSided (minima as peaks with
negative signal) are further out.

## Repro

```matlab
clear;
findpeaks([1 3 2 5 1 6 1], 'MinPeakWidth', 1.4, 'WidthReference', 'halfheight')
% nk: Error — findpeaks: option 'MinPeakWidth' not supported
% MATLAB R2025b (probed 2026-09-17): pk = [3 5]  (halfheight widths are
%   [1.75 1.45833 1.2]; the >=1.4 filter keeps peaks 1-2)
% 'MaxPeakWidth', 1.4 → pk = 6 (keeps only peak 3)
```

## Suggested fix

Parse both filters into PeakOpts and apply them to the per-peak widths
AFTER WidthReference resolution (they filter on the chosen reference's
widths; keep peaks with w >= minW / w <= maxW). The width computation
(peakWidth) is shared and already reference-aware. Annotate needs the
plot extents layer; DoubleSided needs minima detection on -x plus
sign handling — file separately if picked up.

## References

- **Guard:** `FindpeaksWidthOptions`
  (src/toolboxes/signal/tests/known_bugs_test.cpp)
- bugs/closed/signal/findpeaks-widthreference.md (the width machinery +
  reference-probe tables)
