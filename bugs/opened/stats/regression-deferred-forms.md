# regression deferred forms: glmval bounds output, Simultaneous, custom links

- **Kind:** stub
- **Component:** stats (glmval)
- **Found:** 2026-09-19, stats argcheck campaign regression portion
  (probe76; contracts landed as ridge_full / nlparci_full /
  glmval_full in regress/regress_full.cpp).

## Deferred branches

1. **glmval confidence bounds** (`[yhat, ylo, yhi]`) — the second
   output needs the STATS struct's `se` / `coeffcorr` /
   `estdisp` / `dfe` covariance machinery plus the simultaneous
   critical values. Requesting bounds without STATS errors with the
   reference's NeedSTATS class; with STATS it is a voiced stub
   (`nk:glmval:boundsUnsupported`).
2. **'Simultaneous' NV** — parsed and inert (bounds-only option,
   rides on gap 1).
3. **Custom (struct) link specifications** — the reference's
   stattestlink accepts a link struct; nk accepts the canned names
   only (identity/logit/log/probit/reciprocal/canonical — case
   insensitive) and voices UnrecognizedLink otherwise.

ridge and nlparci are complete to the probed contracts (values
parity-pinned in tools/parity/specs/regression_forms.json).

**Guard:** deferred (voiced stubs; no silent wrong values).
