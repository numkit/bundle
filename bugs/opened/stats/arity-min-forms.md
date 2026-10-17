# stats — reference-legal 0-argument forms rejected (fitdist / haltonset / randg)

- **Status:** 🔴 OPEN
- **Severity:** P4 (rarely used default-argument forms)
- **Kind:** stub
- **Found:** 2026-09-17 during the stats max-arity migration — the
  dedicated k=0 probe pass (the []-wall probe starting at k=1 cannot see
  them) found three legal 0-arg forms in R2025b.

## Symptom

Three stats registrations have documented 0-argument default forms in
the reference engine; nk's regs enforce min 1 and reject them.

## Repro

```matlab
clear;
c = fitdist();
% nk:     Error nk:fitdist:nargin (min 1)
% MATLAB R2025b (probed 2026-09-17): c = 1xN cell of distribution names

h = haltonset();
% nk:     Error nk:haltonset:nargin (min 1)
% MATLAB R2025b: h = haltonset (default dimension set)

g = randg();
% nk:     Error nk:randg:nargin (min 1)
% MATLAB R2025b: g = scalar gamma(1,1) draw (builtin)
```

## Root cause

The compute kernels behind the three regs have no 0-arg default path;
the 2026-09-17 arity migration kept min 1 rather than letting a call
through that the body cannot compute.

## Suggested fix

Add the documented defaults: fitdist() → list of supported
distributions; haltonset() → default d (1); randg() → scalar randg(1)
draw. Then lower the reg bounds to min 0.

## References

- **Guard:** `DISABLED_ZeroArgForms`
  (src/toolboxes/stats/tests/known_bugs_test.cpp)
