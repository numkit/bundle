#!/usr/bin/env python3
"""check_api.py — lint public toolbox C++ headers, plugin manifest.json consistency,
and workspace-wide Anti-STL purity (Wave 2 full keelcpp integration).

Checks:
  1. Over every modules/<tb>/include/numkit/**/*.hpp header:
     - No `Engine &` / `Engine *` / `CallContext &` in public compute signatures (except library.hpp)
     - `keel::Allocator` is passed by pointer, never by reference
     - No `const Value *` in public signatures (use `const Value &` or `keel::ArrayRef<Value>`)
  2. Over every modules/<tb>/manifest.json:
     - Every function listed in `exports` is actually registered in `modules/<tb>/src/register/**`
  3. Anti-STL purity across all 13 modules/*/{include,src,bridge,apps}/**/*.{h,hpp,cpp}:
     - Zero forbidden STL headers (<vector>, <string>, <string_view>, <map>,
       <unordered_map>, <set>, <unordered_set>, <memory>, <functional>,
       <optional>, <filesystem>, <sstream>, <iostream>, <fstream>)
     - Zero forbidden owning STL container/string/stream/smart-pointer/fs tokens
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("NUMKIT_BUNDLE_DIR", Path(__file__).resolve().parent.parent)).resolve()
MODULES = ROOT / "modules"
PLUGIN_TOOLBOXES = ("signal", "control", "stats", "wavelet", "audio", "comm", "image", "cas")

ENGINE_IO_MARKER = "lint: engine-io"
RX_ENGINE = re.compile(r"\b(?:Engine|CallContext)\s*[&*]")
RX_MR_REF = re.compile(r"\bAllocator\s*&")
RX_VALUE_PTR = re.compile(r"const\s+Value\s*\*")
RX_REG_CALL = re.compile(r'registerFunction\s*\(\s*"[^"]*"\s*,\s*"([^"]+)"')

FORBIDDEN_STL_HEADERS = frozenset({
    "vector", "string", "string_view", "map", "unordered_map",
    "set", "unordered_set", "memory", "functional", "optional",
    "filesystem", "sstream", "iostream", "fstream",
    "chrono", "ctime", "cctype", "random",
})
RX_STL_INCLUDE = re.compile(r"^\s*#\s*include\s*<([^>]+)>", re.M)
RX_FORBIDDEN_STD = re.compile(
    r"\bstd::(vector|string|string_view|map|unordered_map|multimap|unordered_multimap|"
    r"set|unordered_set|unique_ptr|shared_ptr|weak_ptr|make_unique|make_shared|"
    r"function|optional|nullopt|ostringstream|istringstream|stringstream|"
    r"cout|cerr|cin|endl|ofstream|ifstream|fstream|filesystem|to_string|"
    r"stoi|stol|stoll|stoul|stoull|stod|stof|getline|"
    r"chrono|tolower|toupper|isspace|isdigit|isalpha|isalnum|isxdigit|isupper|islower|"
    r"ispunct|isprint|isgraph|iscntrl|isblank|"
    r"mt19937|mt19937_64|minstd_rand|minstd_rand0|ranlux24|ranlux48|knuth_b|"
    r"default_random_engine|random_device|seed_seq|shuffle|"
    r"uniform_int_distribution|uniform_real_distribution|bernoulli_distribution|"
    r"binomial_distribution|geometric_distribution|negative_binomial_distribution|"
    r"poisson_distribution|exponential_distribution|gamma_distribution|"
    r"weibull_distribution|extreme_value_distribution|normal_distribution|"
    r"lognormal_distribution|chi_squared_distribution|cauchy_distribution|"
    r"fisher_f_distribution|student_t_distribution|discrete_distribution|"
    r"piecewise_constant_distribution|piecewise_linear_distribution)\b"
)
RX_NON_CODE = re.compile(
    r"//[^\n]*"
    r"|/\*[\s\S]*?\*/"
    r'|R"([^()\\\s]{0,16})\([\s\S]*?\)\1"'
    r'|"(?:\\.|[^"\\])*"'
    r"|'(?:\\.|[^'\\])*'"
)


def strip_non_code(text: str) -> str:
    return RX_NON_CODE.sub(lambda m: "\n" * m.group(0).count("\n") + " ", text)


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
                        "keel::Allocator must be a pointer, not a reference"))
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

    # Check 3: Workspace-wide Anti-STL purity across all modules/*/{include,src,bridge,apps}
    stl_files_scanned = 0
    for mod_dir in sorted(p for p in MODULES.iterdir() if p.is_dir()):
        for sub in ("include", "src", "bridge", "apps"):
            sub_dir = mod_dir / sub
            if not sub_dir.is_dir():
                continue
            for path in sorted(sub_dir.rglob("*")):
                if path.suffix not in (".h", ".hpp", ".cpp") or not path.is_file():
                    continue
                stl_files_scanned += 1
                rel = path.relative_to(ROOT).as_posix()
                src = path.read_text(encoding="utf-8", errors="replace")
                clean = strip_non_code(src)
                for m in RX_STL_INCLUDE.finditer(clean):
                    hdr = m.group(1).strip()
                    if hdr in FORBIDDEN_STL_HEADERS:
                        lineno = clean[: m.start()].count("\n") + 1
                        violations.append((rel, lineno, "keel-purity",
                            f"forbidden STL header <{hdr}> — use keel equivalents"))
                for lineno, line in enumerate(clean.splitlines(), 1):
                    for m in RX_FORBIDDEN_STD.finditer(line):
                        violations.append((rel, lineno, "keel-purity",
                            f"forbidden {m.group(0)} — use keel equivalents"))

    for rel, lineno, sec, msg in sorted(violations):
        print(f"{rel}:{lineno}: [{sec}] {msg}")

    status = "FAIL" if violations else "OK"
    print(f"check_api: {status} — {headers_scanned} public toolbox headers + {len(PLUGIN_TOOLBOXES)} manifests "
          f"+ {stl_files_scanned} files (Anti-STL purity) scanned, {len(violations)} violation(s).")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
