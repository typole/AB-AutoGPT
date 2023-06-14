"""
首页【Chatbot悬浮窗口】
1. 数据流转 -> 数据应用场景
2. 各功能模块介绍和跳转
3. 侧边栏：介绍、子功能模块【筛选器】
"""
import os
from io import StringIO

import pandas as pd
import streamlit as st
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

from custom import *

st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖')
# 自定义元素样式
st.markdown(css_code, unsafe_allow_html=True)

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# 侧边栏内容
with st.sidebar:
    st.markdown("# 🤖 AB-AutoGPT")
    st.markdown("### 【0-1】面向AI/BigData从业者的AutoGPT！")
    st.write("---")

    st.write("\n")
    st.text_input("OpenAI API key：", key="set_chat_name", placeholder="点击输入")
    st.selectbox("选择模型：", index=0, options=['gpt-3.5-turbo', 'gpt-4'], key="select_model")
    st.write("\n")
    st.caption("""
    - 双击页面可直接定位输入栏
    - Ctrl + Enter 可快捷提交问题
    """)
    st.markdown('<a href="https://github.com/typole/AB-AutoGPT" target="_blank" rel="ChatGPT-Assistant">'
                '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=AB-AutoGPT" alt="GitHub">'
                '</a>', unsafe_allow_html=True)

    st.write("\n")
    st.write("---")
    st.markdown("### 📊 选择数据源")
    st.write("\n")
    st.selectbox("数据源加载：", index=0, options=['本地文件[CSV]', 'MySQL', 'Hive', 'Doris'], key="select_data_source")
    if st.session_state['select_data_source'] == '本地文件[CSV]':
        def load_offline_csvfile():
            os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                # To read file as bytes:
                bytes_data = uploaded_file.getvalue()

                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

                # To read file as string:
                string_data = stringio.read()

                # Can be used wherever a "file-like" object is accepted:
                return pd.read_csv(uploaded_file)


        data_obj = load_offline_csvfile()

st.write("\n")
st.header('AB-AutoGPT')
tap_example, tap_interactive = st.tabs(['📰 数据示例', '💬️ 数据交互'])
with tap_example:
    if data_obj is not None:
        st.write(data_obj)
    else:
        st.write("请先选择数据源！")

with tap_interactive:
    # 将模型选择为：model_name="gpt-3.5-turbo"
    if data_obj is not None:
        st.write("数据源已加载！开始你的数据探索之旅吧！")
        # Generate empty lists for generated and past.
        # generated stores AI generated responses
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["我是 AB-AutoGPT, 有什么能够帮助你呢?"]
        # past stores User's questions
        if 'past' not in st.session_state:
            st.session_state['past'] = ['哈喽!']

        # Layout of input/response containers
        input_container = st.container()
        colored_header(label='', description='', color_name='blue-30')
        response_container = st.container()


        # User input
        # Function for taking user provided prompt as input
        def get_text():
            input_text = st.text_input("请输入你的问题: ", "", key="input")
            return input_text


        # Applying the user input box
        with input_container:
            user_input = get_text()


        # Response output
        # Function for taking user prompt as input followed by producing AI generated responses
        def generate_response(prompt):
            agent = create_pandas_dataframe_agent(OpenAI(model_name="gpt-3.5-turbo", temperature=0), data_obj,
                                                  verbose=True)
            response = agent.run(prompt)
            return response


        # Conditional display of AI generated responses as a function of user provided prompts
        with response_container:
            if user_input:
                response = generate_response(user_input)
                st.session_state.past.append(user_input)
                st.session_state.generated.append(response)

            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))

    else:
        st.write("请先选择数据源！")
