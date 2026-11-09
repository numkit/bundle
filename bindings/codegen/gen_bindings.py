#!/usr/bin/env python3
"""bindings/codegen/gen_bindings.py

Automatic multi-language binding generator for NumKit.
Scans:
  1. `modules/<tb>/manifest.json` (canonical list of exported toolbox functions)
  2. `modules/<tb>/include/numkit/<tb>/**/*.hpp` (strongly-typed C++ signatures & Doxygen docs)
  3. `audits/baselines/arity_reference.json` (min/max arity bounds)

Generates:
  - Python SDK modules (`bindings/python/numkit/<tb>.py` + PEP 484 `.pyi` type stubs)
  - Rust SDK modules (`bindings/rust/numkit/src/tb/<tb>.rs` + `mod.rs`)
"""

from __future__ import annotations

import json
import keyword
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MODULES_DIR = ROOT / "modules"
ARITY_FILE = ROOT / "audits" / "baselines" / "arity_reference.json"
PY_OUT_DIR = ROOT / "bindings" / "python" / "numkit"
RS_OUT_DIR = ROOT / "bindings" / "rust" / "numkit" / "src" / "tb"

TOOLBOXES = ("signal", "control", "stats", "wavelet", "audio", "comm", "image", "cas")

RUST_KEYWORDS = {
    "as", "break", "const", "continue", "crate", "else", "enum", "extern",
    "false", "fn", "for", "if", "impl", "in", "let", "loop", "match", "mod",
    "move", "mut", "pub", "ref", "return", "self", "Self", "static", "struct",
    "super", "trait", "true", "type", "unsafe", "use", "where", "while",
    "async", "await", "dyn", "abstract", "become", "box", "do", "final",
    "macro", "override", "priv", "typeof", "unsized", "virtual", "yield", "try",
}

SKIP_CPP_NAMES = {
    "if", "for", "while", "switch", "return", "catch", "sizeof", "operator",
    "install",
}


@dataclass
class ParamSpec:
    name: str
    cpp_type: str
    py_type: str
    rs_type: str | None  # None if variadic / unsupported for fixed typed wrapper
    default_cpp: str | None = None
    default_py: str | None = None


@dataclass
class FuncSpec:
    name: str
    toolbox: str
    doc: str = ""
    return_arity: int = 1
    params: list[ParamSpec] = field(default_factory=list)
    has_typed_sig: bool = False
    min_args: int = 0
    max_args: int | None = None


