# NumKit Multi-Language Bindings (`bindings/`)

This directory contains the canonical **C-ABI layer (`numkit_c.h`)**, automatic **binding generator (`codegen/gen_bindings.py`)**, and official **Python** and **Rust** SDKs for the NumKit scientific computing ecosystem.

---

## Architecture

1. **Canonical C-ABI (`bindings/c_api/`):**
   - Header: [`c_api/include/numkit_c.h`](c_api/include/numkit_c.h) (pure C99/C11, zero C++ dependencies).
   - **`libnumkit_c_lite`**: Engine-free toolbox-only runtime (`numkit_ctx_create_lite`). Links **only** `numkit_value`, `numkit_sys`, and `numkit_ops` (no `.m` parser, AST, or VM). Dynamically loads any of the 8 toolbox plugins (`signal`, `control`, `stats`, `wavelet`, `audio`, `comm`, `image`, `cas`).
   - **`libnumkit_c`**: Unified library supporting both Lite mode (`numkit_ctx_create_lite`) and Full Engine mode (`numkit_ctx_create_full`, enabling `numkit_eval("...")` and workspace access).
   - **Zero-Copy Views**: `numkit_val_view` wraps host memory (`numpy.ndarray` in Fortran order or Rust `&[f64]`) via `numkit::Value::view` in $O(1)$ without copying, with automatic Copy-on-Write if mutated.

2. **Binding Generator (`bindings/codegen/gen_bindings.py`):**
   - Scans `modules/<tb>/manifest.json`, `modules/<tb>/include/numkit/<tb>/**/*.hpp`, and `audits/baselines/arity_reference.json`.
   - Generates **1,128 toolbox functions** (881 with strict C++ header signatures) across all 8 toolboxes for both Python (`.py` + `.pyi` PEP 484 type stubs) and Rust (`src/tb/*.rs`).

3. **Python SDK (`bindings/python/`):**
   - Supports automatic multi-output tuple unpacking (`b, a = signal.butter(4, 0.25)`), zero-copy NumPy arrays (when `numpy` is installed), and pure-Python sequences (when `numpy` is absent).

4. **Rust SDK (`bindings/rust/`):**
   - Workspace with `numkit-sys` (raw FFI) and `numkit` (safe RAII `Value` with `Drop`/`Clone`, lifetime-checked `ValueView<'a>`, strongly-typed `<fn>_typed` functions, and dynamic MATLAB overload calls).

---

## Quick Usage

### Regenerate Python & Rust Toolbox Modules
```bash
python3 bindings/codegen/gen_bindings.py
```

### Run C-ABI and Python Tests
```bash
ctest --test-dir build -R numkit_c_api_test --output-on-failure
python3 bindings/python/tests/test_python_api.py
```
