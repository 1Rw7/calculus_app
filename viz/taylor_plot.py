"""泰勒展开可视化：f(x) 与 n 阶泰勒多项式对比"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from core.numeric import safe_eval


def plot_taylor(expr, n, around, x_range=(-5, 5)):
    """
    画出 f(x) 与 n 阶泰勒多项式在 around 处的逼近效果。
    返回 (fig, taylor_expr)
    """
    x = sp.Symbol('x')
    xs = np.linspace(x_range[0], x_range[1], 500)
    ys = safe_eval(expr, xs)

    # 泰勒多项式
    taylor_expr = sp.series(expr, x, around, n + 1).removeO()
    taylor_y = safe_eval(taylor_expr, xs)

    # 精确值范围裁剪（防止高阶多项式飞出图外）
    y_max = np.nanmax(np.abs(ys)) if np.any(np.isfinite(ys)) else 10
    clip = max(y_max * 3, 20)

    fig = go.Figure()

    # 原函数
    fig.add_trace(go.Scatter(
        x=xs, y=ys, name='f(x)',
        line=dict(width=3, color='#1f77b4')
    ))

    # 泰勒多项式
    ty_clipped = np.where(np.abs(taylor_y) > clip, np.nan, taylor_y)
    fig.add_trace(go.Scatter(
        x=xs, y=ty_clipped, name=f'P_{n}(x) 泰勒多项式',
        line=dict(width=2.5, color='#ff7f0e', dash='dash')
    ))

    # 展开点标记
    y0 = float(expr.subs(x, float(around)))
    fig.add_trace(go.Scatter(
        x=[around], y=[y0], mode='markers',
        marker=dict(size=14, color='red', symbol='star'),
        name=f'展开点 x={around}'
    ))

    fig.update_layout(
        title=f"泰勒展开：{n} 阶，在 x = {around} 处",
        xaxis_title='x', yaxis_title='y',
        height=560, hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
    )
    return fig, taylor_expr