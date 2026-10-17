# control — reference-legal short forms rejected (constructors, demo plots, model forms)

- **Status:** 🔴 OPEN
- **Severity:** P4 (default-argument and convenience forms)
- **Kind:** stub
- **Found:** 2026-09-17 during the control arity migration — the k=0
  probe pass plus valid-model minis found reference-legal short forms
  that nk's floors reject.

## Symptom

Several registrations have documented short forms in R2025b; nk's 2026-
09-17 arity migration kept the implementation floors rather than
letting a call through that the compute kernels cannot produce.

| Function | Reference form (probed 2026-09-17) | nk floor |
|---|---|---|
| tf / zpk / ss / filt | `tf()` empty model, `tf(1)` static gain | min 2/3/4/2 |
| frd | `frd()` empty model (note the HOLE: `frd(x)` 1-arg is REJECTED by the reference's own frd2 check) | min 2 |
| step / impulse / bode / nyquist / rlocus / margin | 0-arg form runs a random-model DEMO plot | min 1 |
| freqresp | `freqresp(sys)` over the default grid | min 2 |
| lsim | `lsim(sys, u)` with t derived from Ts | min 3 |
| lqr / dlqr | model form `lqr(sys, Q, R)` (matrix form needs R: `lqr(A,B,Q,R)`) | min 4, matrix-only |

The old nk 3-arg matrix form `lqr(A,B,Q)` (implicit R = I) was removed
with the migration: the reference rejects it, so it silently answered a
call class the reference engine refuses.

## Repro

```matlab
clear;
t = tf();
% nk:     Error nk:tf:nargin ("at least 2 required")
% MATLAB R2025b (probed 2026-09-17): t = empty 0x0 tf model

g = tf(1);
% nk:     Error nk:tf:nargin
% MATLAB R2025b: g = static gain tf (num=1, den=1)

s = tf([1], [1 1]);
fr = freqresp(s);
% nk:     Error nk:freqresp:nargin
% MATLAB R2025b: fr = response over the default frequency grid

sd = tf([1], [1 1], 0.1);
y = lsim(sd, [1 2 3]);
% nk:     Error nk:lsim:nargin
% MATLAB R2025b: y = 3 samples, t derived from Ts

sm = ss([0 1; -1 -2], [1; 0], [1 0], 0);
[K, S, P] = lqr(sm, eye(2), 1);
% nk:     Error nk:lqr:nargin (matrix form needs 4; model form deferred)
% MATLAB R2025b: returns gain/Riccati/poles from the model form

step();
% nk:     Error nk:step:nargin
% MATLAB R2025b: runs a random-model demo step plot (cosmetic)
```

## Root cause

The compute kernels have no paths for empty/static-gain construction
without explicit num/den, default response grids, Ts-derived time
bases, model-form Riccati entry, or demo plots.

## Suggested fix

Constructors: add empty/static-gain defaults in lti.cpp and lower the
floors; freqresp/lsim: add the documented default-argument paths; lqr/
dlqr: route a sys-struct first argument to the care/dare path. The
0-arg demo-plot forms are cosmetic — accept-and-document or leave
rejected deliberately.

## References

- **Guard:** `DISABLED_ControlShortForms`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
