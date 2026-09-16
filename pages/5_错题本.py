import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_mistakes, delete_mistake, clear_all

st.set_page_config(page_title="错题本", page_icon="📕", layout="wide")
st.title("📕 错题本")

rows = get_mistakes()

if not rows:
    st.info("暂无错题。去 ✏️ 练习测评 做几道题吧！")
else:
    df = pd.DataFrame(
        rows,
        columns=["ID", "知识点", "题目", "你的答案", "正确答案", "时间"],
    )
    st.dataframe(
        df[["知识点", "题目", "你的答案", "正确答案", "时间"]],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("管理")
    c1, c2 = st.columns(2)
    with c1:
        del_id = st.number_input("删除某条（输入 ID）", min_value=0, step=1)
        if st.button("删除"):
            delete_mistake(del_id)
            st.success(f"已删除 ID={del_id}")
            st.rerun()
    with c2:
        if st.button("⚠️ 清空全部"):
            clear_all()
            st.success("已清空")
            st.rerun()

    st.divider()
    st.subheader("按知识点统计")
    st.bar_chart(df["知识点"].value_counts())