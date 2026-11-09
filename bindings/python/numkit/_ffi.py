# bindings/python/numkit/_ffi.py
"""Low-level C-ABI bridge (`numkit_c.h`) for Python.

Supports:
  - Both Lite (engine-free toolbox-only) and Full (StandardEngine) contexts.
  - Zero-copy `numkit_val_view` when `numpy` is installed and array is Fortran-contiguous `float64`.
  - Pure-Python fallback (`list`, `tuple`, `float`, `int`, `bool`, `complex`, `str`, `dict`)
    when `numpy` is not installed.
  - Automatic caller `nargout` unpacking detection (`b, a = signal.butter(4, 0.25)`).
"""

from __future__ import annotations

import ctypes
import dis
import inspect
import os
import sys
from pathlib import Path
from typing import Any, Sequence

try:
    import numpy as _np  # type: ignore
except ImportError:
    _np = None

# ---------------------------------------------------------------------------
# 1. C-ABI Data Types (`numkit_c.h`)
# ---------------------------------------------------------------------------

NUMKIT_DTYPE_DOUBLE = 0
NUMKIT_DTYPE_SINGLE = 1
NUMKIT_DTYPE_COMPLEX = 2
NUMKIT_DTYPE_LOGICAL = 3
NUMKIT_DTYPE_CHAR = 4
NUMKIT_DTYPE_STRING = 5
NUMKIT_DTYPE_INT8 = 6
NUMKIT_DTYPE_INT16 = 7
NUMKIT_DTYPE_INT32 = 8
NUMKIT_DTYPE_INT64 = 9
NUMKIT_DTYPE_UINT8 = 10
NUMKIT_DTYPE_UINT16 = 11
NUMKIT_DTYPE_UINT32 = 12
NUMKIT_DTYPE_UINT64 = 13
NUMKIT_DTYPE_CELL = 14
NUMKIT_DTYPE_STRUCT = 15
NUMKIT_DTYPE_FUNC_HANDLE = 16
NUMKIT_DTYPE_OBJECT = 17
NUMKIT_DTYPE_UNKNOWN = 255


class NumkitErrorStruct(ctypes.Structure):
    _fields_ = [
        ("code", ctypes.c_int),
        ("message", ctypes.c_char * 512),
    ]


class NumKitError(RuntimeError):
    """Exception raised when a NumKit C-ABI call reports an error."""


_CtxPtr = ctypes.c_void_p
_ValPtr = ctypes.c_void_p


def _find_c_library() -> str:
    env_lib = os.environ.get("NUMKIT_C_LIBRARY")
    if env_lib and os.path.isfile(env_lib):
        return env_lib

    here = Path(__file__).resolve().parent
    bundle_root = here.parent.parent.parent
    search_dirs = [
        here,
        bundle_root / "build" / "lib",
        bundle_root / "build" / "bin",
        bundle_root / "build" / "lib" / "Release",
        bundle_root / "build" / "bin" / "Release",
    ]
    if sys.platform == "win32":
        names = ["numkit_c.dll", "libnumkit_c.dll", "numkit_c_lite.dll", "libnumkit_c_lite.dll"]
    elif sys.platform == "darwin":
        names = ["libnumkit_c.dylib", "libnumkit_c_lite.dylib", "libnumkit_c.so", "libnumkit_c_lite.so"]
    else:
        names = ["libnumkit_c.so", "libnumkit_c_lite.so"]

    for d in search_dirs:
        for name in names:
            cand = d / name
            if cand.is_file():
                return str(cand)
    raise FileNotFoundError(
        "Could not locate libnumkit_c or libnumkit_c_lite shared library. "
        "Build the project with CMake (`cmake --build build`) or set NUMKIT_C_LIBRARY."
    )


_LIB: ctypes.CDLL | None = None


