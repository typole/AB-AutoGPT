import streamlit as st

from helper import general_sidebar

# 页面设置
st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖', initial_sidebar_state="auto")

# 侧边栏设置
general_sidebar()

# 主页面内容
st.subheader("🏗️ 机器学习流程")
st.caption("敬请期待！！！")
tap_preparation, tap_clean, tap_preprocess, tap_feature, tap_tuning, tap_fusion, tap_validation, tap_persistence = st.tabs(
    ['📰 数据准备', '💬️ 数据清洗', '💬️ 数据预处理', '特征工程', '💬️ 模型调优', '💬️模型融合', '💬️ 模型验证', '💬️模型持久化'])

with tap_preparation:
    st.caption("敬请期待！！！")

with tap_clean:
    st.caption("敬请期待！！！")

with tap_preprocess:
    st.caption("敬请期待！！！")

with tap_feature:
    st.caption("敬请期待！！！")

with tap_tuning:
    st.caption("敬请期待！！！")

with tap_fusion:
    st.caption("敬请期待！！！")

with tap_validation:
    st.caption("敬请期待！！！")

with tap_persistence:
    st.caption("敬请期待！！！")
