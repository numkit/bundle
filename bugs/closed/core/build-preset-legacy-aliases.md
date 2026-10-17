# core.build — legacy preset aliases `desktop-fast` / `browser`

- **Status:** ✅ FIXED (2026-09-17)
- **Severity:** P3 minor/style
- **Kind:** cleanup (stale config)
- **Found:** 2026-09-17 legacy sweep ("есть легаси которое стоит вычистить?")

## What rotted

`CMakePresets.json` kept two documented-legacy aliases that duplicated the
canonical presets entry-for-entry (same binaryDir, same cache):

- `desktop-fast` == `windows-release` (inherited `portable` + SIMD/THREADS ON,
  binaryDir `build/windows/release`);
- `browser` == `wasm-release` (same toolchain, flags, cache, binaryDir).

No script or CI referenced them (all scripts had moved to the canonical
names); they survived only in `AGENTS.md` as "(legacy aliases … remain
supported)" plus stale doc paths. `desktop-fast-threads` was an exact
duplicate of `windows-release` once threads became always-on there.

## Fix

- Removed configure/build/test preset entries for `desktop-fast`, `browser`,
  `desktop-fast-threads`.
- Re-parented inheritors: `bench-simd` → `windows-release`; `bench-wasm`,
  `browser-threads` → `wasm-release` (effective caches unchanged; the bench
  family stays — it is live perf infrastructure).
- Living docs updated: `AGENTS.md` (dropped the legacy-alias note),
  `handbook/parity_agent_prompt.md`, `handbook/coordination.md` (build paths →
  `build/windows/release`, `build/wasm/release`), `benchmarks/simd/bench_simd.sh`
  output label → "portable vs. bench-simd" (what it actually runs).
- Historical records (`dev-docs/memory/*`, `bugs/closed/*`, the dated
  validation list in `handbook/namespace_design.md:916`) deliberately left
  unrewritten — they name the presets used at the time.

**Guard:** none needed (cleanup). `cmake --list-presets` validates the file
and every inheritance edge.
