# `signal` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **11** | 0 | 11 |
| 🟡 **Medium** | **18** | 0 | 18 |
| 🟢 **Low** | **24** | 0 | 24 |
| **Total** | **53** | 0 | 53 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 2 | 11 | 0 | 13 | **13** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 8 | 0 | 8 | **8** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 7 | 0 | 0 | 0 | 7 | **7** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 5 | 1 | 0 | 6 | **6** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 4 | 1 | 0 | 5 | **5** |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | 3 | 0 | 0 | 0 | 3 | **3** |
| [V612](https://pvs-studio.com/en/docs/warnings/v612/) | 0 | 3 | 0 | 0 | 3 | **3** |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V1083](https://pvs-studio.com/en/docs/warnings/v1083/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V501](https://pvs-studio.com/en/docs/warnings/v501/) | 1 | 0 | 0 | 0 | 1 | **1** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V501](https://pvs-studio.com/en/docs/warnings/v501/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/toolboxes/signal/src/filter_implementation/conversions_extras.cpp:384`](../../../src/toolboxes/signal/src/filter_implementation/conversions_extras.cpp#L384) | There are identical sub-expressions to the left and to the right of the '&#124;&#124;' operator: SV.isEmpty() &#124;&#124; SV.isEmpty() |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | [CWE-783](https://cwe.mitre.org/data/definitions/783.html) | [`src/toolboxes/signal/src/filter_implementation/conversions_extras.cpp:373`](../../../src/toolboxes/signal/src/filter_implementation/conversions_extras.cpp#L373) | The '?:' operator, regardless of its conditional expression, always returns one and the same value: v.dims().cols(). |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:60`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L60) | Possible overflow. Consider casting operands of the 'n * p' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:88`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L88) | Possible overflow. Consider casting operands of the 'p * p' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:89`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L89) | Possible overflow. Consider casting operands of the 'p * n' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:105`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L105) | Possible overflow. Consider casting operands of the 'n * n' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:128`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L128) | Possible overflow. Consider casting operands of the 'p * p' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:138`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L138) | Possible overflow. Consider casting operands of the 'p * p' operator to the 'std::size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/smoothing/sgolay.cpp:145`](../../../src/toolboxes/signal/src/smoothing/sgolay.cpp#L145) | Possible overflow. Consider casting operands of the 'n * p' operator to the 'std::size_t' type, not the result. |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | [CWE-783](https://cwe.mitre.org/data/definitions/783.html) | [`src/toolboxes/signal/src/spectral_analysis/ar.cpp:136`](../../../src/toolboxes/signal/src/spectral_analysis/ar.cpp#L136) | The '?:' operator, regardless of its conditional expression, always returns one and the same value: 256. |
| [V583](https://pvs-studio.com/en/docs/warnings/v583/) | [CWE-783](https://cwe.mitre.org/data/definitions/783.html) | [`src/toolboxes/signal/src/transforms/fft.cpp:640`](../../../src/toolboxes/signal/src/transforms/fft.cpp#L640) | The '?:' operator, regardless of its conditional expression, always returns one and the same value: R. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/signal/src/convolution/extras.cpp:57`](../../../src/toolboxes/signal/src/convolution/extras.cpp#L57) | Variables 'xp', 'yp' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 56, 57. |
| [V1083](https://pvs-studio.com/en/docs/warnings/v1083/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/signal/src/filter_design/filter_design.cpp:542`](../../../src/toolboxes/signal/src/filter_design/filter_design.cpp#L542) | Signed integer overflow is possible in 'npt + 1' arithmetic expression. This leads to undefined behavior. Left operand is in range 1 u [0x40000001..0x7FFFFFFF], right operand is '1'. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/toolboxes/signal/src/filter_design/filter_design.cpp:623`](../../../src/toolboxes/signal/src/filter_design/filter_design.cpp#L623) | Expression 'nn == 1' is always false. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/signal/src/filter_design/filter_design.cpp:1145`](../../../src/toolboxes/signal/src/filter_design/filter_design.cpp#L1145) | Expression 'L + 1 >= 1' is always true. |
| [V730](https://pvs-studio.com/en/docs/warnings/v730/) | [CWE-457](https://cwe.mitre.org/data/definitions/457.html) | [`src/toolboxes/signal/src/filter_design/iir_designs.cpp:208`](../../../src/toolboxes/signal/src/filter_design/iir_designs.cpp#L208) | Not all members of a class are initialized inside the compiler generated constructor. Consider inspecting: ratio, Wo_passband, Wo_stopband, ftype. |
| [V612](https://pvs-studio.com/en/docs/warnings/v612/) | [CWE-670](https://cwe.mitre.org/data/definitions/670.html) | [`src/toolboxes/signal/src/measurements/pulse_metrics.cpp:301`](../../../src/toolboxes/signal/src/measurements/pulse_metrics.cpp#L301) | An unconditional 'break' within a loop. |
| [V612](https://pvs-studio.com/en/docs/warnings/v612/) | [CWE-670](https://cwe.mitre.org/data/definitions/670.html) | [`src/toolboxes/signal/src/measurements/pulse_metrics.cpp:328`](../../../src/toolboxes/signal/src/measurements/pulse_metrics.cpp#L328) | An unconditional 'break' within a loop. |
| [V612](https://pvs-studio.com/en/docs/warnings/v612/) | [CWE-670](https://cwe.mitre.org/data/definitions/670.html) | [`src/toolboxes/signal/src/measurements/pulse_metrics.cpp:359`](../../../src/toolboxes/signal/src/measurements/pulse_metrics.cpp#L359) | An unconditional 'break' within a loop. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/toolboxes/signal/src/measurements/sigroi.cpp:299`](../../../src/toolboxes/signal/src/measurements/sigroi.cpp#L299) | Expression 'totalLen == 0' is always false. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-570](https://cwe.mitre.org/data/definitions/570.html) | [`src/toolboxes/signal/src/measurements/sigroi.cpp:301`](../../../src/toolboxes/signal/src/measurements/sigroi.cpp#L301) | Expression 'totalLen == 0' is always false. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/signal/src/transforms/fft.cpp:331`](../../../src/toolboxes/signal/src/transforms/fft.cpp#L331) | A part of conditional expression is always true: outAxisLen == fftLen. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [CWE-665](https://cwe.mitre.org/data/definitions/665.html) | [`src/toolboxes/signal/src/transforms/hilbert.cpp:280`](../../../src/toolboxes/signal/src/transforms/hilbert.cpp#L280) | Variables 'x_loc', 'y_loc' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 279, 280. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | - | [`src/toolboxes/signal/src/measurements/findpeaks_detail.hpp:22`](../../../src/toolboxes/signal/src/measurements/findpeaks_detail.hpp#L22) | On 64-bit platform, structure size can be reduced from 56 to 48 bytes by rearranging the fields according to their sizes in decreasing order. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/signal/src/filter_design/iir_designs.cpp:455`](../../../src/toolboxes/signal/src/filter_design/iir_designs.cpp#L455) | The 'ws' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp:107`](../../../src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp#L107) | The 'a_prev' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp:152`](../../../src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp#L152) | The 'prev' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp:332`](../../../src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp#L332) | The 'av' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp:341`](../../../src/toolboxes/signal/src/spectral_analysis/signal_modeling.cpp#L341) | The 'prev' variable is not used after copying. Copying can be replaced with move/swap for optimization. |


<details>
<summary><b>🟢 Low Severity (24)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/convolution/convolution.cpp:326`](../../../src/toolboxes/signal/src/convolution/convolution.cpp#L326) | Variables 'cOut', 'lOut' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 325, 326. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/toolboxes/signal/src/convolution/extras.cpp:40`](../../../src/toolboxes/signal/src/convolution/extras.cpp#L40) | The 'n' variable was assigned the same value. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/convolution/extras.cpp:270`](../../../src/toolboxes/signal/src/convolution/extras.cpp#L270) | Variables 'Ap', 'Bf' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 269, 270. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/digital_filtering/filter.cpp:174`](../../../src/toolboxes/signal/src/digital_filtering/filter.cpp#L174) | There might be dereferencing of a potential null pointer 'ziPtr'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/digital_filtering/filter.cpp:237`](../../../src/toolboxes/signal/src/digital_filtering/filter.cpp#L237) | There might be dereferencing of a potential null pointer 'ziPtr'. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/filter_analysis/frequency_response.cpp:162`](../../../src/toolboxes/signal/src/filter_analysis/frequency_response.cpp#L162) | Variables 'W', 'gd' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 161, 162. |
| [V1037](https://pvs-studio.com/en/docs/warnings/v1037/) | [`src/toolboxes/signal/src/filter_design/filter_design.cpp:760`](../../../src/toolboxes/signal/src/filter_design/filter_design.cpp#L760) | Two or more case-branches perform the same actions. Check lines: 760, 762 |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/measurements/findpeaks.cpp:161`](../../../src/toolboxes/signal/src/measurements/findpeaks.cpp#L161) | There might be dereferencing of a potential null pointer 'p'. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/measurements/sig_utils.cpp:111`](../../../src/toolboxes/signal/src/measurements/sig_utils.cpp#L111) | Variables 'R.uppersum', 'R.lowersum' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 110, 111. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/measurements/sig_utils.cpp:113`](../../../src/toolboxes/signal/src/measurements/sig_utils.cpp#L113) | Variables 'R.iupper', 'R.ilower' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 112, 113. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/measurements/vibration.cpp:73`](../../../src/toolboxes/signal/src/measurements/vibration.cpp#L73) | Variables 'Es', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 72, 73. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/spectral_analysis/ar.cpp:55`](../../../src/toolboxes/signal/src/spectral_analysis/ar.cpp#L55) | Variables 'Pxx', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 54, 55. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp:88`](../../../src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp#L88) | Variables 'Pxx', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 87, 88. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp:212`](../../../src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp#L212) | Variables 'Pxx', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 211, 212. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp:362`](../../../src/toolboxes/signal/src/spectral_analysis/periodogram_pwelch.cpp#L362) | Variables 'Cxy', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 361, 362. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/signal/src/spectral_analysis/pseudospectrum.cpp:111`](../../../src/toolboxes/signal/src/spectral_analysis/pseudospectrum.cpp#L111) | Variables 'P', 'F' are initialized through the call to the same function. It's probably an error or un-optimized code. Check lines: 110, 111. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/time_frequency/spectrogram.cpp:233`](../../../src/toolboxes/signal/src/time_frequency/spectrogram.cpp#L233) | There might be dereferencing of a potential null pointer 'frameCd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/time_frequency/spectrogram.cpp:233`](../../../src/toolboxes/signal/src/time_frequency/spectrogram.cpp#L233) | There might be dereferencing of a potential null pointer 'xc'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/time_frequency/spectrogram.cpp:237`](../../../src/toolboxes/signal/src/time_frequency/spectrogram.cpp#L237) | There might be dereferencing of a potential null pointer 'frameRd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/time_frequency/spectrogram.cpp:237`](../../../src/toolboxes/signal/src/time_frequency/spectrogram.cpp#L237) | There might be dereferencing of a potential null pointer 'xr'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/signal/src/time_frequency/spectrogram.cpp:342`](../../../src/toolboxes/signal/src/time_frequency/spectrogram.cpp#L342) | There might be dereferencing of a potential null pointer 'tr'. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [`src/toolboxes/signal/src/transforms/fft.cpp:1052`](../../../src/toolboxes/signal/src/transforms/fft.cpp#L1052) | Expression 'useDim == 3' is always true. |
| [V769](https://pvs-studio.com/en/docs/warnings/v769/) | [`src/toolboxes/signal/src/transforms/fft.cpp:631`](../../../src/toolboxes/signal/src/transforms/fft.cpp#L631) | The 'srcD' pointer in the 'srcD + inBase' expression could be nullptr. In such case, resulting value will be senseless and it should not be used. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | [`src/toolboxes/signal/src/waveform_generation/waveform_generation.cpp:496`](../../../src/toolboxes/signal/src/waveform_generation/waveform_generation.cpp#L496) | The 'mixed' variable is not used after copying. Copying can be replaced with move/swap for optimization. |

</details>