def sanitize_py_ident(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    if keyword.iskeyword(cleaned) or cleaned in ("None", "True", "False", "call"):
        return f"{cleaned}_"
    return cleaned


def sanitize_rs_ident(name: str) -> str:
    # Convert camelCase to snake_case for Rust or keep lower if clean
    s = re.sub(r"[^a-zA-Z0-9_]", "_", name).lower()
    if not s or s[0].isdigit():
        s = f"fn_{s}"
    if s in RUST_KEYWORDS:
        return f"r#{s}"
    return s


def map_cpp_type(cpp_type: str) -> tuple[str, str | None]:
    """Return (py_type_annotation, rust_type_or_None)."""
    t = " ".join(cpp_type.replace("numkit::", "").split())
    if "Span<" in t or "vector<" in t:
        return ("Any", None)
    if t in ("int", "int32_t", "long", "short"):
        return ("int", "i32")
    if t in ("size_t", "std::size_t", "uint32_t", "uint64_t", "int64_t"):
        return ("int", "usize")
    if t in ("double", "float"):
        return ("float", "f64")
    if t == "bool":
        return ("bool", "bool")
    if "string" in t or "char *" in t or "char*" in t:
        return ("str", "&str")
    if "Value" in t:
        return ("Any", "&Value")
    # Custom enum or struct -> dynamic Any in Python, skip fixed typed wrapper in Rust
    return ("Any", None)


def map_default_to_py(default_cpp: str, py_type: str) -> str:
    d = default_cpp.strip()
    if d in ("true", "false"):
        return "True" if d == "true" else "False"
    if d.startswith('"') and d.endswith('"'):
        return d
    if "Empty" in d or "Value()" in d or d == "{}":
        return "None"
    if re.match(r"^[+-]?\d+(\.\d+)?([eE][+-]?\d+)?$", d):
        return d
    return "None"


def parse_header_functions(hdr_path: Path, toolbox: str) -> dict[str, FuncSpec]:
    text = hdr_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    specs: dict[str, FuncSpec] = {}

    # Collect Doxygen blocks preceding declarations
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if line.startswith("///"):
            doc_lines: list[str] = []
            while i < n and lines[i].strip().startswith("///"):
                dline = lines[i].strip()[3:].strip()
                if not dline.startswith("@ingroup") and not dline.startswith("@{") and not dline.startswith("@}"):
                    doc_lines.append(dline)
                i += 1
            # Gather the declaration immediately following the Doxygen comment
            decl_chunks: list[str] = []
            while i < n:
                cur = lines[i].strip()
                if not cur or cur.startswith("//"):
                    if decl_chunks:
                        break
                    i += 1
                    continue
                if cur.startswith(("class ", "struct ", "enum ", "namespace ", "#", "template")):
                    break
                decl_chunks.append(re.sub(r"//.*$", "", lines[i]).strip())
                if ";" in cur or "{" in cur:
                    i += 1
                    break
                i += 1
            decl = " ".join(decl_chunks)
            spec = _try_parse_decl(decl, "\n".join(doc_lines).strip(), toolbox)
            if spec and spec.name not in specs:
                specs[spec.name] = spec
        else:
            i += 1
    return specs


def _try_parse_decl(decl: str, doc: str, toolbox: str) -> FuncSpec | None:
    if not decl or "(" not in decl or ")" not in decl:
        return None
    open_p = decl.find("(")
    close_p = decl.rfind(")")
    if close_p < open_p:
        return None
    prefix = decl[:open_p].strip()
    params_raw = decl[open_p + 1 : close_p].strip()

    # Extract function name (last identifier in prefix)
    m_name = re.search(r"([a-zA-Z_]\w*)\s*$", prefix)
    if not m_name:
        return None
    fn_name = m_name.group(1)
    if fn_name in SKIP_CPP_NAMES or fn_name.endswith("_argcheck"):
        return None
    ret_type = prefix[: m_name.start()].strip()
    if not ret_type or ret_type.startswith(("using", "typedef", "return")):
        return None

    # Count tuple outputs
    return_arity = 1
    if "tuple<" in ret_type:
        inner = ret_type[ret_type.find("tuple<") + 6 : ret_type.rfind(">")]
        return_arity = inner.count(",") + 1

    # Split parameters outside angle brackets / parens
    param_strs = _split_top_level(params_raw)
    params: list[ParamSpec] = []
    seen_names: set[str] = set()
    all_rust_typed = True

    for idx, p_str in enumerate(param_strs):
        p_str = p_str.strip()
        if not p_str or p_str == "void":
            continue
        # Skip memory_resource and RngContext parameters (managed by numkit_ctx)
        if "memory_resource" in p_str or "RngContext" in p_str or "PluginContext" in p_str:
            continue
        if "Span<const Value>" in p_str or "Span<const numkit::Value>" in p_str:
            all_rust_typed = False
            continue

        default_cpp = None
        if "=" in p_str:
            lhs, rhs = p_str.split("=", 1)
            p_str = lhs.strip()
            default_cpp = rhs.strip()

        m_pname = re.search(r"([a-zA-Z_]\w*)\s*$", p_str)
        if m_pname:
            pname = m_pname.group(1)
            ptype = p_str[: m_pname.start()].strip()
        else:
            pname = f"arg{idx + 1}"
            ptype = p_str

        if not ptype:
            all_rust_typed = False
            continue

        py_ident = sanitize_py_ident(pname)
        while py_ident in seen_names:
            py_ident = f"{py_ident}_{idx + 1}"
        seen_names.add(py_ident)

        py_t, rs_t = map_cpp_type(ptype)
        if rs_t is None or default_cpp is not None:
            # Keep Rust typed signature for clean required parameters
            if rs_t is None:
                all_rust_typed = False
        default_py = map_default_to_py(default_cpp, py_t) if default_cpp is not None else None
        params.append(
            ParamSpec(
                name=py_ident,
                cpp_type=ptype,
                py_type=py_t,
                rs_type=rs_t,
                default_cpp=default_cpp,
                default_py=default_py,
            )
        )

    has_typed = len(params) > 0 and all(p.rs_type is not None for p in params) and all_rust_typed
    return FuncSpec(
        name=fn_name,
        toolbox=toolbox,
        doc=doc,
        return_arity=return_arity,
        params=params,
        has_typed_sig=has_typed,
    )


def _split_top_level(s: str) -> list[str]:
    parts: list[str] = []
    cur: list[str] = []
    depth = 0
    for ch in s:
        if ch in "<({":
            depth += 1
        elif ch in ">)}":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return parts


def collect_toolbox_specs(tb: str, arity_db: dict) -> list[FuncSpec]:
    tb_dir = MODULES_DIR / tb
    manifest = json.loads((tb_dir / "manifest.json").read_text(encoding="utf-8"))
    exports: list[str] = manifest.get("exports") or manifest.get("functions") or []

    # Parse all public C++ headers in modules/<tb>/include
    header_map: dict[str, FuncSpec] = {}
    for hdr in sorted((tb_dir / "include").rglob("*.hpp")):
        if "/internal/" in hdr.as_posix() or "/detail/" in hdr.as_posix():
            continue
        parsed = parse_header_functions(hdr, tb)
        for k, v in parsed.items():
            if k not in header_map or (v.has_typed_sig and not header_map[k].has_typed_sig):
                header_map[k] = v

    tb_arity = arity_db.get(tb, {})
    result: list[FuncSpec] = []
    seen: set[str] = set()
    for fn_name in exports:
        if fn_name in seen:
            continue
        seen.add(fn_name)
        spec = header_map.get(fn_name)
        if spec is None:
            spec = FuncSpec(
                name=fn_name,
                toolbox=tb,
                doc=f"`{tb}.{fn_name}` — MATLAB-compatible {tb} toolbox function.",
            )
        ar = tb_arity.get(fn_name, {})
        spec.min_args = ar.get("min", 0)
        spec.max_args = ar.get("max", None)
        result.append(spec)
    return result


def generate_python_module(tb: str, specs: list[FuncSpec]) -> tuple[str, str]:
    py_lines = [
        f'# AUTO-GENERATED by bindings/codegen/gen_bindings.py — DO NOT EDIT MANUALLY.',
        f'"""NumKit `{tb}` toolbox bindings (Level 1 typed wrappers + Level 2 dynamic dispatch)."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "from ._ffi import Context, default_context, infer_caller_nargout",
        "",
        f'_TOOLBOX = "{tb}"',
        "",
        "",
        "def call(name: str, *args: Any, nargout: int | None = None, ctx: Context | None = None) -> Any:",
        f'    """Dynamically invoke any function in the `{tb}` toolbox."""',
        "    c = ctx if ctx is not None else default_context()",
        "    actual = nargout if nargout is not None else infer_caller_nargout(1, depth=2)",
        "    return c.call(_TOOLBOX, name, *args, nargout=actual)",
        "",
    ]

    pyi_lines = [
        f"# AUTO-GENERATED by bindings/codegen/gen_bindings.py — DO NOT EDIT MANUALLY.",
        "from __future__ import annotations",
        "from typing import Any",
        "from ._ffi import Context",
        "",
        "def call(name: str, *args: Any, nargout: int | None = None, ctx: Context | None = None) -> Any: ...",
        "",
    ]

    exported_names = ["call"]
    for sp in specs:
        py_fn = sanitize_py_ident(sp.name)
        exported_names.append(py_fn)
        doc_clean = (
            (sp.doc or f"`{tb}.{sp.name}` toolbox function.")
            .replace("\\", "\\\\")
            .replace('"""', "'''")
        )

        # Even when a C++ header has a typed overload, MATLAB functions often accept flexible
        # positional overload forms (e.g. `butter(4, 0.25)` or `butter(4, 0.25, 'high')`).
        # We expose the exact parameter names in `.pyi` for IDE autocompletion and support
        # flexible `*args` + optional named arguments in `.py`!
        py_lines.append(
            f"def {py_fn}(*args: Any, nargout: int | None = None, ctx: Context | None = None) -> Any:"
        )
        py_lines.append(f'    """{doc_clean}"""')
        py_lines.append("    c = ctx if ctx is not None else default_context()")
        py_lines.append(
            f"    actual = nargout if nargout is not None else infer_caller_nargout({sp.return_arity}, depth=2)"
        )
        py_lines.append(
            f'    return c.call(_TOOLBOX, "{sp.name}", *args, nargout=actual, default_nargout={sp.return_arity})'
        )
        py_lines.append("")

        # Rich `.pyi` stub signature from parsed C++ header parameters when available
        if sp.params:
            stub_params: list[str] = []
            has_default = False
            for p in sp.params:
                if p.default_py is not None:
                    has_default = True
                    stub_params.append(f"{p.name}: {p.py_type} = {p.default_py}")
                elif has_default:
                    stub_params.append(f"{p.name}: {p.py_type} = ...")
                else:
                    stub_params.append(f"{p.name}: {p.py_type}")
            stub_params.append("*extra_args: Any")
            stub_params.append("nargout: int | None = None")
            stub_params.append("ctx: Context | None = None")
            sig_str = ", ".join(stub_params)
        else:
            sig_str = "*args: Any, nargout: int | None = None, ctx: Context | None = None"

        ret_ann = (
            "Any"
            if sp.return_arity <= 1
            else f"tuple[{', '.join(['Any'] * sp.return_arity)}]"
        )
        pyi_lines.append(f"def {py_fn}({sig_str}) -> {ret_ann}: ...")

    py_lines.append(f"__all__ = {json.dumps(exported_names, indent=4)}")
    py_lines.append("")
    return "\n".join(py_lines), "\n".join(pyi_lines) + "\n"


def generate_rust_module(tb: str, specs: list[FuncSpec]) -> str:
    rs_lines = [
        f"//! AUTO-GENERATED by `bindings/codegen/gen_bindings.py` — DO NOT EDIT MANUALLY.",
        f"//! NumKit `{tb}` toolbox bindings:",
        f"//! - Level 1: `<fn>_typed` with strict compile-time parameter & return types from C++ headers.",
        f"//! - Level 2: `<fn>` (1-output / tuple default) and `<fn>_n` (dynamic `nargout`) for all MATLAB overloads.",
        "#![allow(clippy::too_many_arguments, non_snake_case)]",
        "",
        "use crate::{Context, Error, IntoValue, Value};",
        "",
        f'pub const TOOLBOX: &str = "{tb}";',
        "",
        f"/// Dynamically call any function in the `{tb}` toolbox.",
        "pub fn call(ctx: &Context, name: &str, args: &[&Value], nargout: usize) -> Result<Vec<Value>, Error> {",
        "    ctx.call(TOOLBOX, name, args, nargout)",
        "}",
        "",
    ]

    used_rs_names: set[str] = {"call"}
    for sp in specs:
        rs_fn = sanitize_rs_ident(sp.name)
        if rs_fn in used_rs_names:
            rs_fn = f"{rs_fn}_fn"
        used_rs_names.add(rs_fn)

        for dline in (sp.doc or f"`{tb}.{sp.name}` toolbox function.").splitlines()[:6]:
            rs_lines.append(f"/// {dline}")

        # Level 2a: ergonomic default-arity call `<fn>(ctx, args)`
        if sp.return_arity == 2:
            rs_lines.append(
                f"pub fn {rs_fn}(ctx: &Context, args: &[&Value]) -> Result<(Value, Value), Error> {{"
            )
            rs_lines.append(f'    let mut outs = ctx.call(TOOLBOX, "{sp.name}", args, 2)?;')
            rs_lines.append("    let b = outs.pop().unwrap();")
            rs_lines.append("    let a = outs.pop().unwrap();")
            rs_lines.append("    Ok((a, b))")
            rs_lines.append("}")
        elif sp.return_arity == 3:
            rs_lines.append(
                f"pub fn {rs_fn}(ctx: &Context, args: &[&Value]) -> Result<(Value, Value, Value), Error> {{"
            )
            rs_lines.append(f'    let mut outs = ctx.call(TOOLBOX, "{sp.name}", args, 3)?;')
            rs_lines.append("    let c = outs.pop().unwrap();")
            rs_lines.append("    let b = outs.pop().unwrap();")
            rs_lines.append("    let a = outs.pop().unwrap();")
            rs_lines.append("    Ok((a, b, c))")
            rs_lines.append("}")
        else:
            rs_lines.append(
                f"pub fn {rs_fn}(ctx: &Context, args: &[&Value]) -> Result<Value, Error> {{"
            )
            rs_lines.append(f'    let mut outs = ctx.call(TOOLBOX, "{sp.name}", args, 1)?;')
            rs_lines.append("    Ok(outs.pop().unwrap())")
            rs_lines.append("}")

        # Level 2b: explicit `nargout` variant `<fn>_n(ctx, args, nargout)`
        rs_n_fn = f"{rs_fn.lstrip('r#')}_n"
        if rs_n_fn not in used_rs_names:
            used_rs_names.add(rs_n_fn)
            rs_lines.append(
                f"pub fn {rs_n_fn}(ctx: &Context, args: &[&Value], nargout: usize) -> Result<Vec<Value>, Error> {{"
            )
            rs_lines.append(f'    ctx.call(TOOLBOX, "{sp.name}", args, nargout)')
            rs_lines.append("}")

        # Level 1: Strictly-typed C++ header signature wrapper `<fn>_typed(...)`
        if sp.has_typed_sig and 1 <= sp.return_arity <= 3:
            rs_typed_fn = f"{rs_fn.lstrip('r#')}_typed"
            if rs_typed_fn not in used_rs_names:
                used_rs_names.add(rs_typed_fn)
                p_decls: list[str] = ["ctx: &Context"]
                p_lets: list[str] = []
                p_refs: list[str] = []
                for idx, p in enumerate(sp.params):
                    pname = f"p_{idx}_{sanitize_rs_ident(p.name).lstrip('r#')}"
                    assert p.rs_type is not None
                    p_decls.append(f"{pname}: {p.rs_type}")
                    if p.rs_type == "&Value":
                        p_refs.append(pname)
                    else:
                        vname = f"v_{idx}"
                        p_lets.append(f"    let {vname} = ({pname}).into_numkit_value()?;")
                        p_refs.append(f"&{vname}")

                ret_t = (
                    "Value"
                    if sp.return_arity == 1
                    else f"({', '.join(['Value'] * sp.return_arity)})"
                )
                rs_lines.append(
                    f"/// Strongly-typed wrapper for `{tb}::{sp.name}` generated from its C++ header."
                )
                rs_lines.append(f"pub fn {rs_typed_fn}({', '.join(p_decls)}) -> Result<{ret_t}, Error> {{")
                rs_lines.extend(p_lets)
                rs_lines.append(
                    f'    let mut outs = ctx.call(TOOLBOX, "{sp.name}", &[{", ".join(p_refs)}], {sp.return_arity})?;'
                )
                if sp.return_arity == 1:
                    rs_lines.append("    Ok(outs.pop().unwrap())")
                elif sp.return_arity == 2:
                    rs_lines.append("    let b = outs.pop().unwrap();")
                    rs_lines.append("    let a = outs.pop().unwrap();")
                    rs_lines.append("    Ok((a, b))")
                else:
                    rs_lines.append("    let c = outs.pop().unwrap();")
                    rs_lines.append("    let b = outs.pop().unwrap();")
                    rs_lines.append("    let a = outs.pop().unwrap();")
                    rs_lines.append("    Ok((a, b, c))")
                rs_lines.append("}")

        rs_lines.append("")

    return "\n".join(rs_lines)


def main() -> int:
    PY_OUT_DIR.mkdir(parents=True, exist_ok=True)
    RS_OUT_DIR.mkdir(parents=True, exist_ok=True)

    arity_db = json.loads(ARITY_FILE.read_text(encoding="utf-8")) if ARITY_FILE.exists() else {}

    total_fns = 0
    total_typed = 0
    rs_mod_lines = [
        "//! AUTO-GENERATED by `bindings/codegen/gen_bindings.py` — DO NOT EDIT MANUALLY.",
        "",
    ]

    for tb in TOOLBOXES:
        specs = collect_toolbox_specs(tb, arity_db)
        total_fns += len(specs)
        typed_count = sum(1 for s in specs if s.has_typed_sig)
        total_typed += typed_count

        py_src, pyi_src = generate_python_module(tb, specs)
        (PY_OUT_DIR / f"{tb}.py").write_text(py_src, encoding="utf-8")
        (PY_OUT_DIR / f"{tb}.pyi").write_text(pyi_src, encoding="utf-8")

        rs_src = generate_rust_module(tb, specs)
        (RS_OUT_DIR / f"{tb}.rs").write_text(rs_src, encoding="utf-8")
        rs_mod_lines.append(f"pub mod {tb};")

        print(f"  [{tb:8s}] generated {len(specs):4d} functions ({typed_count:3d} strict C++ typed)")

    (RS_OUT_DIR / "mod.rs").write_text("\n".join(rs_mod_lines) + "\n", encoding="utf-8")
    print(f"gen_bindings: OK — {total_fns} functions across {len(TOOLBOXES)} toolboxes ({total_typed} C++ typed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
