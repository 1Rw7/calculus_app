"""SymPy 符号计算封装：解析、求导、积分、极限、泰勒展开"""
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def _local_dict(x):
    return {
        'x': x,
        'e': sp.E,
        'pi': sp.pi,
        'ln': sp.log,
        'log': sp.log,
        'sin': sp.sin,
        'cos': sp.cos,
        'tan': sp.tan,
        'exp': sp.exp,
        'sqrt': sp.sqrt,
        'abs': sp.Abs,
    }


def parse(expr_str: str):
    """把字符串解析成 (SymPy表达式, 符号x)。失败抛异常。"""
    x = sp.Symbol('x')
    expr = parse_expr(
        expr_str,
        local_dict=_local_dict(x),
        transformations=TRANSFORMS,
        evaluate=True,
    )
    return expr, x


def derivative(expr_str: str, order: int = 1):
    expr, x = parse(expr_str)
    return sp.simplify(sp.diff(expr, x, order))


def integral(expr_str: str, definite: bool = False, a=None, b=None):
    expr, x = parse(expr_str)
    if definite:
        return sp.integrate(expr, (x, a, b))
    return sp.integrate(expr, x)


def limit(expr_str: str, point: str, direction: str = '+-'):
    expr, x = parse(expr_str)
    if point in ('oo', 'inf', '+inf'):
        p = sp.oo
    elif point in ('-oo', '-inf'):
        p = -sp.oo
    else:
        p = sp.sympify(point)
    return sp.limit(expr, x, p, dir=direction)


def taylor(expr_str: str, n: int, around: float = 0):
    expr, x = parse(expr_str)
    return sp.series(expr, x, around, n).removeO()


def to_latex(expr):
    return sp.latex(expr)