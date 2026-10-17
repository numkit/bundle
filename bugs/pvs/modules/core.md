# `core` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **0** | 0 | 0 |
| 🟡 **Medium** | **25** | 1 | 24 |
| 🟢 **Low** | **32** | 2 | 30 |
| **Total** | **57** | 3 | 54 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 5 | 11 | 2 | 14 | **16** |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | 0 | 9 | 0 | 1 | 8 | **9** |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | 0 | 2 | 3 | 0 | 5 | **5** |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | 0 | 0 | 4 | 0 | 4 | **4** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | 0 | 0 | 3 | 0 | 3 | **3** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 2 | 1 | 0 | 3 | **3** |
| [V1096](https://pvs-studio.com/en/docs/warnings/v1096/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | 0 | 1 | 1 | 0 | 2 | **2** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1029](https://pvs-studio.com/en/docs/warnings/v1029/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V553](https://pvs-studio.com/en/docs/warnings/v553/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V571](https://pvs-studio.com/en/docs/warnings/v571/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/compiler.hpp:284`](../../../src/core/include/nk/core/compiler.hpp#L284) | Consider inspecting the 'tempReg' function. The return value is not always used. Total calls: 111, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/compiler.hpp:321`](../../../src/core/include/nk/core/compiler.hpp#L321) | Consider inspecting the 'compileNode' function. The return value is not always used. Total calls: 104, discarded results: 9. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/parser.hpp:64`](../../../src/core/include/nk/core/parser.hpp#L64) | Consider inspecting the 'match' function. The return value is not always used. Total calls: 17, discarded results: 1. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/core/src/compiler.cpp:1954`](../../../src/core/src/compiler.cpp#L1954) | The 'stepReg' variable was assigned the same value. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/core/src/compiler.cpp:878`](../../../src/core/src/compiler.cpp#L878) | A part of conditional expression is always true: !node->lhsTargets.empty(). |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/core/src/compiler.cpp:3637`](../../../src/core/src/compiler.cpp#L3637) | A part of conditional expression is always true: nargs > 0. |
| [V571](https://pvs-studio.com/en/docs/warnings/v571/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/core/src/compiler.cpp:4805`](../../../src/core/src/compiler.cpp#L4805) | Recurring check. The 'ins.d < (int16_t) chunk.constants.size()' condition was already verified in line 4804. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/core/src/engine.cpp:2880`](../../../src/core/src/engine.cpp#L2880) | The 'node->suppressOutput' variable was assigned the same value. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/core/src/engine.cpp:1715`](../../../src/core/src/engine.cpp#L1715) | Expression 'next == s' is always true. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/core/src/parser.cpp:17`](../../../src/core/src/parser.cpp#L17) | The 'eof.type' variable was assigned the same value. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [CWE-691](https://cwe.mitre.org/data/definitions/691.html) | [`src/core/src/vm.cpp:2384`](../../../src/core/src/vm.cpp#L2384) | Two or more case-branches perform the same actions. Check lines: 2384, 2473 |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/core/src/vm.cpp:898`](../../../src/core/src/vm.cpp#L898) | The 'fs.rangeType' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/core/src/vm.cpp:938`](../../../src/core/src/vm.cpp#L938) | The 'fs.rangeType' variable was assigned the same value. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/core/src/vm.cpp:481`](../../../src/core/src/vm.cpp#L481) | Expression '!frames_.empty()' is always true. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/debug_session.hpp:49`](../../../src/core/include/nk/core/debug_session.hpp#L49) | Consider inspecting the 'start' function. The return value is not always used. Total calls: 35, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/debug_session.hpp:52`](../../../src/core/include/nk/core/debug_session.hpp#L52) | Consider inspecting the 'resume' function. The return value is not always used. Total calls: 65, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/engine.hpp:334`](../../../src/core/include/nk/core/engine.hpp#L334) | Consider inspecting the 'eval' function. The return value is not always used. Total calls: 11, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/engine.hpp:334`](../../../src/core/include/nk/core/engine.hpp#L334) | Consider inspecting the 'eval' function. The return value is not always used. Total calls: 120, discarded results: 1. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/include/nk/core/engine.hpp:334`](../../../src/core/include/nk/core/engine.hpp#L334) | Consider inspecting the 'eval' function. The return value is not always used. Total calls: 28, discarded results: 2. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/core/tests/parser_test.cpp:13`](../../../src/core/tests/parser_test.cpp#L13) | Consider inspecting the 'parseSource' function. The return value is not always used. Total calls: 206, discarded results: 18. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | - | [`src/core/src/compiler.cpp:2867`](../../../src/core/src/compiler.cpp#L2867) | On 64-bit platform, structure size can be reduced from 24 to 16 bytes by rearranging the fields according to their sizes in decreasing order. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | - | [`src/core/src/compiler.cpp:4257`](../../../src/core/src/compiler.cpp#L4257) | Passing the const-qualified object 'entry.second' to the 'std::move' function disables move semantics. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/core/src/engine.cpp:233`](../../../src/core/src/engine.cpp#L233) | The 'hdr' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/core/src/engine.cpp:2442`](../../../src/core/src/engine.cpp#L2442) | The 'userPath' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | - | [`src/core/src/engine.cpp:2701`](../../../src/core/src/engine.cpp#L2701) | Passing the const-qualified object 'entry.second' to the 'std::move' function disables move semantics. |


<details>
<summary><b>🟢 Low Severity (32)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V1096](https://pvs-studio.com/en/docs/warnings/v1096/) | [`src/core/include/nk/core/vm.hpp:157`](../../../src/core/include/nk/core/vm.hpp#L157) | The 'kEmpty' variable with static storage duration is declared inside the inline function with external linkage. This may lead to ODR violation. |
| [V1096](https://pvs-studio.com/en/docs/warnings/v1096/) | [`src/core/include/nk/core/vm.hpp:219`](../../../src/core/include/nk/core/vm.hpp#L219) | The 'kEmpty' variable with static storage duration is declared inside the inline function with external linkage. This may lead to ODR violation. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/core/include/nk/core/debug_session.hpp:178`](../../../src/core/include/nk/core/debug_session.hpp#L178) | It is odd that the body of 'onBreakpoint' function is fully equivalent to the body of 'onLine' function. |
| [V1029](https://pvs-studio.com/en/docs/warnings/v1029/) | [`src/core/src/compiler.cpp:3997`](../../../src/core/src/compiler.cpp#L3997) | Numeric Truncation Error. Return value of the 'size' function is written to the 8-bit variable. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/core/src/debug_session.cpp:294`](../../../src/core/src/debug_session.cpp#L294) | There might be dereferencing of a potential null pointer 'ctl->currentFrame()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/core/src/debug_session.cpp:413`](../../../src/core/src/debug_session.cpp#L413) | There might be dereferencing of a potential null pointer 'ctl->currentFrame()'. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/core/src/engine.cpp:662`](../../../src/core/src/engine.cpp#L662) | It is odd that the body of 'accessWord' function is fully equivalent to the body of 'accessName' function. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/core/src/engine.cpp:2068`](../../../src/core/src/engine.cpp#L2068) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/core/src/engine.cpp:2419`](../../../src/core/src/engine.cpp#L2419) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/core/src/engine.cpp:2429`](../../../src/core/src/engine.cpp#L2429) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V565](https://pvs-studio.com/en/docs/warnings/v565/) | [`src/core/src/engine.cpp:2473`](../../../src/core/src/engine.cpp#L2473) | An empty exception handler. Silent suppression of exceptions can hide the presence of bugs in source code during testing. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/core/src/environment.cpp:130`](../../../src/core/src/environment.cpp#L130) | It is odd that the body of 'setLocalFast' function is fully equivalent to the body of 'setLocal' function. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/parser.cpp:20`](../../../src/core/src/parser.cpp#L20) | The 'eof.col' variable was assigned the same value. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/core/src/parser.cpp:524`](../../../src/core/src/parser.cpp#L524) | There might be dereferencing of a potential null pointer 'expr'. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:441`](../../../src/core/src/vm.cpp#L441) | The 'cf.regBase' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:443`](../../../src/core/src/vm.cpp#L443) | The 'cf.forStackBase' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:444`](../../../src/core/src/vm.cpp#L444) | The 'cf.tryStackBase' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:892`](../../../src/core/src/vm.cpp#L892) | The 'fs.index' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:896`](../../../src/core/src/vm.cpp#L896) | The 'fs.rows' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:897`](../../../src/core/src/vm.cpp#L897) | The 'fs.data' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:900`](../../../src/core/src/vm.cpp#L900) | The 'fs.count' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/src/vm.cpp:935`](../../../src/core/src/vm.cpp#L935) | The 'fs.index' variable was assigned the same value. |
| [V553](https://pvs-studio.com/en/docs/warnings/v553/) | [`src/core/src/vm.cpp:507`](../../../src/core/src/vm.cpp#L507) | The length of 'dispatchLoop' function's body is more than 2000 lines long. You should consider refactoring the code. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/tests/object_model_test.cpp:57`](../../../src/core/tests/object_model_test.cpp#L57) | The 'valCls.isHandle' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/core/tests/object_model_test.cpp:150`](../../../src/core/tests/object_model_test.cpp#L150) | The 'pt.isHandle' variable was assigned the same value. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | [`src/core/include/nk/core/vm.hpp:310`](../../../src/core/include/nk/core/vm.hpp#L310) | On 64-bit platform, structure size can be reduced from 88 to 80 bytes by rearranging the fields according to their sizes in decreasing order. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | [`src/core/src/engine.cpp:795`](../../../src/core/src/engine.cpp#L795) | Passing 'std::move' function's result as lvalue reference to const parameter disables move semantics. Check the 'fifth' parameter of the 'registerClassDefImpl_' function. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | [`src/core/src/engine.cpp:795`](../../../src/core/src/engine.cpp#L795) | Passing 'std::move' function's result as lvalue reference to const parameter disables move semantics. Check the 'fourth' parameter of the 'registerClassDefImpl_' function. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | [`src/core/src/engine.cpp:795`](../../../src/core/src/engine.cpp#L795) | Passing 'std::move' function's result as lvalue reference to const parameter disables move semantics. Check the 'sixth' parameter of the 'registerClassDefImpl_' function. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/core/src/environment.cpp:162`](../../../src/core/src/environment.cpp#L162) | The 'newParent' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/core/src/tree_walker.cpp:1132`](../../../src/core/src/tree_walker.cpp#L1132) | Decreased performance. The 'fname' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/core/src/vm.cpp:302`](../../../src/core/src/vm.cpp#L302) | Decreased performance. The 'restorer' variable can be constructed in a lower level scope. |

</details>
