# `value` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **2** | 0 | 2 |
| 🟡 **Medium** | **0** | 0 | 0 |
| 🟢 **Low** | **38** | 0 | 38 |
| **Total** | **40** | 0 | 40 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 18 | 0 | 18 | **18** |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | 0 | 0 | 5 | 0 | 5 | **5** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 4 | 0 | 4 | **4** |
| [V1111](https://pvs-studio.com/en/docs/warnings/v1111/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V595](https://pvs-studio.com/en/docs/warnings/v595/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V773](https://pvs-studio.com/en/docs/warnings/v773/) | 1 | 0 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V595](https://pvs-studio.com/en/docs/warnings/v595/) | [CWE-476](https://cwe.mitre.org/data/definitions/476.html) | [`src/value/src/value.cpp:3785`](../../../src/value/src/value.cpp#L3785) | The 'heap_' pointer was utilized before it was verified against nullptr. Check lines: 3785, 3808. |
| [V773](https://pvs-studio.com/en/docs/warnings/v773/) | [CWE-401](https://cwe.mitre.org/data/definitions/401.html) | [`src/value/src/value.cpp:2682`](../../../src/value/src/value.cpp#L2682) | The exception was thrown without releasing the 'h' pointer. A memory leak is possible. |


<details>
<summary><b>🟢 Low Severity (38)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/value/include/nk/value/value.hpp:676`](../../../src/value/include/nk/value/value.hpp#L676) | It is odd that the body of 'isHeap' function is fully equivalent to the body of 'hasHeap' function. |
| [V524](https://pvs-studio.com/en/docs/warnings/v524/) | [`src/value/include/nk/value/argcheck.hpp:160`](../../../src/value/include/nk/value/argcheck.hpp#L160) | It is odd that the body of 'reshapeSizeReal' function is fully equivalent to the body of 'arrayDimReal' function. |
| [V525](https://pvs-studio.com/en/docs/warnings/v525/) | [`src/value/src/dims.cpp:23`](../../../src/value/src/dims.cpp#L23) | The code contains the collection of similar blocks. Check items 'r', 'c', '1', '1' in lines 23, 24, 25, 26. |
| [V1111](https://pvs-studio.com/en/docs/warnings/v1111/) | [`src/value/src/value.cpp:3612`](../../../src/value/src/value.cpp#L3612) | The third argument in function call was used without check after it was checked in previous lines. |
| [V1111](https://pvs-studio.com/en/docs/warnings/v1111/) | [`src/value/src/value.cpp:3678`](../../../src/value/src/value.cpp#L3678) | The third argument in function call was used without check after it was checked in previous lines. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3196`](../../../src/value/src/value.cpp#L3196) | There might be dereferencing of a potential null pointer 'complexData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3200`](../../../src/value/src/value.cpp#L3200) | There might be dereferencing of a potential null pointer 'complexData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3297`](../../../src/value/src/value.cpp#L3297) | There might be dereferencing of a potential null pointer 'doubleData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3301`](../../../src/value/src/value.cpp#L3301) | There might be dereferencing of a potential null pointer 'doubleData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3305`](../../../src/value/src/value.cpp#L3305) | There might be dereferencing of a potential null pointer 'doubleData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3311`](../../../src/value/src/value.cpp#L3311) | There might be dereferencing of a potential null pointer 'doubleDataMut()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3315`](../../../src/value/src/value.cpp#L3315) | There might be dereferencing of a potential null pointer 'doubleDataMut()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3319`](../../../src/value/src/value.cpp#L3319) | There might be dereferencing of a potential null pointer 'doubleDataMut()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3326`](../../../src/value/src/value.cpp#L3326) | There might be dereferencing of a potential null pointer 'charData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3332`](../../../src/value/src/value.cpp#L3332) | There might be dereferencing of a potential null pointer 'charDataMut()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:3347`](../../../src/value/src/value.cpp#L3347) | There might be dereferencing of a potential null pointer 'cd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4065`](../../../src/value/src/value.cpp#L4065) | There might be dereferencing of a potential null pointer 'dd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4080`](../../../src/value/src/value.cpp#L4080) | There might be dereferencing of a potential null pointer 'cd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4107`](../../../src/value/src/value.cpp#L4107) | There might be dereferencing of a potential null pointer 'ld'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4271`](../../../src/value/src/value.cpp#L4271) | There might be dereferencing of a potential null pointer 'logicalData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4310`](../../../src/value/src/value.cpp#L4310) | There might be dereferencing of a potential null pointer 'singleData()'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4323`](../../../src/value/src/value.cpp#L4323) | There might be dereferencing of a potential null pointer 'fd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/value/src/value.cpp:4355`](../../../src/value/src/value.cpp#L4355) | There might be dereferencing of a potential null pointer 'static_cast< const int8_t * > (raw)'. |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | [`src/value/src/value.cpp:1871`](../../../src/value/src/value.cpp#L1871) | The 'then' statement is equivalent to the 'else' statement. |
| [V523](https://pvs-studio.com/en/docs/warnings/v523/) | [`src/value/src/value.cpp:1919`](../../../src/value/src/value.cpp#L1919) | The 'then' statement is equivalent to the 'else' statement. |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | [`src/value/src/value.cpp:3698`](../../../src/value/src/value.cpp#L3698) | Declarations of functions with 'Value::cellAt' name differ in the 'const' keyword only, but the bodies of these functions have different composition. This is suspicious and can possibly be an error. Check lines: 3689, 3698. |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | [`src/value/src/value.cpp:3713`](../../../src/value/src/value.cpp#L3713) | Declarations of functions with 'Value::cellDataVec' name differ in the 'const' keyword only, but the bodies of these functions have different composition. This is suspicious and can possibly be an error. Check lines: 3706, 3713. |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | [`src/value/src/value.cpp:3736`](../../../src/value/src/value.cpp#L3736) | Declarations of functions with 'Value::field' name differ in the 'const' keyword only, but the bodies of these functions have different composition. This is suspicious and can possibly be an error. Check lines: 3720, 3736. |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | [`src/value/src/value.cpp:3765`](../../../src/value/src/value.cpp#L3765) | Declarations of functions with 'Value::structFields' name differ in the 'const' keyword only, but the bodies of these functions have different composition. This is suspicious and can possibly be an error. Check lines: 3757, 3765. |
| [V659](https://pvs-studio.com/en/docs/warnings/v659/) | [`src/value/src/value.cpp:3979`](../../../src/value/src/value.cpp#L3979) | Declarations of functions with 'Value::structArrayElem' name differ in the 'const' keyword only, but the bodies of these functions have different composition. This is suspicious and can possibly be an error. Check lines: 3970, 3979. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/value/src/value.cpp:2510`](../../../src/value/src/value.cpp#L2510) | The 'dstRaw' pointer in the 'dstRaw + dstOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/value/src/value.cpp:2510`](../../../src/value/src/value.cpp#L2510) | The 'srcRaw' pointer in the 'srcRaw + srcOff * es' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/value/src/value_type.cpp:10`](../../../src/value/src/value_type.cpp#L10) | Two or more case-branches perform the same actions. Check lines: 10, 15 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/value/src/value_type.cpp:40`](../../../src/value/src/value_type.cpp#L40) | Two or more case-branches perform the same actions. Check lines: 40, 47, 51 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/value/src/value_type.cpp:45`](../../../src/value/src/value_type.cpp#L45) | Two or more case-branches perform the same actions. Check lines: 45, 49 |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/value/src/value_type.cpp:46`](../../../src/value/src/value_type.cpp#L46) | Two or more case-branches perform the same actions. Check lines: 46, 50, 52 |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/value/src/value.cpp:2897`](../../../src/value/src/value.cpp#L2897) | The 'newDims' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/value/src/value.cpp:3532`](../../../src/value/src/value.cpp#L3532) | The 'newD' variable is not used after copying. Copying can be replaced with move/swap for optimization. |

</details>
