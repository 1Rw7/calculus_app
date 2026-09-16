import streamlit as st
import sympy as sp
import random
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.symbolic import parse
from core.database import add_mistake

st.set_page_config(page_title="练习测评", page_icon="✏️", layout="wide")
st.title("✏️ 练习测评")


# ---------- 题目生成器 ----------
def gen_power_question():
    n = random.randint(2, 6)
    a = random.randint(1, 5)
    question = f"求 d/dx[{a}*x^{n}]"
    x = sp.Symbol('x')
    correct = sp.diff(a * x**n, x)
    return question, correct, f"{a}*x**{n}"


def gen_sin_question():
    a = random.randint(1, 5)
    question = f"求 d/dx[sin({a}*x)]"
    x = sp.Symbol('x')
    correct = sp.diff(sp.sin(a * x), x)
    return question, correct, f"sin({a}*x)"


def gen_product_question():
    a = random.randint(1, 4)
    n = random.randint(1, 3)
    question = f"求 d/dx[x^{n} * exp({a}*x)]"
    x = sp.Symbol('x')
    correct = sp.diff(x**n * sp.exp(a * x), x)
    return question, correct, f"x**{n} * exp({a}*x)"


GENERATORS = [gen_power_question, gen_sin_question, gen_product_question]


# ---------- Session state 初始化 ----------
if "current_q" not in st.session_state:
    gen = random.choice(GENERATORS)
    q, c, e = gen()
    st.session_state.current_q = (q, c, e)
    st.session_state.answered = False

if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0


q, correct, e_str = st.session_state.current_q

st.markdown(f"### 题目：`{q}`")
st.caption("请输入导数表达式（如 `2*x`、`cos(x)`、`3*x**2`）")

user_input = st.text_input("你的答案：", key="user_ans")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("提交", type="primary"):
        if not user_input.strip():
            st.warning("请输入答案")
        else:
            try:
                user_expr, x = parse(user_input)
                diff = sp.simplify(user_expr - correct)
                st.session_state.total += 1
                if diff == 0:
                    st.success("✅ 正确！")
                    st.session_state.score += 1
                    st.session_state.answered = True
                else:
                    st.error("❌ 错误。正确答案：")
                    st.latex(sp.latex(correct))
                    add_mistake(
                        topic="求导",
                        question=q,
                        user_answer=user_input,
                        correct_answer=sp.latex(correct),
                    )
                    st.session_state.answered = True
            except Exception as ex:
                st.error(f"无法解析你的输入：{type(ex).__name__}: {ex}")

with col2:
    if st.button("下一题 🔄"):
        gen = random.choice(GENERATORS)
        q, c, e = gen()
        st.session_state.current_q = (q, c, e)
        st.session_state.answered = False
        st.rerun()

if st.session_state.total > 0:
    st.divider()
    st.metric(
        "得分",
        f"{st.session_state.score} / {st.session_state.total}",
        delta=f"正确率 {st.session_state.score / st.session_state.total * 100:.0f}%",
    )