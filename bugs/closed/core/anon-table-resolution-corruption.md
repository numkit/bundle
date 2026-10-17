# Anonymous-handle cell tables corrupt name resolution (compiler/VM)

- **Kind:** bug
- **Found:** 2026-09-18, image argcheck portion probe battery (probe12).
- **Component:** core compiler / VM (`src/core/src/compiler.cpp`, `compileAnonFunc`).
- **Fixed:** 2026-09-18, engine-gap portion.

## Repro

```matlab
clear;
grayfns = {
 'fn1', @(x) sin(x + 1);
 'fn2', @(x) sin(x + 2);
 % ... 46 rows of 'fnN', @(x) sin(x + N) ...
 'fn46', @(x) sin(x + 46);
};
for i = 1:size(grayfns, 1)
  r = grayfns{i, 2}(1);   % fn1 must give sin(2) = 0.9093
end
```

Generate the 46 rows programmatically for a copy-paste repro:

```matlab
clear;
grayfns = cell(46, 2);
for k = 1:46
  grayfns{k, 1} = sprintf('fn%d', k);
  grayfns{k, 2} = @(x) sin(x + k);   % loop-built table shows the same failure
end
r = grayfns{1, 2}(1);                % expect sin(2) = 0.9093
fprintf('%.4f\n', r);
```

**MATLAB R2025b:** `0.9093` (and every row resolves to `sin(1 + k)`).
**nk:** first call dies with

```
nk:error | Undefined function or variable 'xdata'
```

— the closure body resolves to an UNRELATED registered function body (the
m-source builtin `lsqcurvefit`, whose body references `xdata`;
`src/bundle/src/register/optim/lsqnonlin_reg.cpp`), not to `sin`.

## Facts (probed 2026-09-18)

- Threshold is content-dependent, not a fixed row count:
  * sin-body table: 42 rows OK, 43 rows corrupt (first call already wrong);
  * image-function table (heavier handles, 2-arg bodies, captures): 37 rows
    OK, 38 rows corrupt.
- No anonymous functions in the table → no failure (a 200-element pure-data
  cell literal is fine), so the trigger is the anonymous-handle literals.
- Local functions, nested `@()` thunks and probe wrappers are NOT required
  (an inline loop with try/catch reproduces).
- Failure is deterministic and hits the FIRST closure call, i.e. the script's
  handle table is already wrong by the time it is consumed.
- nk_repl (VM backend) reproduces; the dual-backend guard confirms the bug
  is **VM/compiler-only** — TreeWalker computes sin(2) correctly on the same
  script.

## Suspicion (not root-caused)

`Compiler::compileAnonFunc` (src/core/src/compiler.cpp:3791) returns a
`uint8_t` register index and mints `__anon_<N>` chunk functions; the failing
scripts have ~43+ anonymous literals plus their varargout-forwarding lowered
helpers in one chunk. Something in that path (register allocation, inner
function table indexing, or the `__anon_<N>` user-function registry) silently
aliases once the script grows past a content-dependent size, so the call
inside a closure body resolves to the wrong compiled body.

## Guard

`DISABLED_AnonTableResolutionCorruption` in
`src/bundle/tests/known_bugs_test.cpp` (dual-backend).

## ROOT CAUSE (found + fixed 2026-09-18, engine-gap portion)

The VM compiler and the TreeWalker fallback each minted `__anon_<N>`
names from INDEPENDENT per-instance counters. A large literal-table
script (the ~43-row threshold = the 255-register VM budget) exhausts
registers mid-compile: the compilation attempt aborts and falls back to
TreeWalker execution — but its already-registered anon chunks STAY in
the shared compiledFuncs_ map. The TreeWalker re-execution then mints
its own `__anon_0..` ids that COLLIDE with the leftover compiled chunks,
and VM-side handle calls resolve names through findCompiledFunc (the
chunk table) FIRST — executing a foreign body with an off-by-N shift
(every table row ran the previous row's closure; row 1 hit the embedded
lsqnonlin helper `resfn` and died on `xdata`).

Verified by runtime instrumentation: only row 1 errored and rows 2..46
each returned the PREVIOUS row's value — the smoking gun for the
shifted-collision model.

## Fix

One engine-wide atomic counter (`Engine::anonNameCounter_`) shared by
Compiler::compileAnonFunc and TreeWalker::execAnonFunc — names can
never collide across backends or compilation attempts. The per-backend
counters were removed.

**Guard:** `AnonTableResolutionCorruption` in
src/bundle/tests/known_bugs_test.cpp (live, dual-backend — the VM-only
skip removed).
