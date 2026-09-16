"""切线滑动器"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from core.numeric import safe_eval


def plot_tangent(expr, x0, x_range=(-5, 5)):
    x = sp.Symbol('x')
    xs = np.linspace(x_range[0], x_range[1], 500)
    ys = safe_eval(expr, xs)

    f0 = float(expr.subs(x, float(x0)))
    slope = float(sp.diff(expr, x).subs(x, float(x0)))
    tangent_y = f0 + slope * (xs - x0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, name='f(x)',
                             line=dict(width=3, color='#1f77b4')))
    fig.add_trace(go.Scatter(x=xs, y=tangent_y, name=f'切线 k={slope:.3f}',
                             line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=[x0], y=[f0], mode='markers',
                             marker=dict(size=12, color='red'),
                             name=f'切点 ({x0:.2f}, {f0:.2f})'))
    fig.update_layout(
        title=f"f(x) 在 x = {x0} 处的切线",
        xaxis_title='x', yaxis_title='y',
        height=520, hovermode='x unified',
        template='plotly_white',
    )
    return fig