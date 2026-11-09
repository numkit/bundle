# bindings/python/numkit/__init__.py
"""NumKit Python SDK.

Provides both:
  1. Engine-free Lite Toolbox access (`from numkit import signal, stats, control, cas, ...`)
  2. Full Engine MATLAB-compatible evaluation (`numkit.eval("...")`)
"""

from __future__ import annotations

from typing import Any

from ._ffi import Context, NumKitError, ObjectHandle, default_context, get_lib
from . import audio, cas, comm, control, image, signal, stats, wavelet


def create_lite_context() -> Context:
    """Create a fresh isolated Lite (engine-free toolbox-only) context."""
    return Context(mode="lite")


def create_full_context() -> Context:
    """Create a fresh isolated Full Engine context (supports `eval`)."""
    return Context(mode="full")


def call(name: str, *args: Any, ns: str = "", nargout: int | None = None) -> Any:
    """Invoke a function in the default context."""
    ctx = default_context(mode="lite" if ns else "full")
    return ctx.call(ns, name, *args, nargout=nargout)


def eval(code: str) -> Any:  # noqa: A001
    """Evaluate MATLAB-compatible source `code` in the default Full Engine context."""
    ctx = default_context(mode="full")
    return ctx.eval(code)


def live_handles() -> int:
    """Return the number of currently live `numkit_val*` handles across the C-ABI."""
    return int(get_lib().numkit_debug_live_values())


__all__ = [
    "Context",
    "NumKitError",
    "ObjectHandle",
    "audio",
    "call",
    "cas",
    "comm",
    "control",
    "create_full_context",
    "create_lite_context",
    "default_context",
    "eval",
    "image",
    "live_handles",
    "signal",
    "stats",
    "wavelet",
]
