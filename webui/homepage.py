"""
首页
- 平台介绍信息
"""
import streamlit as st
from helper import general_sidebar

from st_pages import Page, show_pages

st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖')

# # online
# show_pages(
#     [
#         Page("webui/homepage.py", "首页", "🏠"),
#         Page("webui/chatbot.py", "聊天机器人", "🤖"),
#         Page("webui/data_analysis.py", "数据分析师", "💹"),
#         Page("webui/data_engineer.py", "数据工程师", "⚙️"),
#         Page("webui/ml_precess.py", "机器学习流程", "🏗️"),
#         Page("webui/tools.py", "常用工具箱", "🧰")
#     ]
# )

# local
show_pages(
    [
        Page("homepage.py", "首页", "🏠"),
        Page("chatbot.py", "聊天机器人", "🤖"),
        Page("data_analysis.py", "数据分析师", "💹"),
        Page("data_engineer.py", "数据工程师", "⚙️"),
        Page("ml_precess.py", "机器学习流程", "🏗️"),
        Page("tools.py", "常用工具箱", "🧰")
    ]
)


# 侧边栏设置
general_sidebar()

# 主页面设置
st.markdown("# AB-AutoGPT")
st.caption("[0-1] 面向AI/BigData从业者的AutoGPT")
st.markdown("""<hr style="height:6px;border:none;border-top:6px groove skyblue;" />""", unsafe_allow_html=True)

st.markdown(
    """
    ### 前言
    1. 愿景：让AI应用替我们更好的工作，让人类享受更好的生活。  
    2. AI应用-成长之路：【0-1】面向AI/BigData从业者的AutoGPT  
    3. GitHub：https://github.com/typole/AB-AutoGPT  
    4. 应用网址：https://ab-autogpt.streamlit.app/


    \n\n### AB-AutoGPT初衷和成长计划：
    \n数据从业者实现自身价值最大的难点是过度依赖业务价值生存，业务和数据又是比较独立的职业规划，虽然说是双赢，但在公司的真实情况又比较对立的存在。  
    \n职场中最大的痛点，是我们很容易做着做着就成为业务的工具人，今天业务需要我们帮忙清洗个数，明天约我让我们帮忙提个数，后天也可能帮业务做个指标，最好的情况下也就和业务共同实现报表或可视化看板。  
    \n这些工作也不是说没有意义，只是不够了解数据价值的业务方，很快就会把我们当成提数工具人、做报表和看板的工具人。慢慢的消磨了数据从业者“数据驱动社会发展”的伟大抱负和愿景，开始怀疑自己的职业价值，职业规划也会越来越偏离。  
    \nAutoGPT生成式的问世，让我有了更大的抱负和愿景，解放我们的双手和时间，让AB-AutoGPT帮助我们实现大量的数据加工处理、数据浅层分析的工作量，更多的时间去挖掘数据价值，投身于业务的发展和商业价值的思考中。  
    \n这是一个探索性的项目计划，需要很长的时间从工作的真实痛点案例中捕捉灵感，实现伟大的愿景和目标。当然也有可能，这就是个不切实际的想法，最终寥寥收场。  
    \n但我相信，愿景是美好的，过程也会是美好的，即使再不济，最终也能差强人意吧。  
    \n人人都能玩转数据，人人都是数据分析师！！！  
    \n如果您有任何产品或技术方面的建议，欢迎评论区交流或加入企微沟通群，一起创造美好的职场未来。  
    """
)
