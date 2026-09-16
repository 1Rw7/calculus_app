"""数值工具：纯 subs 逐点求值"""
import numpy as np
import sympy as sp


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return float('nan')


def eval_expr(expr, x_vals):
    x = sp.Symbol('x')
    arr = np.asarray(x_vals, dtype=float)
    out = np.empty_like(arr, dtype=float)
    for i, v in enumerate(arr):
        out[i] = _to_float(expr.subs(x, float(v)))
    return out


def difference_quotient(expr, x0, dx):
    x = sp.Symbol('x')
    f0 = float(expr.subs(x, float(x0)))
    f1 = float(expr.subs(x, float(x0 + dx)))
    return (f1 - f0) / dx


def tangent_line(expr, x0):
    x = sp.Symbol('x')
    f0 = float(expr.subs(x, float(x0)))
    slope = float(sp.diff(expr, x).subs(x, float(x0)))
    return f0, slope


def safe_eval(expr, x_vals):
    y = eval_expr(expr, x_vals)
    y = np.where(np.isfinite(y), y, np.nan)
    return y