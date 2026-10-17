# core.compiler — Debug-config suite aborts at CompilerRegisterOverflowTest.OverflowInSingleExpression/TW (Release passes)

- **Status:** ✅ FIXED (91f6f0f5f)
- **Kind:** bug
- **Severity:** P2 latent (Debug-only manifestation; the test is green in the Release config)
- **Found:** 2026-09-06, portion 23b: with the suite-name collision and the ncfrnd poisson issue fixed, the Debug-config full run got further than ever before and now aborts at this test (process dies mid-run, no gtest failure line).

## Symptom

`nk_gtest.exe` (Debug) aborts during
`TW_VM/CompilerRegisterOverflowTest.OverflowInSingleExpression/TW` — the
test deliberately compiles a huge single expression to trigger
RegisterExhaustionError; in Debug the deeper per-frame stack footprint
(MSVC iterator debug + asserts) appears to blow the stack (or hit an
assert) before the graceful throw. Release runs green.

## Repro

```
cmake --build build/windows/release --target nk_gtest   # Debug
build/windows/release/tests/gtest/Debug/nk_gtest.exe --gtest_filter='*OverflowInSingleExpression*'
# → process aborts (no test verdict)
```

## Root cause (confirmed 2026-09-16 under cdb)

STATUS_STACK_OVERFLOW (0xC00000FD): `TreeWalker::tryEvalFast` recursed
into itself for BINARY_OP children (tree_walker.cpp ~448) with NO
StackGuard check — the guard sits in `execNodeExpand`, which the fast
path bypasses entirely. A left-assoc chain `1+2+...+1000` recursed 1000
levels purely through tryEvalFast; a Debug frame there is ~1.8 KB
(cdb-observed stride 0x720), so 1000 levels ≈ 1.8 MB > the MSVC default
1 MB stack — hard abort before any guard could fire. Release frames are
small enough to fit, hence green.

## Fix

Two independent pieces:
1. `StackGuard::check` at the top of the tryEvalFast BINARY_OP case
   (the only recursive case; leaves don't need it) — over-limit depth
   now throws a clean "Stack exhaustion" error instead of aborting.
2. `/STACK:8388608` for the nk_gtest target in the MSVC Debug config
   (tests/gtest/CMakeLists.txt) — realistic stress depths (~1000 AST
   levels) fit; the guard covers anything beyond.

Verified: Debug `CompilerRegisterOverflowTest` 10/10 green (previously
aborted mid-suite); Release suite green.

## References

- Test: `CompilerRegisterOverflowTest` (tests/gtest/integration/
  try_first_block_bug_test.cpp) — live regression guard (it was the
  aborting test itself; now passes in Debug).
- Prior Debug-only finds, same pattern: bugs/closed/core/
  debug-build-setup-crash.md, ncfrnd/ncx2/negbin/poisson guards
  (portion 23b commit)
- Stack architecture: dev-docs/memory/stack_safety_architecture.md
- Deferred idea (unchanged): a Debug-config CI lane.
