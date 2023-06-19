"""
总结整理所有重要功能模块的基类
"""

import streamlit as st


class BaseChatClass(object):
    """"""

    def __init__(self, driver):
        # 初始化session聊天模型等信息
        pass


class BaseMetaDataClass(object):
    """"""

    def __init__(self, driver):
        self.driver = driver


class BaseDataSourceClass(object):
    """"""

    def __init__(self, driver):
        self.driver = driver
