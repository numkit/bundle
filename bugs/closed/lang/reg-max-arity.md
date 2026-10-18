# lang.reg — extra positional arguments are silently ignored (no max-arity bound)

- **Status:** ✅ FIXED (2026-10-18, all 261 reg files across all 8 modules migrated to `argcheck::checkNargin`, `raw-arity = 0`)
- **Severity:** P2 (systemic: silently wrong acceptance instead of the
  reference's "Too many input arguments" — typos like a duplicated
  argument compute a plausible-but-wrong result instead of erroring)
- **Kind:** bug
- **Found:** 2026-09-17 while reviewing argcheck diagnostic output (probed
  against R2025b). Quantified earlier the same day as the "raw-arity
  backlog": ~110 of 261 reg files have no `checkNargin` bound at all.

## Symptom

Reg adapters that check only the MINIMUM arity let extra positional
arguments through and drop them, so the call computes as if they were
absent. The reference rejects extra arguments ("Too many input
arguments", ids `MATLAB:maxrhs` / `MATLAB:narginchk:tooManyInputs`).

## Repro

```matlab
clear;
u = triu(ones(3), 1, 2);
% nk:     u = triu(ones(3), 1)      (3rd argument silently dropped)
% MATLAB R2025b (probed 2026-09-17): Error using triu — Too many input
%         arguments. (MATLAB:maxrhs)

r = strncmp('a', 'b', 1, 1);
% nk:     r = strncmp('a','b',1)    (4th argument silently dropped)
% MATLAB: Error (MATLAB:maxrhs)

w = hamming(6, 'symmetric', 1);
% nk:     w = hamming(6,'symmetric')  (3rd argument silently dropped)
% MATLAB: Error (MATLAB:narginchk:tooManyInputs)
```

## Root cause

`nk::argcheck::checkNargin(actual, min, max, fn)` exists (the max form,
id `nk:<fn>:maxnargin`, message "at most N accepted (got M)") but most
reg files never call any max bound; hand-rolled minimum checks dominate
the ~110-file raw-arity backlog.

## Suggested fix

Work the backlog per domain (same order as the raw-cast campaign):
every reg whose reference signature has a finite max gets the 3-arg
`checkNargin`; variadic ones (reshape trailing sizes, option-tail
parsers) document why they are unbounded.

## Progress

- **builtin domain — ✅ DONE (2026-09-17):** all reg files under
  `src/bundle/src/register/builtin/` migrated (234 hand sites + 11 reg
  macros + the issortedrows split). Bounds are probed, not guessed: a
  `nargin` probe over the 476 literal registrations + a behavioral
  `tooManyInputs` probe over the varargin-plumbed subset (the effective
  wall can be tighter than nargin reports — e.g. hamming: nargin -1 but
  effective max 2). Applied bounds: `tools/arity_reference.json`;
  table-driven guards: `src/builtin/tests/arity_bounds_test.cpp` (238
  max+1 rejection cases, `ArityBoundsTest`). Min-only checkNargin
  everywhere else.
- **signal domain — ✅ DONE (2026-09-17):** all 245 registrations across
  14 subdomains migrated (201 direct defs incl. 9 pure insertions +
  43 macro instantiations via 11 macro edits). Guards:
  `src/toolboxes/signal/tests/arity_bounds_test.cpp` (217 max+1 cases,
  `SignalArityBoundsTest`). Method notes for the next domains:
  - `nargin` returns **-2** (builtin-like, runtime-determined signature)
    and **-3** (arguments-block) besides -1 — ALL of them need the
    behavioral wall probe, not just -1.
  - `[]`-dummy probes UNDERSTATE minimums: domain errors mask
    notEnoughInputs. After any codemod, diff the applied min against the
    replaced hand-check's threshold per function (full-body, not a
    ±2-line diff window) and keep the higher value unless the short form
    is actually implemented; verified short-form gaps are filed as
    `bugs/opened/signal/arity-min-forms.md`.
  - Name-Value tails (findpeaks/risetime/dutycycle/…): reference has NO
    count wall — min-only + comment; a junk option string errors as
    "unrecognized option" at every arity.
  - Arity HOLES exist: fft2/ifft2 accept {1, 3+}, never 2
    (`bugs/opened/signal/fft2-two-arg.md`); checkNargin ranges can't
    express sets — file them when found.
  - Alias registrations share one reg (hanning → hann_reg): the bound is
    the UNION of the per-name probed contracts.
  - nk-only or object-model divergences documented in reg comments:
    tsa 3..5 (legacy continuous-rpm form), resample 3..3, tachorpm 2..4,
    sigrangebinmask 2..2, isfir 1..2, sosfiltfilt 2..2 (absent from the
    R2025b reference build), lowercase spectral* vs the reference's
    camelCase spellings.
  - The behavioral probe per domain (245 names: ~2 min for nargin + ~2
    min for walls) is cheap; the earlier global 1598-name stall was a
    single-function hang, not the method.
