# `ops` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **3** | 0 | 3 |
| 🟡 **Medium** | **2** | 0 | 2 |
| 🟢 **Low** | **9** | 0 | 9 |
| **Total** | **14** | 0 | 14 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 2 | 0 | 0 | 0 | 2 | **2** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 1 | 0 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/ops/include/nk/ops/poly_helpers.hpp:119`](../../../src/ops/include/nk/ops/poly_helpers.hpp#L119) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/ops/include/nk/ops/poly_helpers.hpp:124`](../../../src/ops/include/nk/ops/poly_helpers.hpp#L124) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'std::size_t' type, not the result. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/ops/src/compression/deflate.cpp:590`](../../../src/ops/src/compression/deflate.cpp#L590) | Expression 'rem != 0' is always false. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/ops/include/nk/ops/value_factory.hpp:28`](../../../src/ops/include/nk/ops/value_factory.hpp#L28) | Decreased performance. The 'd' argument should probably be rendered as a constant reference. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/ops/include/nk/ops/io_helpers.hpp:68`](../../../src/ops/include/nk/ops/io_helpers.hpp#L68) | Decreased performance. The 'sz' argument should probably be rendered as a constant reference. |


<details>
<summary><b>🟢 Low Severity (9)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/ops/include/nk/ops/rng_context.hpp:81`](../../../src/ops/include/nk/ops/rng_context.hpp#L81) | Variables 'v1', 'v2' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the '2.0 * v4Uniform() - 1.0' expression. Check lines: 80, 81. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/ops/include/nk/ops/reductions.hpp:319`](../../../src/ops/include/nk/ops/reductions.hpp#L319) | Variables 'out', 'outIdx' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 316, 319. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/ops/include/nk/ops/reductions.hpp:130`](../../../src/ops/include/nk/ops/reductions.hpp#L130) | The 'src' pointer in the 'src + base' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/ops/include/nk/ops/reductions.hpp:216`](../../../src/ops/include/nk/ops/reductions.hpp#L216) | The 'src' pointer in the 'src + o * sliceLen' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/ops/include/nk/ops/reductions.hpp:217`](../../../src/ops/include/nk/ops/reductions.hpp#L217) | The 'base' pointer in the 'base + sliceLen' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | [`src/ops/src/compression/deflate.cpp:480`](../../../src/ops/src/compression/deflate.cpp#L480) | Consider checking for misprints. It's possible that the 'bestDist' should be checked here. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/ops/src/compression/deflate.cpp:229`](../../../src/ops/src/compression/deflate.cpp#L229) | The code contains the collection of similar blocks. Check items '8', '9', '7', '8' in lines 229, 230, 231, 232. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/ops/src/blas/blas3_highway.cpp:878`](../../../src/ops/src/blas/blas3_highway.cpp#L878) | Decreased performance. The 'f0' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/ops/src/blas/blas3_highway.cpp:879`](../../../src/ops/src/blas/blas3_highway.cpp#L879) | Decreased performance. The 'f1' variable can be constructed in a lower level scope. |

</details>
