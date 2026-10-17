# `io` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **0** | 0 | 0 |
| 🟢 **Low** | **5** | 3 | 2 |
| **Total** | **5** | 3 | 2 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V815](https://pvs-studio.com/en/docs/warnings/v815/) | 0 | 0 | 3 | 2 | 1 | **3** |
| [V688](https://pvs-studio.com/en/docs/warnings/v688/) | 0 | 0 | 1 | 1 | 0 | **1** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |


<details>
<summary><b>🟢 Low Severity (5)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V688](https://pvs-studio.com/en/docs/warnings/v688/) | [`src/toolboxes/io/tests/fileio_test.cpp:2054`](../../../src/toolboxes/io/tests/fileio_test.cpp#L2054) | The 'fs' local variable possesses the same name as one of the class members, which can result in a confusion. |
| [V815](https://pvs-studio.com/en/docs/warnings/v815/) | [`src/toolboxes/io/tests/fileio_test.cpp:678`](../../../src/toolboxes/io/tests/fileio_test.cpp#L678) | Decreased performance. Consider replacing the expression 'fs->files()["empty.bin"] = ""' with 'fs->files()["empty.bin"].clear()'. |
| [V815](https://pvs-studio.com/en/docs/warnings/v815/) | [`src/toolboxes/io/tests/fileio_test.cpp:2013`](../../../src/toolboxes/io/tests/fileio_test.cpp#L2013) | Decreased performance. Consider replacing the expression 'fs->files()["empty.txt"] = ""' with 'fs->files()["empty.txt"].clear()'. |
| [V815](https://pvs-studio.com/en/docs/warnings/v815/) | [`src/toolboxes/io/src/paths/paths.cpp:95`](../../../src/toolboxes/io/src/paths/paths.cpp#L95) | Decreased performance. Consider replacing the expression 'folder = ""' with 'folder.clear()'. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/io/src/paths/paths.cpp:133`](../../../src/toolboxes/io/src/paths/paths.cpp#L133) | Decreased performance. The 'p' variable can be constructed in a lower level scope. |

</details>
