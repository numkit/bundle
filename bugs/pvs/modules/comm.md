# `comm` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **5** | 0 | 5 |
| 🟡 **Medium** | **1** | 0 | 1 |
| 🟢 **Low** | **7** | 1 | 6 |
| **Total** | **13** | 1 | 12 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 3 | 0 | 0 | 0 | 3 | **3** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | 0 | 0 | 2 | 1 | 1 | **2** |
| [V501](https://pvs-studio.com/en/docs/warnings/v501/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V610](https://pvs-studio.com/en/docs/warnings/v610/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V501](https://pvs-studio.com/en/docs/warnings/v501/) | - | [`src/toolboxes/comm/src/channel/channel.cpp:244`](../../../src/toolboxes/comm/src/channel/channel.cpp#L244) | There are identical sub-expressions to the left and to the right of the '/' operator: std::pow(half, n) / std::pow(half, n) |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/comm/src/coding/blockcoding.cpp:98`](../../../src/toolboxes/comm/src/coding/blockcoding.cpp#L98) | Possible overflow. Consider casting operands, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/comm/src/modulation/fsk_ofdm.cpp:150`](../../../src/toolboxes/comm/src/modulation/fsk_ofdm.cpp#L150) | Possible overflow. Consider casting operands of the 'nfft + cplen' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/comm/src/modulation/fsk_ofdm.cpp:197`](../../../src/toolboxes/comm/src/modulation/fsk_ofdm.cpp#L197) | Possible overflow. Consider casting operands of the 'nfft + cplen' operator to the 'size_t' type, not the result. |
| [V610](https://pvs-studio.com/en/docs/warnings/v610/) | [CWE-758](https://cwe.mitre.org/data/definitions/758.html) | [`src/toolboxes/comm/src/source/base_conversions.cpp:88`](../../../src/toolboxes/comm/src/source/base_conversions.cpp#L88) | Undefined behavior. Check the shift operator '>>'. The right operand is negative ('bitPos' = [-63..63]). |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/comm/src/coding/blockcoding.cpp:500`](../../../src/toolboxes/comm/src/coding/blockcoding.cpp#L500) | The 'e' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (7)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | [`src/toolboxes/comm/src/channel/channel.cpp:407`](../../../src/toolboxes/comm/src/channel/channel.cpp#L407) | The 'then' statement is equivalent to the 'else' statement. |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | [`src/toolboxes/comm/src/channel/channel.cpp:410`](../../../src/toolboxes/comm/src/channel/channel.cpp#L410) | The 'then' statement is equivalent to the 'else' statement. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/comm/src/coding/convcoding.cpp:120`](../../../src/toolboxes/comm/src/coding/convcoding.cpp#L120) | Variables 'ns', 'ou' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 119, 120. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/comm/src/source/dpcm.cpp:76`](../../../src/toolboxes/comm/src/source/dpcm.cpp#L76) | Variables 'indx_v', 'quanterr_v' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 74, 76. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/comm/src/source/dpcm.cpp:112`](../../../src/toolboxes/comm/src/source/dpcm.cpp#L112) | Variables 'sig_v', 'quanterr_v' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 110, 112. |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | [`src/toolboxes/comm/tests/arity_bounds_test.cpp:97`](../../../src/toolboxes/comm/tests/arity_bounds_test.cpp#L97) | Passing cheap-to-copy argument by reference may lead to decreased performance. To avoid this, replace the first argument 'const Case& c' with 'Case c'. |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | [`src/toolboxes/comm/src/source/huffman.cpp:39`](../../../src/toolboxes/comm/src/source/huffman.cpp#L39) | Passing cheap-to-copy argument by reference may lead to decreased performance. To avoid this, replace the first argument 'const HeapNode& b' with 'HeapNode b'. |

</details>
