import streamlit as st

from helper import general_sidebar

# 页面设置
st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖', initial_sidebar_state="auto")

# 侧边栏设置
general_sidebar()

# 主页面内容
st.subheader("⚙️ 数据工程开发")
st.caption("敬请期待！！！")
tap_index, tap_measure, tap_explore, tap_schema, tap_chart = st.tabs(
    ['1️⃣ 业务指标', '2️⃣ 指标量化', '3️⃣ 数据探索', '4️⃣ 数据建模', '5️⃣ 数据可视化'])

with tap_index:
    st.caption("敬请期待！！！")

with tap_measure:
    st.caption("敬请期待！！！")

with tap_explore:
    st.caption("敬请期待！！！")

with tap_schema:
    st.caption("敬请期待！！！")
