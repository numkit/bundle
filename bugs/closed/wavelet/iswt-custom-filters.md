# iswt / swt custom-filter forms (Lo_R/Hi_R and Lo_D/Hi_D) are documented but refused

- **Status:** ✅ FIXED (2026-10-17)
- **Kind:** stub
- **Component:** wavelet (iswt, swt)
- **Found:** 2026-09-18, bug-quartet portion (iswt.m/swt.m source read
  during the integer-arithmetic port)

## Repro

```
clear;
swc = uint8([10 20 30 40; 1 2 3 4]);
y = iswt(swc, [0.7071 0.7071], [0.7071 -0.7071]);   % iswt(SWC, Lo_R, Hi_R)
```

- MATLAB R2025b: computes (filters validated as real finite vectors of
  equal even length ≥ 2; `iswt(SWA, SWD, Lo_R, Hi_R)` also documented).
- nk: `nk:iswt:optionUnsupported` (the reg stub-refuses non-wname
  filter args; swt's `(x, n, Lo_D, Hi_D)` form is likewise absent —
  swt's reg requires a wname string).

The compute kernels take `std::vector<double>` filters internally
already (iswtPhase / the swt conv port), so wiring is a reg+overload
exercise; deferred until a cycle touches these functions.

**Guard:** `IswtCustomFilters` (src/toolboxes/wavelet/tests/known_bugs_test.cpp)
