# PVS-Studio Static Analysis Report

> **Commit:** [`c54445d3e`] (branch `main`) | **Updated:** 2026-09-23 10:28 UTC | **tests vs prod:** 15 / 966

Per-module details: every `modules/<name>.md` below carries the counts, a rule histogram and the warning tables for one subsystem (tests/prod split throughout). Test-tier noise rules (macro plumbing, might-null heuristics, MATLAB-pinned literal expectations — see TEST_FILTERED_RULES in tools/pvs_report_summary.py) are dropped from test code at report time; every rule stays live for production code. Regenerate with `scripts/windows/pvs-scan.cmd --input build/pvs/nk.plog.json` (or the Linux twin) after a fresh analysis run.

## Summary

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **166** | 0 | 166 |
| 🟡 **Medium** | **347** | 4 | 343 |
| 🟢 **Low** | **468** | 11 | 457 |
| **Total** | **981** | 15 | 966 |

## Warnings by Module

| Module | High | Medium | Low | Total | tests | prod |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [`core`](modules/core.md) | 0 | 25 | 32 | **57** | 3 | 54 |
| [`builtin`](modules/builtin.md) | 8 | 43 | 27 | **78** | 1 | 77 |
| [`ops`](modules/ops.md) | 3 | 2 | 9 | **14** | 0 | 14 |
| [`value`](modules/value.md) | 2 | 0 | 38 | **40** | 0 | 40 |
| [`runtime`](modules/runtime.md) | 2 | 15 | 11 | **28** | 1 | 27 |
| [`scriptgraph`](modules/scriptgraph.md) | 0 | 4 | 7 | **11** | 0 | 11 |
| [`fs`](modules/fs.md) | 0 | 1 | 2 | **3** | 0 | 3 |
| [`codegen`](modules/codegen.md) | 0 | 13 | 25 | **38** | 2 | 36 |
| [`figure`](modules/figure.md) | 5 | 8 | 6 | **19** | 0 | 19 |
| [`graphics`](modules/graphics.md) | 0 | 16 | 15 | **31** | 2 | 29 |
| [`linalg`](modules/linalg.md) | 2 | 8 | 31 | **41** | 0 | 41 |
| [`signal`](modules/signal.md) | 11 | 18 | 24 | **53** | 0 | 53 |
| [`stats`](modules/stats.md) | 11 | 64 | 53 | **128** | 1 | 127 |
| [`image`](modules/image.md) | 85 | 35 | 53 | **173** | 0 | 173 |
| [`audio`](modules/audio.md) | 4 | 19 | 17 | **40** | 0 | 40 |
| [`comm`](modules/comm.md) | 5 | 1 | 7 | **13** | 1 | 12 |
| [`control`](modules/control.md) | 1 | 12 | 16 | **29** | 0 | 29 |
| [`io`](modules/io.md) | 0 | 0 | 5 | **5** | 3 | 2 |
| [`ode`](modules/ode.md) | 5 | 2 | 1 | **8** | 0 | 8 |
| [`wavelet`](modules/wavelet.md) | 11 | 6 | 9 | **26** | 0 | 26 |
| [`bundle`](modules/bundle.md) | 9 | 48 | 78 | **135** | 0 | 135 |
| [`apps`](modules/apps.md) | 2 | 5 | 2 | **9** | 0 | 9 |
| [`tests`](modules/tests.md) | 0 | 1 | 0 | **1** | 1 | 0 |
| [`other`](modules/other.md) | 0 | 1 | 0 | **1** | 0 | 1 |


## Top Rules (repo-wide)

| Rule | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 109 | 0 | 109 |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 109 | 0 | 109 |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 99 | 0 | 99 |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 91 | 0 | 91 |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 81 | 2 | 79 |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | 62 | 0 | 62 |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 45 | 0 | 45 |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 44 | 0 | 44 |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 43 | 0 | 43 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 33 | 0 | 33 |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 25 | 0 | 25 |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | 19 | 0 | 19 |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | 16 | 0 | 16 |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | 15 | 2 | 13 |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | 13 | 2 | 11 |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | 11 | 0 | 11 |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | 9 | 0 | 9 |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | 9 | 0 | 9 |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | 8 | 0 | 8 |
| [V609](https://pvs-studio.com/en/docs/warnings/v609/) | 8 | 0 | 8 |

