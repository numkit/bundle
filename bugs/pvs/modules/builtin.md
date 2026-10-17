# `builtin` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **8** | 0 | 8 |
| 🟡 **Medium** | **43** | 1 | 42 |
| 🟢 **Low** | **27** | 0 | 27 |
| **Total** | **78** | 1 | 77 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | 0 | 26 | 0 | 0 | 26 | **26** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 7 | 0 | 7 | **7** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 3 | 0 | 3 | 0 | 6 | **6** |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | 0 | 0 | 6 | 0 | 6 | **6** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 5 | 0 | 0 | 5 | **5** |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | 0 | 0 | 4 | 0 | 4 | **4** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 3 | 0 | 0 | 0 | 3 | **3** |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | 0 | 3 | 0 | 0 | 3 | **3** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | 0 | 2 | 0 | 0 | 2 | **2** |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1008](https://pvs-studio.com/en/docs/warnings/v1008/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V601](https://pvs-studio.com/en/docs/warnings/v601/) | 0 | 1 | 0 | 1 | 0 | **1** |
| [V624](https://pvs-studio.com/en/docs/warnings/v624/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V636](https://pvs-studio.com/en/docs/warnings/v636/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V751](https://pvs-studio.com/en/docs/warnings/v751/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V839](https://pvs-studio.com/en/docs/warnings/v839/) | 1 | 0 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [CWE-628](https://cwe.mitre.org/data/definitions/628.html) | [`src/builtin/src/polyfun/integration.cpp:338`](../../../src/builtin/src/polyfun/integration.cpp#L338) | Dereferencing of the null pointer 'x' might take place. The null pointer is passed into 'cumtrapzVector' function. Inspect the second argument. Check lines: 338, 468. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [CWE-628](https://cwe.mitre.org/data/definitions/628.html) | [`src/builtin/src/polyfun/integration.cpp:395`](../../../src/builtin/src/polyfun/integration.cpp#L395) | Dereferencing of the null pointer 'x' might take place. The null pointer is passed into 'cumtrapzVectorC' function. Inspect the second argument. Check lines: 395, 463. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/builtin/src/polyfun/polynomials.cpp:1027`](../../../src/builtin/src/polyfun/polynomials.cpp#L1027) | Possible overflow. Consider casting operands of the 'np * np' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/builtin/src/polyfun/polynomials.cpp:1039`](../../../src/builtin/src/polyfun/polynomials.cpp#L1039) | Possible overflow. Consider casting operands, not the result. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [CWE-628](https://cwe.mitre.org/data/definitions/628.html) | [`src/builtin/src/polyfun/polynomials_detail.hpp:81`](../../../src/builtin/src/polyfun/polynomials_detail.hpp#L81) | Dereferencing of the null pointer 'v' might take place. The null pointer is passed into 'rowFromVec' function. Inspect the first argument. Check lines: 'polynomials_detail.hpp:81', 'polynomials.cpp:189'. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/builtin/src/specfun/special.cpp:666`](../../../src/builtin/src/specfun/special.cpp#L666) | Possible overflow. Consider casting operands of the 'n + 1' operator to the 'size_t' type, not the result. |
| [V1008](https://pvs-studio.com/en/docs/warnings/v1008/) | [CWE-691](https://cwe.mitre.org/data/definitions/691.html) | [`src/builtin/src/datafun/reductions_detail.hpp:74`](../../../src/builtin/src/datafun/reductions_detail.hpp#L74) | Consider inspecting the 'for' operator. No more than one iteration of the loop will be performed. |
| [V839](https://pvs-studio.com/en/docs/warnings/v839/) | - | [`src/builtin/src/strfun/strings_detail.hpp:814`](../../../src/builtin/src/strfun/strings_detail.hpp#L814) | The 'strInput' function returns a constant value. This may interfere with move semantics. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/builtin/src/datafun/logical_reductions_highway.cpp:237`](../../../src/builtin/src/datafun/logical_reductions_highway.cpp#L237) | A part of conditional expression is always true: d >= 1. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/builtin/src/elmat/matrix.cpp:1536`](../../../src/builtin/src/elmat/matrix.cpp#L1536) | A part of conditional expression is always true: d >= 1. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/specfun/discrete_detail.hpp:270`](../../../src/builtin/src/specfun/discrete_detail.hpp#L270) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/specfun/discrete_detail.hpp:304`](../../../src/builtin/src/specfun/discrete_detail.hpp#L304) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/datafun/discrete_detail.hpp:271`](../../../src/builtin/src/datafun/discrete_detail.hpp#L271) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/datafun/discrete_detail.hpp:305`](../../../src/builtin/src/datafun/discrete_detail.hpp#L305) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/datatypes/types_detail.hpp:52`](../../../src/builtin/src/datatypes/types_detail.hpp#L52) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/datatypes/types_detail.hpp:301`](../../../src/builtin/src/datatypes/types_detail.hpp#L301) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/manip_detail.hpp:352`](../../../src/builtin/src/elmat/manip_detail.hpp#L352) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:35`](../../../src/builtin/src/elmat/matrix_detail.hpp#L35) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:124`](../../../src/builtin/src/elmat/matrix_detail.hpp#L124) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:138`](../../../src/builtin/src/elmat/matrix_detail.hpp#L138) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:692`](../../../src/builtin/src/elmat/matrix_detail.hpp#L692) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:1021`](../../../src/builtin/src/elmat/matrix_detail.hpp#L1021) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:1052`](../../../src/builtin/src/elmat/matrix_detail.hpp#L1052) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/elmat/matrix_detail.hpp:1239`](../../../src/builtin/src/elmat/matrix_detail.hpp#L1239) | Do not define an unnamed namespace in a header file. |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | [CWE-683](https://cwe.mitre.org/data/definitions/683.html) | [`src/builtin/src/ops/unary_ops_detail.hpp:61`](../../../src/builtin/src/ops/unary_ops_detail.hpp#L61) | Possible incorrect order of arguments passed to 'complexMatrix' function: 'cols' and 'rows'. |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | [CWE-683](https://cwe.mitre.org/data/definitions/683.html) | [`src/builtin/src/ops/unary_ops_detail.hpp:72`](../../../src/builtin/src/ops/unary_ops_detail.hpp#L72) | Possible incorrect order of arguments passed to 'cell' function: 'cols' and 'rows'. |
| [V764](https://pvs-studio.com/en/docs/warnings/v764/) | [CWE-683](https://cwe.mitre.org/data/definitions/683.html) | [`src/builtin/src/ops/unary_ops_detail.hpp:90`](../../../src/builtin/src/ops/unary_ops_detail.hpp#L90) | Possible incorrect order of arguments passed to 'matrix' function: 'cols' and 'rows'. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/polyfun/interp_detail.hpp:903`](../../../src/builtin/src/polyfun/interp_detail.hpp#L903) | Do not define an unnamed namespace in a header file. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/builtin/src/polyfun/interp_detail.hpp:154`](../../../src/builtin/src/polyfun/interp_detail.hpp#L154) | Expression 'm >= 2' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/builtin/src/polyfun/interp_detail.hpp:177`](../../../src/builtin/src/polyfun/interp_detail.hpp#L177) | Expression 'm >= 2' is always true. |
| [V751](https://pvs-studio.com/en/docs/warnings/v751/) | - | [`src/builtin/src/polyfun/interp_detail.hpp:117`](../../../src/builtin/src/polyfun/interp_detail.hpp#L117) | Parameter 'x' is not used inside function body. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/polyfun/polynomials_detail.hpp:31`](../../../src/builtin/src/polyfun/polynomials_detail.hpp#L31) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/polyfun/polynomials_detail.hpp:94`](../../../src/builtin/src/polyfun/polynomials_detail.hpp#L94) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/regex_detail.hpp:33`](../../../src/builtin/src/strfun/regex_detail.hpp#L33) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:274`](../../../src/builtin/src/strfun/strings_detail.hpp#L274) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:354`](../../../src/builtin/src/strfun/strings_detail.hpp#L354) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:479`](../../../src/builtin/src/strfun/strings_detail.hpp#L479) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:531`](../../../src/builtin/src/strfun/strings_detail.hpp#L531) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:609`](../../../src/builtin/src/strfun/strings_detail.hpp#L609) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:638`](../../../src/builtin/src/strfun/strings_detail.hpp#L638) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:740`](../../../src/builtin/src/strfun/strings_detail.hpp#L740) | Do not define an unnamed namespace in a header file. |
| [V1068](https://pvs-studio.com/en/docs/warnings/v1068/) | - | [`src/builtin/src/strfun/strings_detail.hpp:797`](../../../src/builtin/src/strfun/strings_detail.hpp#L797) | Do not define an unnamed namespace in a header file. |
| [V601](https://pvs-studio.com/en/docs/warnings/v601/) | [CWE-704](https://cwe.mitre.org/data/definitions/704.html) | [`src/builtin/tests/lang_test.cpp:48`](../../../src/builtin/tests/lang_test.cpp#L48) | The bool type is implicitly cast to the class type. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/builtin/src/elfun/trig_recip_highway.cpp:92`](../../../src/builtin/src/elfun/trig_recip_highway.cpp#L92) | Decreased performance. The 'v' argument should probably be rendered as a constant reference. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/builtin/src/polyfun/polynomials.cpp:517`](../../../src/builtin/src/polyfun/polynomials.cpp#L517) | The 'B' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/builtin/src/polyfun/polynomials.cpp:639`](../../../src/builtin/src/polyfun/polynomials.cpp#L639) | The 'poles' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/builtin/src/polyfun/polynomials.cpp:762`](../../../src/builtin/src/polyfun/polynomials.cpp#L762) | The 'av' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/builtin/src/polyfun/polynomials.cpp:762`](../../../src/builtin/src/polyfun/polynomials.cpp#L762) | The 'bv' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/builtin/src/polyfun/polynomials.cpp:779`](../../../src/builtin/src/polyfun/polynomials.cpp#L779) | The 'B' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V813](https://pvs-studio.com/en/docs/warnings/v813/) | - | [`src/builtin/src/strfun/scan.cpp:275`](../../../src/builtin/src/strfun/scan.cpp#L275) | Decreased performance. The 'sz' argument should probably be rendered as a constant reference. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | - | [`src/builtin/include/nk/builtin/datafun.hpp:260`](../../../src/builtin/include/nk/builtin/datafun.hpp#L260) | On 64-bit platform, structure size can be reduced from 56 to 40 bytes by rearranging the fields according to their sizes in decreasing order. |


<details>
<summary><b>🟢 Low Severity (27)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/builtin/src/datafun/accum.cpp:43`](../../../src/builtin/src/datafun/accum.cpp#L43) | Two or more case-branches perform the same actions. Check lines: 43, 44, 48 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/builtin/src/datafun/accum.cpp:45`](../../../src/builtin/src/datafun/accum.cpp#L45) | Two or more case-branches perform the same actions. Check lines: 45, 49 |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/datafun/var_reduction_highway.cpp:30`](../../../src/builtin/src/datafun/var_reduction_highway.cpp#L30) | Variables 'a0', 'a1' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'hn::Zero(d)' expression. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/datafun/var_reduction_highway.cpp:81`](../../../src/builtin/src/datafun/var_reduction_highway.cpp#L81) | Variables 'a0', 'a1' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'hn::Zero(d)' expression. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/builtin/src/elmat/manip.cpp:592`](../../../src/builtin/src/elmat/manip.cpp#L592) | The 'dst' pointer in the 'dst + dstOuterOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/builtin/src/elmat/manip.cpp:592`](../../../src/builtin/src/elmat/manip.cpp#L592) | The 'src' pointer in the 'src + srcOuterOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/elmat/matrix.cpp:1081`](../../../src/builtin/src/elmat/matrix.cpp#L1081) | Variables 'r', 'idx' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 1079, 1081. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/elmat/matrix.cpp:1252`](../../../src/builtin/src/elmat/matrix.cpp#L1252) | Variables 'X', 'Y' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 1251, 1252. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/elmat/matrix.cpp:1294`](../../../src/builtin/src/elmat/matrix.cpp#L1294) | Variables 'X', 'Y' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 1293, 1294. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/builtin/src/elmat/nd_manip.cpp:169`](../../../src/builtin/src/elmat/nd_manip.cpp#L169) | The 'dst' pointer in the 'dst + dstOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/builtin/src/elmat/nd_manip.cpp:169`](../../../src/builtin/src/elmat/nd_manip.cpp#L169) | The 'src' pointer in the 'src + srcOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/src/iofun/formatted_io.cpp:35`](../../../src/builtin/src/iofun/formatted_io.cpp#L35) | It is odd that the body of 'textscan' function is fully equivalent to the body of 'sscanf' function. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/builtin/src/polyfun/integration.cpp:339`](../../../src/builtin/src/polyfun/integration.cpp#L339) | Dereferencing of the null pointer 'y' might take place. The potential null pointer is passed into 'cumtrapzVector' function. Inspect the first argument. Check lines: 339, 494. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/builtin/src/polyfun/integration.cpp:396`](../../../src/builtin/src/polyfun/integration.cpp#L396) | Dereferencing of the null pointer 'y' might take place. The potential null pointer is passed into 'cumtrapzVectorC' function. Inspect the first argument. Check lines: 396, 493. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/polyfun/polynomials.cpp:389`](../../../src/builtin/src/polyfun/polynomials.cpp#L389) | Variables 'numV', 'denV' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 388, 389. |
| [V636](https://pvs-studio.com/en/docs/warnings/v636/) | [`src/builtin/src/specfun/special.cpp:58`](../../../src/builtin/src/specfun/special.cpp#L58) | The 'm * (m + n)' expression was implicitly cast from 'int' type to 'double' type. Consider utilizing an explicit type cast to avoid overflow. An example: double A = (double)(X) * Y;. |
| [V624](https://pvs-studio.com/en/docs/warnings/v624/) | [`src/builtin/src/specfun/special_highway.cpp:173`](../../../src/builtin/src/specfun/special_highway.cpp#L173) | The constant 0.69314718055966295651160180568695068359375 is being utilized. The resulting value could be inaccurate. Consider using the M_LN2 constant from <math.h>. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/src/polyfun/interp_detail.hpp:601`](../../../src/builtin/src/polyfun/interp_detail.hpp#L601) | It is odd that the body of 'keysCubic' function is fully equivalent to the body of 'keys1d' function. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/builtin/src/strfun/strings_detail.hpp:124`](../../../src/builtin/src/strfun/strings_detail.hpp#L124) | Variables 'commonLead', 'commonTrail' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'lines.empty() ? 0 : lines[0].size()' expression. Check lines: 123, 124. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/include/nk/builtin/ops.hpp:373`](../../../src/builtin/include/nk/builtin/ops.hpp#L373) | It is odd that the body of 'logicalAnd' function is fully equivalent to the body of 'and_op' function. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/include/nk/builtin/ops.hpp:376`](../../../src/builtin/include/nk/builtin/ops.hpp#L376) | It is odd that the body of 'logicalOr' function is fully equivalent to the body of 'or_op' function. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/include/nk/builtin/ops.hpp:379`](../../../src/builtin/include/nk/builtin/ops.hpp#L379) | It is odd that the body of 'logicalNot' function is fully equivalent to the body of 'not_op' function. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/builtin/include/nk/builtin/ops.hpp:382`](../../../src/builtin/include/nk/builtin/ops.hpp#L382) | It is odd that the body of 'logicalXor' function is fully equivalent to the body of 'xor_op' function. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/builtin/src/datafun/discrete_detail.hpp:175`](../../../src/builtin/src/datafun/discrete_detail.hpp#L175) | Dereferencing of the null pointer 'p' might take place. The potential null pointer is passed into 'rowHasNan' function. Inspect the first argument. Check lines: 'discrete_detail.hpp:175', 'math_discrete_reg.cpp:596'. |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | [`src/builtin/src/datafun/sets.cpp:376`](../../../src/builtin/src/datafun/sets.cpp#L376) | Passing cheap-to-copy argument by reference may lead to decreased performance. To avoid this, replace the first argument 'const CxKey& o' with 'CxKey o'. |
| [V835](https://pvs-studio.com/en/docs/warnings/v835/) | [`src/builtin/src/datafun/sets.cpp:378`](../../../src/builtin/src/datafun/sets.cpp#L378) | Passing cheap-to-copy argument by reference may lead to decreased performance. To avoid this, replace the first argument 'const CxKey& k' with 'CxKey k'. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/builtin/src/polyfun/polynomials.cpp:879`](../../../src/builtin/src/polyfun/polynomials.cpp#L879) | Decreased performance. The 'h' variable can be constructed in a lower level scope. |

</details>
