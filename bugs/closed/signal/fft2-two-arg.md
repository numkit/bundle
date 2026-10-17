# signal.fft2 — 2-argument call computed, reference rejects it (arity hole)

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (rejected-by-reference input accepted with a plausible
  result)
- **Kind:** bug
- **Found:** 2026-09-17 signal max-arity sweep: the reference accepts
  `fft2(X)` or `fft2(X,m,n)` — a call with EXACTLY 2 arguments errors
  `MATLAB:minrhs` (m given without n), while nk computes `fft2(x, m)`.

## Repro (self-contained)

```matlab
clear;
y = fft2(ones(4), 3);
% nk:     3-row padded FFT computed (2-arg form accepted)
% MATLAB R2025b (probed 2026-09-17): Error using fft2 — Not enough input
%         arguments. (MATLAB:minrhs) — fft2 takes 1 or 3 args, never 2
```

Same shape for `ifft2` (its 3rd/4th args are the symmetric flag, so the
2-arg hole applies there too: probed `ifft2([],[])` → `MATLAB:minrhs`).

## Root cause

`checkNargin` expresses a min..max range; the reference contract for
fft2/ifft2 is the SET {1, 3+}, not a range. The applied bound (1..3 for
fft2, 1..4 for ifft2) is the closest safe range — it never rejects a legal
call, but accepts the illegal 2-arg form.

## Fix direction

Either a dedicated arity-hole form in `argcheck` (accepted-arity set), or
an explicit rejection in `fft2_reg`/`ifft2_reg` for `args.size() == 2`
with an nk-voiced error (`nk:fft2:nargin`, message noting the 1-or-3
shape, richer than the reference's).

**Guard:** `SignalKnownBug.Fft2TwoArgRejected` in
`src/toolboxes/signal/tests/known_bugs_test.cpp`.
