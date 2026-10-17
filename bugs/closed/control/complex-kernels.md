# control — complex kernels: reference computes complex, nk kernels are double-only

- **Status:** ✅ FIXED (2026-10-17)
- **Severity:** P3 (honest stubs; no wrong numerics shipped)
- **Kind:** stub
- **Found:** 2026-09-18 during the control argcheck portion — the raw
  `elemAsDouble` reads used to take the real part SILENTLY (wrong
  results); now every entry below rejects with
  `nk:<fn>:complexUnsupported` instead.

## Symptom

The reference engine computes complex results for complex operands in
all of the entries below; nk's kernels (Kronecker LU, ctrb/obsv block
powers, Ackermann solve, ss2ss similarity transform, lsim simulation)
consume double buffers only, so complex inputs are stubbed.

| Entry | Complex arg | Reference result (probed R2025b, probe9) |
|---|---|---|
| `lyap` | A or Q | complex solution |
| `dlyap` | A or Q | complex solution |
| `ctrb` | A or B | complex controllability matrix |
| `obsv` | A or C | complex observability matrix |
| `acker` | A (or B) | complex K `[8+2i 15-4i]` (+ its pole warning) |
| `ss2ss` | T | complex ss model |
| `lsim` | u or x0 | complex response trajectory |

Note the split inside `acker`: complex **poles** are ACCEPTED and
already correct — conjugate pairs give the real K `[7 18]` in both
engines, and a non-conjugate set degenerates to the SAME real answer
the reference computes (`[8 21]`, with the reference emitting its
"pole locations >10% in error" warning — probed, mirrored by accident
of the same real-arithmetic path, kept deliberately).

## Repro

```matlab
clear;
X = lyap(complex([-1 0; 0 -2], 1), eye(2));
% MATLAB R2025b (probed 2026-09-18):
%   [0.4444 - 0.0556i; ... 0.2778]  (complex solution)
% nk: nk:lyap:complexUnsupported (honest stub; the old build silently
%   returned the real-part-only [0.5 0; 0 0.25])

Co = ctrb(complex([2 1; 1 3], 1), [1; 0]);
% MATLAB: [1, 2+1i; 0, 1+1i]
% nk: nk:ctrb:complexUnsupported
```

## Root cause

All shared kernels in `toolboxes/control` (internal/numerics.hpp and
the per-file Mat/Vec algebra) are `std::vector<double>`; a complex
template pass (like linalg's) does not exist yet.

## Suggested fix

Template the Kronecker solve + block powers over `std::complex<double>`
(mirroring `nk::linalg::detail`'s complex helpers), starting with
lyap/dlyap (smallest kernel), then ctrb/obsv, then lsim's simulate.

## References

- **Guard:** `DISABLED_LyapComplexKernel`, `DISABLED_DlyapComplexKernel`,
  `DISABLED_CtrbObsvComplexKernel`, `DISABLED_AckerComplexKernel`,
  `DISABLED_Ss2ssComplexKernel`, `DISABLED_LsimComplexKernel`
  (src/toolboxes/control/tests/known_bugs_test.cpp)
- Probe batteries: `build/probe9_control_ref.m` (gitignored)