- **image domain — ✅ DONE (2026-09-17):** all 256 registrations migrated
  (221 direct defs incl. hsv_cmap_reg + 32 macro instantiations via 4
  parameterized macros NK_BIN/COLOR/IM_UNARY/MORPH(_NV)). Guards:
  `src/toolboxes/image/tests/arity_bounds_test.cpp` (170 max+1 cases,
  `ImageArityBoundsTest`). Applied bounds: `tools/arity_reference.json`
  ("image", 174 bounded / 80 min-only / 13 absent-from-reference).
  Additional method notes beyond signal's (all cost real debugging time):
  - **[]-dummies hide value-dependent walls**: the reference's colormap
    fns, dctmtx, cmap2gray, rgb2/ycbcr converters accept any number of
    `[]` args but reject a 2nd REAL argument (MATLAB:TooManyInputs).
    Any unbounded classification of a plausibly-1-arg fn needs a
    real-value spot check (`gray(1, 2)` -> TooManyInputs).
  - **Hand parsers reject junk NV as TooManyInputs**: imcolordiff /
    demosaic accept documented name-value forms (4-6 args) but answer
    a junk string tail with TooManyInputs — a junk-only wall probe
    reads as bounded 2. Cross-check fns with documented NV options via
    a valid NV pair, or trust the domain tests (they encode the doc).
    The reverse also holds: `MATLAB:TooManyInputs` (capital T, generic
    M-file) vs `MATLAB:narginchk:tooManyInputs` — match case-sensitively
    or you re-decode the wall table by hand.
  - **0-arg forms need a dedicated k=0 pass**: colormaps accept `gray()`
    (default n); checkerboard/phantom/strel/gabor/whitepoint too. The
    []-wall probe starting at k=1 cannot see them. Gaps filed as
    `bugs/opened/image/arity-min-forms.md`.
  - **Interactive fns hang batch probes**: bwselect (stopped a 256-name
    probe at 194), roipoly, imcrop wait for figure clicks when called
    bare. Exclude from bulk probes; hand-probe with a valid
    non-interactive prefix (bwselect(BW,r,c), roipoly(I,c,r),
    imcrop(I,rect)) + dummy tail.
  - **Strict-1 surprises in R2025b**: graythresh, otsuthresh, bwarea
    reject a 2nd argument even when documented forms once existed
    (`graythresh(I,'minerror')` -> TooManyInputs). Probe with a VALID
    2nd arg before believing a wall=1 — and with a VALID option NAME:
    cc2bw read as strict-1 because the probe passed 'KeepRegions' (not
    a real option) — with 'ObjectsToKeep' it is an NV tail (min-only);
    the test fallout caught it.
  - **High-wall corroboration**: for walls >= 8 test valid NV-PAIR tails
    ('zzjunk', 1, ...) at wall and wall+1: a real wall gives
    tooManyInputs exactly at wall+1 and param-name errors at wall
    (adaptthresh 8, imreducehaze 10, locallapfilt 10, houghpeaks 8
    confirmed); parser artifacts give param errors at both
    (graycomatrix, imdiffusefilt, multissim, multissim3 -> min-only).
  - **nk-only names may exist in the reference**: isbw/isgray/isind/
    isrgb report `images:removed:functionNoReplacement`; planar2raw/
    raw2planar/imkeepborder/rgbwide*/xyz2double/xyz2uint16/
    rgb2lightness DO exist in the R2025b build. Never assume — classify
    from the probe ids.
  - **Codemod specifics**: some image regs name the Span parameter `a`
    (segment_reg.cpp) — generated checks must use the signature's name;
    the span-end regex for old bounded throws can cut inside a message
    string containing ')' (deconvreg) — always build after the codemod
    and hand-repair the bounded-shape survivors; macro-block comments
    between two #defines must NOT end with a line-continuation
    backslash (swallows the following #define).
- **stats domain — ✅ DONE (2026-09-17):** all 317 registrations migrated
  (254 hand min-checks replaced in place + 57 insertions for helper-only
  regs + 5 macro instantiations via 2 macro edits in nan_aware_reg.cpp).
  Guards: `src/toolboxes/stats/tests/arity_bounds_test.cpp` (179 max+1
  cases, `StatsArityBoundsTest`). Applied bounds: `tools/arity_reference.json`
  ("stats", 180 bounded / 135 min-only; kde excluded — alias union).
  Fallout: 4 tests (nk 'upper'-flag extensions the reference rejects —
  raylcdf/unifcdf/gevcdf/gpcdf; tests + 2 smokes updated to expect
  nk:<fn>:maxnargin). Method notes beyond image's:
  - **Case-INSENSITIVE wall matching is mandatory in toolbox domains**:
    the generic M-file dispatch error is `MATLAB:TooManyInputs`
    (capital T) — a case-sensitive `contains(id,'tooManyInputs')`
    classified 310/317 stats fns as unbounded. Decode offline; accept
    namespaced count ids by suffix (`:TooManyInputs`/`:TooManyArgs`)
    but NOT domain ids (`kmeans:TooManyClusters` matched the substring
    and faked a wall).
  - **Dispatch rule: nargin>0 ⇒ wall==nargin, zero exceptions.** For
    M-files with a fixed declared signature the count error fires at
    dispatch BEFORE the body — value-independent ([]- and real-passes
    agree). Positive nargin alone settles the wall; the behavioral
    probe corroborates.
  - **Run BOTH []-dummy and real-scalar passes** and take the min wall:
    bodies that validate values before their narginchk can mask the
    count error for one dummy class.
  - **Domain ids containing 'toofew' inflate probed minimums**
    (toofewpoints/toofewknots/TooFewDimensions/delegated TooFewInputs
    at k<true-min): the understated-min detector over-trusts them —
    hand-override from the documented form + impl floor (8 stats cases).
  - **Committed "reference-probed" comments can lie**: parse_rng_size's
    "more than two size inputs is too many" (and its test) encoded an
    nk 2-D-kernel cap; the probe showed the reference accepts unbounded
    N-D size tails (geornd(p,2,3,4) → 2x3x4). Extended
    bugs/opened/stats/rnd-size-vector-nd.md with the rejected-tail
    symptom + a DISABLED_ guard; rnd regs stay min-only.
  - **Alias unions across reference products**: kde is a BASE-MATLAB
    datafun function (positional max 1 + NV tail) sharing ksdensity_reg
    — the shared reg serves the union (min-only); no per-name guard.
  - **exist() beats error-id archaeology** for the absent class:
    naka*/rice*/net are exist()=0 (min-only + absent comment); randg is
    a builtin (exist=5, unbounded size tail); hampel's internal
    UndefinedFunction on [] dummies is NOT absence.
  - **0-arg k0 pass**: fitdist()/haltonset()/randg() are reference-legal
    0-arg forms — filed as bugs/opened/stats/arity-min-forms.md.
  - **R2025b strict-wall surprises** (contradict older docs): grp2idx,
    pcacov, tabulate, dummyvar strict-1; nancov strict-2; betafit
    strict-2; the 'upper' trailing flag is rejected by
    raylcdf/unifcdf/gevcdf/gpcdf yet accepted by the normcdf/wblcdf/
    expcdf/betacdf family — asymmetric declared signatures, walls
    follow the behavior, not the doc page.
  - **Tooling traps**: a gtest multi-suite filter needs `.*` per name
    (`A:B:C.*` runs only C); on MSVC multi-config builds
    `cmake --build` without `--config Release` builds Debug and the
    Release test binary silently stays STALE (verify timestamps before
    trusting a green run).
- **comm domain — ✅ DONE (2026-09-17):** all 78 registrations across 23
  reg files migrated (71 codemod replacements + 7 hand edits carrying new
  R2025b short forms + 4 reference-absent nk contracts). Classes: 67
  bounded / 11 min-only / 4 absent (rayleighchan, ricianchan, scrambler,
  descrambler — System objects in R2025b; nk contracts pinned to the
  implemented signatures). Guards: `src/toolboxes/comm/tests/
  arity_bounds_test.cpp` (65 max+1 rejection cases +
  `CommArityFormsTest` pinning the new short forms). Method notes:
  - **Body narginchk walls exist BELOW the dispatch wall**: decode
    declares 8 params (nargin=8) but its body narginchk caps at 6 — the
    first count error fires at 7, so the behavioral probe's wall (6) is
    the observable contract; the dispatch rule alone would have said 8.
  - **Arguments-block interleaved validation MASKS minimums both ways**:
    modnorm([]-pass min 1, dummy-real min 2) — but a VALID 2-arg call
    (`modnorm(1:4,'peakpow')`) errors minrhs: true min 3. A validation
    error at k only proves the count gate passed if k-1 produced a
    COUNT-class error (narginchk/minrhs) AND the k-th args are valid;
    when in doubt, re-probe with genuinely valid values (modnorm vs
    hammgen: hammgen(4) succeeds, min 1 real).
  - **Custom too-few ids carry the count in the MESSAGE**: dpskmod
    `numarg1` "Too few input arguments" (min 2), berawgn `numArgs`
    "requires at least 3", berconfint `minArgs` "at least 2", noisebw
    `InvalidNumberOfArgs` "requires four", poly2trellis
    `InvalidNumOfInpArgs` "two or three" (= bounded (2,3)!) — read the
    message text, not just the id class.
  - **R2025b added argument defaults**: gaussdesign(bt) legal (span=3,
    sps=2 defaults, probed equal), fskmod/fskdemod 4-arg legal (fs=1
    default, probed equal), compand 3-arg legal ('mu/compressor'
    default, probed equal), randsrc() 0-arg + randsrc(m) m×m, randerr(m)
    m×m — all implemented with the migration.
  - **Arity probes expose domain-set divergences**: mil188qammod M set is
    {16,32,64,256} in R2025b; nk accepted 128/512/1024 — fixed alongside
    (existing Mil188Test already expected the 128 rejection).
  - **Argument-SEMANTICS divergences surface too**: convertSNR parses
    positional mode values in the reference but keyword names in nk
    (filed: bugs/opened/comm/convertSNR-arg-semantics.md); symerr's
    3rd flag accepted+deferred (nk:symerr:flg, filed stub); ignored
    option tails consolidated in
    bugs/opened/comm/ignored-option-tails.md (awgn powertype must be
    LAST and errors after — nk silently accepted a 5th arg).
- **control domain — ✅ DONE (2026-09-17):** all 55 registrations (54
  names; impulse also serves the impulse_lti alias) across 11 reg files
  migrated (52 codemod replacements + 2 behavioral hand edits). Classes:
  38 bounded / 16 min-only. Guards: `src/toolboxes/control/tests/
  arity_bounds_test.cpp` (38 max+1 cases; isstable guarded via
  `import control.props.isstable` because bare isstable belongs to
  signal; impulse guarded through the impulse_lti alias because the
  m-source dispatcher owns the bare name). Method notes:
  - **Classdef methods are invisible to exist()/nargin**: 13 names
    (tfdata/zpkdata/ssdata/frdata, isct/isdt/issiso/isproper/isstatic,
    order, pole, zero, evalfr) report exist()=0 yet are callable with a
    real model — probe them behaviorally with a valid sys argument;
    their contracts (mostly (1,1) or unbounded model-array tails) came
    from the valid-args mini pass, never from dummy probes.
  - **Empty/dummy sys arguments mask minimums at scale**: the []-pass
    understated almost every response function (step said min 2,
    d2c said min 3, lsim said min 4 — all wrong; valid-model probing
    gave step(sys)=1, d2c(sysd)=1, lsim(sys,u)=2). For object-model
    domains the valid-args pass is the PRIMARY min source, not a
    cross-check.
  - **Type-dependent walls exist**: the reference dispatches on the
    first argument's class (model path vs obsolete matrix path) and the
    paths have different walls — covar/ss2ss accept 5 numeric dummies
    but reject 3+ model args; gram walls at 2 numerically yet accepts
    name-value tails for models. Single (min,max) contracts can't
    express this — catalog keeps the numeric-dummy wall, divergence
    filed (bugs/opened/control/type-dependent-walls.md).
  - **0-arg quirks**: constructors (tf/zpk/ss/filt/frd) accept 0-arg
    empty forms; the six plot functions (step/impulse/bode/nyquist/
    rlocus/margin) run a random-model DEMO with no args — nk floors
    kept, filed (bugs/opened/control/arity-min-forms.md).
  - **lqr/dlqr tightened (3,5)→(4,5)**: the reference matrix form
    requires R (lqr(A,B,Q) → notEnoughInputs; probed); the model form
    lqr(sys,Q,R) is the legal 3-arg shape and stays a filed stub. nk's
    old 3-arg matrix form (implicit R=I) silently answered a call class
    the reference refuses — removed.
  - **ctrb/obsv are (1,2)**: the 1-arg model forms are legal (probed
    ctrb(ss(...))=OK) — nk's sys-form paths already matched.
  - **feedback argcheck mislabel fixed**: expectedReal(a[2], 4, ...)
    reported position 4 for the 3rd argument.
- **audio, wavelet, linalg, io, ode, optim, graphics, timefun, matfun,
  lang domains — ✅ DONE (2026-10-18):** all remaining 47 reg files
  migrated to `argcheck::checkNargin` (`raw-arity = 0` across all 261
  reg files in all 8 modules). Guards:
  `modules/audio/tests/arity_bounds_test.cpp` (`AudioArityBoundsTest`),
  `modules/wavelet/tests/arity_bounds_test.cpp` (`WaveletArityBoundsTest`),
  and `BuiltinKnownBug.RegMaxArityBounds` in
  `modules/numkit/tests/gtest/known_bugs_test.cpp`.

## References

- **Guard:** `BuiltinKnownBug.TriuMaxArity`, `BuiltinKnownBug.StrncmpMaxArity`,
  `BuiltinKnownBug.RegMaxArityBounds` (`modules/numkit/tests/gtest/known_bugs_test.cpp`);
  per-module table guards in `modules/{numkit,signal,image,stats,comm,control,audio,wavelet}/tests/arity_bounds_test.cpp`.
- dev-docs/todo/argcheck_separation.md (raw-arity backlog closed).

