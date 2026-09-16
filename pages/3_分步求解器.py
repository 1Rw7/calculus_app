import streamlit as st
import sympy as sp
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.symbolic import parse, derivative, integral, limit, taylor
from core.step_solver import derivative_steps

st.set_page_config(page_title="分步求解器", page_icon="🧮", layout="wide")
st.title("🧮 分步求解器")

mode = st.radio("选择运算", ["求导", "不定积分", "定积分", "极限", "泰勒展开"], horizontal=True)

if mode == "求导":
    expr_str = st.text_input("f(x) =", value="x**3 * sin(x)")
    order = st.number_input("阶数", 1, 5, 1)
    if st.button("计算", type="primary"):
        try:
            steps = derivative_steps(expr_str)
            st.subheader("分步过程")
            for i, (desc, ex) in enumerate(steps, 1):
                st.markdown(f"**第 {i} 步**：{desc}")
                st.latex(sp.latex(ex))
            st.success("完成")
        except Exception as e:
            st.error(f"错误：{type(e).__name__}: {e}")

elif mode == "不定积分":
    expr_str = st.text_input("f(x) =", value="x**2")
    if st.button("计算", type="primary"):
        try:
            expr, x = parse(expr_str)
            F = integral(expr_str)
            st.latex(rf"\int {sp.latex(expr)}\,dx = {sp.latex(F)} + C")
        except Exception as e:
            st.error(f"错误：{type(e).__name__}: {e}")

elif mode == "定积分":
    expr_str = st.text_input("f(x) =", value="x**2")
    c1, c2 = st.columns(2)
    a = c1.text_input("下限 a", value="0")
    b = c2.text_input("上限 b", value="2")
    if st.button("计算", type="primary"):
        try:
            expr, x = parse(expr_str)
            val = integral(expr_str, True, sp.sympify(a), sp.sympify(b))
            st.latex(rf"\int_{{{a}}}^{{{b}}} {sp.latex(expr)}\,dx = {sp.latex(val)}")
            st.write("数值 ≈", float(val))
        except Exception as e:
            st.error(f"错误：{type(e).__name__}: {e}")

elif mode == "极限":
    expr_str = st.text_input("f(x) =", value="sin(x)/x")
    point = st.text_input("x →", value="0")
    direction = st.selectbox("方向", ["+-", "+", "-"], index=0)
    if st.button("计算", type="primary"):
        try:
            expr, x = parse(expr_str)
            val = limit(expr_str, point, direction)
            st.latex(rf"\lim_{{x \to {point}}} {sp.latex(expr)} = {sp.latex(val)}")
        except Exception as e:
            st.error(f"错误：{type(e).__name__}: {e}")

elif mode == "泰勒展开":
    expr_str = st.text_input("f(x) =", value="sin(x)")
    n = st.slider("展开阶数", 1, 12, 6)
    around = st.number_input("展开点", value=0.0)
    if st.button("计算", type="primary"):
        try:
            expr, x = parse(expr_str)
            t = taylor(expr_str, n, around)
            st.latex(rf"{sp.latex(expr)} \approx {sp.latex(t)}")
        except Exception as e:
            st.error(f"错误：{type(e).__name__}: {e}")