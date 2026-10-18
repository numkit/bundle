# regression deferred forms: glmval bounds output, Simultaneous, custom links

- **Status:** ✅ FIXED (2026-10-18)
- **Kind:** stub
- **Component:** stats (glmval / glmfit)
- **Found:** 2026-09-19, stats argcheck campaign regression portion
  (probe76; contracts landed as ridge_full / nlparci_full /
  glmval_full in regress/regress_full.cpp).

## Resolution

1. **glmval confidence bounds** (`[yhat, dylo, dyhi]`) — implemented in
   `glmval_full_bounds` (`modules/stats/src/regress/regress_full.cpp`)
   and `glmfit` (`modules/stats/src/regress/glm.cpp` now returns the 3rd
   `stats` struct output with `covb`, `se`, `coeffcorr`, `dfe`, `s`,
   `sfit`, `estdisp`, `beta`, `t`, `resid`, `wts`).
2. **'Simultaneous' NV** — implemented via Scheffé simultaneous critical
   multiplier ($\sqrt{p \cdot F_{1-\alpha, p, \text{dfe}}}$ when
   `estdisp` is true, $\sqrt{\chi^2_{1-\alpha, p}}$ otherwise).
3. **Custom (struct / cell) link specifications** — implemented via
   `FnHandle` callback on the `Inverse` field of a link struct or 3rd
   element of a link cell array.

**Guard:** `RegressionContractTest.GlmvalFormsAndGates` (`modules/stats/tests/regression_contract_test.cpp`).

