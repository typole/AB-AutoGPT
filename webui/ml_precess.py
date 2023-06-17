import streamlit as st

from helper import general_sidebar

# 页面设置
st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖', initial_sidebar_state="auto")

# 侧边栏设置
general_sidebar()

st.caption("敬请期待！！！")
