#!/usr/bin/env python3
"""argcheck_audit.py — adoption report + fail-on-new gate for the
argcheck-separation pattern across `modules/*`.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODULES = ROOT / "modules"
BASELINE = HERE / "baselines" / "argcheck_baseline.json"

RE_RAW_CAST = re.compile(r"static_cast<(?:size_t|int)>\([^)]*toScalar\(\)\)")
RE_RAW_ARITY = re.compile(r"if\s*\(\s*args\.size\(\)\s*<")
RE_ARGCHECK = re.compile(r"argcheck::")
RE_FN_ARGCHECK = re.compile(r"\w+_argcheck\s*\(")
RE_TRADEMARK_STRING = re.compile(r'"[^"\n]*MATLAB[^"\n]*"')

R0_ALLOWLIST = {"modules/numkit/src/runtime/saveload_mat.cpp"}


def trademark_string_violations():
    out = []
    files = list(MODULES.rglob("*.cpp")) + list(MODULES.rglob("*.hpp"))
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if "tests" in rel or "_test" in rel or "/build/" in rel or "/apps/" in rel or rel in R0_ALLOWLIST:
            continue
        for i, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if "MATLAB" not in line:
                continue
            code = line.split("//")[0]
            m = RE_TRADEMARK_STRING.search(code)
            if m:
                out.append(f"{rel}:{i}: {m.group(0)[:90]}")
    return out


def reg_files():
    for f in sorted(MODULES.rglob("*_reg.cpp")):
        rel = f.relative_to(ROOT).as_posix()
        if "/build/" in rel:
            continue
        src = f.read_text(encoding="utf-8", errors="replace")
        yield rel, {
            "adopted": 1 if RE_ARGCHECK.search(src) else 0,
            "raw_cast": 1 if RE_RAW_CAST.search(src) else 0,
            "raw_arity": 1 if (RE_RAW_ARITY.search(src)
                               and not RE_ARGCHECK.search(src)) else 0,
        }


def compute_stats() -> tuple[int, int]:
    total = adopted = 0
    for f in sorted(MODULES.rglob("*.cpp")):
        rel = f.relative_to(ROOT).as_posix()
        if "/build/" in rel or "/tests/" in rel or rel.endswith("_reg.cpp") or rel.endswith("module.cpp"):
            continue
        src = f.read_text(encoding="utf-8", errors="replace")
        total += 1
        if RE_FN_ARGCHECK.search(src) or RE_ARGCHECK.search(src):
            adopted += 1
    return total, adopted


def report(summary: bool) -> None:
    tm = trademark_string_violations()
    print(f"=== R0 trademark strings (shipped, non-allowlist): {len(tm)} ===")
    for v in tm:
        print(f"  {v}")
    per_dir: dict[str, dict] = {}
    for rel, st in reg_files():
        domain = rel.split("/")[1]
        d = per_dir.setdefault(domain, {"files": 0, "adopted": 0,
                                        "raw_cast": 0, "raw_arity": 0})
        d["files"] += 1
        d["adopted"] += st["adopted"]
        d["raw_cast"] += st["raw_cast"]
        d["raw_arity"] += st["raw_arity"]

    print("=== argcheck adoption: reg adapters (modules/*) ===")
    print(f"{'module':<14}{'files':>7}{'adopted':>9}"
          f"{'raw-cast':>10}{'raw-arity':>11}")
    tot = {"files": 0, "adopted": 0, "raw_cast": 0, "raw_arity": 0}
    for dom, d in sorted(per_dir.items()):
        for k in tot:
            tot[k] += d[k]
        if not summary:
            print(f"{dom:<14}{d['files']:>7}{d['adopted']:>9}"
                  f"{d['raw_cast']:>10}{d['raw_arity']:>11}")
    print(f"{'TOTAL':<14}{tot['files']:>7}{tot['adopted']:>9}"
          f"{tot['raw_cast']:>10}{tot['raw_arity']:>11}")

    c_tot, c_ad = compute_stats()
    print(f"\n=== compute files referencing <fn>_argcheck / argcheck:: "
          f"=== {c_ad}/{c_tot}")


def write_baseline() -> None:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    files = dict(reg_files())
    c_tot, c_ad = compute_stats()
    payload = {
        "generated": datetime.date.today().isoformat(),
        "compute_adopted": c_ad,
        "compute_total": c_tot,
        "reg_files": files,
    }
    BASELINE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"wrote {BASELINE.relative_to(ROOT)} ({len(files)} reg files)")


def gate() -> int:
    if not BASELINE.exists():
        print(f"MISSING baseline {BASELINE} — run with --write-baseline first",
              file=sys.stderr)
        return 2
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    base_files: dict[str, dict] = base["reg_files"]
    cur_files = dict(reg_files())

    problems: list[str] = []
    for v in trademark_string_violations():
        problems.append(f"R0 TRADEMARK STRING in shipped literal: {v}")
    for rel, cur in cur_files.items():
        prev = base_files.get(rel)
        if prev is None:
            if cur["raw_cast"]:
                problems.append(
                    f"NEW raw static_cast<...>(toScalar()) in {rel}")
            if cur["raw_arity"]:
                problems.append(
                    f"NEW hand-rolled arity check in {rel}")
            continue
        if prev["adopted"] and not cur["adopted"]:
            problems.append(f"REGRESSION {rel}: lost argcheck:: reference")
        if not prev["raw_cast"] and cur["raw_cast"]:
            problems.append(f"REGRESSION {rel}: gained raw toScalar() cast")
        if not prev["raw_arity"] and cur["raw_arity"]:
            problems.append(f"REGRESSION {rel}: gained hand-rolled arity check")

    if problems:
        print("argcheck_audit --gate FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  * {p}", file=sys.stderr)
        return 1
    print(f"argcheck_audit --gate OK ({len(cur_files)} reg files checked)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args()
    if args.write_baseline:
        write_baseline()
        return 0
    if args.gate:
        return gate()
    report(args.summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
