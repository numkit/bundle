# `audio` — PVS-Studio warnings

> Module of [the report index](../summary.md) | **Commit:** [`c54445d3e`]

## Counts

| Severity | Total | tests | prod |
| :--- | :---: | :---: | :---: |
| 🔴 **High** | **4** | 0 | 4 |
| 🟡 **Medium** | **19** | 0 | 19 |
| 🟢 **Low** | **17** | 0 | 17 |
| **Total** | **40** | 0 | 40 |

## Rules

| Rule | High | Medium | Low | tests | prod | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | 0 | 7 | 1 | 0 | 8 | **8** |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | 0 | 0 | 8 | 0 | 8 | **8** |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | 0 | 3 | 3 | 0 | 6 | **6** |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | 0 | 5 | 0 | 0 | 5 | **5** |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | 2 | 1 | 0 | 0 | 3 | **3** |
| [V1026](https://pvs-studio.com/en/docs/warnings/v1026/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | 2 | 0 | 0 | 0 | 2 | **2** |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | 0 | 0 | 2 | 0 | 2 | **2** |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | 0 | 0 | 1 | 0 | 1 | **1** |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | 0 | 1 | 0 | 0 | 1 | **1** |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | 0 | 1 | 0 | 0 | 1 | **1** |


## 🔴 High Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/audio/src/features/pitch_harmonics.cpp:312`](../../../src/toolboxes/audio/src/features/pitch_harmonics.cpp#L312) | Possible overflow. Consider casting operands of the 'jHi - jLo + 1' operator to the 'size_t' type, not the result. |
| [V1028](https://pvs-studio.com/en/docs/warnings/v1028/) | [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | [`src/toolboxes/audio/src/spectral/melspec_delta.cpp:76`](../../../src/toolboxes/audio/src/spectral/melspec_delta.cpp#L76) | Possible overflow. Consider casting operands of the 'fftLen / 2 + 1' operator to the 'size_t' type, not the result. |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | - | [`src/toolboxes/audio/src/io/mp3_codec.cpp:318`](../../../src/toolboxes/audio/src/io/mp3_codec.cpp#L318) | 'synthBuffer' object of 'vector' type was created but was not utilized. |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | - | [`src/toolboxes/audio/src/io/mp3_codec.cpp:319`](../../../src/toolboxes/audio/src/io/mp3_codec.cpp#L319) | 'synthOffset' object of 'vector' type was created but was not utilized. |


## 🟡 Medium Severity

| Rule | CWE | Location | Message |
| :--- | :--- | :--- | :--- |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:130`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L130) | The 'bytesPerSample' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:183`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L183) | The 'bitsPerSample' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:183`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L183) | The 'bytesPerSample' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:300`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L300) | The 'bytesPerSample' variable was assigned the same value. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:300`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L300) | The 'encoding' variable was assigned the same value. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/io/au_codec.cpp:154`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L154) | A part of conditional expression is always true: len > 0. |
| [V1071](https://pvs-studio.com/en/docs/warnings/v1071/) | - | [`src/toolboxes/audio/src/io/flac_codec.cpp:46`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L46) | Consider inspecting the 'readBits' function. The return value is not always used. Total calls: 48, discarded results: 2. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/io/flac_codec.cpp:306`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L306) | A part of conditional expression is always true: blockSizeCode >= 2. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/io/flac_codec.cpp:309`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L309) | A part of conditional expression is always true: blockSizeCode >= 8. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/io/mp3_codec.cpp:422`](../../../src/toolboxes/audio/src/io/mp3_codec.cpp#L422) | The 'res.bitsPerSample' variable was assigned the same value. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/spectral/cepstral.cpp:588`](../../../src/toolboxes/audio/src/spectral/cepstral.cpp#L588) | Expression 'H >= 1' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/spectral/melspec_delta.cpp:282`](../../../src/toolboxes/audio/src/spectral/melspec_delta.cpp#L282) | Expression 'L > 1' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/spectral/melspec_delta.cpp:285`](../../../src/toolboxes/audio/src/spectral/melspec_delta.cpp#L285) | Expression 'L > 1' is always true. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [CWE-1164](https://cwe.mitre.org/data/definitions/1164.html) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:375`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L375) | The 'd.isTime' variable was assigned the same value. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:289`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L289) | A part of conditional expression is always true: M > 0. |
| [V560](https://pvs-studio.com/en/docs/warnings/v560/) | [CWE-571](https://cwe.mitre.org/data/definitions/571.html) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:317`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L317) | A part of conditional expression is always true: M > 0. |
| [V808](https://pvs-studio.com/en/docs/warnings/v808/) | - | [`src/toolboxes/audio/src/io/flac_codec.cpp:273`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L273) | 'sampleRateTable' array was declared but was not utilized. |
| [V820](https://pvs-studio.com/en/docs/warnings/v820/) | - | [`src/toolboxes/audio/src/io/flac_codec.cpp:217`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L217) | The 'val' variable is not used after copying. Copying can be replaced with move/swap for optimization. |
| [V802](https://pvs-studio.com/en/docs/warnings/v802/) | - | [`src/toolboxes/audio/src/io/mp3_codec.cpp:176`](../../../src/toolboxes/audio/src/io/mp3_codec.cpp#L176) | On 64-bit platform, structure size can be reduced from 24 to 20 bytes by rearranging the fields according to their sizes in decreasing order. |


<details>
<summary><b>🟢 Low Severity (17)</b></summary>

| Rule | Location | Message |
| :--- | :--- | :--- |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/features/pitch_harmonics.cpp:201`](../../../src/toolboxes/audio/src/features/pitch_harmonics.cpp#L201) | There might be dereferencing of a potential null pointer 'cc'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/features/pitch_harmonics.cpp:201`](../../../src/toolboxes/audio/src/features/pitch_harmonics.cpp#L201) | There might be dereferencing of a potential null pointer 'cr'. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [`src/toolboxes/audio/src/io/aiff_codec.cpp:415`](../../../src/toolboxes/audio/src/io/aiff_codec.cpp#L415) | Expression 'bitsPerSample == 32' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [`src/toolboxes/audio/src/io/au_codec.cpp:302`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L302) | Expression 'bitsPerSample == 32' is always true. |
| [V547](https://pvs-studio.com/en/docs/warnings/v547/) | [`src/toolboxes/audio/src/io/au_codec.cpp:343`](../../../src/toolboxes/audio/src/io/au_codec.cpp#L343) | Expression 'bitsPerSample == 32' is always true. |
| [V1026](https://pvs-studio.com/en/docs/warnings/v1026/) | [`src/toolboxes/audio/src/io/flac_codec.cpp:381`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L381) | The 'samples[i]' variable is incremented in the loop. Undefined behavior will occur in case of signed integer overflow. |
| [V1026](https://pvs-studio.com/en/docs/warnings/v1026/) | [`src/toolboxes/audio/src/io/flac_codec.cpp:425`](../../../src/toolboxes/audio/src/io/flac_codec.cpp#L425) | The 'samples[i]' variable is incremented in the loop. Undefined behavior will occur in case of signed integer overflow. |
| [V1048](https://pvs-studio.com/en/docs/warnings/v1048/) | [`src/toolboxes/audio/src/io/wav_codec.cpp:289`](../../../src/toolboxes/audio/src/io/wav_codec.cpp#L289) | The 'res.totalSamples' variable was assigned the same value. |
| [V656](https://pvs-studio.com/en/docs/warnings/v656/) | [`src/toolboxes/audio/src/scale/freq_scales.cpp:190`](../../../src/toolboxes/audio/src/scale/freq_scales.cpp#L190) | Variables 'ys', 'xs_s' are initialized through the call to the same function. It's probably an error or un-optimized code. Consider inspecting the 'tab5SoneVec(mr)' expression. Check lines: 189, 190. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/cepstral.cpp:373`](../../../src/toolboxes/audio/src/spectral/cepstral.cpp#L373) | There might be dereferencing of a potential null pointer 'od_d'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/melspec_delta.cpp:287`](../../../src/toolboxes/audio/src/spectral/melspec_delta.cpp#L287) | There might be dereferencing of a potential null pointer 'od'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/melspec_delta.cpp:301`](../../../src/toolboxes/audio/src/spectral/melspec_delta.cpp#L301) | There might be dereferencing of a potential null pointer 'fd'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:426`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L426) | There might be dereferencing of a potential null pointer 'od'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:760`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L760) | There might be dereferencing of a potential null pointer 'od'. |
| [V522](https://pvs-studio.com/en/docs/warnings/v522/) | [`src/toolboxes/audio/src/spectral/shape_descriptors.cpp:781`](../../../src/toolboxes/audio/src/spectral/shape_descriptors.cpp#L781) | There might be dereferencing of a potential null pointer 'fd'. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/audio/src/spectral/cepstral.cpp:409`](../../../src/toolboxes/audio/src/spectral/cepstral.cpp#L409) | Decreased performance. The 'zero' variable can be constructed in a lower level scope. |
| [V821](https://pvs-studio.com/en/docs/warnings/v821/) | [`src/toolboxes/audio/src/spectral/cepstral.cpp:521`](../../../src/toolboxes/audio/src/spectral/cepstral.cpp#L521) | Decreased performance. The 'zero' variable can be constructed in a lower level scope. |

</details>
