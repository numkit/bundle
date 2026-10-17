#!/usr/bin/env python3
"""Architectural layering guard for numkit/bundle.

Enforces the strict acyclic dependency DAG across `modules/*`:

    value    (L0)   -> value
    sys      (L0)   -> value, sys
    ops      (L1)   -> value, ops (and its own builtin/linalg/ode/optim/signal/image compute headers)
                       NEVER sys, core, runtime, pkg, or plugin toolboxes
    numkit   (L2)   -> value, sys, ops, core, runtime, pkg, builtin, linalg, ode, optim, graphics, io, codegen, scriptgraph
                       NEVER plugin-only toolboxes (stats, control, wavelet, audio, comm)
    plugins  (L3)   -> compute TUs (outside src/register/ and src/module.cpp) must never include <numkit/core/...>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"

INCLUDE_RE = re.compile(r'#\s*include\s*<numkit/([a-zA-Z0-9_]+)/')
SRC_SUFFIXES = {".cpp", ".hpp", ".h", ".cc", ".cxx", ".ipp"}

OPS_OWN_PREFIXES = {"value", "ops", "builtin", "linalg", "ode", "optim", "signal", "image"}
CORE_ALLOWED_PREFIXES = OPS_OWN_PREFIXES | {
    "sys", "core", "runtime", "pkg", "graphics", "io", "codegen", "scriptgraph"
}
PLUGIN_TOOLBOXES = ("signal", "control", "stats", "wavelet", "audio", "comm", "image")


def iter_source_files(root: Path):
    for d in ("include", "src"):
        sub = root / d
        if not sub.exists():
            continue
        for p in sorted(sub.rglob("*")):
            if p.is_file() and p.suffix in SRC_SUFFIXES:
                yield p


def main() -> int:
    violations: list[str] = []
    scanned = 0

    # 1. value (L0)
    for f in iter_source_files(MODULES / "value"):
        scanned += 1
        rel = f.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = INCLUDE_RE.search(line)
            if m and m.group(1) != "value":
                violations.append(f"{rel}:{lineno}: [value] forbidden include <numkit/{m.group(1)}/...>")

    # 2. sys (L0)
    for f in iter_source_files(MODULES / "sys"):
        scanned += 1
        rel = f.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = INCLUDE_RE.search(line)
            if m and m.group(1) not in {"value", "sys"}:
                violations.append(f"{rel}:{lineno}: [sys] forbidden include <numkit/{m.group(1)}/...>")

    # 3. ops (L1)
    for f in iter_source_files(MODULES / "ops"):
        scanned += 1
        rel = f.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = INCLUDE_RE.search(line)
            if m and m.group(1) not in OPS_OWN_PREFIXES:
                violations.append(f"{rel}:{lineno}: [ops] forbidden include <numkit/{m.group(1)}/...>")

    # 4. numkit (L2)
    for f in iter_source_files(MODULES / "numkit"):
        scanned += 1
        rel = f.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = INCLUDE_RE.search(line)
            if m and m.group(1) not in CORE_ALLOWED_PREFIXES:
                violations.append(f"{rel}:{lineno}: [numkit] forbidden plugin include <numkit/{m.group(1)}/...>")

    # 5. Plugin toolboxes (L3): compute TUs must not include <numkit/core/...>
    for tb in PLUGIN_TOOLBOXES:
        tb_dir = MODULES / tb
        manifest = tb_dir / "manifest.json"
        if not manifest.exists():
            violations.append(f"modules/{tb}/manifest.json: missing plugin manifest")
        else:
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                if not data.get("exports") and not data.get("functions"):
                    violations.append(f"modules/{tb}/manifest.json: empty exports list")
            except Exception as e:
                violations.append(f"modules/{tb}/manifest.json: invalid JSON ({e})")

        for f in iter_source_files(tb_dir):
            scanned += 1
            rel = f.relative_to(ROOT).as_posix()
            for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                m = INCLUDE_RE.search(line)
                if m and m.group(1) == "core":
                    violations.append(f"{rel}:{lineno}: [{tb}] plugin must use <numkit/sys/plugin.hpp>, not <numkit/core/...>")

    for v in violations:
        print(f"  VIOLATION: {v}")

    status = "FAIL" if violations else "OK"
    print(f"check_layering: {status} — {scanned} source/header files scanned across 11 submodules, "
          f"{len(violations)} violation(s).")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
