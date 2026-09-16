import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content.lessons import LESSONS

st.set_page_config(page_title="学习路径", page_icon="📚", layout="wide")
st.title("📚 学习路径")

titles = list(LESSONS.keys())
selected = st.sidebar.radio("选择章节", titles)

st.subheader(selected)
st.markdown(LESSONS[selected])

st.divider()
st.caption("完成阅读后，到 🔬 可视化实验室 或 🧮 分步求解器 实践一下。")