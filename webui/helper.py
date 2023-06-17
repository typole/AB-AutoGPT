import json
import os
import re
import uuid

import openai
import streamlit as st
import pandas as pd
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent

from custom import *
import copy
import io


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


# ----------------------------------------------------------------
def get_history_chats(path: str) -> list:
    if "apikey" in st.secrets:
        if not os.path.exists(path):
            os.makedirs(path)
        files = [f for f in os.listdir(f'./{path}') if f.endswith('.json')]
        files_with_time = [(f, os.stat(f'./{path}/' + f).st_ctime) for f in files]
        sorted_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)
        chat_names = [os.path.splitext(f[0])[0] for f in sorted_files]
        if len(chat_names) == 0:
            chat_names.append('New Chat_' + str(uuid.uuid4()))
    else:
        chat_names = ['New Chat_' + str(uuid.uuid4())]
    return chat_names


def save_data(path: str, file_name: str, history: list, paras: dict, contexts: dict, **kwargs):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"./{path}/{file_name}.json", 'w', encoding='utf-8') as f:
        json.dump({"history": history, "paras": paras, "contexts": contexts, **kwargs}, f)


def remove_data(path: str, chat_name: str):
    try:
        os.remove(f"./{path}/{chat_name}.json")
    except FileNotFoundError:
        pass
    # 清除缓存
    try:
        st.session_state.pop('history' + chat_name)
        for item in ["context_select", "context_input", "context_level", *initial_content_all['paras']]:
            st.session_state.pop(item + chat_name + "value")
    except KeyError:
        pass


def load_data(path: str, file_name: str) -> dict:
    try:
        with open(f"./{path}/{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        content = copy.deepcopy(initial_content_all)
        if "apikey" in st.secrets:
            with open(f"./{path}/{file_name}.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(content))
        return content


def show_each_message(message: str, role: str, idr: str, area=None):
    if area is None:
        area = [st.markdown] * 2
    if role == 'user':
        icon = user_svg
        name = user_name
        background_color = user_background_color
        data_idr = idr + "_user"
        class_name = 'user'
    else:
        icon = gpt_svg
        name = gpt_name
        background_color = gpt_background_color
        data_idr = idr + "_assistant"
        class_name = 'assistant'
    message = url_correction(message)
    area[0](f"\n<div class='avatar'>{icon}<h2>{name}：</h2></div>", unsafe_allow_html=True)
    area[1](
        f"""<div class='content-div {class_name}' data-idr='{data_idr}' style='background-color: {background_color};'>\n\n{message}""",
        unsafe_allow_html=True)


# def show_messages(current_chat: str, messages: list):
#     id_role = 0
#     id_assistant = 0
#     for each in messages:
#         if each["role"] == "user":
#             idr = id_role
#             id_role += 1
#         elif each["role"] == "assistant":
#             idr = id_assistant
#             id_assistant += 1
#         else:
#             idr = False
#         if idr is not False:
#             show_each_message(each["content"], each["role"], str(idr))
#             if "open_text_toolkit_value" not in st.session_state or st.session_state["open_text_toolkit_value"]:
#                 st.session_state['delete_dict'][current_chat + ">" + str(idr)] = text_toolkit(
#                     data_idr=str(idr) + '_' + each["role"])
#         if each["role"] == "assistant":
#             st.write("---")


# 根据context_level提取history
def get_history_input(history: list, level: int) -> list:
    if level != 0 and history:
        df_input = pd.DataFrame(history).query('role!="system"')
        df_input = df_input[-level * 2:]
        res = df_input.to_dict('records')
    else:
        res = []
    return res


# 去除#号右边的空格
# def remove_hashtag_right__space(text: str) -> str:
#     text = re.sub(r"(#+)\s*", r"\1", text)
#     return text


# 提取文本
def extract_chars(text: str, num: int) -> str:
    char_num = 0
    chars = ''
    for char in text:
        # 汉字算两个字符
        if '\u4e00' <= char <= '\u9fff':
            char_num += 2
        else:
            char_num += 1
        chars += char
        if char_num >= num:
            break
    return chars


@st.cache_data(max_entries=20, show_spinner=False)
def download_history(history: list):
    md_text = ""
    for msg in history:
        if msg['role'] == 'user':
            md_text += f'## {user_name}：\n{msg["content"]}\n'
        elif msg['role'] == 'assistant':
            md_text += f'## {gpt_name}：\n{msg["content"]}\n'
    output = io.BytesIO()
    output.write(md_text.encode('utf-8'))
    output.seek(0)
    return output


def filename_correction(filename: str) -> str:
    pattern = r'[^\w\.-]'
    filename = re.sub(pattern, '', filename)
    return filename


def url_correction(text: str) -> str:
    pattern = r'((?:http[s]?://|www\.)(?:[a-zA-Z0-9]|[$-_\~#!])+)'
    text = re.sub(pattern, r' \g<1> ', text)
    return text


# st的markdown会错误渲染英文引号加英文字符，例如 :abc
# def colon_correction(text):
#     pattern = r':[a-zA-Z]'
#     if re.search(pattern, text):
#         text = text.replace(":", "&#58;")
#         pattern = r'`([^`]*)&#58;([^`]*)`|```([^`]*)&#58;([^`]*)```'
#         text = re.sub(pattern, lambda m: m.group(0).replace('&#58;', ':') if '&#58;' in m.group(0) else m.group(0),
#                       text)
#     return text

# 数据写入文件
def write_data(current_chat):
    if "apikey" in st.secrets:
        st.session_state["paras"] = {
            "temperature": st.session_state["temperature" + current_chat],
            "top_p": st.session_state["top_p" + current_chat],
            "presence_penalty": st.session_state["presence_penalty" + current_chat],
            "frequency_penalty": st.session_state["frequency_penalty" + current_chat],
        }
        st.session_state["contexts"] = {
            "context_select": st.session_state["context_select" + current_chat],
            "context_input": st.session_state["context_input" + current_chat],
            "context_level": st.session_state["context_level" + current_chat],
        }
        save_data(st.session_state["path"], current_chat, st.session_state["history" + current_chat],
                  st.session_state["paras"], st.session_state["contexts"])


def reset_chat_name_fun(chat_name, current_chat):
    chat_name = chat_name + '_' + str(uuid.uuid4())
    new_name = filename_correction(chat_name)
    current_chat_index = st.session_state['history_chats'].index(current_chat)
    st.session_state['history_chats'][current_chat_index] = new_name
    st.session_state["current_chat_index"] = current_chat_index
    # 写入新文件
    write_data(new_name)
    # 转移数据
    st.session_state['history' + new_name] = st.session_state['history' + current_chat]
    for item in ["context_select", "context_input", "context_level", *initial_content_all['paras']]:
        st.session_state[item + new_name + "value"] = st.session_state[item + current_chat + "value"]
    remove_data(st.session_state["path"], current_chat)


def create_chat_fun():
    st.session_state['history_chats'] = ['New Chat_' + str(uuid.uuid4())] + st.session_state['history_chats']
    st.session_state["current_chat_index"] = 0


def delete_chat_fun(current_chat):
    if len(st.session_state['history_chats']) == 1:
        chat_init = 'New Chat_' + str(uuid.uuid4())
        st.session_state['history_chats'].append(chat_init)
    pre_chat_index = st.session_state['history_chats'].index(current_chat)
    if pre_chat_index > 0:
        st.session_state["current_chat_index"] = st.session_state['history_chats'].index(current_chat) - 1
    else:
        st.session_state["current_chat_index"] = 0
    st.session_state['history_chats'].remove(current_chat)
    remove_data(st.session_state["path"], current_chat)
