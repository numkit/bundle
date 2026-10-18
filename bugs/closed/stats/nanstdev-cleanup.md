# stats.nanstdev — reference-absent extension (R2025b does not ship it)

- **Status:** ✅ FIXED (2026-10-18 — language-level function is `nanstd`,
  which ships in the reference Statistics and Machine Learning Toolbox;
  `numkit::stats::nanstdev` is the C++ identifier analogous to
  `numkit::stats::stdev` for `std`)
- **Severity:** P3
- **Kind:** cleanup
- **Found:** 2026-09-19, stats argcheck campaign final sweep
  (memory: stats_arity_probe_method; runbook decision).

## Resolution

`stats_library.cpp` registers `nanstd` (`reg("nan", "nanstd", &stats::detail::nanstd_reg)`),
which IS part of the reference Statistics and Machine Learning Toolbox.
`nanstdev` is never registered as a script function — it is the C++
function name (`numkit::stats::nanstdev`, matching `numkit::stats::stdev`
since `std` is a C++ reserved namespace). Added `nanstd` coverage in
`DescriptiveContractTest.NanFamilyAllFlagAndSingle`.

**Guard:** `DescriptiveContractTest.NanFamilyAllFlagAndSingle` (`modules/stats/tests/descriptive_contract_test.cpp`).
