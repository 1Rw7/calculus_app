"""黎曼和可视化"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from core.numeric import safe_eval


def plot_riemann(expr, a, b, n, x_range=None):
    x = sp.Symbol('x')
    xs = np.linspace(a, b, 500) if x_range is None else np.linspace(*x_range, 500)
    ys = safe_eval(expr, xs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, name='f(x)',
                             line=dict(width=3, color='#1f77b4')))

    # 左端点黎曼和
    dx = (b - a) / n
    rect_x = []
    rect_y = []
    total = 0.0
    f = sp.lambdify(x, expr, 'numpy')
    for i in range(n):
        xi = a + i * dx
        fi = float(f(xi))
        if not np.isfinite(fi):
            fi = 0.0
        total += fi * dx
        rect_x += [xi, xi, xi + dx, xi + dx, xi]
        rect_y += [0, fi, fi, 0, 0]

    fig.add_trace(go.Scatter(x=rect_x, y=rect_y, fill='toself',
                             fillcolor='rgba(255,165,0,0.35)',
                             line=dict(color='orange', width=1),
                             name=f'黎曼和 ≈ {total:.4f}'))

    exact = float(sp.integrate(expr, (x, a, b)))

    fig.update_layout(
        title=f"n = {n} 个矩形，黎曼和 ≈ {total:.5f}，精确积分 = {exact:.5f}",
        xaxis_title='x', yaxis_title='y',
        height=520, hovermode='x unified',
        template='plotly_white',
    )
    return fig, total, exact