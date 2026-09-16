"""上下双图：f(x) 与 f'(x) 联动，横坐标共享"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sympy as sp
from core.numeric import safe_eval


def plot_derivative_pair(expr, x_range=(-5, 5), cursor_x=None):
    """
    上下两子图：上画 f(x)，下画 f'(x)。
    如果给定 cursor_x，在两图上都画竖线标记。
    """
    x = sp.Symbol('x')
    xs = np.linspace(x_range[0], x_range[1], 500)
    ys = safe_eval(expr, xs)
    dys = safe_eval(sp.diff(expr, x), xs)

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=('f(x)', "f'(x)"),
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(x=xs, y=ys, name='f(x)',
                   line=dict(width=3, color='#1f77b4')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=xs, y=dys, name="f'(x)",
                   line=dict(width=3, color='#2ca02c')),
        row=2, col=1
    )

    # 零线
    fig.add_hline(y=0, line=dict(color='gray', width=1, dash='dot'),
                  row=2, col=1)

    # 光标竖线
    if cursor_x is not None:
        fig.add_vline(x=cursor_x, line=dict(color='red', width=2, dash='dash'),
                      row=1, col=1)
        fig.add_vline(x=cursor_x, line=dict(color='red', width=2, dash='dash'),
                      row=2, col=1)
        # f 上的点
        fx = float(expr.subs(x, float(cursor_x)))
        dfx = float(sp.diff(expr, x).subs(x, float(cursor_x)))
        fig.add_trace(
            go.Scatter(x=[cursor_x], y=[fx], mode='markers',
                       marker=dict(size=12, color='red'),
                       name='当前点'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=[cursor_x], y=[dfx], mode='markers',
                       marker=dict(size=12, color='red'),
                       showlegend=False),
            row=2, col=1
        )

    fig.update_layout(
        height=680, hovermode='x unified',
        template='plotly_white', showlegend=True,
    )
    return fig