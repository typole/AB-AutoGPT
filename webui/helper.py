import os
import openai
import streamlit as st
import pandas as pd
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent


def load_offline_file():
    # 加载离线数据，支持csv、excel
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_type = os.path.splitext(uploaded_file.name)[1]
        if file_type == '.csv':
            df = pd.read_csv(uploaded_file)
        elif file_type == '.xlsx':
            df = pd.read_excel(uploaded_file)
        else:
            assert False, "不支持的文件格式"
        return df


def general_sidebar():
    # 通用侧边栏
    with st.sidebar:
        # 侧边栏标题
        st.markdown("# AB-AutoGPT")
        st.caption("[0-1]面向AI/BigData从业者的AutoGPT")

        st.write("\n")
        st.write("\n")
        st.markdown('<a href="https://github.com/typole/AB-AutoGPT" target="_blank" rel="ChatGPT-Assistant">'
                    '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=AB-AutoGPT" alt="GitHub">'
                    '</a>', unsafe_allow_html=True)


def built_agent_llm(df):
    """构建LLM Agent"""
    agent = create_pandas_dataframe_agent(OpenAI(model_name=st.session_state['select_model'], temperature=0),
                                          df, verbose=True)
    return agent


def _built_chat_llm(messages):
    """构建LLM Agent"""
    model = openai.ChatCompletion.create(model=st.session_state['select_model'], messages=messages)
    return model
