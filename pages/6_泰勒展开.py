import streamlit as st
import sympy as sp
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.symbolic import parse
from viz.taylor_plot import plot_taylor

st.set_page_config(page_title="泰勒展开", page_icon="🎢", layout="wide")
st.title("🎢 泰勒展开可视化")
st.caption("用多项式逐步逼近函数 —— 微积分最优雅的思想之一")

col1, col2 = st.columns([1, 3])

with col1:
    expr_str = st.text_input("函数 f(x)", value="sin(x)", key="tl_expr")
    n = st.slider("泰勒多项式阶数 n", 1, 15, 3, key="tl_n")
    around = st.slider("展开点 a", -3.0, 3.0, 0.0, 0.5, key="tl_a")
    rng = st.slider("显示范围 ±", 2.0, 20.0, 6.0, key="tl_rng")

try:
    expr, x = parse(expr_str)
    st.latex(rf"f(x) = {sp.latex(expr)}")

    fig, taylor_expr = plot_taylor(expr, n, around, (-rng, rng))
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("当前泰勒多项式")
    st.latex(rf"P_{{{n}}}(x) = {sp.latex(taylor_expr)}")

    st.divider()
    st.markdown(f"""
### 🧪 观察建议

拖动 **阶数 n**，看橙色虚线如何越来越贴合蓝色曲线：

- 在**展开点 a 附近**，多项式逼近得特别好（这正是泰勒展开的本意）
- 离 a 越远，越需要更高阶才能逼近
- n 越大，"贴合区间"越宽

**试试这些函数：**
- `sin(x)` 在 a=0：观察奇偶项规律
- `exp(x)` 在 a=0：每阶都在贡献
- `log(1+x)` 在 a=0：只在 x > -1 收敛
- `1/(1-x)` 在 a=0：等比级数
""")
except Exception as e:
    st.error(f"解析失败：{type(e).__name__}: {e}")