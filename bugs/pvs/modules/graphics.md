# `graphics` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **16** | 0 | 16 |
| 🟢 **Low** | **15** | 2 | 13 |
| **Total** | **31** | 2 | 29 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 11 | 0 | 0 | 11 | **11** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 1 | 7 | 0 | 8 | **8** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 3 | 0 | 0 | 3 | **3** |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V575](https://pvs-studio.com/en/docs/warnings/v575/) | 0 | 0 | 2 | 2 | 0 | **2** |
| [V1034](https://pvs-studio.com/en/docs/warnings/v1034/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/graphics/src/plots/bar.cpp:152`](../../../src/graphics/src/plots/bar.cpp#L152) | Expression 'Yc > 1' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/graphics/src/plots/bar.cpp:385`](../../../src/graphics/src/plots/bar.cpp#L385) | Expression 'xs.size() > 1' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/bar.cpp:1477`](../../../src/graphics/src/plots/bar.cpp#L1477) | Expression 'm == 1' is always false. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/graphics/src/plots/helpers.cpp:94`](../../../src/graphics/src/plots/helpers.cpp#L94) | The 'nvStart' variable was assigned the same value. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/graphics/src/plots/layout.cpp:1230`](../../../src/graphics/src/plots/layout.cpp#L1230) | Variables 'xv', 'yv' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 1229, 1230. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:215`](../../../src/graphics/src/plots/surface.cpp#L215) | A part of conditional expression is always false: !V. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/graphics/src/plots/surface.cpp:411`](../../../src/graphics/src/plots/surface.cpp#L411) | A part of conditional expression is always true: sx. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/graphics/src/plots/surface.cpp:417`](../../../src/graphics/src/plots/surface.cpp#L417) | A part of conditional expression is always true: sy. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/graphics/src/plots/surface.cpp:423`](../../../src/graphics/src/plots/surface.cpp#L423) | A part of conditional expression is always true: sz. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:430`](../../../src/graphics/src/plots/surface.cpp#L430) | A part of conditional expression is always false: !sx. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:430`](../../../src/graphics/src/plots/surface.cpp#L430) | A part of conditional expression is always false: !sy. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:431`](../../../src/graphics/src/plots/surface.cpp#L431) | A part of conditional expression is always false: !sz. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:942`](../../../src/graphics/src/plots/surface.cpp#L942) | A part of conditional expression is always false: !U. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:942`](../../../src/graphics/src/plots/surface.cpp#L942) | A part of conditional expression is always false: !Vv. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:942`](../../../src/graphics/src/plots/surface.cpp#L942) | A part of conditional expression is always false: !W. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/graphics/src/plots/surface.cpp:1147`](../../../src/graphics/src/plots/surface.cpp#L1147) | A part of conditional expression is always false: !U. |


<details>
<summary><b>🟢 Low Severity (15)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V575](https://pvs-studio.com/en/docs/warnings/v575/) | [`src/graphics/tests/figure_export_test.cpp:62`](../../../src/graphics/tests/figure_export_test.cpp#L62) | The potential null pointer is passed into 'fread' function. Inspect the fourth argument. |
| [V575](https://pvs-studio.com/en/docs/warnings/v575/) | [`src/graphics/tests/figure_export_test.cpp:313`](../../../src/graphics/tests/figure_export_test.cpp#L313) | The potential null pointer is passed into 'fread' function. Inspect the fourth argument. |
| [V1034](https://pvs-studio.com/en/docs/warnings/v1034/) | [`src/graphics/src/plots/bar.cpp:754`](../../../src/graphics/src/plots/bar.cpp#L754) | Do not use real type variables as loop counters. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/bar.cpp:594`](../../../src/graphics/src/plots/bar.cpp#L594) | Variables 'mn', 'mx' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'data.elemAsDouble(0)' expression. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/bar.cpp:603`](../../../src/graphics/src/plots/bar.cpp#L603) | Variables 'centers', 'counts' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 602, 603. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/bar.cpp:1638`](../../../src/graphics/src/plots/bar.cpp#L1638) | Variables 'ax.xTickLabelsJson', 'ax.yTickLabelsJson' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'js.str()' expression. Check lines: 1637, 1638. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/bar.cpp:1647`](../../../src/graphics/src/plots/bar.cpp#L1647) | Variables 'ax.xTicksJson', 'ax.yTicksJson' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'ts.str()' expression. Check lines: 1646, 1647. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/graphics/src/plots/line.cpp:359`](../../../src/graphics/src/plots/line.cpp#L359) | There might be dereferencing of a potential null pointer 'xData'. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/graphics/src/plots/line.cpp:537`](../../../src/graphics/src/plots/line.cpp#L537) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/graphics/src/plots/line.cpp:652`](../../../src/graphics/src/plots/line.cpp#L652) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/line.cpp:566`](../../../src/graphics/src/plots/line.cpp#L566) | Variables 'Xv', 'Yv' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 565, 566. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/line.cpp:601`](../../../src/graphics/src/plots/line.cpp#L601) | Variables 'Xv', 'Yv' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 600, 601. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/graphics/src/plots/line.cpp:644`](../../../src/graphics/src/plots/line.cpp#L644) | Variables 'x', 'y' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'std::nan("")' expression. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/graphics/src/plots/shared.cpp:146`](../../../src/graphics/src/plots/shared.cpp#L146) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | [`src/graphics/src/plots/contour.cpp:345`](../../../src/graphics/src/plots/contour.cpp#L345) | Passing cheap-to-copy argument by reference may lead to decreased performance. To avoid this, replace the first argument 'const Pt& p' with 'Pt p'. |

</details>