def get_lib() -> ctypes.CDLL:
    global _LIB
    if _LIB is not None:
        return _LIB
    lib = ctypes.CDLL(_find_c_library())

    # 1. Context lifecycle
    lib.numkit_abi_version.argtypes = []
    lib.numkit_abi_version.restype = ctypes.c_uint32

    lib.numkit_ctx_create_lite.argtypes = [ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_ctx_create_lite.restype = _CtxPtr

    lib.numkit_ctx_create_full.argtypes = [ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_ctx_create_full.restype = _CtxPtr

    lib.numkit_ctx_destroy.argtypes = [_CtxPtr]
    lib.numkit_ctx_destroy.restype = None

    lib.numkit_ctx_is_full.argtypes = [_CtxPtr]
    lib.numkit_ctx_is_full.restype = ctypes.c_int

    lib.numkit_ctx_load_plugin.argtypes = [_CtxPtr, ctypes.c_char_p, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_ctx_load_plugin.restype = ctypes.c_int

    lib.numkit_ctx_add_plugin_search_dir.argtypes = [_CtxPtr, ctypes.c_char_p]
    lib.numkit_ctx_add_plugin_search_dir.restype = None

    lib.numkit_ctx_has_function.argtypes = [_CtxPtr, ctypes.c_char_p, ctypes.c_char_p]
    lib.numkit_ctx_has_function.restype = ctypes.c_int

    lib.numkit_ctx_seed_rng.argtypes = [_CtxPtr, ctypes.c_uint64]
    lib.numkit_ctx_seed_rng.restype = None

    # 2. Value creation & lifecycle
    lib.numkit_val_empty.argtypes = []
    lib.numkit_val_empty.restype = _ValPtr

    lib.numkit_val_scalar.argtypes = [ctypes.c_double]
    lib.numkit_val_scalar.restype = _ValPtr

    lib.numkit_val_logical.argtypes = [ctypes.c_int]
    lib.numkit_val_logical.restype = _ValPtr

    lib.numkit_val_complex_scalar.argtypes = [ctypes.c_double, ctypes.c_double]
    lib.numkit_val_complex_scalar.restype = _ValPtr

    lib.numkit_val_string.argtypes = [ctypes.c_char_p]
    lib.numkit_val_string.restype = _ValPtr

    lib.numkit_val_char.argtypes = [ctypes.c_char_p]
    lib.numkit_val_char.restype = _ValPtr

    lib.numkit_val_func_handle.argtypes = [ctypes.c_char_p]
    lib.numkit_val_func_handle.restype = _ValPtr

    lib.numkit_val_array_copy.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.c_int,
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_val_array_copy.restype = _ValPtr

    lib.numkit_val_view.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.c_int,
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_val_view.restype = _ValPtr

    lib.numkit_val_clone.argtypes = [_ValPtr]
    lib.numkit_val_clone.restype = _ValPtr

    lib.numkit_val_release.argtypes = [_ValPtr]
    lib.numkit_val_release.restype = None

    lib.numkit_debug_live_values.argtypes = []
    lib.numkit_debug_live_values.restype = ctypes.c_int64

    # 3. Introspection & data access
    lib.numkit_val_type.argtypes = [_ValPtr]
    lib.numkit_val_type.restype = ctypes.c_int

    lib.numkit_val_numel.argtypes = [_ValPtr]
    lib.numkit_val_numel.restype = ctypes.c_size_t

    lib.numkit_val_ndims.argtypes = [_ValPtr]
    lib.numkit_val_ndims.restype = ctypes.c_size_t

    lib.numkit_val_dims.argtypes = [_ValPtr, ctypes.POINTER(ctypes.c_size_t), ctypes.c_size_t]
    lib.numkit_val_dims.restype = ctypes.c_size_t

    lib.numkit_val_is_empty.argtypes = [_ValPtr]
    lib.numkit_val_is_empty.restype = ctypes.c_int

    lib.numkit_val_is_scalar.argtypes = [_ValPtr]
    lib.numkit_val_is_scalar.restype = ctypes.c_int

    lib.numkit_val_raw_data.argtypes = [_ValPtr]
    lib.numkit_val_raw_data.restype = ctypes.c_void_p

    lib.numkit_val_raw_bytes.argtypes = [_ValPtr]
    lib.numkit_val_raw_bytes.restype = ctypes.c_size_t

    lib.numkit_val_copy_bytes.argtypes = [_ValPtr, ctypes.c_void_p, ctypes.c_size_t]
    lib.numkit_val_copy_bytes.restype = ctypes.c_size_t

    lib.numkit_val_as_double.argtypes = [_ValPtr, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_val_as_double.restype = ctypes.c_double

    lib.numkit_val_as_bool.argtypes = [_ValPtr, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_val_as_bool.restype = ctypes.c_int

    lib.numkit_val_as_complex.argtypes = [
        _ValPtr,
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_val_as_complex.restype = ctypes.c_int

    lib.numkit_val_string_bytes.argtypes = [_ValPtr]
    lib.numkit_val_string_bytes.restype = ctypes.c_size_t

    lib.numkit_val_write_string.argtypes = [_ValPtr, ctypes.c_char_p, ctypes.c_size_t]
    lib.numkit_val_write_string.restype = ctypes.c_size_t

    lib.numkit_val_object_class.argtypes = [_ValPtr, ctypes.c_char_p, ctypes.c_size_t]
    lib.numkit_val_object_class.restype = ctypes.c_size_t

    # 4. Containers
    lib.numkit_cell_create.argtypes = [
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.c_int,
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_cell_create.restype = _ValPtr

    lib.numkit_cell_get.argtypes = [_ValPtr, ctypes.c_size_t, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_cell_get.restype = _ValPtr

    lib.numkit_cell_set.argtypes = [_ValPtr, ctypes.c_size_t, _ValPtr, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_cell_set.restype = ctypes.c_int

    lib.numkit_struct_create.argtypes = [ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_struct_create.restype = _ValPtr

    lib.numkit_struct_num_fields.argtypes = [_ValPtr]
    lib.numkit_struct_num_fields.restype = ctypes.c_size_t

    lib.numkit_struct_field_name.argtypes = [_ValPtr, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t]
    lib.numkit_struct_field_name.restype = ctypes.c_size_t

    lib.numkit_struct_get.argtypes = [
        _ValPtr,
        ctypes.c_size_t,
        ctypes.c_char_p,
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_struct_get.restype = _ValPtr

    lib.numkit_struct_set.argtypes = [
        _ValPtr,
        ctypes.c_size_t,
        ctypes.c_char_p,
        _ValPtr,
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_struct_set.restype = ctypes.c_int

    # 5. Dispatch & eval
    lib.numkit_call.argtypes = [
        _CtxPtr,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(_ValPtr),
        ctypes.c_size_t,
        ctypes.c_size_t,
        ctypes.POINTER(_ValPtr),
        ctypes.POINTER(NumkitErrorStruct),
    ]
    lib.numkit_call.restype = ctypes.c_int

    lib.numkit_eval.argtypes = [_CtxPtr, ctypes.c_char_p, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_eval.restype = _ValPtr

    lib.numkit_workspace_get.argtypes = [_CtxPtr, ctypes.c_char_p, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_workspace_get.restype = _ValPtr

    lib.numkit_workspace_set.argtypes = [_CtxPtr, ctypes.c_char_p, _ValPtr, ctypes.POINTER(NumkitErrorStruct)]
    lib.numkit_workspace_set.restype = ctypes.c_int

    _LIB = lib
    return lib


def _check_err(err: NumkitErrorStruct) -> None:
    if err.code != 0:
        raise NumKitError(err.message.decode("utf-8", errors="replace"))


class ObjectHandle:
    """Wrapper for opaque MATLAB/NumKit object values (e.g. `sym`, `tf`, `ss`)."""

    def __init__(self, handle: int, class_name: str, text: str) -> None:
        self._handle = _ValPtr(handle)
        self.class_name = class_name
        self.text = text

    def __del__(self) -> None:
        if getattr(self, "_handle", None) and _LIB is not None:
            _LIB.numkit_val_release(self._handle)
            self._handle = _ValPtr(0)

    def __repr__(self) -> str:
        return f"<numkit.{self.class_name}: {self.text}>"

    def __str__(self) -> str:
        return self.text


def box_value(val: Any, keep_alive: list[Any]) -> _ValPtr:
    """Convert a Python / NumPy value into an owned `numkit_val*` handle."""
    lib = get_lib()
    err = NumkitErrorStruct()

    if isinstance(val, ObjectHandle):
        return lib.numkit_val_clone(val._handle)

    if val is None:
        return lib.numkit_val_empty()

    if isinstance(val, bool):
        return lib.numkit_val_logical(1 if val else 0)

    if isinstance(val, (int, float)):
        return lib.numkit_val_scalar(float(val))

    if isinstance(val, complex):
        return lib.numkit_val_complex_scalar(val.real, val.imag)

    if isinstance(val, str):
        if val.startswith("@"):
            return lib.numkit_val_func_handle(val[1:].encode("utf-8"))
        return lib.numkit_val_char(val.encode("utf-8"))

    if isinstance(val, dict):
        st = lib.numkit_struct_create(1, 1, ctypes.byref(err))
        _check_err(err)
        for k, v in val.items():
            sub = box_value(v, keep_alive)
            try:
                lib.numkit_struct_set(st, 0, str(k).encode("utf-8"), sub, ctypes.byref(err))
                _check_err(err)
            finally:
                lib.numkit_val_release(sub)
        return st

    if _np is not None and isinstance(val, _np.ndarray):
        if val.ndim == 0:
            return box_value(val.item(), keep_alive)
        arr = _np.asfortranarray(val)
        shape = (1, arr.shape[0]) if arr.ndim == 1 else arr.shape
        c_dims = (ctypes.c_size_t * len(shape))(*shape)
        if arr.dtype == _np.float64:
            keep_alive.append(arr)
            h = lib.numkit_val_view(
                arr.ctypes.data_as(ctypes.c_void_p),
                NUMKIT_DTYPE_DOUBLE,
                c_dims,
                len(shape),
                ctypes.byref(err),
            )
            _check_err(err)
            return h
        if arr.dtype == _np.complex128:
            keep_alive.append(arr)
            h = lib.numkit_val_view(
                arr.ctypes.data_as(ctypes.c_void_p),
                NUMKIT_DTYPE_COMPLEX,
                c_dims,
                len(shape),
                ctypes.byref(err),
            )
            _check_err(err)
            return h
        arr64 = _np.asfortranarray(arr, dtype=_np.float64)
        keep_alive.append(arr64)
        h = lib.numkit_val_view(
            arr64.ctypes.data_as(ctypes.c_void_p),
            NUMKIT_DTYPE_DOUBLE,
            c_dims,
            len(shape),
            ctypes.byref(err),
        )
        _check_err(err)
        return h

    if isinstance(val, Sequence):
        if len(val) == 0:
            return lib.numkit_val_empty()
        # 2D nested sequence [[...], [...]]
        if isinstance(val[0], Sequence) and not isinstance(val[0], (str, bytes)):
            rows = len(val)
            cols = len(val[0])
            # Column-major flatten
            flat = [float(val[r][c]) for c in range(cols) for r in range(rows)]
            c_buf = (ctypes.c_double * len(flat))(*flat)
            c_dims = (ctypes.c_size_t * 2)(rows, cols)
            h = lib.numkit_val_array_copy(
                ctypes.cast(c_buf, ctypes.c_void_p),
                NUMKIT_DTYPE_DOUBLE,
                c_dims,
                2,
                ctypes.byref(err),
            )
            _check_err(err)
            return h
        # 1D sequence
        flat = [float(x) for x in val]
        c_buf = (ctypes.c_double * len(flat))(*flat)
        c_dims = (ctypes.c_size_t * 2)(1, len(flat))
        h = lib.numkit_val_array_copy(
            ctypes.cast(c_buf, ctypes.c_void_p),
            NUMKIT_DTYPE_DOUBLE,
            c_dims,
            2,
            ctypes.byref(err),
        )
        _check_err(err)
        return h

    raise TypeError(f"Unsupported argument type for NumKit: {type(val)!r}")


def unbox_value(handle: _ValPtr, ctx_ptr: _CtxPtr | None = None) -> Any:
    """Convert an owned `numkit_val*` handle into a Python / NumPy value and release the handle."""
    if not handle:
        return None
    lib = get_lib()
    err = NumkitErrorStruct()
    try:
        dtype = lib.numkit_val_type(handle)
        numel = lib.numkit_val_numel(handle)
        ndims = lib.numkit_val_ndims(handle)
        c_dims = (ctypes.c_size_t * max(2, ndims))()
        lib.numkit_val_dims(handle, c_dims, max(2, ndims))
        dims = tuple(c_dims[i] for i in range(ndims))

        if dtype == NUMKIT_DTYPE_OBJECT:
            cls_len = lib.numkit_val_object_class(handle, None, 0)
            cls_buf = ctypes.create_string_buffer(cls_len + 1)
            lib.numkit_val_object_class(handle, cls_buf, cls_len + 1)
            cls_name = cls_buf.value.decode("utf-8", errors="replace")

            text = ""
            if ctx_ptr:
                c_in = (_ValPtr * 1)(handle)
                c_out = (_ValPtr * 1)()
                char_err = NumkitErrorStruct()
                lib.numkit_call(ctx_ptr, None, b"char", c_in, 1, 1, c_out, ctypes.byref(char_err))
                if char_err.code == 0 and c_out[0]:
                    res = unbox_value(c_out[0], None)
                    if isinstance(res, str):
                        text = res
            if not text:
                str_len = lib.numkit_val_string_bytes(handle)
                str_buf = ctypes.create_string_buffer(str_len + 1)
                lib.numkit_val_write_string(handle, str_buf, str_len + 1)
                text = str_buf.value.decode("utf-8", errors="replace")

            cloned = lib.numkit_val_clone(handle)
            return ObjectHandle(cloned, cls_name, text)

        if dtype in (NUMKIT_DTYPE_CHAR, NUMKIT_DTYPE_STRING):
            nbytes = lib.numkit_val_string_bytes(handle)
            buf = ctypes.create_string_buffer(nbytes + 1)
            lib.numkit_val_write_string(handle, buf, nbytes + 1)
            return buf.value.decode("utf-8", errors="replace")

        if dtype == NUMKIT_DTYPE_LOGICAL and numel == 1:
            return bool(lib.numkit_val_as_bool(handle, ctypes.byref(err)))

        if dtype == NUMKIT_DTYPE_DOUBLE and numel == 1:
            return float(lib.numkit_val_as_double(handle, ctypes.byref(err)))

        if dtype == NUMKIT_DTYPE_COMPLEX and numel == 1:
            re = ctypes.c_double()
            im = ctypes.c_double()
            lib.numkit_val_as_complex(handle, ctypes.byref(re), ctypes.byref(im), ctypes.byref(err))
            return complex(re.value, im.value)

        if dtype == NUMKIT_DTYPE_STRUCT:
            nfields = lib.numkit_struct_num_fields(handle)
            result: dict[str, Any] = {}
            for i in range(nfields):
                flen = lib.numkit_struct_field_name(handle, i, None, 0)
                fbuf = ctypes.create_string_buffer(flen + 1)
                lib.numkit_struct_field_name(handle, i, fbuf, flen + 1)
                fname = fbuf.value.decode("utf-8", errors="replace")
                fval = lib.numkit_struct_get(handle, 0, fbuf.value, ctypes.byref(err))
                result[fname] = unbox_value(fval)
            return result

        if dtype == NUMKIT_DTYPE_CELL:
            return [
                unbox_value(lib.numkit_cell_get(handle, i, ctypes.byref(err)))
                for i in range(numel)
            ]

        # Numeric / logical array
        if _np is not None:
            if dtype == NUMKIT_DTYPE_COMPLEX:
                out = _np.empty(dims, dtype=_np.complex128, order="F")
            else:
                out = _np.empty(dims, dtype=_np.float64, order="F")
            if numel > 0:
                lib.numkit_val_copy_bytes(handle, out.ctypes.data_as(ctypes.c_void_p), out.nbytes)
            if len(dims) == 2 and (dims[0] == 1 or dims[1] == 1):
                return out.reshape(-1)
            return out

        # Pure-Python fallback (without NumPy)
        if dtype == NUMKIT_DTYPE_COMPLEX:
            c_arr = (ctypes.c_double * (2 * numel))()
            lib.numkit_val_copy_bytes(handle, ctypes.cast(c_arr, ctypes.c_void_p), ctypes.sizeof(c_arr))
            vals = [complex(c_arr[2 * i], c_arr[2 * i + 1]) for i in range(numel)]
        else:
            c_arr = (ctypes.c_double * numel)()
            lib.numkit_val_copy_bytes(handle, ctypes.cast(c_arr, ctypes.c_void_p), ctypes.sizeof(c_arr))
            vals = [float(c_arr[i]) for i in range(numel)]

        if len(dims) == 2 and dims[0] > 1 and dims[1] > 1:
            rows, cols = dims
            return [[vals[c * rows + r] for c in range(cols)] for r in range(rows)]
        return vals
    finally:
        lib.numkit_val_release(handle)


def infer_caller_nargout(default: int = 1, depth: int = 2) -> int:
    """Inspect caller bytecode to detect tuple unpacking (`b, a = signal.butter(...)`)."""
    try:
        frame = sys._getframe(depth)
        code = frame.f_code
        lasti = frame.f_lasti
        instructions = list(dis.get_instructions(code))
        for idx, instr in enumerate(instructions):
            if instr.offset == lasti:
                # Look ahead skipping CACHE / COPY / EXTENDED_ARG instructions in Python 3.11+
                for nxt in instructions[idx + 1 : idx + 6]:
                    if nxt.opname == "UNPACK_SEQUENCE":
                        return max(1, int(nxt.argval))
                    if nxt.opname not in ("CACHE", "PRECALL", "CALL", "KW_NAMES"):
                        break
                break
    except Exception:
        pass
    return default


class Context:
    """NumKit execution context (`mode='lite'` for engine-free toolboxes, `'full'` for engine)."""

    def __init__(self, mode: str = "lite") -> None:
        lib = get_lib()
        err = NumkitErrorStruct()
        if mode == "full":
            ptr = lib.numkit_ctx_create_full(ctypes.byref(err))
        elif mode == "lite":
            ptr = lib.numkit_ctx_create_lite(ctypes.byref(err))
        else:
            raise ValueError(f"Invalid context mode {mode!r}; expected 'lite' or 'full'")
        _check_err(err)
        self._ptr = _CtxPtr(ptr)
        self._loaded_plugins: set[str] = set()

    def __del__(self) -> None:
        if getattr(self, "_ptr", None) and _LIB is not None:
            _LIB.numkit_ctx_destroy(self._ptr)
            self._ptr = _CtxPtr(0)

    @property
    def is_full(self) -> bool:
        return bool(get_lib().numkit_ctx_is_full(self._ptr))

    def load_plugin(self, name_or_path: str) -> None:
        if name_or_path in self._loaded_plugins:
            return
        lib = get_lib()
        err = NumkitErrorStruct()
        lib.numkit_ctx_load_plugin(self._ptr, name_or_path.encode("utf-8"), ctypes.byref(err))
        _check_err(err)
        self._loaded_plugins.add(name_or_path)

    def seed_rng(self, seed: int) -> None:
        get_lib().numkit_ctx_seed_rng(self._ptr, int(seed))

    def call(
        self,
        ns: str,
        name: str,
        *args: Any,
        nargout: int | None = None,
        default_nargout: int = 1,
    ) -> Any:
        if ns and ns not in self._loaded_plugins:
            self.load_plugin(ns)
        actual_nargout = (
            nargout if nargout is not None else infer_caller_nargout(default_nargout, depth=3)
        )
        lib = get_lib()
        keep_alive: list[Any] = []
        boxed = [box_value(a, keep_alive) for a in args]
        c_args = (_ValPtr * len(boxed))(*boxed) if boxed else None
        out_count = max(1, actual_nargout)
        c_outs = (_ValPtr * out_count)()
        err = NumkitErrorStruct()
        try:
            lib.numkit_call(
                self._ptr,
                ns.encode("utf-8") if ns else None,
                name.encode("utf-8"),
                c_args,
                len(boxed),
                out_count,
                c_outs,
                ctypes.byref(err),
            )
            _check_err(err)
            if actual_nargout == 0:
                for i in range(out_count):
                    lib.numkit_val_release(c_outs[i])
                return None
            if actual_nargout == 1:
                return unbox_value(c_outs[0], self._ptr)
            return tuple(unbox_value(c_outs[i], self._ptr) for i in range(actual_nargout))
        finally:
            for h in boxed:
                lib.numkit_val_release(h)

    def eval(self, code: str) -> Any:
        lib = get_lib()
        err = NumkitErrorStruct()
        h = lib.numkit_eval(self._ptr, code.encode("utf-8"), ctypes.byref(err))
        _check_err(err)
        return unbox_value(h, self._ptr)

    def workspace_get(self, name: str) -> Any:
        lib = get_lib()
        err = NumkitErrorStruct()
        h = lib.numkit_workspace_get(self._ptr, name.encode("utf-8"), ctypes.byref(err))
        _check_err(err)
        return unbox_value(h, self._ptr)

    def workspace_set(self, name: str, val: Any) -> None:
        lib = get_lib()
        keep_alive: list[Any] = []
        h = box_value(val, keep_alive)
        err = NumkitErrorStruct()
        try:
            lib.numkit_workspace_set(self._ptr, name.encode("utf-8"), h, ctypes.byref(err))
            _check_err(err)
        finally:
            lib.numkit_val_release(h)


_DEFAULT_CTX: Context | None = None


def default_context(mode: str = "lite") -> Context:
    global _DEFAULT_CTX
    if _DEFAULT_CTX is None or (mode == "full" and not _DEFAULT_CTX.is_full):
        _DEFAULT_CTX = Context(mode=mode)
    return _DEFAULT_CTX
