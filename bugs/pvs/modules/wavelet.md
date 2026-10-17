# `wavelet` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **11** | 0 | 11 |
| 🟡 **Medium** | **6** | 0 | 6 |
| 🟢 **Low** | **9** | 0 | 9 |
| **Total** | **26** | 0 | 26 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 10 | 0 | 0 | 0 | 10 | **10** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 2 | 6 | 0 | 8 | **8** |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 3 | 0 | 0 | 3 | **3** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1008](https://pvs-studio.com/en/docs/warnings/v1008/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1008](https://pvs-studio.com/en/docs/warnings/v1008/) | [CWE-691](https://cwe.mitre.org/data/definitions/691.html) | [`src/toolboxes/wavelet/src/denoise/denoise.cpp:154`](../../../src/toolboxes/wavelet/src/denoise/denoise.cpp#L154) | Consider inspecting the 'for' operator. No more than one iteration of the loop will be performed. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/dwt/multilevel.cpp:222`](../../../src/toolboxes/wavelet/src/dwt/multilevel.cpp#L222) | Possible overflow. Consider casting operands of the 'nMax - level + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/dwt/multilevel2.cpp:146`](../../../src/toolboxes/wavelet/src/dwt/multilevel2.cpp#L146) | Possible overflow. Consider casting operands of the 'N - m + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/dwt/multilevel2.cpp:152`](../../../src/toolboxes/wavelet/src/dwt/multilevel2.cpp#L152) | Possible overflow. Consider casting operands of the 'N - lev + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/dwt/multilevel2.cpp:207`](../../../src/toolboxes/wavelet/src/dwt/multilevel2.cpp#L207) | Possible overflow. Consider casting operands of the 'N - lev + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/dwt/multilevel2.cpp:209`](../../../src/toolboxes/wavelet/src/dwt/multilevel2.cpp#L209) | Possible overflow. Consider casting operands of the 'N - level + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:170`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L170) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:175`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L175) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:384`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L384) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:405`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L405) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:408`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L408) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/wavelet/src/dwt/haart.cpp:161`](../../../src/toolboxes/wavelet/src/dwt/haart.cpp#L161) | Variables 'aMat', 'dMat' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'Value::matrix(H, ncols, vt, mr)' expression. Check lines: 160, 161. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/toolboxes/wavelet/src/dwt/multilevel2.cpp:133`](../../../src/toolboxes/wavelet/src/dwt/multilevel2.cpp#L133) | A part of conditional expression is always false: level < 0. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp:179`](../../../src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp#L179) | The 'start1' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp:423`](../../../src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp#L423) | The 'extRows' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp:424`](../../../src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp#L424) | The 'extCols' variable was assigned the same value. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/wavelet/src/swt/swt.cpp:115`](../../../src/toolboxes/wavelet/src/swt/swt.cpp#L115) | Variables 'swa', 'swd' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 113, 115. |


<details>
<summary><b>🟢 Low Severity (9)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/wavelet/src/denoise/denoise.cpp:124`](../../../src/toolboxes/wavelet/src/denoise/denoise.cpp#L124) | There might be dereferencing of a potential null pointer 'yd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/wavelet/src/dwt/dwt.cpp:226`](../../../src/toolboxes/wavelet/src/dwt/dwt.cpp#L226) | There might be dereferencing of a potential null pointer 'rd'. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:52`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L52) | Variables 'loM', 'hiM' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 51, 52. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:95`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L95) | Variables 'loM', 'hiM' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 94, 95. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:133`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L133) | Variables 'colA', 'colD' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 132, 133. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:163`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L163) | Variables 'rowA', 'rowD' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 162, 163. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:264`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L264) | Variables 'a', 'd' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 263, 264. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/wavelet/src/dwt/dwt2.cpp:270`](../../../src/toolboxes/wavelet/src/dwt/dwt2.cpp#L270) | Variables 'a', 'd' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 269, 270. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [`src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp:474`](../../../src/toolboxes/wavelet/src/dwt/wkeep_wextend.cpp#L474) | Expression 's.size() >= 1' is always true. |

</details>
