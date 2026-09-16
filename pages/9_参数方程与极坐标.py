import streamlit as st
import sympy as sp
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from viz.parametric import plot_parametric, plot_polar

st.set_page_config(page_title="参数方程与极坐标", page_icon="🌀", layout="wide")
st.title("🌀 参数方程与极坐标")
st.caption("换一种方式描述曲线，切线又该怎么求？")

tab1, tab2 = st.tabs(["📐 参数方程", "🎯 极坐标"])

# =============== 参数方程 ===============
with tab1:
    col1, col2 = st.columns([1, 4])

    with col1:
        x_expr_str = st.text_input("x(t) =", value="cos(t)", key="par_x")
        y_expr_str = st.text_input("y(t) =", value="sin(t)", key="par_y")
        t0 = st.slider("切点参数 t₀", 0.0, float(2 * np.pi), 1.0, 0.05, key="par_t0")

    try:
        t = sp.Symbol('t')
        x_expr = sp.sympify(x_expr_str,
                             locals={'t': t, 'sin': sp.sin, 'cos': sp.cos,
                                     'exp': sp.exp, 'log': sp.log,
                                     'sqrt': sp.sqrt, 'pi': sp.pi})
        y_expr = sp.sympify(y_expr_str,
                             locals={'t': t, 'sin': sp.sin, 'cos': sp.cos,
                                     'exp': sp.exp, 'log': sp.log,
                                     'sqrt': sp.sqrt, 'pi': sp.pi})

        st.latex(rf"x(t) = {sp.latex(x_expr)}")
        st.latex(rf"y(t) = {sp.latex(y_expr)}")

        fig, slope = plot_parametric(x_expr, y_expr, (0, 2 * np.pi), 500, t0)
        with col2:
            st.plotly_chart(fig, use_container_width=True)

        # 计算 t₀ 处信息
        dx_dt = sp.diff(x_expr, t)
        dy_dt = sp.diff(y_expr, t)

        st.divider()
        st.subheader("求导公式")
        st.markdown("参数曲线的切线斜率：")
        st.latex(r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{y'(t)}{x'(t)}")

        st.latex(rf"\frac{{dy}}{{dt}} = {sp.latex(dy_dt)}, \quad \frac{{dx}}{{dt}} = {sp.latex(dx_dt)}")

        if slope is not None:
            if np.isfinite(slope):
                st.success(f"在 t₀ = {t0:.2f} 处，切线斜率 dy/dx = **{slope:.4f}**")
            else:
                st.warning(f"在 t₀ = {t0:.2f} 处，切线**竖直**（dx/dt = 0）")

        st.divider()
        st.markdown("""
### 💡 试试这些曲线

- `x(t)=cos(t), y(t)=sin(t)`：单位圆，切线斜率 = -x/y
- `x(t)=t**2, y(t)=t**3`：尖点曲线（t=0 处不可导）
- `x(t)=cos(t)**3, y(t)=sin(t)**3`：星形线
- `x(t)=t - sin(t), y(t)=1 - cos(t)`：摆线

**观察**：把 t₀ 拖到某些特殊点（比如 0、π/2、π），看看切线怎么变。
""")
    except Exception as e:
        st.error(f"解析失败：{type(e).__name__}: {e}")

# =============== 极坐标 ===============
with tab2:
    col1, col2 = st.columns([1, 4])

    with col1:
        r_expr_str = st.text_input("r(θ) =", value="1 + cos(theta)", key="pol_r")
        theta0 = st.slider("切点 θ₀", 0.0, float(2 * np.pi), 1.0, 0.05, key="pol_t0")

    try:
        theta = sp.Symbol('theta')
        r_expr = sp.sympify(r_expr_str,
                             locals={'theta': theta, 'sin': sp.sin, 'cos': sp.cos,
                                     'exp': sp.exp, 'log': sp.log,
                                     'sqrt': sp.sqrt, 'pi': sp.pi})

        st.latex(rf"r(\theta) = {sp.latex(r_expr)}")

        fig, slope = plot_polar(r_expr, (0, 2 * np.pi), 800, theta0)
        with col2:
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("求导公式")
        st.markdown("极坐标下用 θ 做参数，则 $x = r\\cos\\theta$，$y = r\\sin\\theta$：")
        st.latex(r"\frac{dy}{dx} = \frac{r'\sin\theta + r\cos\theta}{r'\cos\theta - r\sin\theta}")

        if slope is not None:
            if np.isfinite(slope):
                st.success(f"在 θ₀ = {theta0:.2f} 处，切线斜率 dy/dx = **{slope:.4f}**")
            else:
                st.warning(f"在 θ₀ = {theta0:.2f} 处，切线**竖直**")

        st.divider()
        st.markdown("""
### 💡 试试这些极坐标曲线

- `1 + cos(theta)`：心形线（cardioid）
- `cos(2*theta)`：四叶玫瑰
- `theta`：阿基米德螺线
- `exp(theta/5)`：对数螺线
- `1`：单位圆
- `2*cos(theta)`：经过原点的圆（θ 范围会有周期性问题，观察曲线闭合处）

**观察**：拖动 θ₀ 沿曲线走一圈，切线方向怎么变？
""")
    except Exception as e:
        st.error(f"解析失败：{type(e).__name__}: {e}")