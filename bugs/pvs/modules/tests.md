# `tests` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **1** | 1 | 0 |
| 🟢 **Low** | **0** | 0 | 0 |
| **Total** | **1** | 1 | 0 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | 0 | 1 | 0 | 1 | 0 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | [CWE-457](https://cwe.mitre.org/data/definitions/457.html) | [`tests/gtest/integration/debugger_phase234_test.cpp:15`](../../../tests/gtest/integration/debugger_phase234_test.cpp#L15) | Not all members of a class are initialized inside the compiler generated constructor. Consider inspecting: type. |

