#!/usr/bin/env python3
"""
Parity harness for NumKit (numkit/bundle).

Runs function specs against three engines (numkit native, MATLAB R2025b,
Octave 11.1.0), compares output for correctness, measures wall-clock time,
and updates PROGRESS.md and BENCHMARK.md.

Usage:
    python parity/run_parity.py parity/specs/core/erf.json
    python parity/run_parity.py erf                         # auto-resolves across specs/*/
    python parity/run_parity.py --module signal             # run all signal specs
    python parity/run_parity.py --module signal --isolated  # test in NamespaceMode::Isolated
    python parity/run_parity.py --all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PARITY_DIR = Path(__file__).resolve().parent
ROOT = PARITY_DIR.parent
SPECS_ROOT = PARITY_DIR / "specs"
PROGRESS_MD = PARITY_DIR / "PROGRESS.md"
BENCHMARK_MD = PARITY_DIR / "BENCHMARK.md"


def _find_numkit_exe() -> Path:
    candidates = [
        ROOT / "build" / "bin" / "Release" / "numkit.exe",
        ROOT / "build" / "bin" / "numkit.exe",
        ROOT / "build" / "bin" / "numkit",
        ROOT / "build" / "Release" / "numkit.exe",
        ROOT / "modules" / "numkit" / "build" / "Release" / "numkit.exe",
        ROOT.parent / "numkit" / "build" / "Release" / "numkit.exe",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0] if sys.platform == "win32" else candidates[2]


NK_EXE = _find_numkit_exe()
MATLAB_EXE = "matlab"
OCTAVE_EXE = r"C:\Program Files\GNU Octave\Octave-11.1.0\mingw64\bin\octave-cli.exe"


def _nk_stale() -> tuple[float, float, str] | None:
    """Detect whether numkit.exe / staged plugins are older than any submodule source file."""
    if not NK_EXE.exists():
        return None
    exe_mtime = NK_EXE.stat().st_mtime
    plugins_dir = NK_EXE.parent / "modules"
    if plugins_dir.exists():
        for p in plugins_dir.rglob("*"):
            if p.suffix in (".dll", ".so", ".dylib"):
                try:
                    exe_mtime = max(exe_mtime, p.stat().st_mtime)
                except OSError:
                    pass
    newest_mtime = 0.0
    newest_path: Path | None = None
    modules_dir = ROOT / "modules"
    if not modules_dir.exists():
        return None
    for dirpath, dirs, files in os.walk(modules_dir):
        dirs[:] = [d for d in dirs if d not in ("tests", "benchmarks", "build", ".git")]
        for f in files:
            if f.endswith((".cpp", ".cc", ".cxx", ".hpp", ".h")):
                fp = Path(dirpath) / f
                try:
                    m = fp.stat().st_mtime
                except OSError:
                    continue
                if m > newest_mtime:
                    newest_mtime, newest_path = m, fp
    if newest_path is not None and newest_mtime > exe_mtime:
        rel = str(newest_path.relative_to(ROOT)).replace("\\", "/")
        return (exe_mtime, newest_mtime, rel)
    return None


def _warn_if_nk_stale() -> None:
    st = _nk_stale()
    if st is None:
        return
    exe_m, src_m, src_rel = st
    fmt = lambda t: time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
    bar = "!" * 74
    try:
        exe_rel = str(NK_EXE.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        exe_rel = str(NK_EXE)
    print(
        f"\n{bar}\n"
        f"  WARNING: numkit.exe is STALE — parity may under-report.\n"
        f"    binary : {exe_rel}  (built  {fmt(exe_m)})\n"
        f"    newest : {src_rel}  (edited {fmt(src_m)})\n"
        f"  Rebuild with:\n"
        f"    cmake --build build --config Release\n"
        f"{bar}\n",
        file=sys.stderr, flush=True)


BENCH_SMALL = 1000
BENCH_LARGE = 1000000


@dataclass
class Spec:
    name: str
    namespace: str
    setup: str
    expr: str
    iters: int = 10
    tol: float = 1e-9
    fingerprint: list[str] = field(default_factory=list)
    comment: str = ""
    out_var: str = ""
    covers: list[str] = field(default_factory=list)
    bench_setup: str = ""
    bench_expr: str = ""
    bench_sizes: list = field(default_factory=lambda: [1000, 1000000])
    bench_note: str = ""
    deep_verified: bool = False

    @classmethod
    def from_json(cls, path: Path) -> "Spec":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)


SAVE_DUMP_TEMPLATE = r"""
sv__ = __VAR__;
if isnumeric(sv__) || islogical(sv__)
    flat__ = double(sv__(:));
    fprintf('SAVE_NUM_BEGIN %d\n', numel(flat__));
    for i__ = 1:numel(flat__)
        fprintf('%.17g\n', flat__(i__));
    end
    fprintf('SAVE_END\n');
