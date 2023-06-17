import streamlit as st

from helper import general_sidebar

# 页面设置
st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖', initial_sidebar_state="auto")

# 侧边栏设置
general_sidebar()

# 主页面内容
st.subheader("🧰 常用工具箱")
tap_sql, tap_regex = st.tabs(['📰 Text2SQL', '💬️ 正则表达式'])

with tap_sql:
    st.caption("敬请期待！！！")

with tap_regex:
    st.caption("敬请期待！！！")
