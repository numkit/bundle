# mvdist deferred forms: sampler value parity (randn/gamrnd cascades), mvncdf d>=3 accuracy, mvnrnd semidef T shape

- **Kind:** stub
- **Component:** stats (mvnrnd / mvncdf / mvtrnd / mvnpdf)
- **Found:** 2026-09-19, stats argcheck campaign distributions portion
  (probe73/probe74; contracts landed with the mvnpdf/mvtpdf/mnpdf
  rewrites in mvdist.cpp and mvnrnd_full/mvncdf_full/mvtrnd_full in
  distributions/mv_full.cpp).

## Deferred branches (all deterministic contracts are parity-pinned;
these are the remaining approximations)

1. **Sampler VALUE parity** — nk's `randn` (std::normal_distribution on
   the genRes53 cascade) and `gamrnd` (std::gamma_distribution) are not
   bit-identical with the reference's ziggurat randn / Marsaglia-Tsang
   gamrnd, so seeded mvnrnd/mvtrnd draw VALUES differ. Draw ORDER now
   matches the reference (column-major normals, then the scale draws)
   so a future randn/gamrnd cascade restores bit-parity with no further
   changes. Distributional moments are tested statistically.
2. **mvncdf d ≥ 3** — nk uses seeded antithetic Monte Carlo; the
   reference uses Genz separation-of-variables quasi-MC. Agreement is
   ~1e-3 (contract test guards with 1e-2). The d ≤ 2 closed forms and
   the diagonal path are exact.
3. **mvnrnd semidefinite T output shape** — for a rank-deficient Sigma
   the second output is the d×d eigenvalue factor (zero null-space
   rows); the reference's cholcov returns an r×d compact factor.
   Sampling is distributionally identical either way.
4. **mvnrnd/mvncdf options struct** — a trailing options struct is
   stripped and ignored (integrator options are inert for the exact
   paths; MaxFns/Tol for the MC path are fixed).

**Guard:** deferred (approximations on numerically-hard paths; no
silent wrong classes or shapes — every rejection is probed-parity and
the deterministic outputs are pinned in tools/parity/specs/
dist_forms.json).
