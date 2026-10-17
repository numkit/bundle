# `apps` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **2** | 0 | 2 |
| 🟡 **Medium** | **5** | 0 | 5 |
| 🟢 **Low** | **2** | 0 | 2 |
| **Total** | **9** | 0 | 9 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V640](https://pvs-studio.com/en/docs/warnings/v640/) | 0 | 3 | 0 | 0 | 3 | **3** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 2 | 0 | 0 | 0 | 2 | **2** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`apps/nk/ide_serializer.hpp:331`](../../../apps/nk/ide_serializer.hpp#L331) | Possible overflow. Consider casting operands of the 'r0 + rowsIn' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`apps/nk/ide_serializer.hpp:332`](../../../apps/nk/ide_serializer.hpp#L332) | Possible overflow. Consider casting operands of the 'c0 + colsIn' operator to the 'size_t' type, not the result. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`apps/nk/ide_serializer.hpp:542`](../../../apps/nk/ide_serializer.hpp#L542) | Expression 'sliceLen == 0' is always false. |
| [V640](https://pvs-studio.com/en/docs/warnings/v640/) | [CWE-483](https://cwe.mitre.org/data/definitions/483.html) | [`apps/nk/ide_serializer.hpp:74`](../../../apps/nk/ide_serializer.hpp#L74) | The code's operational logic does not correspond with its formatting. The second statement will always be executed. It is possible that curly brackets are missing. |
| [V640](https://pvs-studio.com/en/docs/warnings/v640/) | [CWE-483](https://cwe.mitre.org/data/definitions/483.html) | [`apps/nk/ide_serializer.hpp:128`](../../../apps/nk/ide_serializer.hpp#L128) | The code's operational logic does not correspond with its formatting. The second statement will always be executed. It is possible that curly brackets are missing. |
| [V640](https://pvs-studio.com/en/docs/warnings/v640/) | [CWE-483](https://cwe.mitre.org/data/definitions/483.html) | [`apps/nk/ide_serializer.hpp:347`](../../../apps/nk/ide_serializer.hpp#L347) | The code's operational logic does not correspond with its formatting. The second statement will always be executed. It is possible that curly brackets are missing. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`apps/nk/main.cpp:633`](../../../apps/nk/main.cpp#L633) | The 'arg' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (2)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`apps/nk/ide_serializer.hpp:476`](../../../apps/nk/ide_serializer.hpp#L476) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`apps/nk/main.cpp:170`](../../../apps/nk/main.cpp#L170) | Decreased performance. The 'abs' variable can be constructed in a lower level scope. |

</details>
