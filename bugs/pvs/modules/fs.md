# `fs` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **1** | 0 | 1 |
| 🟢 **Low** | **2** | 0 | 2 |
| **Total** | **3** | 0 | 3 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 1 | 1 | 0 | 2 | **2** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/fs/src/vfs.cpp:74`](../../../src/fs/src/vfs.cpp#L74) | The 'fs.kind' variable was assigned the same value. |


<details>
<summary><b>🟢 Low Severity (2)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/fs/src/vfs.cpp:67`](../../../src/fs/src/vfs.cpp#L67) | The 'fs.size' variable was assigned the same value. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/fs/src/vfs.cpp:78`](../../../src/fs/src/vfs.cpp#L78) | Decreased performance. The 't' variable can be constructed in a lower level scope. |

</details>
