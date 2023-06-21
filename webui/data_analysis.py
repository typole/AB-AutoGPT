import openai
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

import config
import helper

st.set_page_config(page_title='人人都是数据分析师', layout='wide', page_icon='🤖')

# 侧边栏配置
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key：[有默认值]", key="set_api_key", placeholder="点击输入")
    st.selectbox("大语言模型：", index=0, options=config.MODEL_OPTIONS, key="select_model")
    # 加载数据源
    st.write("\n")
    st.markdown("### 🕋 选择数据源")
    st.selectbox("数据源加载：", index=0, options=config.DATA_SOURCES, key="select_data_source")
    if st.session_state['select_data_source'] == '本地文件[CSV]':
        data_lst, metadata_lst = helper.load_offline_file()
    elif st.session_state['select_data_source'] == 'MySQL':
        # 请配置MySQL数据库连接
        pass
    else:
        assert False, "数据源加载失败！"
    st.write("---")
    st.markdown('<a href="https://github.com/typole/AB-AutoGPT" target="_blank" rel="ChatGPT-Assistant">'
                '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=AB-AutoGPT" alt="GitHub">'
                '</a>', unsafe_allow_html=True)

# 主页面内容
st.subheader("💹 人人都是数据分析师")
st.caption("实战全流程：业务指标 → 指标量化 → 数据探索 → 数据建模 → 数据可视化 → 观点输出 → 业务指标 → ...")

tap_chat, tap_example, tap_meta, tap_chart, tap_methodology = st.tabs(
    ['👆 数据探索', '👉 数据示例', '👇 元数据', '👉 数据可视化', '👊 分析方法论'])
with tap_chat:
    if not data_lst:
        st.caption("请配置数据源，并加载数据！")
    else:
        st.write("数据源已加载！开始你的数据探索之旅吧！")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "有什么我能帮助您？"}]

    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_input = a.text_input(
            label="请输入:",
            placeholder="你想和我聊什么?",
            label_visibility="collapsed",
        )
        b.form_submit_button("Send", use_container_width=True)

    for msg in st.session_state.messages:
        colored_header(label='', description='', color_name='blue-30')
        message(msg["content"], is_user=msg["role"] == "user")

    if openai_api_key:
        openai.api_key = openai_api_key
    else:
        openai.api_key = st.secrets['OPENAI_API_KEY']

    if user_input and data_lst != []:
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)
        agent = helper.built_agent_llm(data_lst)
        response = agent.run(user_input)
        st.session_state.messages.append(response)
        message(response)
    else:
        st.caption("请配置数据源，并加载数据！")

with tap_example:
    if data_lst:
        option = st.selectbox("选择数据对象：", index=0, options=metadata_lst, key="select_metadata_example")
        for idx in range(len(metadata_lst)):
            if metadata_lst[idx] == option:
                st.data_editor(data_lst[idx], height=600)
    else:
        st.caption("请配置数据源，并加载数据！")

with tap_meta:
    if data_lst:
        option = st.selectbox("选择数据对象：", index=0, options=metadata_lst, key="select_metadata_meta")
        for idx in range(len(metadata_lst)):
            if metadata_lst[idx] == option:
                st.markdown("#### 数据统计")
                st.data_editor(data_lst[idx].describe(), height=600)
    else:
        st.caption("请配置数据源，并加载数据！")

with tap_chart:
    if not data_lst:
        st.caption("请配置数据源，并加载数据！")
    else:
        st.write("敬请期待！")

with tap_methodology:
    st.caption("敬请期待！")
