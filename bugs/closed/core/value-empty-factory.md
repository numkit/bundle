# core.Value — dead deprecated factory `Value::empty()`

- **Status:** ✅ FIXED (2026-09-17)
- **Severity:** P3 minor/style
- **Kind:** cleanup (dead code)
- **Found:** 2026-09-17 legacy sweep ("есть легаси которое стоит вычистить?")

## What rotted

`Value::empty()` (`src/value/include/nk/value/value.hpp`,
`src/value/src/value.cpp`) was marked `[[deprecated("Use Value::Empty … or
Value() …")]]` — but the deprecation was never followed by removal: 0
production call sites remained; the single user was
`src/builtin/tests/types_public_api_test.cpp` `IsemptyOnEmpty`, which tested
`isempty()` on the unset sentinel — accidentally true there, but semantically
the test meant a MATLAB empty. Misleading name (returns the unset sentinel,
NOT a MATLAB empty) was a trap for new code.

## Fix

- Removed the declaration + definition.
- `IsemptyOnEmpty` now tests `isempty(Value::Empty)` (0×0 DOUBLE) — the value
  the test always meant.

**Guard:** none needed (cleanup, no behavior change). Compile is the guard:
0 remaining references. `*Value*:*TypesPublicApi*` suites green (306 tests).

## Historical mentions

Historical logs (`dev-docs/memory/`, `bugs/closed/`) that mention the factory
or the legacy build presets record what was true at the time and are
deliberately left unrewritten.
