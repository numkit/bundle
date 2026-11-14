# NumKit Bundle (`numkit/bundle`)

Unified C++20 CMake superbuild for the NumKit scientific computing runtime, AOT compiler, and domain plugin toolboxes.

## Repository Layout

```text
numkit/bundle/
├── CMakeLists.txt          # Unified C++20 superbuild (compiles foundation once, stages all plugins)
├── modules/                # Git submodules for all 13 NumKit repositories
│   ├── value/              # L0: Value, ValueType, Dims, Span, ScratchArena, argcheck
│   ├── sys/                # L0: OS/FS abstractions and C ABI plugin interface (PluginContext)
│   ├── ops/                # L1: Highway SIMD kernels, BLAS, FFT/conv/filter, linalg, ode, optim, builtin math
│   ├── numkit/             # L2: Core runtime (Lexer, Parser, AST, TreeWalker, Bytecode VM, CLI)
│   ├── codegen/            # L2: M-language-to-C++20 AOT transpiler and bundler (`numkit-codegen`)
│   ├── cas/                # L3 plugin: Symbolic Math & Computer Algebra (`nkcas`)
│   ├── signal/             # L3 plugin: Signal Processing
│   ├── control/            # L3 plugin: Control Systems
│   ├── stats/              # L3 plugin: Statistics & Machine Learning
│   ├── wavelet/            # L3 plugin: Wavelet Transforms & Multiresolution Analysis
│   ├── audio/              # L3 plugin: Audio Processing & Feature Extraction
│   ├── comm/               # L3 plugin: Digital Communications
│   └── image/              # L3 plugin: Image Processing & Morphology
└── scripts/                # Ecosystem build/release utilities & architectural guards
    ├── check_layering.py   # Enforces strict acyclic dependency DAG across modules/*
    ├── check_api.py        # Verifies public C++ headers & plugin manifest.json consistency
    └── tag_release.py      # Synchronized annotated release tagger across all 13 submodules + bundle
```

External differential QA, specification-driven parity/benchmark suites, real-world corpus testing, and baseline migration audits live in the sibling repository [`numkit/qa`](https://github.com/numkit/qa).

## Quick Start

### 1. Clone with Submodules
```bash
git clone --recurse-submodules git@github.com:numkit/bundle.git
```

### 2. Configure & Build (Core + All 8 Plugins + All Test Suites)
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DNUMKIT_BUILD_TESTS=ON
cmake --build build --config Release -j
```
All executables and staged plugin shared libraries + `manifest.json` files are placed automatically under `build/bin/` (or `build/bin/Release/` on multi-config generators).

### 3. Run Unit Tests & Architectural Guards
```bash
ctest --test-dir build -C Release --output-on-failure
```

Or run the fast static architecture and API checks directly:
```bash
python3 scripts/check_layering.py
python3 scripts/check_api.py
```
