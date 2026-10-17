# signal.arity — reference accepts fewer args than nk requires (missing short forms)

- **Status:** 🔴 OPEN
- **Severity:** P2 (documented short forms rejected: "not enough input
  arguments" where the reference computes)
- **Kind:** stub (documented argument forms not supported)
- **Found:** 2026-09-17 during the signal max-arity sweep
  (bugs/opened/lang/reg-max-arity.md): the regs' hand minimums protect
  unconditional `args[i]` reads, and for these functions the reference
  genuinely accepts the shorter form.

## Symptom

The reference accepts these shorter calls (probed R2025b: the k-arg call
gets past the entry arity check and produces a domain-success or domain
error, never "not enough inputs"); nk's reg rejects them with
`nk:<fn>:nargin` because the implementation reads the later argument
unconditionally.

## Verified gaps (k-arg call accepted by the reference)

| fn | nk min | reference accepts | note |
|---|---|---|---|
| `freqz` | 2 | 1 | `freqz(b)` FIR form (a defaults to 1) |
| `freqs` | 3 | 2 | `freqs(b, a)` analog FIR/IIR form |
| `phasez` | 2 | 1 | `phasez(b)` |
| `grpdelay` | 2 | 1 | `grpdelay(b)` |
| `isallpass` | 2 | 1 | `isallpass(b)` |
| `tf2zpk` | 2 | 1 | `tf2zpk(b)` |
| `lpc` | 2 | 1 | `lpc(x)` (order defaults) |
| `prony` | 3 | 2 | `prony(x, n)` |
| `rc2ac` | 2 | 1 | `rc2ac(k)` |
| `conv` | 2 | 1 | probed: `conv([])` gets past arity (reference-internal validation order) |
| `impinvar` | 3 | 2 | `impinvar(b, fs)` |
| `upfirdn` | 3 | 2 | `upfirdn(x, h)` |
| `gauspuls` | 2 | 1 | `gauspuls(t)` defaults |
| `gmonopuls` | 2 | 1 | `gmonopuls(t)` |
| `lowpass`/`highpass`/`bandpass`/`bandstop` | 2 | 1 | spec-string design form: `lowpass(x, 'fc', …)` |

## Unverified (min-4 fns; k=3 not probed — check before fixing)

`ellip`, `ellipord`, `ss2zp`, `ss2sos`, `invfreqs`, `invfreqz`, `demod`,
`modulate`, `chirp` (chirp(t) is a documented reference form — almost
certainly a gap).

## Fix direction

Per function: give the missing argument its documented default (or option
parsing), lower the `checkNargin` minimum, and add the short form to the
arity table + a live test. Do NOT just lower the bound — the bodies read
`args[i]` unconditionally.

## Repro (self-contained)

```matlab
clear;
% nk:     Error ... not enough input arguments — at least 2 required
% MATLAB: [h, w] = freqz([1 1 1]) — FIR response of the 3-tap filter
h = freqz([1 1 1]);

% nk:     Error (min 4)
% MATLAB: y = chirp(0:0.01:1) — default linear sweep 0→100 Hz
y = chirp(0:0.01:1);
```

**Guard:** `SignalKnownBug.DISABLED_FewerArgForms` in
`src/toolboxes/signal/tests/known_bugs_test.cpp`.
