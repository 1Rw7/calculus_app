import streamlit as st
import sympy as sp
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.symbolic import parse
from viz.derivative_pair import plot_derivative_pair

st.set_page_config(page_title="函数与导函数", page_icon="🔗", layout="wide")
st.title("🔗 函数与导函数联动")
st.caption("上图画 f(x)，下图画 f'(x)，一眼看穿极值点与导数的关系")

col1, col2 = st.columns([1, 3])

with col1:
    expr_str = st.text_input("函数 f(x)", value="x**3 - 3*x", key="dp_expr")
    rng = st.slider("显示范围 ±", 2.0, 20.0, 4.0, key="dp_rng")
    cursor_x = st.slider("光标位置 x", -10.0, 10.0, 0.0, 0.1, key="dp_cursor")

try:
    expr, x = parse(expr_str)
    st.latex(rf"f(x) = {sp.latex(expr)}")
    st.latex(rf"f'(x) = {sp.latex(sp.diff(expr, x))}")

    fig = plot_derivative_pair(expr, (-rng, rng), cursor_x)
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    # 当前点数据
    x_sym = sp.Symbol('x')
    fx = float(expr.subs(x_sym, float(cursor_x)))
    dfx = float(sp.diff(expr, x_sym).subs(x_sym, float(cursor_x)))

    c1, c2, c3 = st.columns(3)
    c1.metric("x", f"{cursor_x:.2f}")
    c2.metric("f(x)", f"{fx:.4f}")
    c3.metric("f'(x)", f"{dfx:.4f}",
              delta="切线水平" if abs(dfx) < 1e-2 else None)

    st.divider()
    st.markdown("""
### 🔍 观察要点

1. **f'(x) = 0 的地方** → 下图穿过零线 → 上图出现**极值点**（山顶或谷底）
2. **f'(x) > 0** 的区间 → 下图在零线上方 → 上图**上升**
3. **f'(x) < 0** 的区间 → 下图在零线下方 → 上图**下降**
4. 拖动 **光标位置 x**，同步观察 f 与 f' 的瞬时对应关系

**试试这些函数：**
- `x**3 - 3*x`：两个极值点
- `sin(x)`：周期性极值
- `x**4 - 2*x**2`：拐点与极值
""")
except Exception as e:
    st.error(f"解析失败：{type(e).__name__}: {e}")