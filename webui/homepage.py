"""
首页
- 平台介绍信息
"""
import streamlit as st
from helper import general_sidebar

from st_pages import Page, show_pages

st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖')

show_pages(
    [
        Page("webui/homepage.py", "首页", "icon/首页.ico"),
        Page("webui/chatbot.py", "聊天机器人", "🤖"),
        Page("webui/data_analysis.py", "数据分析师", "💹"),
        Page("webui/data_engineer.py", "数据工程师", "📄"),
        Page("webui/ml_precess.py", "文本生成SQL", "🏗️"),
        Page("webui/text_to_sql.py", "机器学习流程", "⏳")
    ]
)

# 侧边栏设置
general_sidebar()

# 主页面设置
st.markdown("# AB-AutoGPT")
st.caption("[0-1] 面向AI/BigData从业者的AutoGPT")
st.markdown("""<hr style="height:6px;border:none;border-top:6px groove skyblue;" />""", unsafe_allow_html=True)

st.markdown("## 🤖 平台介绍")