elseif ischar(sv__)
    fprintf('SAVE_CHAR_BEGIN %d\n', numel(sv__));
    fprintf('%s\n', reshape(sv__, 1, []));
    fprintf('SAVE_END\n');
elseif isstring(sv__)
    fprintf('SAVE_STR_BEGIN %d\n', numel(sv__));
    for i__ = 1:numel(sv__)
        fprintf('%s\n', char(sv__(i__)));
    end
    fprintf('SAVE_END\n');
elseif iscell(sv__)
    fprintf('SAVE_CELL_BEGIN %d\n', numel(sv__));
    for i__ = 1:numel(sv__)
        el__ = sv__{i__};
        if ischar(el__) || isstring(el__)
            fprintf('%s\n', char(el__));
        elseif isnumeric(el__) && isscalar(el__)
            fprintf('%.17g\n', double(el__));
        else
            fprintf('?\n');
        end
    end
    fprintf('SAVE_END\n');
else
    fprintf('SAVE_NONE\n');
end
"""


def _indent(code: str, n: int) -> str:
    pad = " " * n
    return "\n".join(pad + ln for ln in code.splitlines())


def _indent_stmts(code: str, n: int) -> str:
    return _indent(";\n".join(code.split(";")), n)


def _spec_fn(name: str) -> str:
    return "spec_" + re.sub(r"\W", "_", name)


def build_spec_call(spec: Spec) -> str:
    fn = _spec_fn(spec.name)
    return (
        f"fprintf('__SPECBEGIN__ {spec.name}\\n');\n"
        f"try; {fn}(); "
        f"catch ME__; fprintf('__SPECERR__ %s\\n', ME__.message); end\n"
        f"fprintf('__SPECEND__ {spec.name}\\n');\n"
    )


def build_spec_func(spec: Spec, *, engine: str, isolated: bool = False) -> str:
    lhs = spec.expr.split("=")[0].strip()
    if lhs.startswith("[") and lhs.endswith("]"):
        first_var = lhs[1:-1].split(",")[0].strip()
    else:
        first_var = lhs
    fp_exprs = spec.fingerprint or [
        f"sum({first_var}(:))",
        f"{first_var}(1)",
        f"{first_var}(end)",
    ]
    fp_print = "\n".join(
        f"    fprintf('FP %d %.17g\\n', {i}, double({e}));"
        for i, e in enumerate(fp_exprs)
    )
    save_dump = ""
    if spec.out_var:
        save_dump = _indent(
            SAVE_DUMP_TEMPLATE.replace("__VAR__", spec.out_var), 4)

    reimport = ""
    if engine == "nk" and isolated and spec.namespace and spec.namespace != "core":
        reimport = f"    import {spec.namespace}.*;\n"

    correctness = (
        f"{_indent_stmts(spec.setup, 4)}\n"
        f"{_indent_stmts(spec.expr, 4)}\n"
        f"{fp_print}\n"
        f"{save_dump}\n"
    )

    if not spec.bench_setup.strip():
        return (
            f"function {_spec_fn(spec.name)}()\n"
            f"{reimport}"
            f"{correctness}"
            f"end\n"
        )

    bench_expr = spec.bench_expr.strip() or spec.expr

    def timed(size: int, iters: int, label: str) -> str:
        return (
            f"    N = {size};\n"
            f"{_indent_stmts(spec.bench_setup, 4)}\n"
            f"{_indent_stmts(bench_expr, 4)}\n"
            f"    t0__ = tic;\n"
            f"    for kk__ = 1:{iters}\n"
            f"{_indent_stmts(bench_expr, 8)}\n"
            f"    end\n"
            f"    elapsed_ms__ = toc(t0__) * 1000.0 / {iters};\n"
            f"    fprintf('{label} %.6f\\n', elapsed_ms__);\n"
        )

    iters_small = max(spec.iters, 50)
    iters_large = max(spec.iters, 5)
    sizes = (list(spec.bench_sizes) + [BENCH_SMALL, BENCH_LARGE])[:2]
    return (
        f"function {_spec_fn(spec.name)}()\n"
        f"{reimport}"
        f"{correctness}"
        f"{timed(sizes[0], iters_small, 'TIMING_SMALL')}"
        f"{timed(sizes[1], iters_large, 'TIMING_LARGE')}"
        f"end\n"
    )


def build_batch_script(specs: list[Spec], *, engine: str, isolated: bool = False) -> str:
    if engine == "octave":
        prelude = (
            "try; pkg load signal; end_try_catch\n"
            "try; pkg load statistics; end_try_catch\n"
            "try; pkg load control; end_try_catch\n"
            "try; pkg load image; end_try_catch\n"
        )
    else:
        prelude = ""
    calls = "".join(build_spec_call(s) for s in specs)
    funcs = "\n".join(build_spec_func(s, engine=engine, isolated=isolated) for s in specs)
    return prelude + calls + "\n" + funcs


@dataclass
class SaveBlock:
    kind: str = ""
    items: list = field(default_factory=list)

    def is_empty(self) -> bool:
        return self.kind == "" or (self.kind != "char" and len(self.items) == 0)


@dataclass
class Result:
    ok: bool
    elapsed_ms: float | None = None
    ms_small: float | None = None
    ms_large: float | None = None
    fingerprint: list[float] = field(default_factory=list)
    save: SaveBlock = field(default_factory=SaveBlock)
    raw_stdout: str = ""
    raw_stderr: str = ""
    error: str = ""


def parse_save_block(lines: list[str]) -> SaveBlock:
    sb = SaveBlock()
    n = len(lines)
    i = 0
    while i < n:
        line = lines[i].strip()
        m = re.match(r"^SAVE_NUM_BEGIN\s+(\d+)$", line)
        if m:
            count = int(m.group(1))
            sb.kind = "num"
            sb.items = []
            for j in range(i + 1, min(i + 1 + count, n)):
                try:
                    sb.items.append(float(lines[j].strip()))
                except ValueError:
                    break
            return sb
        m = re.match(r"^SAVE_CHAR_BEGIN\s+(\d+)$", line)
        if m:
            sb.kind = "char"
            sb.items = [lines[i + 1] if i + 1 < n else ""]
            return sb
        m = re.match(r"^SAVE_(STR|CELL)_BEGIN\s+(\d+)$", line)
        if m:
            count = int(m.group(2))
            sb.kind = "str" if m.group(1) == "STR" else "cell"
            sb.items = []
            for j in range(i + 1, min(i + 1 + count, n)):
                sb.items.append(lines[j])
            return sb
        i += 1
    return sb


def parse_output(out: str) -> tuple[float | None, float | None, float | None,
                                    list[float], SaveBlock]:
    timing = None
    ts = None
    tl = None
    fps: dict[int, float] = {}
    lines = out.splitlines()
    for line in lines:
        m = re.match(r"^TIMING_SMALL\s+(\S+)$", line.strip())
        if m:
            ts = float(m.group(1))
            continue
        m = re.match(r"^TIMING_LARGE\s+(\S+)$", line.strip())
        if m:
            tl = float(m.group(1))
            continue
        m = re.match(r"^TIMING\s+(\S+)$", line.strip())
        if m:
            timing = float(m.group(1))
        m = re.match(r"^FP\s+(\d+)\s+(\S+)$", line.strip())
        if m:
            tok = m.group(2)
            if tok in ("NA", "NaN", "nan"):
                val = float("nan")
            elif tok in ("Inf", "inf"):
                val = float("inf")
            elif tok in ("-Inf", "-inf"):
                val = float("-inf")
            else:
                val = float(tok)
            fps[int(m.group(1))] = val
    fp_list = [fps[i] for i in sorted(fps.keys())]
    sb = parse_save_block(lines)
    return timing, ts, tl, fp_list, sb


def _write_script(script: str) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".m", delete=False, encoding="utf-8")
    f.write(script)
    f.close()
    return Path(f.name)


def parse_batch(text: str) -> dict[str, Result]:
    out: dict[str, Result] = {}
    cur: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        st = line.strip()
        if st.startswith("__SPECBEGIN__ "):
            cur = st[len("__SPECBEGIN__ "):].strip()
            buf = []
        elif st.startswith("__SPECEND__ "):
            if cur is not None:
                chunk = "\n".join(buf)
                err_lines = [l.strip() for l in buf if l.strip().startswith("__SPECERR__")]
                err = len(err_lines) > 0
                timing, ts, tl, fp, sb = parse_output(chunk)
                out[cur] = Result(
                    ok=(not err and (len(fp) > 0 or not sb.is_empty())),
                    elapsed_ms=timing, ms_small=ts, ms_large=tl,
                    fingerprint=fp, save=sb,
                    raw_stdout=chunk,
                    error=(err_lines[0] if err else ""),
                )
            cur, buf = None, []
        elif cur is not None:
            buf.append(line)
    return out


def _run_engine_raw(specs: list[Spec],
                    engine: str,
                    *,
                    isolated: bool = False) -> tuple[dict[str, Result], str]:
    if engine == "nk" and not NK_EXE.exists():
        return {}, f"numkit binary missing: {NK_EXE}"
    script = build_batch_script(specs, engine=engine, isolated=isolated)
    path = _write_script(script)
    timeout = max(300, 8 * len(specs))
    try:
        if engine == "nk":
            cmd = [str(NK_EXE)]
            if isolated:
                cmd.append("--isolated")
            cmd.append(str(path))
        elif engine == "matlab":
            cmd = [MATLAB_EXE, "-batch", f"run('{path.as_posix()}')"]
        else:
            cmd = [OCTAVE_EXE, "--no-gui", "--quiet", str(path)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout)
        except subprocess.TimeoutExpired:
            return {}, f"{engine}: chunk timed out after {timeout}s"
    finally:
        path.unlink(missing_ok=True)
    results = parse_batch(p.stdout)
    err = "" if p.returncode == 0 else f"{engine}: exit {p.returncode}"
    return results, err


def _bisect_run(specs: list[Spec], engine: str, *, isolated: bool = False) -> dict[str, Result]:
    res, err = _run_engine_raw(specs, engine, isolated=isolated)
    if not err or len(specs) == 1:
        return res
    mid = len(specs) // 2
    merged: dict[str, Result] = {}
    merged.update(_bisect_run(specs[:mid], engine, isolated=isolated))
    merged.update(_bisect_run(specs[mid:], engine, isolated=isolated))
    return merged


def run_engine_batch(specs: list[Spec],
                     engine: str,
                     *,
                     isolated: bool = False) -> tuple[dict[str, Result], str]:
    results, err = _run_engine_raw(specs, engine, isolated=isolated)
    if err and len(specs) > 1:
        results = _bisect_run(specs, engine, isolated=isolated)
        missing = [s.name for s in specs if s.name not in results]
        err = ("" if not missing
               else f"{engine}: {len(missing)} spec(s) failed to parse/run "
                    f"(isolated: {', '.join(missing[:5])}"
                    f"{'…' if len(missing) > 5 else ''})")
    return results, err


def fp_close(a: list[float], b: list[float], tol: float) -> bool:
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != x and y != y:
            continue
        diff = abs(x - y)
        scale = max(abs(x), abs(y), 1.0)
        if diff > tol * scale:
            return False
    return True


def save_close(a: SaveBlock, b: SaveBlock, tol: float) -> tuple[bool, str]:
    if a.kind != b.kind:
        return False, f"kind mismatch: {a.kind} vs {b.kind}"
    if a.kind == "num":
        if len(a.items) != len(b.items):
            return False, f"length mismatch: {len(a.items)} vs {len(b.items)}"
        worst = 0.0
        worst_idx = -1
        for i, (x, y) in enumerate(zip(a.items, b.items)):
            if x != x and y != y:
                continue
            diff = abs(x - y)
            scale = max(abs(x), abs(y), 1.0)
            rel = diff / scale
            if rel > worst:
                worst = rel
                worst_idx = i
            if rel > tol:
                return False, (f"elem {i}: {x:.17g} vs {y:.17g} "
                               f"(rel={rel:.3g} > tol={tol:.3g})")
        return True, f"max rel diff {worst:.3g} at idx {worst_idx}"
    if a.kind == "char":
        ok = a.items == b.items
        return ok, "" if ok else f"char text differs: {a.items[0][:40]!r} vs {b.items[0][:40]!r}"
    if a.kind in ("str", "cell"):
        if len(a.items) != len(b.items):
            return False, f"length mismatch: {len(a.items)} vs {len(b.items)}"
        for i, (x, y) in enumerate(zip(a.items, b.items)):
            if x != y:
                return False, f"elem {i}: {x!r} vs {y!r}"
        return True, ""
    return False, f"unknown kind {a.kind}"


PROGRESS_ROW_FMT = "| `{name}` | {status} | {comment} |"


def compose_status(cur_status: str, correctness: str,
                   implemented: bool, deep_verified: bool) -> str:
    s = cur_status.replace("❗", "").replace("➖", "")
    s = " ".join(s.split())
    has_micro = "🔬" in s
    base = s.replace("🔬", "").strip() or "—"
    if implemented and base == "❌":
        base = "✅"
    parts = [base]
    if deep_verified or has_micro:
        parts.append("🔬")
    if correctness == "MISMATCH":
        parts.append("❗")
    elif correctness == "N/A":
        parts.append("➖")
    return " ".join(parts)


BENCH_ROW_FMT = ("| `{name}` | {nk_s} | {ml_s} | {oc_s} "
                 "| {nk_l} | {ml_l} | {oc_l} | {notes} |")


def fmt_ms(x: float | None) -> str:
    return "" if x is None else f"{x:.4g}"


def fmt_ratio(num: float | None, den: float | None) -> str:
    if num is None or den is None or den <= 0:
        return ""
    return f"{num / den:.2f}×"


def make_row_finder(name: str) -> re.Pattern:
    return re.compile(
        r"^\|\s*`" + re.escape(name) + r"`\s*\|"
        r"\s*(?P<status>[^|]+?)\s*\|"
        r"[^\n]*$",
        re.MULTILINE,
    )


def update_progress_row(*, name: str, nk: Result | None,
                        ml: Result | None, oc: Result | None,
                        correctness: str, comment: str,
                        implemented: bool = False,
                        deep_verified: bool = False) -> int:
    if not PROGRESS_MD.exists():
        return 0
    text = PROGRESS_MD.read_text(encoding="utf-8")
    rx = make_row_finder(name)
    touched = 0

    def replace(m: re.Match) -> str:
        nonlocal touched
        touched += 1
        status = compose_status(m.group("status").strip(),
                                correctness, implemented, deep_verified)
        return PROGRESS_ROW_FMT.format(name=name, status=status, comment=comment)

    new_text = rx.sub(replace, text)
    if touched == 0:
        misc = "## Misc / not in TODO"
        if misc not in new_text:
            new_text = new_text.rstrip() + "\n\n" + misc + "\n\n"
            new_text += ("Functions exercised by the harness that don't appear "
                         "in any MATLAB-doc section above.\n\n")
            new_text += "| function | status | comment |\n"
            new_text += "|---|:---:|---|\n"
        status = compose_status("—", correctness, implemented, deep_verified)
        new_text = new_text.rstrip() + "\n" + PROGRESS_ROW_FMT.format(
            name=name, status=status, comment=comment) + "\n"
        touched = 1

    PROGRESS_MD.write_text(new_text, encoding="utf-8")
    return touched


def update_benchmark_row(*, name: str, nk: Result | None,
                         ml: Result | None, oc: Result | None,
                         note: str = "") -> int:
    if not BENCHMARK_MD.exists():
        return 0
    if not (nk and nk.ok and nk.ms_small is not None and nk.ms_large is not None):
        return 0
    nk_s, nk_l = nk.ms_small, nk.ms_large
    ml_s = ml.ms_small if (ml and ml.ok) else None
    ml_l = ml.ms_large if (ml and ml.ok) else None
    oc_s = oc.ms_small if (oc and oc.ok) else None
    oc_l = oc.ms_large if (oc and oc.ok) else None
    row = BENCH_ROW_FMT.format(
        name=name,
        nk_s=fmt_ms(nk_s), ml_s=fmt_ratio(ml_s, nk_s), oc_s=fmt_ratio(oc_s, nk_s),
        nk_l=fmt_ms(nk_l), ml_l=fmt_ratio(ml_l, nk_l), oc_l=fmt_ratio(oc_l, nk_l),
        notes=note,
    )
    text = BENCHMARK_MD.read_text(encoding="utf-8")
    rx = make_row_finder(name)
    touched = 0

    def replace(m: re.Match) -> str:
        nonlocal touched
        touched += 1
        return row

    new_text = rx.sub(replace, text)
    if touched == 0:
        misc = "## Misc / not in TODO"
        if misc not in new_text:
            new_text = new_text.rstrip() + "\n\n" + misc + "\n\n"
            new_text += ("| function | nk small (ms) | ML× s | OC× s "
                         "| nk large (ms) | ML× l | OC× l | notes |\n")
            new_text += "|---|---:|---:|---:|---:|---:|---:|---|\n"
        new_text = new_text.rstrip() + "\n" + row + "\n"
        touched = 1

    BENCHMARK_MD.write_text(new_text, encoding="utf-8")
    return touched


def evaluate(spec: Spec, nk: Result | None, ml: Result | None,
             oc: Result | None) -> tuple[str, str]:
    if nk is None or not nk.ok:
        return "FAIL", "N/A"
    ref = ml if (ml and ml.ok) else (oc if (oc and oc.ok) else None)
    if ref is None:
        return "DONE", "N/A"
    use_save = (spec.out_var and not nk.save.is_empty()
                and not ref.save.is_empty())
    if use_save:
        ok, _ = save_close(nk.save, ref.save, spec.tol)
        return "DONE", ("OK" if ok else "MISMATCH")
    if fp_close(nk.fingerprint, ref.fingerprint, spec.tol):
        return "DONE", "OK"
    return "DONE", "MISMATCH"


def run_chunk(specs: list[Spec], *, no_matlab: bool, no_octave: bool,
              isolated: bool, verbose: bool) -> tuple[int, dict[str, int]]:
    nk_res, nk_err = run_engine_batch(specs, "nk", isolated=isolated)
    ml_res, ml_err = (({}, "") if no_matlab
                      else run_engine_batch(specs, "matlab"))
    oc_res, oc_err = (({}, "") if no_octave
                      else run_engine_batch(specs, "octave"))
    for err in (nk_err, ml_err, oc_err):
        if err:
            print(f"  ! {err}", flush=True)

    rc = 0
    tally = {"OK": 0, "MISMATCH": 0, "FAIL": 0, "N/A": 0}
    for spec in specs:
        nk = nk_res.get(spec.name)
        ml = ml_res.get(spec.name)
        oc = oc_res.get(spec.name)
        status, correctness = evaluate(spec, nk, ml, oc)
        if status == "FAIL":
            tally["FAIL"] += 1
            rc = 1
        else:
            tally[correctness] += 1
            if correctness == "MISMATCH":
                rc = 1
        rows = 0
        if nk is not None and nk.ok:
            for nm in (spec.covers or [spec.name]):
                rows += update_progress_row(
                    name=nm, nk=nk, ml=ml, oc=oc,
                    correctness=correctness, comment=spec.comment,
                    implemented=nk.ok, deep_verified=spec.deep_verified)
                update_benchmark_row(name=nm, nk=nk, ml=ml, oc=oc,
                                     note=spec.bench_note)
        flag = "" if (status == "DONE"
                      and correctness in ("OK", "N/A")) else "  <<"
        print(f"  [{spec.namespace:<7}] {spec.name:<30} {status:<5} {correctness:<9} "
              f"rows={rows}{flag}", flush=True)
        if verbose and nk is not None and not nk.ok:
            print(f"      nk error: {nk.error}", flush=True)
    return rc, tally


def resolve_spec_targets(args) -> list[Path]:
    if args.all:
        return sorted(SPECS_ROOT.rglob("*.json"))
    if args.module:
        mod_dir = SPECS_ROOT / args.module
        if not mod_dir.exists():
            sys.exit(f"Unknown module '{args.module}'. Available: "
                     f"{', '.join(sorted(d.name for d in SPECS_ROOT.iterdir() if d.is_dir()))}")
        return sorted(mod_dir.glob("*.json"))
    targets: list[Path] = []
    for raw in args.specs:
        p = Path(raw)
        if p.exists():
            if p.is_dir():
                targets.extend(sorted(p.rglob("*.json")))
            else:
                targets.append(p)
            continue
        stem = raw[:-5] if raw.endswith(".json") else raw
        matches = sorted(SPECS_ROOT.rglob(f"{stem}.json"))
        if matches:
            targets.extend(matches)
        else:
            print(f"  SKIP {raw}: not found under {SPECS_ROOT}")
    return targets


def main():
    p = argparse.ArgumentParser(description="NumKit MATLAB-parity validation harness")
    p.add_argument("specs", nargs="*", help="spec JSON path(s) or function name(s)")
    p.add_argument("--all", action="store_true",
                   help="run every spec across all domain folders in parity/specs/")
    p.add_argument("-m", "--module", type=str, default="",
                   help="run all specs for a specific domain (core, signal, stats, image, comm, control, wavelet, audio)")
    p.add_argument("--isolated", action="store_true",
                   help="run numkit in NamespaceMode::Isolated (--isolated) with explicit domain imports")
    p.add_argument("--no-matlab", action="store_true")
    p.add_argument("--no-octave", action="store_true")
    p.add_argument("--chunk", type=int, default=100,
                   help="specs per engine launch (default 100)")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    targets = resolve_spec_targets(args)
    if not targets:
        p.error("no specs supplied (use --all, --module <name>, or pass spec names/paths)")

    specs: list[Spec] = []
    for sp in targets:
        try:
            specs.append(Spec.from_json(sp))
        except Exception as e:
            print(f"  SKIP {sp.name}: bad spec ({e})")
    if not specs:
        return 1

    chunk = max(1, args.chunk)
    nchunks = (len(specs) + chunk - 1) // chunk
    mode_tag = "isolated" if args.isolated else "compat"
    print(f"{len(specs)} spec(s) · mode={mode_tag} · chunk={chunk} · "
          f"{nchunks} launch(es) per engine", flush=True)

    _warn_if_nk_stale()

    rc = 0
    total = {"OK": 0, "MISMATCH": 0, "FAIL": 0, "N/A": 0}
    for ci in range(nchunks):
        batch = specs[ci * chunk:(ci + 1) * chunk]
        print(f"\n── chunk {ci + 1}/{nchunks} ({len(batch)} specs) ──",
              flush=True)
        crc, tally = run_chunk(batch, no_matlab=args.no_matlab,
                               no_octave=args.no_octave,
                               isolated=args.isolated,
                               verbose=args.verbose)
        rc = rc or crc
        for k in total:
            total[k] += tally[k]

    print(f"\nsummary: OK={total['OK']}  MISMATCH={total['MISMATCH']}  "
          f"FAIL={total['FAIL']}  N/A={total['N/A']}", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
