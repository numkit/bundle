# lang — sort_bench drifted from the sort() public API (bench preset did not build)

- **Status:** ✅ FIXED (2026-09-17 — argcheck Phase-2 portion)
- **Severity:** P3 (tooling rot: the NK_BUILD_BENCHMARKS preset could not
  compile, so the perf gate was unusable)
- **Kind:** cleanup
- **Found:** 2026-09-17 (running the dsp_bench perf gate for the filter
  FilterPlan refactor)

## Symptom

`cmake --preset bench` / any `NK_BUILD_BENCHMARKS=ON` build failed in
`src/builtin/benchmarks/sort_bench.cpp`: it still called the pre-overload
`sort(x, mr)` signature, while the API had gained
`sort(x, dim, descend, nanPlace, mr)` ([elmat.hpp:654]).

## Root cause

The bench executable is only built on demand; the sort signature evolved
(no bench in the default presets) and nothing gated the bench compile.

## Fix

`sort_bench.cpp` now calls `sort(x, 0, false, NanPlace::Auto, mr)`; the
`build/windows/bench` tree builds clean end-to-end and the filter family
benches run (BM_FilterFIR33: 36–44M items/s across 1024–65536 samples).

**Guard:** deferred — no gtest for a benchmark compile; the honest gate
would be building `nk_bench` in CI. Note for future API changes to
benched functions: grep `src/*/benchmarks/` when changing a public
signature.
