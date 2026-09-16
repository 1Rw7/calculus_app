import streamlit as st
import sympy as sp
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from viz.surface3d import plot_surface_3d

st.set_page_config(page_title="3D 曲面与偏导", page_icon="🏔️", layout="wide")
st.title("🏔️ 3D 曲面与偏导数")
st.caption("从一元微积分走进多元世界 —— 切平面如何『贴合』曲面？")

col1, col2 = st.columns([1, 4])

with col1:
    expr_str = st.text_input("z = f(x, y)", value="x**2 + y**2", key="s3_expr")
    x0 = st.slider("切点 x₀", -3.0, 3.0, 0.5, 0.1, key="s3_x0")
    y0 = st.slider("切点 y₀", -3.0, 3.0, 0.5, 0.1, key="s3_y0")
    rng = st.slider("显示范围 ±", 1.0, 6.0, 3.0, key="s3_rng")
    grid_n = st.slider("网格密度", 20, 80, 40, key="s3_n")

try:
    x, y = sp.symbols('x y')
    expr = sp.sympify(expr_str, locals={'x': x, 'y': y,
                                         'sin': sp.sin, 'cos': sp.cos,
                                         'exp': sp.exp, 'log': sp.log,
                                         'sqrt': sp.sqrt, 'pi': sp.pi})

    st.latex(rf"f(x, y) = {sp.latex(expr)}")
    fx = sp.diff(expr, x)
    fy = sp.diff(expr, y)
    st.latex(rf"\frac{{\partial f}}{{\partial x}} = {sp.latex(fx)}")
    st.latex(rf"\frac{{\partial f}}{{\partial y}} = {sp.latex(fy)}")

    fig, f0, fx_val, fy_val = plot_surface_3d(
        expr, x0, y0, (-rng, rng), (-rng, rng), grid_n
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader(f"切点 ({x0:.2f}, {y0:.2f}) 处的信息")
    c1, c2, c3 = st.columns(3)
    c1.metric("f(x₀, y₀)", f"{f0:.4f}")
    c2.metric("∂f/∂x", f"{fx_val:.4f}")
    c3.metric("∂f/∂y", f"{fy_val:.4f}")

    st.latex(
        rf"z = {f0:.3f} + {fx_val:.3f}(x - {x0:.2f}) + {fy_val:.3f}(y - {y0:.2f})"
    )

    st.divider()
    st.markdown("""
### 🔍 观察要点

- **偏导数 ∂f/∂x** = 固定 y，沿 x 方向的斜率（切平面在 x 方向的"倾斜度"）
- **偏导数 ∂f/∂y** = 固定 x，沿 y 方向的斜率
- **切平面** 由两个偏导共同决定，是曲面的局部线性近似（就像一元的切线）

**试试这些曲面：**
- `x**2 + y**2`：抛物面（碗形），切平面在原点水平
- `x**2 - y**2`：马鞍面（鞍点，一个方向上升一个方向下降）
- `sin(x) * cos(y)`：波浪面
- `exp(-(x**2 + y**2))`：钟形（高斯）
- `sqrt(x**2 + y**2)`：圆锥面（原点处不可导，试试切点靠近原点）

**🖱️ 鼠标操作**：
- 左键拖动：旋转视角
- 滚轮：缩放
- 右键拖动：平移
""")
except Exception as e:
    st.error(f"解析失败：{type(e).__name__}: {e}")