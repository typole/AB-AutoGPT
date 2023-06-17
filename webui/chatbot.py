import random

from requests.exceptions import ChunkedEncodingError

from helper import *
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

import config

st.set_page_config(page_title='ChatBot', layout='wide', page_icon='🤖')

# button样式
button_css = '''
<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > 
div.block-container.css-z5fcl4.e1g8pov64 > div:nth-child(1) > div > div.css-ocqkz7.esravye3 > div.css-17xod8c.esravye1 > 
div:nth-child(1) > div > div.css-ocqkz7.esravye3 > div:nth-child(1) > div:nth-child(1) > div > div > div > button{
background-color:rgb(71 181 74);
border-color:rgb(166 220 255);
color: rgb(255 255 255);
};
</style>
<style>
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.e1g8pov65 > 
div.block-container.css-z5fcl4.e1g8pov64 > div:nth-child(1) > div > div.css-ocqkz7.esravye3 > div.css-17xod8c.esravye1 > 
div:nth-child(1) > div > div.css-ocqkz7.esravye3 > div:nth-child(2) > div:nth-child(1) > div > div > div > button{
background-color:rgb(231 105 105);
border-color:rgb(166 220 255);
color:rgb(255 255 255);
};
</style>
'''
st.markdown(button_css, unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key：[有默认值]", key="set_api_key", placeholder="点击输入")
    st.selectbox("大语言模型：[有默认值]", index=0, options=config.MODEL_OPTIONS, key="select_model")

    st.write("\n")
    st.write("\n")
    st.markdown('<a href="https://github.com/typole/AB-AutoGPT" target="_blank" rel="ChatGPT-Assistant">'
                '<img src="https://badgen.net/badge/icon/GitHub?icon=github&amp;label=AB-AutoGPT" alt="GitHub">'
                '</a>', unsafe_allow_html=True)

# 主页面内容
st.subheader("🤖 ChatBot[todo:语音输入]")

# 整体设置
c1, c2 = st.columns(2)
with c1:
    if "open_text_toolkit_value" in st.session_state:
        default = st.session_state["open_text_toolkit_value"]
    else:
        default = True
    st.checkbox("开启文本下的功能组件", value=default, key='open_text_toolkit',
                on_change=save_set, args=("open_text_toolkit",))
with c2:
    if "open_voice_toolkit_value" in st.session_state:
        default = st.session_state["open_voice_toolkit_value"]
    else:
        default = True
    st.checkbox("开启语音输入组件", value=default, key='open_voice_toolkit',
                on_change=save_set, args=('open_voice_toolkit',))
colored_header(label='', description='', color_name='blue-30')

# 初始化session聊天模型等信息
if "initial_settings" not in st.session_state:
    # 历史聊天窗口
    st.session_state["path"] = 'history_chats_file'
    st.session_state['history_chats'] = get_history_chats(st.session_state["path"])
    # ss参数初始化
    st.session_state['delete_dict'] = {}
    st.session_state['delete_count'] = 0
    st.session_state['voice_flag'] = ''
    st.session_state['user_voice_value'] = ''
    st.session_state['error_info'] = ''
    st.session_state["current_chat_index"] = 0
    st.session_state['user_input_content'] = ''
    # 读取全局设置
    if os.path.exists('./set.json'):
        with open('./set.json', 'r', encoding='utf-8') as f:
            data_set = json.load(f)
        for key, value in data_set.items():
            st.session_state[key] = value
    # 设置完成
    st.session_state["initial_settings"] = True

# 聊天窗口和对话历史
col_chat, col_history = st.columns([8, 3])

# 对话历史
with col_history:
    # 历史聊天记录
    expander = st.expander("📜 历史聊天", expanded=True)
    with expander:
        current_chat = st.radio(
            label='历史聊天窗口',
            format_func=lambda x: x.split('_')[0] if '_' in x else x,
            options=st.session_state['history_chats'],
            label_visibility='collapsed',
            index=st.session_state["current_chat_index"],
            key='current_chat' + st.session_state['history_chats'][st.session_state["current_chat_index"]],
            # on_change=current_chat_callback  # 此处不适合用回调，无法识别到窗口增减的变动
        )

    # 聊天记录管理
    c1, c2 = st.columns(2)
    create_chat_button = c1.button('新建', use_container_width=True, key='create_chat_button')
    if create_chat_button:
        create_chat_fun()
        st.experimental_rerun()

    delete_chat_button = c2.button('删除', use_container_width=True, key='delete_chat_button')
    if delete_chat_button:
        delete_chat_fun(current_chat=current_chat)
        st.experimental_rerun()

    # 重命名聊天窗口
    if ("set_chat_name" in st.session_state) and st.session_state['set_chat_name'] != '':
        reset_chat_name_fun(st.session_state['set_chat_name'], current_chat=current_chat)
        st.session_state['set_chat_name'] = ''
        st.experimental_rerun()
    st.text_input("设定窗口名称：", key="set_chat_name", placeholder="点击输入")

# 聊天窗口
with col_chat:
    # 聊天提交表单
    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_input = a.text_input(
            label="请输入:",
            placeholder="你想和我聊什么?",
            label_visibility="collapsed",
            key="user_input_text",
        )
        submitted = b.form_submit_button("Send", use_container_width=True)
    if submitted:
        st.session_state['user_input_content'] = user_input
        st.session_state['user_voice_value'] = ''
        st.experimental_rerun()

    # 加载数据
    current_chat = st.session_state[
        'current_chat' + st.session_state['history_chats'][st.session_state["current_chat_index"]]]
    if "history" + current_chat not in st.session_state:
        for key, value in load_data(st.session_state["path"], current_chat).items():
            if key == 'history':
                st.session_state[key + current_chat] = value
            else:
                for k, v in value.items():
                    st.session_state[k + current_chat + "value"] = v

    # 保证不同chat的页面层次一致，否则会导致自定义组件重新渲染
    container_show_messages = st.container()
    container_show_messages.write("")
    # 对话展示
    with container_show_messages:
        if st.session_state["history" + current_chat]:
            st.write(st.session_state)
            if openai_api_key and st.session_state['user_input_content']:
                st.session_state['user_input_content' + current_chat] = st.session_state['user_input_content']
                openai.api_key = openai_api_key
            else:
                st.session_state['user_input_content' + current_chat] = st.session_state['user_input_content']
                openai.api_key = st.secrets['OPENAI_API_KEY']

            for msg in st.session_state["history" + current_chat]:
                message(msg["content"], is_user=msg["role"] == "user", key='message' + current_chat + str(
                    random.random()))

            if st.session_state['user_input_content' + current_chat]:
                st.session_state["history" + current_chat].append({"role": "user", "content": user_input})
                message(user_input, is_user=True, key='message' + current_chat + str(random.random()))
                response = openai.ChatCompletion.create(model=st.session_state['select_model'],
                                                        messages=st.session_state["history" + current_chat])
                msg = response.choices[0].message
                st.session_state["history" + current_chat].append(msg)
                message(msg.content, key='message' + current_chat + str(random.random()))
        else:
            st.write(st.session_state)
            st.session_state["history" + current_chat] = [{"role": "assistant", "content": "有什么我能帮助您？"}]

    # # 核查是否有对话需要删除
    # if any(st.session_state['delete_dict'].values()):
    #     for key, value in st.session_state['delete_dict'].items():
    #         try:
    #             deleteCount = value.get("deleteCount")
    #         except AttributeError:
    #             deleteCount = None
    #         if deleteCount == st.session_state['delete_count']:
    #             delete_keys = key
    #             st.session_state['delete_count'] = deleteCount + 1
    #             delete_current_chat, idr = delete_keys.split('>')
    #             df_history_tem = pd.DataFrame(st.session_state["history" + delete_current_chat])
    #             df_history_tem.drop(index=df_history_tem.query("role=='user'").iloc[[int(idr)], :].index, inplace=True)
    #             df_history_tem.drop(index=df_history_tem.query("role=='assistant'").iloc[[int(idr)], :].index,
    #                                 inplace=True)
    #             st.session_state["history" + delete_current_chat] = df_history_tem.to_dict('records')
    #             # write_data(current_chat) TODO: 保存数据
    #             # st.experimental_rerun()
    #
    #
    # def input_callback():
    #     if st.session_state['user_input_area'] != "":
    #         # 修改窗口名称
    #         user_input_content = st.session_state['user_input_area']
    #         df_history = pd.DataFrame(st.session_state["history" + current_chat])
    #         # 没有修改过名称的话，第一次对话时修改名称
    #         if df_history.empty or len(df_history.query('role!="system"')) == 0:
    #             new_name = extract_chars(user_input_content, 18)
    #             reset_chat_name_fun(new_name, current_chat=current_chat)
    #
    #
    # # with st.form("input_form", clear_on_submit=True):
    # #     user_input = st.text_area("**输入：**", key="user_input_area",
    # #                               help="内容将以Markdown格式在页面展示，建议遵循相关语言规范，同样有利于GPT正确读取，例如："
    # #                                    "\n- 代码块写在三个反引号内，并标注语言类型"
    # #                                    "\n- 以英文冒号开头的内容或者正则表达式等写在单反引号内",
    # #                               value=st.session_state['user_voice_value'])
    # #     submitted = st.form_submit_button("确认提交", use_container_width=True, on_click=input_callback)
    # # if submitted:
    # #     st.session_state['user_input_content'] = user_input
    # #     st.session_state['user_voice_value'] = ''
    # #     st.experimental_rerun()
    #
    # # 输入内容展示
    # area_user_svg = st.empty()
    # area_user_content = st.empty()
    # # 回复展示
    # area_gpt_svg = st.empty()
    # area_gpt_content = st.empty()
    # # 报错展示
    # area_error = st.empty()

    # if st.session_state['user_input_content'] != '':
    #     if 'r' in st.session_state:
    #         st.session_state.pop("r")
    #         st.session_state[current_chat + 'report'] = ""
    #     st.session_state['pre_user_input_content'] = st.session_state['user_input_content']
    #     st.session_state['user_input_content'] = ''
    #
    #     # 临时展示
    #     show_each_message(st.session_state['pre_user_input_content'], 'user', 'tem',
    #                       [area_user_svg.markdown, area_user_content.markdown])
    #
    #     # 模型输入
    #     history_need_input, paras_need_input = get_model_input(current_chat=current_chat)
    #     # 调用接口
    #     with st.spinner("🤔"):
    #         try:
    #             if apikey := st.session_state['set_api_key']:
    #                 openai.api_key = apikey
    #             # 配置临时apikey，此时不会留存聊天记录，适合公开使用
    #             elif "apikey_tem" in st.secrets:
    #                 openai.api_key = st.secrets["apikey_tem"]
    #             # 注：当st.secrets中配置apikey后将会留存聊天记录，即使未使用此apikey
    #             else:
    #                 openai.api_key = st.secrets["OPENAI_API_KEY"]
    #             r = openai.ChatCompletion.create(model=st.session_state["select_model"], messages=history_need_input,
    #                                              stream=True,
    #                                              **paras_need_input)
    #         except (FileNotFoundError, KeyError):
    #             area_error.error("缺失 OpenAI API Key，请在复制项目后配置Secrets，或者在模型选项中进行临时配置。"
    #                              "详情见[项目仓库](https://github.com/PierXuY/ChatGPT-Assistant)。")
    #         except openai.error.AuthenticationError:
    #             area_error.error("无效的 OpenAI API Key。")
    #         except openai.error.APIConnectionError as e:
    #             area_error.error("连接超时，请重试。报错：   \n" + str(e.args[0]))
    #         except openai.error.InvalidRequestError as e:
    #             area_error.error("无效的请求，请重试。报错：   \n" + str(e.args[0]))
    #         except openai.error.RateLimitError as e:
    #             area_error.error("请求受限。报错：   \n" + str(e.args[0]))
    #         else:
    #             st.session_state["chat_of_r"] = current_chat
    #             st.session_state["r"] = r
    #             st.experimental_rerun()

    # if ("r" in st.session_state) and (current_chat == st.session_state["chat_of_r"]):
    #     if current_chat + 'report' not in st.session_state:
    #         st.session_state[current_chat + 'report'] = ""
    #     try:
    #         for e in st.session_state["r"]:
    #             if "content" in e["choices"][0]["delta"]:
    #                 st.session_state[current_chat + 'report'] += e["choices"][0]["delta"]["content"]
    #                 show_each_message(st.session_state['pre_user_input_content'], 'user', 'tem',
    #                                   [area_user_svg.markdown, area_user_content.markdown])
    #                 show_each_message(st.session_state[current_chat + 'report'], 'assistant', 'tem',
    #                                   [area_gpt_svg.markdown, area_gpt_content.markdown])
    #     except ChunkedEncodingError:
    #         area_error.error("网络状况不佳，请刷新页面重试。")
    #     # 应对stop情形
    #     except Exception:
    #         pass
    #     else:
    #         # 保存内容
    #         st.session_state["history" + current_chat].append(
    #             {"role": "user", "content": st.session_state['pre_user_input_content']})
    #         st.session_state["history" + current_chat].append(
    #             {"role": "assistant", "content": st.session_state[current_chat + 'report']})
    #         # write_data(current_chat)  TODO: 保存聊天记录
    #     # 用户在网页点击stop时，ss某些情形下会暂时为空
    #     if current_chat + 'report' in st.session_state:
    #         st.session_state.pop(current_chat + 'report')
    #     if 'r' in st.session_state:
    #         st.session_state.pop("r")
    #         st.experimental_rerun()

    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant", "content": "有什么我能帮助您？"}]
    #
    # for msg in st.session_state.messages:
    #     message(msg["content"], is_user=msg["role"] == "user")
    #
    # if user_input and openai_api_key:
    #     openai.api_key = openai_api_key
    # else:
    #     openai.api_key = st.secrets['OPENAI_API_KEY']
    #
    # if user_input:
    #     st.session_state.messages.append({"role": "user", "content": user_input})
    #     message(user_input, is_user=True)
    #     response = openai.ChatCompletion.create(model=st.session_state['select_model'],
    #                                             messages=st.session_state.messages)
    #     msg = response.choices[0].message
    #     st.session_state.messages.append(msg)
    #     message(msg.content)
