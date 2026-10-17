#!/usr/bin/env python3
"""Signature audit: compare MATLAB's documented signature against NumKit's.

  python parity/signprobe.py mapminmax hardlim        # audit specific functions
  python parity/signprobe.py --batch fns.list         # audit a list (one fn per line)
"""
import re
import subprocess
import sys
from pathlib import Path

from run_parity import NK_EXE, MATLAB_EXE


def matlab_help(fns):
    """One MATLAB batch call for the whole list: prints per-fn help blocks."""
    calls = ";\n".join(
        f"try, disp('===FN==={f}'), disp(evalc('help {f}')), catch e, disp(['NOHELP: ' e.message]), end"
        for f in fns)
    p = subprocess.run([str(MATLAB_EXE), "-batch", calls], capture_output=True, timeout=240)
    out = p.stdout.decode("utf-8", "replace")
    blocks = {}
    for part in out.split("===FN===")[1:]:
        name, _, rest = part.partition("\n")
        blocks[name.strip()] = rest
    return blocks


def nk_help(fns):
    blocks = {}
    for f in fns:
        p = subprocess.run([str(NK_EXE), "-e", f"help {f}"],
                           capture_output=True, timeout=60)
        blocks[f] = p.stdout.decode("utf-8", "replace")
    return blocks


def signature_lines(help_text, fn):
    sig = []
    for line in help_text.splitlines():
        s = line.strip()
        if not s:
            if sig:
                break
            continue
        started = bool(sig)
        if s.startswith(fn) or (started and re.match(r"^[a-z]\w*\s*\(", s)):
            sig.append(s)
        elif started:
            break
    return sig or [f"(no signature line for '{fn}' in help)"]


def audit(fns):
    ml = matlab_help(fns)
    nk = nk_help(fns)
    n_match = 0
    for f in fns:
        a = signature_lines(ml.get(f, ""), f)
        b = signature_lines(nk.get(f, ""), f)
        norm = lambda xs: [re.sub(r"\s+", " ", x) for x in xs]
        if norm(a) == norm(b):
            print(f"  OK    {f:<20} {a[0][:70]}")
            n_match += 1
        else:
            print(f"  DIFF  {f}:")
            for x in a[:3]:
                print(f"        matlab: {x[:90]}")
            for x in b[:3]:
                print(f"        numkit: {x[:90]}")
    print(f"\n{n_match}/{len(fns)} signatures match")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--batch":
        fns = [l.strip() for l in Path(args[1]).read_text().splitlines()
               if l.strip() and not l.startswith("#")]
    else:
        fns = args
    audit(fns)
