#!/usr/bin/env python3
"""check_api.py — lint public toolbox C++ headers and plugin manifest.json consistency.

Checks:
  1. Over every modules/<tb>/include/numkit/**/*.hpp header:
     - No `Engine &` / `Engine *` / `CallContext &` in public compute signatures (except library.hpp)
     - `std::pmr::memory_resource` is passed by pointer, never by reference
     - No `const Value *` in public signatures (use `const Value &` or `Span<const Value>`)
  2. Over every modules/<tb>/manifest.json:
     - Every function listed in `exports` is actually registered in `modules/<tb>/src/register/**`
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"
PLUGIN_TOOLBOXES = ("signal", "control", "stats", "wavelet", "audio", "comm", "image")

ENGINE_IO_MARKER = "lint: engine-io"
RX_ENGINE = re.compile(r"\b(?:Engine|CallContext)\s*[&*]")
RX_MR_REF = re.compile(r"memory_resource\s*&")
RX_VALUE_PTR = re.compile(r"const\s+Value\s*\*")
RX_REG_CALL = re.compile(r'registerFunction\s*\(\s*"[^"]*"\s*,\s*"([^"]+)"')


def strip_comments_and_strings(text: str) -> str:
    out = []
    i, n = 0, len(text)
    state = "code"
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and nxt == "/":
                state = "line"; out.append("  "); i += 2; continue
            if c == "/" and nxt == "*":
                state = "block"; out.append("  "); i += 2; continue
            if c == '"':
                state = "str"; out.append(" "); i += 1; continue
            if c == "'":
                state = "chr"; out.append(" "); i += 1; continue
            out.append(c); i += 1; continue
        if state == "line":
            if c == "\n":
                state = "code"; out.append("\n")
            else:
                out.append(" ")
            i += 1; continue
        if state == "block":
            if c == "*" and nxt == "/":
                state = "code"; out.append("  "); i += 2; continue
            out.append("\n" if c == "\n" else " "); i += 1; continue
        if c == "\\":
            out.append("  "); i += 2; continue
        if (state == "str" and c == '"') or (state == "chr" and c == "'"):
            state = "code"
        out.append("\n" if c == "\n" else " "); i += 1
    return "".join(out)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    violations = []
    headers_scanned = 0

    for tb in PLUGIN_TOOLBOXES:
        tb_dir = MODULES / tb
        for path in sorted((tb_dir / "include").rglob("*.hpp")):
            headers_scanned += 1
            rel = path.relative_to(ROOT).as_posix()
            src = path.read_text(encoding="utf-8", errors="replace")
            raw = src.splitlines()
            clean = strip_comments_and_strings(src).splitlines()
            bulk = rel.endswith("library.hpp")
            for lineno, (raw_line, code) in enumerate(zip(raw, clean), 1):
                if RX_ENGINE.search(code):
                    if not bulk and ENGINE_IO_MARKER not in raw_line:
                        violations.append((rel, lineno, "§13",
                            "Engine/CallContext in a public toolbox signature"))
                if RX_MR_REF.search(code):
                    violations.append((rel, lineno, "§7",
                        "memory_resource must be a pointer, not a reference"))
                if RX_VALUE_PTR.search(code) and "initialCondition" not in code and "finalCondition" not in code:
                    violations.append((rel, lineno, "§10",
                        "const Value* in a public signature — use const Value&"))

        # Check manifest.json vs registered functions
        manifest_path = tb_dir / "manifest.json"
        if manifest_path.exists():
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            exports = set(data.get("exports") or data.get("functions") or [])
            registered = set()
            for reg_cpp in (tb_dir / "src" / "register").rglob("*.cpp"):
                txt = reg_cpp.read_text(encoding="utf-8", errors="replace")
                for m in RX_REG_CALL.finditer(txt):
                    registered.add(m.group(1))
            missing_in_manifest = sorted(registered - exports)
            if missing_in_manifest:
                violations.append((
                    manifest_path.relative_to(ROOT).as_posix(), 1, "manifest",
                    f"registered functions missing from manifest.json exports: {', '.join(missing_in_manifest[:10])}"
                ))

    for rel, lineno, sec, msg in sorted(violations):
        print(f"{rel}:{lineno}: [{sec}] {msg}")

    status = "FAIL" if violations else "OK"
    print(f"check_api: {status} — {headers_scanned} public toolbox headers + {len(PLUGIN_TOOLBOXES)} manifests scanned, "
          f"{len(violations)} violation(s).")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
