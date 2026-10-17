# idwt (1-D) ignored single precision — always returned double

- **Kind:** bug
- **Component:** wavelet (idwt)
- **Found + Fixed:** 2026-09-18, bug-quartet portion (read off the
  reference's idwt.m while fixing idwt-short-filter-input: the result
  class follows `isUnderlyingType(a,'single')`).

## Repro

```
clear;
y = idwt(single([1;0]), single([0;0]), 'db4');
class(y)      % MATLAB: single; nk (before): double
```

## Fix

`idwt_with_filters` casts the result to single when cA is single
(idwt2 already had the any-coefficient contagion from the 2026-09-19
portion; the 1-D form now follows cA exactly like the reference).

**Guard:** single cases covered by the idwt parity spec fingerprints
(single vs double closeness) and the wavelet type-contract suite.
