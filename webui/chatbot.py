import openai
import streamlit as st
from streamlit_chat import message
import config

st.set_page_config(page_title='ChatBot', layout='wide', page_icon='🤖')

# 侧边栏配置
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key：[有默认值]", key="set_api_key", placeholder="点击输入")
    st.selectbox("大语言模型：", index=0, options=config.MODEL_OPTIONS, key="select_model")
    st.markdown('<a href="https://github.com/typole/AB-AutoGPT" target="_blank" rel="ChatGPT-Assistant">'
                '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=AB-AutoGPT" alt="GitHub">'
                '</a>', unsafe_allow_html=True)

# 主页面内容
st.title("🤖 ChatBot[TODO:语音输入]")
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
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and openai_api_key:
    openai.api_key = openai_api_key
else:
    openai.api_key = st.secrets['OPENAI_API_KEY']

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    response = openai.ChatCompletion.create(model=st.session_state['select_model'], messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
