"""参数方程与极坐标曲线可视化"""
import numpy as np
import plotly.graph_objects as go
import sympy as sp


def plot_parametric(x_expr, y_expr, t_range=(0, 2 * np.pi), n=500, t0=None):
    """
    参数曲线 (x(t), y(t))，可选标记切点 t0。
    返回 (fig, slope) —— slope 是 t0 处的 dy/dx
    """
    t = sp.Symbol('t')

    fx = sp.lambdify(t, x_expr, 'numpy')
    fy = sp.lambdify(t, y_expr, 'numpy')

    ts = np.linspace(t_range[0], t_range[1], n)
    xs = fx(ts)
    ys = fy(ts)
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=xs, y=ys, name='参数曲线',
        line=dict(width=3, color='#1f77b4'),
        mode='lines',
    ))

    slope = None
    if t0 is not None:
        x0 = float(x_expr.subs(t, float(t0)))
        y0 = float(y_expr.subs(t, float(t0)))
        dx_dt = float(sp.diff(x_expr, t).subs(t, float(t0)))
        dy_dt = float(sp.diff(y_expr, t).subs(t, float(t0)))
        slope = dy_dt / dx_dt if dx_dt != 0 else float('inf')

        # 切线（如果斜率有限）
        if dx_dt != 0:
            t_line = np.linspace(-3, 3, 50)
            tangent_x = x0 + t_line
            tangent_y = y0 + slope * t_line
        else:
            # 竖直切线
            tangent_x = np.full(50, x0)
            tangent_y = np.linspace(y0 - 3, y0 + 3, 50)

        fig.add_trace(go.Scatter(
            x=tangent_x, y=tangent_y, name=f'切线 斜率={slope:.3f}',
            line=dict(dash='dash', color='red', width=2),
        ))

        fig.add_trace(go.Scatter(
            x=[x0], y=[y0], mode='markers',
            marker=dict(size=12, color='red'),
            name=f'切点 t={t0:.2f}',
        ))

    fig.update_layout(
        title="参数方程曲线" if t0 is None else f"参数曲线 + 切点 t={t0:.2f}",
        xaxis_title='x', yaxis_title='y',
        height=600, hovermode='closest',
        template='plotly_white',
        yaxis=dict(scaleanchor='x', scaleratio=1),  # 保持等比例，圆不变椭圆
    )
    return fig, slope


def plot_polar(r_expr, theta_range=(0, 2 * np.pi), n=800, theta0=None):
    """
    极坐标 r(θ) 曲线。
    返回 (fig, slope) —— theta0 处的 dy/dx（笛卡尔斜率）
    """
    theta = sp.Symbol('theta')

    fr = sp.lambdify(theta, r_expr, 'numpy')
    thetas = np.linspace(theta_range[0], theta_range[1], n)
    rs = fr(thetas)
    rs = np.asarray(rs, dtype=float)

    xs = rs * np.cos(thetas)
    ys = rs * np.sin(thetas)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=xs, y=ys, name='极坐标曲线',
        line=dict(width=3, color='#9467bd'),
    ))

    slope = None
    if theta0 is not None:
        r0 = float(r_expr.subs(theta, float(theta0)))
        x0 = r0 * np.cos(theta0)
        y0 = r0 * np.sin(theta0)

        # 极坐标下的 dy/dx = (r' sinθ + r cosθ) / (r' cosθ - r sinθ)
        r_prime = float(sp.diff(r_expr, theta).subs(theta, float(theta0)))
        num = r_prime * np.sin(theta0) + r0 * np.cos(theta0)
        den = r_prime * np.cos(theta0) - r0 * np.sin(theta0)
        slope = num / den if abs(den) > 1e-9 else float('inf')

        if np.isfinite(slope):
            t_line = np.linspace(-3, 3, 50)
            tangent_x = x0 + t_line
            tangent_y = y0 + slope * t_line
        else:
            tangent_x = np.full(50, x0)
            tangent_y = np.linspace(y0 - 3, y0 + 3, 50)

        fig.add_trace(go.Scatter(
            x=tangent_x, y=tangent_y, name=f'切线 斜率={slope:.3f}',
            line=dict(dash='dash', color='red', width=2),
        ))
        fig.add_trace(go.Scatter(
            x=[x0], y=[y0], mode='markers',
            marker=dict(size=12, color='red'),
            name=f'切点 θ={theta0:.2f}',
        ))

    fig.update_layout(
        title="极坐标曲线" if theta0 is None else f"极坐标曲线 + 切点 θ={theta0:.2f}",
        xaxis_title='x', yaxis_title='y',
        height=600, hovermode='closest',
        template='plotly_white',
        yaxis=dict(scaleanchor='x', scaleratio=1),
    )
    return fig, slope