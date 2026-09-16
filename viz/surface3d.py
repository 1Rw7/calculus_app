"""3D 曲面 + 切平面可视化（多元微积分入门）"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp


def plot_surface_3d(expr_xy, x0, y0, x_range=(-3, 3), y_range=(-3, 3), n=40):
    """
    expr_xy: 二元 SymPy 表达式，含符号 x, y
    x0, y0: 切点坐标
    返回 (fig, f_val, fx_val, fy_val) —— 函数值和两个偏导值
    """
    x, y = sp.symbols('x y')

    # lambdify 数值函数
    f = sp.lambdify((x, y), expr_xy, 'numpy')

    # 网格
    xs = np.linspace(x_range[0], x_range[1], n)
    ys = np.linspace(y_range[0], y_range[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    Z = np.asarray(Z, dtype=float)

    # 切平面：z = f(x0,y0) + fx·(x-x0) + fy·(y-y0)
    f0 = float(expr_xy.subs({x: float(x0), y: float(y0)}))
    fx_val = float(sp.diff(expr_xy, x).subs({x: float(x0), y: float(y0)}))
    fy_val = float(sp.diff(expr_xy, y).subs({x: float(x0), y: float(y0)}))

    Z_plane = f0 + fx_val * (X - x0) + fy_val * (Y - y0)

    fig = go.Figure()

    # 曲面
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Blues',
        opacity=0.85,
        name='f(x, y)',
        showscale=False,
    ))

    # 切平面
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z_plane,
        colorscale=[[0, 'rgba(255,100,100,0.6)'], [1, 'rgba(255,100,100,0.6)']],
        opacity=0.6,
        name='切平面',
        showscale=False,
    ))

    # 切点
    fig.add_trace(go.Scatter3d(
        x=[x0], y=[y0], z=[f0],
        mode='markers',
        marker=dict(size=8, color='red'),
        name=f'切点 ({x0}, {y0}, {f0:.3f})',
    ))

    fig.update_layout(
        title=f"z = f(x, y)，切点 ({x0}, {y0})",
        scene=dict(
            xaxis_title='x', yaxis_title='y', zaxis_title='z',
            aspectmode='cube',
        ),
        height=650,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig, f0, fx_val, fy_val