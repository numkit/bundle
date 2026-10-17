# `runtime` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **2** | 0 | 2 |
| 🟡 **Medium** | **15** | 0 | 15 |
| 🟢 **Low** | **11** | 1 | 10 |
| **Total** | **28** | 1 | 27 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 12 | 1 | 0 | 13 | **13** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 5 | 0 | 5 | **5** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 2 | 0 | 0 | 0 | 2 | **2** |
| [V575](https://pvs-studio.com/en/docs/warnings/v575/) | 0 | 0 | 1 | 1 | 0 | **1** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V719](https://pvs-studio.com/en/docs/warnings/v719/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/runtime/src/saveload_mat.cpp:615`](../../../src/runtime/src/saveload_mat.cpp#L615) | Possible overflow. Consider casting operands of the 'rows * cols' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/runtime/src/saveload_mat.cpp:676`](../../../src/runtime/src/saveload_mat.cpp#L676) | Possible overflow. Consider casting operands of the 'rows * cols' operator to the 'std::size_t' type, not the result. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:247`](../../../src/runtime/src/saveload_mat.cpp#L247) | The 'arrayClass' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:259`](../../../src/runtime/src/saveload_mat.cpp#L259) | The 'arrayClass' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:263`](../../../src/runtime/src/saveload_mat.cpp#L263) | The 'arrayClass' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:264`](../../../src/runtime/src/saveload_mat.cpp#L264) | The 'arrayClass' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:371`](../../../src/runtime/src/saveload_mat.cpp#L371) | The 'dt' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:371`](../../../src/runtime/src/saveload_mat.cpp#L371) | The 'elemSize' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:380`](../../../src/runtime/src/saveload_mat.cpp#L380) | The 'elemSize' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:381`](../../../src/runtime/src/saveload_mat.cpp#L381) | The 'elemSize' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:382`](../../../src/runtime/src/saveload_mat.cpp#L382) | The 'dt' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:382`](../../../src/runtime/src/saveload_mat.cpp#L382) | The 'elemSize' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:533`](../../../src/runtime/src/saveload_mat.cpp#L533) | The 'vt' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/runtime/src/saveload_mat.cpp:543`](../../../src/runtime/src/saveload_mat.cpp#L543) | The 'vt' variable was assigned the same value. |
| [V719](https://pvs-studio.com/en/docs/warnings/v719/) | - | [`src/runtime/src/_handlefn_helpers.hpp:102`](../../../src/runtime/src/_handlefn_helpers.hpp#L102) | The switch statement does not cover all values of the 'ValueType' enum: CSL, OBJECT. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/runtime/src/diagnostics.cpp:73`](../../../src/runtime/src/diagnostics.cpp#L73) | The 'first' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | - | [`src/runtime/src/splitapply_callback.cpp:42`](../../../src/runtime/src/splitapply_callback.cpp#L42) | Passing the const-qualified object 'kv.second' to the 'std::move' function disables move semantics. |


<details>
<summary><b>🟢 Low Severity (11)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V575](https://pvs-studio.com/en/docs/warnings/v575/) | [`src/runtime/tests/coder_test.cpp:120`](../../../src/runtime/tests/coder_test.cpp#L120) | The potential null pointer is passed into 'fputs' function. Inspect the second argument. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/runtime/src/containers.cpp:271`](../../../src/runtime/src/containers.cpp#L271) | The 'dict.isHandle' variable was assigned the same value. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/runtime/src/containers.cpp:312`](../../../src/runtime/src/containers.cpp#L312) | There might be dereferencing of a potential null pointer 'cst(self)'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/runtime/src/containers.cpp:317`](../../../src/runtime/src/containers.cpp#L317) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/runtime/src/containers.cpp:360`](../../../src/runtime/src/containers.cpp#L360) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/runtime/src/containers.cpp:400`](../../../src/runtime/src/containers.cpp#L400) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/runtime/src/containers.cpp:417`](../../../src/runtime/src/containers.cpp#L417) | There might be dereferencing of a potential null pointer 'p'. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/runtime/src/saveload_mat.cpp:247`](../../../src/runtime/src/saveload_mat.cpp#L247) | Two or more case-branches perform the same actions. Check lines: 247, 263 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/runtime/src/saveload_mat.cpp:374`](../../../src/runtime/src/saveload_mat.cpp#L374) | Two or more case-branches perform the same actions. Check lines: 374, 375 |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/runtime/src/scan_io.cpp:372`](../../../src/runtime/src/scan_io.cpp#L372) | Variables 'numCols', 'strCols' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'convs.size(), & scratch' expression. Check lines: 371, 372. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/runtime/src/_handlefn_helpers.hpp:103`](../../../src/runtime/src/_handlefn_helpers.hpp#L103) | Two or more case-branches perform the same actions. Check lines: 103, 105, 120 |

</details>
