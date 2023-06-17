"""
首页
- 平台介绍信息
"""
import streamlit as st
from helper import general_sidebar


from st_pages import show_pages_from_config

st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖')
show_pages_from_config()

# 侧边栏设置
general_sidebar()

# 主页面设置
st.markdown("# AB-AutoGPT")
st.caption("[0-1] 面向AI/BigData从业者的AutoGPT")
st.markdown("""<hr style="height:6px;border:none;border-top:6px groove skyblue;" />""", unsafe_allow_html=True)

st.markdown("## 🤖 平台介绍")
