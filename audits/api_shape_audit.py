#!/usr/bin/env python3
"""api_shape_audit.py — public-API signature-shape report + fail-on-new
gate for the memory_resource placement rule across `modules/*`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODULES = ROOT / "modules"
BASELINE = HERE / "baselines" / "api_shape_baseline.json"

PUBLIC_GLOBS = [
    "modules/*/include/numkit/**/*.hpp",
]

DECL_RE = re.compile(r"^[ \t]*(?:[\w:<>,&* ]+?\s+)?(\w+)\s*\(", re.M)
MR_RE = re.compile(r"std::pmr::memory_resource\s*\*\s*(\w+)")
SKIP_PREFIXES = ("using ", "typedef ", "#", "friend ", "static_assert")
SKIP_NAMES = {"operator", "sizeof", "if", "for", "while", "switch",
              "return", "catch"}


def strip_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    return src


def scan_header(path: Path):
    src = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    rel = path.relative_to(ROOT).as_posix()
    if "/detail/" in rel or "/core/" in rel or "/value/" in rel or "/sys/" in rel:
        return
    for m in DECL_RE.finditer(src):
        line_start = src.rfind("\n", 0, m.start()) + 1
        line_prefix = src[line_start:m.start()]
        stripped = src[line_start:].lstrip()
        if any(stripped.startswith(p) for p in SKIP_PREFIXES):
            continue
        if any(line_prefix.strip().startswith(p) for p in SKIP_PREFIXES):
            continue
        name = m.group(1)
        if name in SKIP_NAMES:
            continue
        depth, i = 0, m.end() - 1
        start = i
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if depth != 0:
            continue
        params = src[start + 1:i]
        pm = MR_RE.search(params)
        if not pm:
            continue
        rest = params[pm.end():].strip()
        line = src.count("\n", 0, m.start()) + 1
        if rest.startswith(",") or (rest.startswith("= nullptr")
                                    and rest[len("= nullptr"):].lstrip()
                                    .startswith(",")):
            yield rel, name, line, "mr-not-last"
        elif not rest.startswith("= nullptr"):
            yield rel, name, line, "mr-no-default"


def collect(globs):
    out = []
    seen = set()
    for g in globs:
        for p in sorted(ROOT.glob(g)):
            if p in seen:
                continue
            seen.add(p)
            out.extend(scan_header(p))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args()

    pub = collect(PUBLIC_GLOBS)
    cur_map = {}
    for rel, name, _line, kind in pub:
        cur_map.setdefault(f"{rel}::{name}", []).append(kind)
    for k in cur_map:
        cur_map[k].sort()

    if args.write_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(
            json.dumps({"public_violations": cur_map}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"wrote {BASELINE.relative_to(ROOT)} ({len(pub)} public violation(s))")
        return 0

    if args.gate:
        if not BASELINE.exists():
            print(f"MISSING baseline {BASELINE} — run with --write-baseline", file=sys.stderr)
            return 2
        base = json.loads(BASELINE.read_text(encoding="utf-8"))["public_violations"]
        problems = []
        for key, kinds in sorted(cur_map.items()):
            prev = base.get(key)
            if prev is None:
                problems.append(f"NEW public API violation: {key} -> {kinds}")
            elif len(kinds) > len(prev) or set(kinds) - set(prev):
                problems.append(f"REGRESSION {key}: was {prev}, now {kinds}")
        if problems:
            print("api_shape_audit --gate FAILED:", file=sys.stderr)
            for p in problems:
                print(f"  * {p}", file=sys.stderr)
            return 1
        print(f"api_shape_audit --gate OK ({len(pub)} public violation(s) <= baseline)")
        return 0

    print(f"=== PUBLIC headers: {len(pub)} violation(s) ===")
    for rel, name, line, kind in pub:
        print(f"  {rel}:{line}: {name}  [{kind}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
