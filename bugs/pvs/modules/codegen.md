# `codegen` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **13** | 1 | 12 |
| 🟢 **Low** | **25** | 1 | 24 |
| **Total** | **38** | 2 | 36 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 10 | 0 | 10 | **10** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 6 | 0 | 6 | **6** |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | 0 | 3 | 0 | 1 | 2 | **3** |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V1004](https://pvs-studio.com/en/docs/warnings/v1004/) | 0 | 1 | 1 | 0 | 2 | **2** |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V728](https://pvs-studio.com/en/docs/warnings/v728/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V553](https://pvs-studio.com/en/docs/warnings/v553/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V778](https://pvs-studio.com/en/docs/warnings/v778/) | 0 | 0 | 1 | 1 | 0 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/codegen/include/nk/codegen/emitter.hpp:108`](../../../src/codegen/include/nk/codegen/emitter.hpp#L108) | Consider inspecting the 'emitFunction' function. The return value is not always used. Total calls: 36, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/codegen/include/nk/codegen/emitter.hpp:125`](../../../src/codegen/include/nk/codegen/emitter.hpp#L125) | Consider inspecting the 'emitProgram' function. The return value is not always used. Total calls: 25, discarded results: 2. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/codegen/tests/emitter_test.cpp:21`](../../../src/codegen/tests/emitter_test.cpp#L21) | Consider inspecting the 'emit' function. The return value is not always used. Total calls: 14, discarded results: 1. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/codegen/src/aot.cpp:86`](../../../src/codegen/src/aot.cpp#L86) | The 'r.status' variable was assigned the same value. |
| [V1004](https://pvs-studio.com/en/docs/warnings/v1004/) | [CWE-476](https://cwe.mitre.org/data/definitions/476.html) | [`src/codegen/src/emitter.cpp:1635`](../../../src/codegen/src/emitter.cpp#L1635) | The 'ci' pointer was used unsafely after it was verified against nullptr. Check lines: 1615, 1635. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/codegen/src/emitter.cpp:5484`](../../../src/codegen/src/emitter.cpp#L5484) | The 'reverse' variable was assigned the same value. |
| [V728](https://pvs-studio.com/en/docs/warnings/v728/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/codegen/src/emitter.cpp:7590`](../../../src/codegen/src/emitter.cpp#L7590) | An excessive check can be simplified. The '&#124;&#124;' operator is surrounded by opposite expressions 'arrays_.at(el->strValue).is2D' and '!arrays_.at(el->strValue).is2D'.  |
| [V728](https://pvs-studio.com/en/docs/warnings/v728/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/codegen/src/emitter.cpp:7724`](../../../src/codegen/src/emitter.cpp#L7724) | An excessive check can be simplified. The '&#124;&#124;' operator is surrounded by opposite expressions. |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | [CWE-457](https://cwe.mitre.org/data/definitions/457.html) | [`src/codegen/src/emitter.cpp:180`](../../../src/codegen/src/emitter.cpp#L180) | Not all members of a class are initialized inside the compiler generated constructor. Consider inspecting: dtype. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/codegen/include/nk/codegen/transfer.hpp:40`](../../../src/codegen/include/nk/codegen/transfer.hpp#L40) | Decreased performance. The 't' argument should probably be rendered as a constant reference. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/codegen/include/nk/codegen/type_lattice.hpp:121`](../../../src/codegen/include/nk/codegen/type_lattice.hpp#L121) | Decreased performance. The 's' argument should probably be rendered as a constant reference. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/codegen/src/emitter.cpp:456`](../../../src/codegen/src/emitter.cpp#L456) | The 'bound' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/codegen/src/emitter.cpp:1674`](../../../src/codegen/src/emitter.cpp#L1674) | The 'argTypes' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (25)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:115`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L115) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:143`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L143) | There might be dereferencing of a potential null pointer 'elems'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:162`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L162) | There might be dereferencing of a potential null pointer 'elems'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:178`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L178) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:192`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L192) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:207`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L207) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:221`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L221) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:236`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L236) | There might be dereferencing of a potential null pointer 'p'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/bridge/nk_codegen_rt.cpp:269`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L269) | There might be dereferencing of a potential null pointer 'args'. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/codegen/bridge/nk_codegen_rt.cpp:566`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L566) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/codegen/bridge/nk_codegen_rt.cpp:589`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L589) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/codegen/bridge/nk_codegen_rt.cpp:604`](../../../src/codegen/bridge/nk_codegen_rt.cpp#L604) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V778](https://pvs-studio.com/en/docs/warnings/v778/) | [`src/codegen/tests/transfer_test.cpp:142`](../../../src/codegen/tests/transfer_test.cpp#L142) | Two similar code fragments were found. Perhaps, this is a typo and 'COMPLEX' variable should be used instead of 'DOUBLE'. |
| [V1004](https://pvs-studio.com/en/docs/warnings/v1004/) | [`src/codegen/src/emitter.cpp:1629`](../../../src/codegen/src/emitter.cpp#L1629) | The 'ci' pointer was used unsafely after it was verified against nullptr. Check lines: 1615, 1629. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/codegen/src/emitter.cpp:33`](../../../src/codegen/src/emitter.cpp#L33) | Two or more case-branches perform the same actions. Check lines: 33, 36 |
| [V553](https://pvs-studio.com/en/docs/warnings/v553/) | [`src/codegen/src/emitter.cpp:2649`](../../../src/codegen/src/emitter.cpp#L2649) | The length of 'emitAssign' function's body is more than 2000 lines long. You should consider refactoring the code. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/codegen/src/inference.cpp:757`](../../../src/codegen/src/inference.cpp#L757) | There might be dereferencing of a potential null pointer 'lhs.children[1]'. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/codegen/src/transfer/shape.cpp:244`](../../../src/codegen/src/transfer/shape.cpp#L244) | It is odd that the body of 'unionMultiTransfer' function is fully equivalent to the body of 'intersectMultiTransfer' function. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/codegen/src/transfer/shape.cpp:793`](../../../src/codegen/src/transfer/shape.cpp#L793) | It is odd that the body of 'identityShape1or2Transfer' function is fully equivalent to the body of 'trilTriuTransfer' function. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:2957`](../../../src/codegen/src/emitter.cpp#L2957) | Decreased performance. The 'Acols' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:2957`](../../../src/codegen/src/emitter.cpp#L2957) | Decreased performance. The 'Arows' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:2994`](../../../src/codegen/src/emitter.cpp#L2994) | Decreased performance. The 'Acols' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:2994`](../../../src/codegen/src/emitter.cpp#L2994) | Decreased performance. The 'Arows' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:3521`](../../../src/codegen/src/emitter.cpp#L3521) | Decreased performance. The 'cmp' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/codegen/src/emitter.cpp:3727`](../../../src/codegen/src/emitter.cpp#L3727) | Decreased performance. The 'Bn' variable can be constructed in a lower level scope. |

</details>
