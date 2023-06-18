"""
总结整理所有重要功能模块的基类
"""

import streamlit as st


class BaseChatClass(object):
    """"""

    def __init__(self, driver):
        # 初始化session聊天模型等信息
        if "initial_settings" not in st.session_state:
            # 历史聊天窗口
            st.session_state["path"] = 'history_chats_file'
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


class BaseMetaDataClass(object):
    """"""

    def __init__(self, driver):
        self.driver = driver


class BaseDataSourceClass(object):
    """"""

    def __init__(self, driver):
        self.driver = driver
