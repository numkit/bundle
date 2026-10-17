# `ode` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **5** | 0 | 5 |
| 🟡 **Medium** | **2** | 0 | 2 |
| 🟢 **Low** | **1** | 0 | 1 |
| **Total** | **8** | 0 | 8 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | 5 | 0 | 0 | 0 | 5 | **5** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | - | [`src/toolboxes/ode/src/options.cpp:88`](../../../src/toolboxes/ode/src/options.cpp#L88) | Decreased performance. Excessive type casting: string -> char * -> string. Consider inspecting first argument of the function field. |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | - | [`src/toolboxes/ode/src/options.cpp:129`](../../../src/toolboxes/ode/src/options.cpp#L129) | Decreased performance. Excessive type casting: string -> char * -> string. Consider inspecting first argument of the function hasField. |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | - | [`src/toolboxes/ode/src/options.cpp:130`](../../../src/toolboxes/ode/src/options.cpp#L130) | Decreased performance. Excessive type casting: string -> char * -> string. Consider inspecting first argument of the function field. |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | - | [`src/toolboxes/ode/src/options.cpp:159`](../../../src/toolboxes/ode/src/options.cpp#L159) | Decreased performance. Excessive type casting: string -> char * -> string. Consider inspecting first argument of the function hasField. |
| [V811](https://pvs-studio.com/en/docs/warnings/v811/) | - | [`src/toolboxes/ode/src/options.cpp:160`](../../../src/toolboxes/ode/src/options.cpp#L160) | Decreased performance. Excessive type casting: string -> char * -> string. Consider inspecting first argument of the function field. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/ode/src/ode23.cpp:262`](../../../src/toolboxes/ode/src/ode23.cpp#L262) | The 'y_new' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/ode/src/ode45.cpp:318`](../../../src/toolboxes/ode/src/ode45.cpp#L318) | The 'y_new' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (1)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [`src/toolboxes/ode/src/options.cpp:120`](../../../src/toolboxes/ode/src/options.cpp#L120) | A part of conditional expression is always true: name.numel() >= 0. Unsigned type value is always >= 0. |

</details>
