#!/usr/bin/env python3
"""Dual-run harness: real scripts through MATLAB R2025b vs NumKit (native + optional WASM).

  python harness.py harvest [N] [flt]   static candidate selection -> data/candidates.json
  python harness.py qualify [N] [flt]   MATLAB-verify candidates -> data/runnable.json
                                        (the committed run corpus — R3)
  python harness.py run [N] [flt]       dual-run runnable.json scripts; compare
                                        workspaces via .mat files (R4) -> reports/
  python harness.py matdiff a.mat b.mat standalone workspace comparator
  python harness.py used-fns <report-json>   list absent fns from a report

Comparison semantics (README "Comparison semantics"): the harness appends
save('<tmp>/out_<engine>.mat') to each run; both .mat files are read by
scipy.io.loadmat (engine-neutral) and numeric variables of the intersection
are compared — class and shape exactly, values at rel 1e-9, NaN==NaN,
±Inf equal to themselves. stdout/exit still drive the parse-error /
runtime-error classes and diagnostics, but the numeric verdict comes from
the workspace; print-format divergences do not count.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.io import loadmat

HERE = Path(__file__).parent
CORPUS = Path(os.environ.get("NUMKIT_CORPUS_DIR", HERE / "corpus"))
WORK = CORPUS / "work"
REPORTS = HERE / "reports"
RUNNABLE = HERE / "data" / "runnable.json"
CANDIDATES = HERE / "data" / "candidates.json"
TMP = CORPUS / "tmp"
CATALOG_CACHE = CORPUS / "catalog.json"
NK = HERE.parent
WASM_CLI = NK / "packages" / "nk" / "bin" / "cli.js"


def _resolve_native_cli():
    for c in (NK / "build" / "bin" / "Release" / "numkit.exe",
              NK / "build" / "bin" / "numkit.exe",
              NK / "build" / "bin" / "numkit",
              NK / "modules" / "numkit" / "build" / "Release" / "numkit.exe"):
        if c.exists():
            return c
    return NK / "build" / "bin" / "Release" / "numkit.exe"


NATIVE_CLI = _resolve_native_cli()
MATLAB = Path(r"C:\Program Files\MATLAB\R2025b\bin\matlab.exe")

REL_TOL = 1e-9

BAD_TOKENS = ["input(", "urlread", "system(", "java.", "actxserver", "parfor",
              "gpuArray", "sym(", "sim(", "mex", "waitfor", "pause(", "tic",
              "clock", "now,", "datenum", "websave", "webread", "video",
              "aviread", "VideoReader"]
# Graphics calls are NOT filtered: both engines execute them headless
# (numkit runs its graphics system and emits __FIGURE_DATA__ for the IDE;
# MATLAB -batch creates invisible figures) and the verdict comes from the
# workspace .mat comparison (R4), to which plots are irrelevant.

ANSWERS_FILE = HERE / "data" / "answers.json"


def answers_for(script):
    """Canned input() answers for INTERACTIVE scripts (list[str] or None)."""
    if not ANSWERS_FILE.exists():
        return None
    try:
        rel = str(Path(script).relative_to(HERE)).replace("\\", "/")
    except ValueError:
        rel = str(script).replace("\\", "/")
    doc = json.loads(ANSWERS_FILE.read_text(encoding="utf-8"))
    return doc.get(rel)


def harvest(limit=None, flt=None, answered=False):
    if answered:
        out = []
        doc = json.loads(ANSWERS_FILE.read_text(encoding="utf-8")) if ANSWERS_FILE.exists() else {}
        for rel in sorted(doc):
            s = HERE / rel
            if not s.exists():
                continue
            if flt and flt.lower() not in str(s).lower():
                continue
            out.append(str(s.relative_to(HERE)))
        return out[:limit] if limit is not None else out
    return _harvest_default(limit, flt)


def _harvest_default(limit=None, flt=None):
    picked, seen = [], set()
    for repo in sorted(WORK.iterdir()):
        if not repo.is_dir():
            continue
        for m in repo.rglob("*.m"):
            try:
                txt = m.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            first_code = re.sub(r"%[^\n]*\n", "", txt.lstrip())
            if first_code.lstrip().startswith("function"):
                continue
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\.m", m.name):
                continue
            if m.stat().st_size > 40_000 or txt.count("\n") > 500:
                continue
            low = txt.lower()
            if any(b in low if "(" in b else re.search(r"\b" + re.escape(b) + r"\b", low)
                   for b in BAD_TOKENS):
                continue
            if flt and flt.lower() not in str(m).lower():
                continue
            if m.name in seen:
                continue
            seen.add(m.name)
            try:
                picked.append(str(m.relative_to(HERE)))
            except ValueError:
                picked.append(str(m))
            if limit is not None and len(picked) >= limit:
                break
        if limit is not None and len(picked) >= limit:
            break
    CANDIDATES.write_text(json.dumps(picked, indent=1), encoding="utf-8")
    print(f"harvested {len(picked)} candidates -> {CANDIDATES.name}")
    return picked


def _tmpdir(script):
    try:
        rel_part = str(Path(script).relative_to(WORK))
    except ValueError:
        rel_part = Path(script).name
    d = TMP / re.sub(r"[^A-Za-z0-9_.-]", "_", rel_part)[:180]
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def run_engine(kind, script, mat_out=None, answers=None):
    """Run `script`; if mat_out is given, save the workspace there after it."""
    s = (HERE / script) if not Path(script).is_absolute() else Path(script)
    cwd = str(s.parent)
    stub = s.parent / "input.m"
    stdin_text = None
    if answers is not None:
        stdin_text = "\n".join(answers) + "\n"
        if kind == "matlab":
            quoted = " ".join("'{}'".format(a.replace("'", "''")) for a in answers)
            stub.write_text(
                "function varargout = input(prompt, fmt)\n"
                "% numkit fieldtest stub (harness-generated): answers injected\n"
                "% because Windows MATLAB -batch rejects the real input().\n"
                "persistent QUEUE\n"
                "if isempty(QUEUE)\n"
                f"  QUEUE = {{ {quoted} }};\n"
                "end\n"
                "if isempty(QUEUE)\n"
                "  s = '';\n"
                "else\n"
                "  s = QUEUE{1};\n"
                "  QUEUE(1) = [];\n"
                "end\n"
                "if nargin > 1\n"
                "  varargout{1} = s;\n"
                "elseif isempty(s)\n"
                "  varargout{1} = [];\n"
                "else\n"
                "  varargout{1} = eval(s);\n"
                "end\n",
                encoding="utf-8")
    try:
        return _run_engine_argv(kind, s, cwd, mat_out, stdin_text)
    finally:
        if stub.exists():
            stub.unlink()


def _run_engine_argv(kind, s, cwd, mat_out, stdin_text):
    t0 = time.perf_counter()
    if kind == "matlab":
        argv = [str(MATLAB), "-batch",
                "restoredefaultpath; clear RESTOREDEFAULTPATH_EXECUTED; "
                + f"run('{s.as_posix()}')" +
                (f"; save('{Path(mat_out).as_posix()}')" if mat_out else "")]
    elif kind in ("wasm", "native"):
        if mat_out is None:
            argv = (["node", str(WASM_CLI), s.name] if kind == "wasm"
                    else [str(NATIVE_CLI), s.name])
        else:
            wrap = s.parent / f"__nk_wrap_{kind}.m"
            wrap.write_text(f"run('{s.as_posix()}');\nsave('{Path(mat_out).as_posix()}');\n",
                            encoding="utf-8")
            argv = (["node", str(WASM_CLI), wrap.name] if kind == "wasm"
                    else [str(NATIVE_CLI), wrap.name])
    else:
        raise ValueError(kind)
    to = 180 if kind == "matlab" else 90
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=to,
                           input=(stdin_text.encode("utf-8") if stdin_text is not None
                                  else None))
        ms = int((time.perf_counter() - t0) * 1000)
        dec = lambda b: (b or b"").decode("utf-8", "replace")
        return {"exit": p.returncode, "out": dec(p.stdout), "err": dec(p.stderr), "ms": ms}
    except subprocess.TimeoutExpired:
        return {"exit": "timeout", "out": "", "err": "", "ms": to * 1000}
    finally:
        if kind in ("wasm", "native") and mat_out is not None:
            wrap.unlink(missing_ok=True)


def _numeric_kind(arr):
    k = arr.dtype.kind
    if k == "b":
        return "b"
    if k == "c":
        return "c"
    if k in "fiu":
        return "r"
    return None


def _values_close(a, b):
    if a.dtype.kind == "b":
        return bool(np.array_equal(a, b))
    a = np.asarray(a, dtype=np.complex128 if "c" in (a.dtype.kind, b.dtype.kind) else np.float64)
    b = np.asarray(b, dtype=a.dtype)
    both_nan = np.isnan(a) & np.isnan(b)
    same_inf = np.isinf(a) & (a == b)
    close = np.abs(a - b) <= 1e-9 + REL_TOL * np.maximum(np.abs(a), np.abs(b))
    return bool(np.all(close | both_nan | same_inf))


def matdiff(path_a, path_b):
    """Compare numeric variables of two .mat files."""
    a = {k: v for k, v in loadmat(str(path_a)).items() if not k.startswith("__")}
    b = {k: v for k, v in loadmat(str(path_b)).items() if not k.startswith("__")}
    lines, ok = [], True
    for name in sorted(set(a) & set(b)):
        ka, kb = _numeric_kind(a[name]), _numeric_kind(b[name])
        if ka is None and kb is None:
            lines.append(f"skip {name}: non-numeric both sides")
            continue
        if ka is None or kb is None:
            lines.append(f"skip {name}: numeric on one side only ({ka} vs {kb})")
            continue
        if ka != kb:
            ok = False
            lines.append(f"DIFF {name}: class {ka} vs {kb}")
            continue
        va = a[name].toarray() if hasattr(a[name], "toarray") else np.asarray(a[name])
        vb = b[name].toarray() if hasattr(b[name], "toarray") else np.asarray(b[name])
        if va.shape != vb.shape:
            ok = False
            lines.append(f"DIFF {name}: shape {va.shape} vs {vb.shape}")
            continue
        if not _values_close(va, vb):
            with np.errstate(invalid="ignore"):
                rel = np.nanmax(np.abs(va - vb) / np.maximum(1e-300, np.maximum(np.abs(va), np.abs(vb))))
            lines.append(f"DIFF {name}: values diverge (max rel {rel:.3e})")
            ok = False
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    if only_a:
        lines.append(f"only-in-{'nk' if 'nk' in str(path_a) or 'native' in str(path_a) else 'A'}: {', '.join(only_a[:8])}")
    if only_b:
        lines.append(f"only-in-{'matlab' if 'matlab' in str(path_b) else 'B'}: {', '.join(only_b[:8])}")
    return ok, lines


NUM = re.compile(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?")


def normalise(text, script):
    t = (text or "").replace("\r", "")
    t = t.replace(str(Path(script).parent), "<DIR>").replace(Path(script).parent.as_posix(), "<DIR>")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{2,}", "\n", t)
    t = re.sub(r"[^\x20-\x7e]+", " # ", t)
    t = re.sub(r"(#\s*)+", "# ", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def stdout_equal(a, b):
    la, lb = a.splitlines(), b.splitlines()
    if len(la) != len(lb):
        return False
    for ra, rb in zip(la, lb):
        ta, tb = NUM.split(ra), NUM.split(rb)
        na, nb = NUM.findall(ra), NUM.findall(rb)
        if ta != tb or len(na) != len(nb):
            return False
        for x, y in zip(na, nb):
            fx, fy = float(x), float(y)
            if fx != fy and abs(fx - fy) > 1e-9 + 1e-6 * max(abs(fx), abs(fy)):
                return False
    return True


def classify(nk, ml):
    """Exit-code-driven classes; the numeric verdict itself is the matdiff."""
    if ml["exit"] == "timeout":
        return "matlab-timeout", ""
    if nk["exit"] == "timeout":
        return "nk-hang", ""
    nk_err, ml_err = nk["exit"] != 0, ml["exit"] != 0
    if ml_err:
        detail = (ml["err"] or ml["out"]).strip()[:120]
        if nk_err:
            return "both-error", detail
        return "matlab-only-error", detail
    if nk_err:
        msg = (nk["err"] or nk["out"]).strip()
        if "undefined function" in msg.lower():
            return "absent-fn", msg[:160]
        if "parse error" in msg.lower():
            return "parse-error", msg[:160]
        if "not supported" in msg.lower():
            return "unsupported", msg[:160]
        return "runtime-error", msg[:160]
    return None, ""


def qualify(limit=None, flt=None, answered=False):
    """MATLAB-verify candidates in PORTIONS; results merge into runnable.json."""
    cands = harvest(limit, flt, answered=answered)
    prev = {}
    if RUNNABLE.exists():
        for e in json.loads(RUNNABLE.read_text(encoding="utf-8"))["scripts"]:
            if (HERE / e["path"]).exists():
                prev[e["path"]] = e
    qualified = []
    for i, s in enumerate(cands):
        full_s = (HERE / s) if not Path(s).is_absolute() else Path(s)
        r = run_engine("matlab", full_s, answers=answers_for(full_s))
        rel = str(full_s.relative_to(HERE))
        if r["exit"] == 0:
            qualified.append({"path": rel, "matlab_ms": r["ms"]})
            prev.pop(rel, None)
        mark = "ok " if r["exit"] == 0 else f"exit={r['exit']}"
        print(f"[{i+1}/{len(cands)}] {full_s.name:<44} {mark} {r['ms']}ms")
    merged = sorted([{"path": p, **{"matlab_ms": e["matlab_ms"]}} for p, e in prev.items()] + qualified,
                    key=lambda e: e["path"])
    doc = {"qualified": f"{datetime.now():%Y-%m-%dT%H:%M:%S}",
           "scripts": merged}
    if CATALOG_CACHE.exists():
        meta = json.loads(CATALOG_CACHE.read_text(encoding="utf-8")).get("metadata", {})
        doc["catalog_compiled"] = meta.get("compiled_date")
    RUNNABLE.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nrunnable.json: +{len(qualified)}/{len(cands)} verified this portion, "
          f"{len(merged)} total (catalog {doc.get('catalog_compiled', '?')})")


def run(scripts):
    REPORTS.mkdir(exist_ok=True)
    results = []
    for i, s in enumerate(scripts):
        s_path = (HERE / s) if not Path(s).is_absolute() else Path(s)
        rel = str(s_path.relative_to(HERE))
        ans = answers_for(s_path)
        d = _tmpdir(s_path)
        native = run_engine("native", s_path, mat_out=d / "out_native.mat", answers=ans)
        native2 = run_engine("native", s_path, mat_out=d / "out_native2.mat", answers=ans)
        det_ok, det_lines = True, ["(probe unavailable)"]
        if (d / "out_native.mat").exists() and (d / "out_native2.mat").exists():
            det_ok, det_lines = matdiff(d / "out_native.mat", d / "out_native2.mat")
        ml = run_engine("matlab", s_path, mat_out=d / "out_matlab.mat", answers=ans)

        v, detail = classify(native, ml)
        mat_ok, mat_lines, stdout_ok = None, [], None
        if v is None:
            stdout_ok = stdout_equal(normalise(native["out"], s_path), normalise(ml["out"], s_path))
            if not det_ok:
                v, detail = "nondeterministic", "; ".join(det_lines)[:160]
            elif (d / "out_native.mat").exists() and (d / "out_matlab.mat").exists():
                mat_ok, mat_lines = matdiff(d / "out_native.mat", d / "out_matlab.mat")
                v = "pass" if mat_ok else "workspace-mismatch"
                detail = "; ".join(mat_lines[:6])[:400]
            else:
                v, detail = "runtime-error", "no workspace .mat produced"
        r = {"script": rel, "verdict": v, "detail": detail,
             "native_ms": native["ms"], "matlab_ms": ml["ms"],
             "stdout_match": stdout_ok,
             "mat_diff": mat_lines[:20],
             "nk_out": (native["out"] or native["err"])[:800],
             "matlab_out": (ml["out"] or ml["err"])[:800]}
        results.append(r)
        print(f"[{i+1}/{len(scripts)}] {Path(rel).name:<40} {v:<20} "
              f"native={r['native_ms']}ms matlab={r['matlab_ms']}ms")
        shutil.rmtree(d, ignore_errors=True)
    out = REPORTS / f"{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nreport: {out}")
    print("=== SUMMARY ===")
    for k, n in Counter(r["verdict"] for r in results).most_common():
        print(f"{n:>4}  {k}")


def load_runnable(n, flt):
    if not RUNNABLE.exists():
        sys.exit("no runnable.json — run `python harness.py qualify` first (R3)")
    doc = json.loads(RUNNABLE.read_text(encoding="utf-8"))
    scripts = [s["path"] for s in doc["scripts"]]
    if flt:
        scripts = [s for s in scripts if flt.lower() in s.lower()]
    return scripts[:n] if n else scripts


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    flt = sys.argv[3] if len(sys.argv) > 3 else None
    if cmd == "harvest":
        harvest(n, flt)
    elif cmd == "qualify":
        qualify(n, flt, answered="--answered" in sys.argv)
    elif cmd == "run":
        run(load_runnable(n, flt))
    elif cmd == "matdiff":
        ok, lines = matdiff(sys.argv[2], sys.argv[3])
        print("\n".join(lines) or "identical (numeric intersection)")
        sys.exit(0 if ok else 1)
    elif cmd == "used-fns":
        for r in json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")):
            if r["verdict"] == "absent-fn":
                m = re.search(r"function '([^']+)'", r["detail"])
                if m:
                    print(m.group(1))
    else:
        sys.exit(__doc__)
