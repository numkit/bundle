# public API: `mr` not last / missing `= nullptr` (library_api.md §7)

- **Kind:** cleanup
- **Namespace:** core (cross-toolbox public API shape)
- **Functions:** strsplit(s, mr) overload (deliberate — see below);
  private-header backlog (report-only list in the audit)
- **Status:** 🟡 OPEN (stats/builtin/control/io portion FIXED 2026-09-18;
  signal 7 FIXED 2026-09-18 in the signal structural portion)
- **Reference:** internal convention — [library_api.md §7](../../dev-docs/handbook/library_api.md)
- **Found:** 2026-09-18, user design review of `rescale`/`zscoreCore`

## The rule

`std::pmr::memory_resource *mr` is **always the final parameter** and
**always defaults to `nullptr`** (ScratchArena resolves null to the
process-default resource). A mid-list `mr` — even dressed with a dead
`= nullptr` default — forces every caller that wants the trailing
optionals to thread `mr` positionally; the default is unreachable
decoration.

## Fixed in this portion (2026-09-18)

| Site | Old shape | Note |
|---|---|---|
| stats `rescale` | `(A, lo, hi, mr, inputMin, inputMax)` | dead default in the middle |
| stats `zscoreCore` (private hdr) | `(A, flag, dim, mr, muOut, sigmaOut)` | out-params after mr |
| builtin `unique`/`uniqueRows`/`uniqueWithIndices`/`uniqueRowsWithIndices` | `(x, mr, stable[, last])` | **silent pointer→bool trap** on 2-arg calls |
| builtin `setUnion`/`setIntersect`/`setDiff` | `(a, b, mr, stable)` | same trap |
| builtin `uniqueComplexFull` (private hdr) | `(x, mr, stable, last)` | follow-on |
| builtin `ismemberComplex` | mr last, no default | added `= nullptr` |
| builtin `scanfEmit` | `(..., outs, mr, ScanfOut &r)` | output struct after mr |
| control `step_response`/`impulse_response`/`lsim`/`initial_response` | `(..., mr, xOut)` | dead default in the middle |
| io fopen-family ×11 | mr last, no default | added `= nullptr` |
| signal `freqz` (grid form) | `(b, a, npts, mr, whole, fs)` | silent pointer→bool trap on 4-arg callers |
| signal `phasez` / `grpdelay` | `(b, a, npts, mr, fs)` | — |
| signal `zp2sosWithGain` | `(zeros, poles, gain, mr, surplusAtOrigin)` | same trap (bool after mr) |
| signal `downsample` / `upsample` | `(x, n, mr, phase)` | — |
| signal `cceps` | `(x, mr, ndOut)` | out-param after mr |

## Remaining

- **`strsplit(const Value &s, std::pmr::memory_resource *mr)`**
  (strfun.hpp) — deliberately WITHOUT default: adding one makes
  `strsplit(s)` ambiguous with the `delim = " "` overload. Permanent
  baseline resident unless the overload set is redesigned.
- **private-header backlog** — 31+ report-only entries
  (`tools/api_shape_audit.py` default report): dsp_helpers, reductions_
  detail dispatchers, image detail headers, … — same disease, internal
  surfaces; clean opportunistically when those files are touched.

## Enforcement

`python tools/api_shape_audit.py --gate` — fails on any NEW public-tree
violation; refresh the baseline with `--write-baseline` when fixes land.
Run before closing a session (alongside bugs_audit / argcheck_audit).

**Guard:** deferred (API-shape cleanup, no behavioral gtest).
