# `linalg` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **2** | 0 | 2 |
| 🟡 **Medium** | **8** | 0 | 8 |
| 🟢 **Low** | **31** | 0 | 31 |
| **Total** | **41** | 0 | 41 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 5 | 9 | 0 | 14 | **14** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 11 | 0 | 11 | **11** |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | 0 | 0 | 5 | 0 | 5 | **5** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1057](https://pvs-studio.com/en/docs/warnings/v1057/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | [CWE-691](https://cwe.mitre.org/data/definitions/691.html) | [`src/toolboxes/linalg/src/linalg_detail.hpp:184`](../../../src/toolboxes/linalg/src/linalg_detail.hpp#L184) | The 'then' statement is equivalent to the 'else' statement. |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | - | [`src/toolboxes/linalg/src/schur_convert.cpp:180`](../../../src/toolboxes/linalg/src/schur_convert.cpp#L180) | 'lam2' object of 'complex <double>' type was created but was not utilized. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/linalg/src/balance.cpp:154`](../../../src/toolboxes/linalg/src/balance.cpp#L154) | Expression 'n > 0' is always true. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/linalg/src/eig.cpp:820`](../../../src/toolboxes/linalg/src/eig.cpp#L820) | A part of conditional expression is always true: k + 1 < N. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/linalg/src/eig.cpp:190`](../../../src/toolboxes/linalg/src/eig.cpp#L190) | Variables 'Vout', 'Dout' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 189, 190. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/linalg/src/eig.cpp:259`](../../../src/toolboxes/linalg/src/eig.cpp#L259) | Variables 'Vout', 'Dout' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'Value::complexMatrix(n, n, mr)' expression. Check lines: 258, 259. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/linalg/src/eig.cpp:300`](../../../src/toolboxes/linalg/src/eig.cpp#L300) | Variables 'Vr', 'Dr' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 299, 300. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/linalg/src/eig.cpp:453`](../../../src/toolboxes/linalg/src/eig.cpp#L453) | Variables 'Vout', 'Dout' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 452, 453. |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | [CWE-683](https://cwe.mitre.org/data/definitions/683.html) | [`src/toolboxes/linalg/src/predicates.cpp:94`](../../../src/toolboxes/linalg/src/predicates.cpp#L94) | Possible incorrect order of arguments passed to 'lin' function: 'j' and 'i'. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/linalg/src/schur_convert.cpp:71`](../../../src/toolboxes/linalg/src/schur_convert.cpp#L71) | Variables 'VRout', 'DRout' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 70, 71. |


<details>
<summary><b>🟢 Low Severity (31)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/balance.cpp:144`](../../../src/toolboxes/linalg/src/balance.cpp#L144) | Variables 'R.d_col', 'R.perm_col' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 143, 144. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/eig.cpp:672`](../../../src/toolboxes/linalg/src/eig.cpp#L672) | Variables 'Hout', 'Pout' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'Value::complexMatrix(n, n, mr)' expression. Check lines: 671, 672. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/eig.cpp:679`](../../../src/toolboxes/linalg/src/eig.cpp#L679) | Variables 'Hout', 'Pout' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 678, 679. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/eig.cpp:883`](../../../src/toolboxes/linalg/src/eig.cpp#L883) | Variables 'U', 'T' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'Value::complexMatrix(n, n, mr)' expression. Check lines: 882, 883. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/eig.cpp:892`](../../../src/toolboxes/linalg/src/eig.cpp#L892) | Variables 'U', 'T' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 891, 892. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/linalg/src/gsvd.cpp:42`](../../../src/toolboxes/linalg/src/gsvd.cpp#L42) | The code contains the collection of similar blocks. Check items 'Ac', 'Ac', 'Bc' in lines 42, 43, 44. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/linalg/src/gsvd.cpp:135`](../../../src/toolboxes/linalg/src/gsvd.cpp#L135) | The code contains the collection of similar blocks. Check items 'Ac', 'Ac', 'Bc' in lines 135, 136, 137. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/ldl.cpp:103`](../../../src/toolboxes/linalg/src/ldl.cpp#L103) | Variables 'L0', 'D0' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 102, 103. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/linalg/src/matrix_functions.cpp:98`](../../../src/toolboxes/linalg/src/matrix_functions.cpp#L98) | The code contains the collection of similar blocks. Check items 'A_s', 'A2', 'A2' in lines 98, 99, 100. |
| [V1051](https://pvs-studio.com/en/docs/warnings/v1051/) | [`src/toolboxes/linalg/src/misc.cpp:64`](../../../src/toolboxes/linalg/src/misc.cpp#L64) | Consider checking for misprints. It's possible that the 'tol' should be checked here. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/ordschur.cpp:157`](../../../src/toolboxes/linalg/src/ordschur.cpp#L157) | Variables 'U_out', 'T_out' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'Value::complexMatrix(n, n, mr)' expression. Check lines: 156, 157. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/linalg/src/page_ops.cpp:444`](../../../src/toolboxes/linalg/src/page_ops.cpp#L444) | There might be dereferencing of a potential null pointer 'xd'. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/page_ops.cpp:166`](../../../src/toolboxes/linalg/src/page_ops.cpp#L166) | Variables 'V', 'D' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 165, 166. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/linalg/src/qz.cpp:215`](../../../src/toolboxes/linalg/src/qz.cpp#L215) | The code contains the collection of similar blocks. Check items 'k', 'k', '0' in lines 215, 216, 217. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/linalg/src/schur_convert.cpp:235`](../../../src/toolboxes/linalg/src/schur_convert.cpp#L235) | Variables 'Uout', 'Tout' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 234, 235. |
| [V1057](https://pvs-studio.com/en/docs/warnings/v1057/) | [`src/toolboxes/linalg/src/svd_sketch.cpp:89`](../../../src/toolboxes/linalg/src/svd_sketch.cpp#L89) | Pseudo random sequence is the same at every program run. Consider assigning the seed to a value not known at compile-time. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/linalg/src/svd_sketch.cpp:28`](../../../src/toolboxes/linalg/src/svd_sketch.cpp#L28) | The code contains the collection of similar blocks. Check items 'A', 'A', 'B' in lines 28, 29, 30. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | [`src/toolboxes/linalg/src/linalg_detail.hpp:145`](../../../src/toolboxes/linalg/src/linalg_detail.hpp#L145) | Passing 'std::move' function's result as lvalue reference to const parameter disables move semantics. Check the 'first' parameter of the 'Error' constructor. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/ordqz.cpp:37`](../../../src/toolboxes/linalg/src/ordqz.cpp#L37) | Decreased performance. The 'v1' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/ordqz.cpp:76`](../../../src/toolboxes/linalg/src/ordqz.cpp#L76) | Decreased performance. The 'b11_new' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/ordschur.cpp:30`](../../../src/toolboxes/linalg/src/ordschur.cpp#L30) | Decreased performance. The 'x' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:184`](../../../src/toolboxes/linalg/src/qz.cpp#L184) | Decreased performance. The 'a11' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:184`](../../../src/toolboxes/linalg/src/qz.cpp#L184) | Decreased performance. The 'a12' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:185`](../../../src/toolboxes/linalg/src/qz.cpp#L185) | Decreased performance. The 'a21' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:186`](../../../src/toolboxes/linalg/src/qz.cpp#L186) | Decreased performance. The 'b11' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:186`](../../../src/toolboxes/linalg/src/qz.cpp#L186) | Decreased performance. The 'b12' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:187`](../../../src/toolboxes/linalg/src/qz.cpp#L187) | Decreased performance. The 'b21' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:196`](../../../src/toolboxes/linalg/src/qz.cpp#L196) | Decreased performance. The 'c1' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/linalg/src/qz.cpp:197`](../../../src/toolboxes/linalg/src/qz.cpp#L197) | Decreased performance. The 'c0' variable can be constructed in a lower level scope. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/toolboxes/linalg/src/solvers.cpp:80`](../../../src/toolboxes/linalg/src/solvers.cpp#L80) | The 'tmp' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/toolboxes/linalg/src/solvers.cpp:87`](../../../src/toolboxes/linalg/src/solvers.cpp#L87) | The 'tmp' variable is not used after copying. Copying can be replaced with move/swap for optimization. |

</details>
