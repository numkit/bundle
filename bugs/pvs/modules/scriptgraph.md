# `scriptgraph` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **4** | 0 | 4 |
| 🟢 **Low** | **7** | 0 | 7 |
| **Total** | **11** | 0 | 11 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 1 | 6 | 0 | 7 | **7** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V719](https://pvs-studio.com/en/docs/warnings/v719/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V719](https://pvs-studio.com/en/docs/warnings/v719/) | - | [`src/scriptgraph/src/ast_serialize.cpp:70`](../../../src/scriptgraph/src/ast_serialize.cpp#L70) | The switch statement does not cover all values of the 'NodeType' enum: CLASSDEF_DEF, CLASSDEF_ENUM_MEMBER, CLASSDEF_PROPERTY, SUPERCLASS_REF. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/scriptgraph/src/lowering.cpp:427`](../../../src/scriptgraph/src/lowering.cpp#L427) | The 'n.kind' variable was assigned the same value. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/scriptgraph/src/lowering.cpp:335`](../../../src/scriptgraph/src/lowering.cpp#L335) | A part of conditional expression is always true: producerId >= 0. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/scriptgraph/src/lowering.cpp:1065`](../../../src/scriptgraph/src/lowering.cpp#L1065) | A part of conditional expression is always true: partitions.size() >= 3. |


<details>
<summary><b>🟢 Low Severity (7)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:344`](../../../src/scriptgraph/src/lowering.cpp#L344) | The 'e.kind' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:641`](../../../src/scriptgraph/src/lowering.cpp#L641) | The 'mn.sourceCol' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:795`](../../../src/scriptgraph/src/lowering.cpp#L795) | The 'mn.sourceCol' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:810`](../../../src/scriptgraph/src/lowering.cpp#L810) | The 'e.kind' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:830`](../../../src/scriptgraph/src/lowering.cpp#L830) | The 'e.kind' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/scriptgraph/src/lowering.cpp:1161`](../../../src/scriptgraph/src/lowering.cpp#L1161) | The 'e.kind' variable was assigned the same value. |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | [`src/scriptgraph/src/lowering.cpp:52`](../../../src/scriptgraph/src/lowering.cpp#L52) | Consider checking for misprints. It's possible that the 'end' should be checked here. |

</details>
