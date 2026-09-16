"""分步求导引擎：识别结构并给出规则标注"""
import sympy as sp
from core.symbolic import parse


def derivative_steps(expr_str: str):
    """
    返回 [(说明, 表达式), ...] 的分步列表
    """
    expr, x = parse(expr_str)
    steps = [("原函数", expr)]

    rule = _detect_rule(expr, x)
    steps.append((rule, sp.diff(expr, x)))
    steps.append(("化简结果", sp.simplify(sp.diff(expr, x))))

    return steps


def _detect_rule(expr, x):
    if not expr.free_symbols:
        return "常数求导法则：d/dx[c] = 0"

    if expr.is_Pow and expr.base == x:
        return "幂函数法则：d/dx[xⁿ] = n·xⁿ⁻¹"

    if expr.is_Pow and x in expr.base.free_symbols:
        return "幂 + 链式法则：d/dx[uⁿ] = n·uⁿ⁻¹·u′"

    if expr.is_Mul:
        return "乘积法则：(uv)′ = u′v + uv′"

    if expr.is_Pow and expr.exp == -1:
        return "商法则 / 倒数法则"

    fname = getattr(expr.func, '__name__', '')
    mapping = {
        'sin': "链式法则 d/dx[sin(u)] = cos(u)·u′",
        'cos': "链式法则 d/dx[cos(u)] = -sin(u)·u′",
        'tan': "链式法则 d/dx[tan(u)] = sec²(u)·u′",
        'exp': "链式法则 d/dx[eᵘ] = eᵘ·u′",
        'log': "链式法则 d/dx[ln u] = u′/u",
        'sqrt': "链式法则 d/dx[√u] = u′/(2√u)",
    }
    if fname in mapping:
        return mapping[fname]

    return "直接应用求导法则"