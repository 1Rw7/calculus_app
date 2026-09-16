import streamlit as st
import sympy as sp
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.symbolic import parse
from viz.tangent import plot_tangent
from viz.secant import plot_secant
from viz.riemann import plot_riemann

st.set_page_config(page_title="可视化实验室", page_icon="🔬", layout="wide")
st.title("🔬 可视化实验室")

tab1, tab2, tab3 = st.tabs(["🎯 切线滑动器", "📉 差商 → 导数", "🧱 黎曼和"])

# ---------- Tab 1: 切线 ----------
with tab1:
    col1, col2 = st.columns([1, 3])
    with col1:
        expr_str = st.text_input("函数 f(x)", value="x**2", key="t_expr")
        x0 = float(st.slider("切点 x₀", -5.0, 5.0, 1.0, 0.1, key="t_x0"))
        rng = float(st.slider("显示范围 ±", 2.0, 20.0, 5.0, key="t_rng"))
    try:
        expr, x = parse(expr_str)
        st.latex(rf"f(x) = {sp.latex(expr)}")
        st.latex(rf"f'(x) = {sp.latex(sp.diff(expr, x))}")
        fig = plot_tangent(expr, x0, (-rng, rng))
        with col2:
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"解析失败：{type(e).__name__}: {e}")

# ---------- Tab 2: 差商 ----------
with tab2:
    col1, col2 = st.columns([1, 3])
    with col1:
        expr_str2 = st.text_input("函数 f(x)", value="sin(x)", key="s_expr")
        x0_2 = float(st.slider("点 x₀", -5.0, 5.0, 1.0, 0.1, key="s_x0"))
        dx = float(st.slider("Δx", 0.001, 2.0, 1.0, 0.001, key="s_dx"))
        rng2 = float(st.slider("显示范围 ±", 2.0, 20.0, 6.0, key="s_rng"))
    try:
        expr2, x2 = parse(expr_str2)
        fig2 = plot_secant(expr2, x0_2, dx, (-rng2, rng2))
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Δx 越小，割线越接近切线，斜率越接近真导数。**")
    except Exception as e:
        st.error(f"解析失败：{type(e).__name__}: {e}")

# ---------- Tab 3: 黎曼和 ----------
with tab3:
    col1, col2 = st.columns([1, 3])
    with col1:
        expr_str3 = st.text_input("函数 f(x)", value="x**2", key="r_expr")
        a = float(st.number_input("下限 a", value=0.0, key="r_a"))
        b = float(st.number_input("上限 b", value=2.0, key="r_b"))
        n = int(st.slider("矩形数量 n", 1, 200, 10, key="r_n"))
    try:
        expr3, x3 = parse(expr_str3)
        if a >= b:
            st.warning("请确保 a < b")
        else:
            fig3, total, exact = plot_riemann(expr3, a, b, n, (min(a, 0) - 1, b + 1))
            with col2:
                st.plotly_chart(fig3, use_container_width=True)
            c1, c2 = st.columns(2)
            c1.metric("黎曼和 (n=%d)" % n, f"{total:.5f}")
            c2.metric("精确积分", f"{exact:.5f}")
    except Exception as e:
        st.error(f"解析失败：{type(e).__name__}: {e}")