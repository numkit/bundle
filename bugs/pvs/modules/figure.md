# `figure` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **5** | 0 | 5 |
| 🟡 **Medium** | **8** | 0 | 8 |
| 🟢 **Low** | **6** | 0 | 6 |
| **Total** | **19** | 0 | 19 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V609](https://pvs-studio.com/en/docs/warnings/v609/) | 2 | 0 | 0 | 0 | 2 | **2** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V1034](https://pvs-studio.com/en/docs/warnings/v1034/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V814](https://pvs-studio.com/en/docs/warnings/v814/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V838](https://pvs-studio.com/en/docs/warnings/v838/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/figure/include/nk/figure/figure_render.hpp:2016`](../../../src/figure/include/nk/figure/figure_render.hpp#L2016) | Possible overflow. Consider casting operands of the 'y * w_ + x' operator to the 'size_t' type, not the result. |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | [CWE-783](https://cwe.mitre.org/data/definitions/783.html) | [`src/figure/include/nk/figure/figure_render.hpp:1308`](../../../src/figure/include/nk/figure/figure_render.hpp#L1308) | The '?:' operator, regardless of its conditional expression, always returns one and the same value: 1.4. |
| [V609](https://pvs-studio.com/en/docs/warnings/v609/) | [CWE-369](https://cwe.mitre.org/data/definitions/369.html) | [`src/figure/include/nk/figure/figure_render.hpp:2034`](../../../src/figure/include/nk/figure/figure_render.hpp#L2034) | Divide by zero. Denominator range [0x0..0x7FFFFFFF]. |
| [V609](https://pvs-studio.com/en/docs/warnings/v609/) | [CWE-369](https://cwe.mitre.org/data/definitions/369.html) | [`src/figure/include/nk/figure/figure_render.hpp:2039`](../../../src/figure/include/nk/figure/figure_render.hpp#L2039) | Divide by zero. Denominator range [0x0..0x7FFFFFFF]. |
| [V814](https://pvs-studio.com/en/docs/warnings/v814/) | - | [`src/figure/include/nk/figure/figure_render.hpp:318`](../../../src/figure/include/nk/figure/figure_render.hpp#L318) | Decreased performance. Calls to the 'strlen' function have being made multiple times when a condition for the loop's continuation was calculated. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/figure/include/nk/figure/figure_render.hpp:758`](../../../src/figure/include/nk/figure/figure_render.hpp#L758) | Variables 'xs', 'ys' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'ax.datasets.size()' expression. |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | [CWE-457](https://cwe.mitre.org/data/definitions/457.html) | [`src/figure/include/nk/figure/figure_render.hpp:357`](../../../src/figure/include/nk/figure/figure_render.hpp#L357) | Not all members of a class are initialized inside the compiler generated constructor. Consider inspecting: kind. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/figure/include/nk/figure/figure_manager.hpp:669`](../../../src/figure/include/nk/figure/figure_manager.hpp#L669) | Consider inspecting the 'current' function. The return value is not always used. Total calls: 52, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/figure/include/nk/figure/figure_manager.hpp:681`](../../../src/figure/include/nk/figure/figure_manager.hpp#L681) | Consider inspecting the 'currentAxes' function. The return value is not always used. Total calls: 41, discarded results: 2. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/figure/include/nk/figure/figure_manager.hpp:821`](../../../src/figure/include/nk/figure/figure_manager.hpp#L821) | The 'savedColorScale' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | - | [`src/figure/include/nk/figure/figure_render.hpp:114`](../../../src/figure/include/nk/figure/figure_render.hpp#L114) | On 64-bit platform, structure size can be reduced from 24 to 16 bytes by rearranging the fields according to their sizes in decreasing order. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/figure/include/nk/figure/figure_render.hpp:707`](../../../src/figure/include/nk/figure/figure_render.hpp#L707) | Decreased performance. The 'box' argument should probably be rendered as a constant reference. |
| [V838](https://pvs-studio.com/en/docs/warnings/v838/) | - | [`src/figure/include/nk/figure/figure_render.hpp:330`](../../../src/figure/include/nk/figure/figure_render.hpp#L330) | Temporary object is constructed during the call of the 'find' function. Consider using an ordered associative container with heterogeneous lookup to avoid construction of temporary objects. |


<details>
<summary><b>🟢 Low Severity (6)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V1034](https://pvs-studio.com/en/docs/warnings/v1034/) | [`src/figure/include/nk/figure/figure_render.hpp:533`](../../../src/figure/include/nk/figure/figure_render.hpp#L533) | Do not use real type variables as loop counters. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/figure/include/nk/figure/figure_render.hpp:82`](../../../src/figure/include/nk/figure/figure_render.hpp#L82) | Two or more case-branches perform the same actions. Check lines: 82, 85 |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/figure/include/nk/figure/figure_render.hpp:204`](../../../src/figure/include/nk/figure/figure_render.hpp#L204) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/figure/include/nk/figure/figure_render.hpp:245`](../../../src/figure/include/nk/figure/figure_render.hpp#L245) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/figure/include/nk/figure/figure_render.hpp:250`](../../../src/figure/include/nk/figure/figure_render.hpp#L250) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/figure/include/nk/figure/figure_render.hpp:711`](../../../src/figure/include/nk/figure/figure_render.hpp#L711) | Decreased performance. The 'kGridCol' variable can be constructed in a lower level scope. |

</details>
