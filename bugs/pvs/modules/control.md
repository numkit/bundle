# `control` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **1** | 0 | 1 |
| 🟡 **Medium** | **12** | 0 | 12 |
| 🟢 **Low** | **16** | 0 | 16 |
| **Total** | **29** | 0 | 29 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 12 | 2 | 0 | 14 | **14** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 6 | 0 | 6 | **6** |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | 0 | 0 | 5 | 0 | 5 | **5** |
| [V519](https://pvs-studio.com/en/docs/warnings/v519/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | 0 | 0 | 1 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | - | [`src/toolboxes/control/src/state/place.cpp:107`](../../../src/toolboxes/control/src/state/place.cpp#L107) | 'B' object of 'vector' type was created but was not utilized. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/conversion/conversion.cpp:306`](../../../src/toolboxes/control/src/conversion/conversion.cpp#L306) | The 'numAcc' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/conversion/conversion.cpp:309`](../../../src/toolboxes/control/src/conversion/conversion.cpp#L309) | The 'coeff' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/discretize/discretize.cpp:149`](../../../src/toolboxes/control/src/discretize/discretize.cpp#L149) | The 'Mplus' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/discretize/discretize.cpp:182`](../../../src/toolboxes/control/src/discretize/discretize.cpp#L182) | The 'Mminus' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/discretize/discretize.cpp:325`](../../../src/toolboxes/control/src/discretize/discretize.cpp#L325) | The 'Aminus' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/internal/numerics.cpp:130`](../../../src/toolboxes/control/src/internal/numerics.cpp#L130) | The 'D' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/internal/numerics.cpp:131`](../../../src/toolboxes/control/src/internal/numerics.cpp#L131) | The 'N' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/internal/numerics.cpp:135`](../../../src/toolboxes/control/src/internal/numerics.cpp#L135) | The 'I' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/internal/numerics.cpp:142`](../../../src/toolboxes/control/src/internal/numerics.cpp#L142) | The 'E' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/riccati/riccati.cpp:293`](../../../src/toolboxes/control/src/riccati/riccati.cpp#L293) | The 'Sp' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/state/state.cpp:115`](../../../src/toolboxes/control/src/state/state.cpp#L115) | The 'B' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/control/src/state/state.cpp:158`](../../../src/toolboxes/control/src/state/state.cpp#L158) | The 'C' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (16)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V519](https://pvs-studio.com/en/docs/warnings/v519/) | [`src/toolboxes/control/src/analyze/analyze.cpp:331`](../../../src/toolboxes/control/src/analyze/analyze.cpp#L331) | The 'y' variable is assigned values twice successively. Perhaps this is a mistake. Check lines: 321, 331. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/control/src/analyze/hinfnorm.cpp:263`](../../../src/toolboxes/control/src/analyze/hinfnorm.cpp#L263) | The code contains the collection of similar blocks. Check items 'rows', 'cols', 'rows' in lines 263, 264, 265. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/discretize/discretize.cpp:143`](../../../src/toolboxes/control/src/discretize/discretize.cpp#L143) | Variables 'Mminus', 'Mplus' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'eyeM(n)' expression. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/discretize/discretize.cpp:314`](../../../src/toolboxes/control/src/discretize/discretize.cpp#L314) | Variables 'Aplus', 'Aminus' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 's.A.size(), 0.0' expression. Check lines: 313, 314. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/freq/freq.cpp:202`](../../../src/toolboxes/control/src/freq/freq.cpp#L202) | Variables 'mag', 'phase' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'w.size()' expression. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/freq/freq.cpp:226`](../../../src/toolboxes/control/src/freq/freq.cpp#L226) | Variables 're', 'im' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'w.size()' expression. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/control/src/internal/numerics.cpp:112`](../../../src/toolboxes/control/src/internal/numerics.cpp#L112) | The code contains the collection of similar blocks. Check items 'A', 'A', 'A2', 'A', 'A2' in lines 112, 113, 114, 115, 116. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/internal/numerics.cpp:121`](../../../src/toolboxes/control/src/internal/numerics.cpp#L121) | Variables 'N', 'D' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'zerosM(n, n)' expression. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/control/src/props/props.cpp:222`](../../../src/toolboxes/control/src/props/props.cpp#L222) | Variables 'wn', 'zeta' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 221, 222. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/control/src/riccati/riccati.cpp:200`](../../../src/toolboxes/control/src/riccati/riccati.cpp#L200) | The code contains the collection of similar blocks. Check items 'n', 'n', 'n', 'm' in lines 200, 201, 202, 203. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/control/src/riccati/riccati.cpp:254`](../../../src/toolboxes/control/src/riccati/riccati.cpp#L254) | The code contains the collection of similar blocks. Check items 'n', 'n', 'n', 'm' in lines 254, 255, 256, 257. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/toolboxes/control/src/state/state.cpp:250`](../../../src/toolboxes/control/src/state/state.cpp#L250) | The code contains the collection of similar blocks. Check items 'rows', 'cols', 'rows' in lines 250, 251, 252. |
| [V833](https://pvs-studio.com/en/docs/warnings/v833/) | [`src/toolboxes/control/include/nk/control/internal/type_gates.hpp:168`](../../../src/toolboxes/control/include/nk/control/internal/type_gates.hpp#L168) | Passing 'std::move' function's result as lvalue reference to const parameter disables move semantics. Check the 'first' parameter of the 'Error' constructor. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/toolboxes/control/src/conversion/conversion.cpp:113`](../../../src/toolboxes/control/src/conversion/conversion.cpp#L113) | The 'scaled' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/toolboxes/control/src/conversion/conversion.cpp:119`](../../../src/toolboxes/control/src/conversion/conversion.cpp#L119) | The 'scaled' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/control/src/freq/freq.cpp:246`](../../../src/toolboxes/control/src/freq/freq.cpp#L246) | Decreased performance. The 'num' variable can be constructed in a lower level scope. |

</details>
