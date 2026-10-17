# NumKit Bundle (`numkit/bundle`)

Umbrella superbuild, MATLAB R2025b parity suite, real-world corpus differential harness (`fieldtest/`), and architectural audit gates (`audits/`) for the NumKit ecosystem.

## Repository Layout

```text
numkit/bundle/
├── CMakeLists.txt          # Unified CMake superbuild (compiles foundation once, stages all plugins)
├── modules/                # Git submodules for all 11 NumKit repositories
│   ├── value/              # L0: Value, ValueType, Dims, Span, ScratchArena, argcheck
│   ├── sys/                # L0: OS/FS abstractions and C ABI plugin interface (PluginContext)
│   ├── ops/                # L1: Highway SIMD kernels, BLAS, FFT/conv/filter, linalg, ode, fzero, builtin math
│   ├── numkit/             # L2: Core runtime (Lexer, Parser, AST, TreeWalker, Bytecode VM, Codegen, CLI)
│   ├── signal/             # L3 plugin: Signal Processing Toolbox
│   ├── control/            # L3 plugin: Control System Toolbox
│   ├── stats/              # L3 plugin: Statistics and Machine Learning Toolbox
│   ├── wavelet/            # L3 plugin: Wavelet Toolbox
│   ├── audio/              # L3 plugin: Audio Toolbox
│   ├── comm/               # L3 plugin: Communications Toolbox
│   └── image/              # L3 plugin: Image Processing Toolbox
├── parity/                 # Specification-driven MATLAB R2025b & Octave parity harness
│   ├── run_parity.py       # Parity & benchmark runner (--all, --module <domain>, --isolated)
│   ├── signprobe.py        # `help <fn>` call-signature comparison vs MATLAB R2025b
│   ├── inventory/          # MATLAB helpfuncbycat.xml TOC extractor and coverage diff
│   ├── specs/              # 1,606 JSON specs organized by domain (core, signal, stats, image, comm, control, wavelet, audio)
│   ├── PROGRESS.md         # Live parity coverage & correctness map
│   └── BENCHMARK.md        # Two-point performance table (NumKit vs MATLAB R2025b vs Octave)
├── fieldtest/              # Real-world MATLAB script differential testing (.mat workspace comparison)
│   ├── fetch.py            # Corpus downloader & UTF-8 normalizer
│   ├── harness.py          # Qualification & batch workspace comparison runner
│   ├── compare.py          # Curated regression group runner
│   ├── groups/             # Curated script groups
│   ├── data/               # runnable.json, candidates.json, answers.json
│   └── reports/            # Batch execution reports
├── bugs/                   # Structured one-file-per-bug catalog (opened/, closed/, pvs/, missing.md)
└── audits/                 # Cross-submodule static architecture & API quality gates
    ├── check_layering.py   # Enforces acyclic dependency DAG across modules/*
    ├── check_api.py        # Verifies public C++ headers & manifest.json export completeness
    ├── argcheck_audit.py   # Verifies argcheck separation & diagnostic conventions (--gate)
    ├── api_shape_audit.py  # Verifies memory_resource parameter placement (--gate)
    ├── bugs_audit.py       # Enforces bug-catalog <-> DISABLED_ guard-test invariants (--guards)
    ├── bugs_tally.py       # Summarizes open/closed bugs by kind, severity, and domain
    └── baselines/          # Committed audit baselines
```

## Quick Start

### 1. Clone with Submodules
```bash
git clone --recurse-submodules git@github.com:numkit/bundle.git
```

### 2. Build Everything (Core + All 7 Plugins + All Test Suites)
```bash
cmake -S . -B build -DNUMKIT_BUILD_TESTS=ON
cmake --build build --config Release -- /m
```
All executables and staged plugins are placed automatically into `build/bin/Release/` (`numkit.exe` + `modules/<pkg>/numkit_<pkg>.dll` + `manifest.json`).

### 3. Run All Unit Tests (Core + Toolboxes)
```bash
ctest --test-dir build -C Release --output-on-failure
```

### 4. Run MATLAB R2025b Parity Suite
```bash
# Single function spec (auto-resolved across parity/specs/*/)
python parity/run_parity.py butter

# Entire domain module (Compat mode vs Isolated namespace mode)
python parity/run_parity.py --module signal
python parity/run_parity.py --module signal --isolated

# Full 1,606-spec suite
python parity/run_parity.py --all
```

### 5. Run Architectural, API & Bug-Guard Audits
```bash
python audits/check_layering.py
python audits/check_api.py
python audits/argcheck_audit.py --gate
python audits/api_shape_audit.py --gate
python audits/bugs_audit.py --guards
python audits/bugs_tally.py
```

