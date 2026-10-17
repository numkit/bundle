# core.compiler — int16 constant/string pool indices wrap silently at 32768 entries (no bound guard)

- **Status:** ✅ FIXED (f40c7680a, 2026-09-15)
- **Kind:** bug
- **Severity:** P3 latent (needs >32767 distinct literals in ONE chunk — machine-generated code scale; but the failure mode is silent wrong code, the worst kind)
- **Found:** 2026-09-15, PVS-Studio audit triage (V1029 family, `src/core/src/compiler.cpp:124` et al. — 16 sites)
- **Found-By:** PVS-Studio (V1029, CWE-197)

## Symptom

`Compiler::addConstant` / `Compiler::addStringConstant` return
`static_cast<int16_t>(pool.size())` with **no bound check**. A chunk that
accumulates 32768 distinct constants (or strings) wraps the index negative;
`LOAD_CONST` / `LOAD_STR` then fetch the wrong pool entry — the script
evaluates to garbage with **no diagnostic**. Registers are guarded
(`RegisterExhaustionError` at 255, src/core/src/compiler.cpp:118 et al.);
the pools are not, and neither are `patchJump` offsets (same int16 space,
>32767 instructions between jump and target).

## Repro

Generate a script with 33000 distinct string literals (one chunk, pool >
32767) and run it:

```
python -c "print('\n'.join(['clear;'] + [f\"s = 'u{i}';\" for i in range(33000)]))" > temp/pool_overflow.m
build/windows/release/apps/nk/Release/nk_repl.exe temp/pool_overflow.m
# MATLAB: s == 'u32999' (no limit at this scale)
# nk:     s is a wrong pool entry (silent index wrap), possibly a crash
```

## Root cause

The bytecode operand width is int16 for pool indices, but the compiler
never enforces the implied capacity, unlike the 255-register ceiling.

## Suggested fix

Mirror the register guard: in `addConstant`/`addStringConstant`, throw a
loud compile error ("constant pool exhausted — split the script") when
`pool.size() >= INT16_MAX`; same for jump offsets in `patchJump`. The
engine's TreeWalker fallback then runs the script correctly (same contract
as `register-exhaustion-no-fallback`, bugs/closed/core/). Secondary: the
linear-scan dedup makes ~33k inserts O(n²) (~10 s); an unordered_map index
falls out naturally alongside.

## References

- Guard: `VMTest.ConstantPoolOverflowThrows` (src/core/tests/vm_test.cpp) — live since f40c7680a
- Precedent: bugs/closed/core/register-exhaustion-no-fallback.md (255-register ceiling → fallback, live guards)
- PVS report: [bugs/pvs/modules/core.md](../../pvs/modules/core.md) (V1029 ×16, all prod)
