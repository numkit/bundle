#!/usr/bin/env python3
"""Integration tests for the NumKit Python SDK (`bindings/python/numkit`)."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

# Add `bindings/python` to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numkit as nk
from numkit import cas, control, signal, stats


class TestNumKitPythonBindings(unittest.TestCase):
    def test_lite_signal_butter_and_filtfilt(self) -> None:
        baseline = nk.live_handles()
        ctx = nk.create_lite_context()
        self.assertFalse(ctx.is_full)

        # Automatic 2-output unpacking (`b, a = ...`) without specifying nargout=2!
        b, a = signal.butter(4, 0.25, "low", ctx=ctx)
        self.assertEqual(len(b), 5)
        self.assertEqual(len(a), 5)
        self.assertAlmostEqual(a[0], 1.0, places=12)

        # Constant DC signal through lowpass filter -> 1.0
        x = [1.0] * 64
        y = signal.filtfilt(b, a, x, ctx=ctx)
        self.assertEqual(len(y), 64)
        self.assertAlmostEqual(y[32], 1.0, places=9)

        del b, a, y, ctx
        self.assertEqual(nk.live_handles(), baseline)

    def test_lite_stats_and_control(self) -> None:
        baseline = nk.live_handles()
        ctx = nk.create_lite_context()

        pdf0 = stats.normpdf(0.0, 0.0, 1.0, ctx=ctx)
        self.assertAlmostEqual(pdf0, 1.0 / math.sqrt(2.0 * math.pi), places=12)

        # Control toolbox: transfer function W(s) = 1 / (s^2 + 2s + 10)
        sys_tf = control.tf([1.0], [1.0, 2.0, 10.0], ctx=ctx)
        dc = control.dcgain(sys_tf, ctx=ctx)
        self.assertAlmostEqual(dc, 0.1, places=12)

        del sys_tf, ctx
        self.assertEqual(nk.live_handles(), baseline)

    def test_lite_cas_symbolic(self) -> None:
        baseline = nk.live_handles()
        ctx = nk.create_lite_context()

        f = cas.sym("2*x + 3", ctx=ctx)
        x = cas.sym("x", ctx=ctx)
        F = cas.int(f, x, ctx=ctx)
        self.assertIn("x^2", str(F))
        s = cas.call("char", F, ctx=ctx)
        self.assertIn("x^2", s)

        del f, x, F, ctx
        self.assertEqual(nk.live_handles(), baseline)

    def test_full_engine_eval_and_workspace(self) -> None:
        baseline = nk.live_handles()
        ctx = nk.create_full_context()
        self.assertTrue(ctx.is_full)

        trace_val = ctx.eval("M = magic(4); sum(diag(M))")
        self.assertAlmostEqual(trace_val, 34.0, places=12)

        ctx.workspace_set("scale", 2.5)
        scaled = ctx.eval("scale * 10")
        self.assertAlmostEqual(scaled, 25.0, places=12)

        del ctx
        self.assertEqual(nk.live_handles(), baseline)


if __name__ == "__main__":
    unittest.main()
