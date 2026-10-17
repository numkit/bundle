# signal.xcorr — negative maxlag returns the full-length correlation instead of the |maxlag| window

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3
- **Kind:** bug
- **Found:** 2026-09-17 while writing the argcheck signal-sweep happy-path
  tests (the maxlag integer validation landed in the same sweep; this is
  the pre-existing shape divergence it surfaced).

## Symptom

`xcorr(x, maxlag)` with a NEGATIVE maxlag is accepted by the reference
(the lag window is `maxlag : -maxlag`, i.e. symmetric ±|maxlag|) but nk
returns the FULL correlation (2*length(x)-1).

## Repro

```matlab
clear;
n = numel(xcorr(1:8, -3));
% nk:     n = 15   (full length)
% MATLAB R2025b (probed 2026-09-17): n = 7   (lags -3..3)
```

## Root cause

The xcorr/xcov compute path only honours a positive maxlag window; a
negative value falls through to the full-length path (the reg's
`maxlag = -1` sentinel for "no maxlag given" collides with a genuine
negative request).

## Suggested fix

Distinguish "no maxlag" (sentinel) from an explicit negative request at
the reg/compute boundary (e.g. an optional/has-maxlag flag), then window
by |maxlag| symmetrically on both sides.

## References

- **Guard:** `XcorrNegativeMaxlagWindow`
  (src/toolboxes/signal/tests/known_bugs_test.cpp)
- The integer validation for maxlag (nk:<fn>:maxlagNotInteger) landed
  2026-09-17 — see argcheck_signal_test.cpp SignalSweepBranchMatrix.
