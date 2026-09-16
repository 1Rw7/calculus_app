"""差商 → 导数：割线随 Δx 收缩逼近切线"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from core.numeric import safe_eval


def plot_secant(expr, x0, dx, x_range=(-5, 5)):
    x = sp.Symbol('x')
    xs = np.linspace(x_range[0], x_range[1], 500)
    ys = safe_eval(expr, xs)

    f0 = float(expr.subs(x, float(x0)))
    f1 = float(expr.subs(x, float(x0 + dx)))
    slope = (f1 - f0) / dx if dx != 0 else float(sp.diff(expr, x).subs(x, float(x0)))

    secant_y = f0 + slope * (xs - x0)
    true_slope = float(sp.diff(expr, x).subs(x, float(x0)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, name='f(x)',
                             line=dict(width=3, color='#1f77b4')))
    fig.add_trace(go.Scatter(x=xs, y=secant_y, name=f'割线 k={slope:.4f}',
                             line=dict(dash='dash', color='orange')))
    fig.add_trace(go.Scatter(x=[x0, x0 + dx], y=[f0, f1],
                             mode='markers+lines',
                             marker=dict(size=10, color='orange'),
                             line=dict(color='orange', width=2),
                             name='Δx 区间'))
    fig.update_layout(
        title=f"Δx = {dx:.4f} → 割线斜率 {slope:.4f}（真导数 {true_slope:.4f}）",
        xaxis_title='x', yaxis_title='y',
        height=520, hovermode='x unified',
        template='plotly_white',
    )
    return fig