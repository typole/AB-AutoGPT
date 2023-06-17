"""
首页【Chatbot悬浮窗口】
1. 数据流转 -> 数据应用场景
2. 各功能模块介绍和跳转
3. 侧边栏：介绍、子功能模块【筛选器】
"""

from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

from config import *
from webui.ab_pages.helper import *
from custom import *

# 页面设置
st.set_page_config(page_title='AB-AutoGPT', layout='wide', page_icon='🤖', initial_sidebar_state="auto")
# 自定义元素样式
st.markdown(css_code, unsafe_allow_html=True)

# 侧边栏设置
with st.sidebar:
    # 侧边栏标题
    st.markdown("# 🤖 AB-AutoGPT")
    st.caption("·【0-1】面向AI/BigData从业者的AutoGPT！")
    st.write("---")

    # API-KEY和模型选择
    st.write("\n")
    st.text_input("OpenAI API key：[有默认值]", key="set_api_key", placeholder="点击输入")
    st.selectbox("选择模型：", index=0, options=MODEL_OPTIONS, key="select_model")
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

    # 数据源加载
    st.markdown("### 📊 选择数据源")
    st.write("\n")
    st.selectbox("数据源加载：", index=0, options=DATA_SOURCES, key="select_data_source")
    if st.session_state['select_data_source'] == '本地文件[CSV]':
        data_obj = load_offline_file()
    elif st.session_state['select_data_source'] == 'MySQL':
        # 请配置MySQL数据库连接
        pass
    else:
        assert False, "数据源加载失败！"

# 主页面设置
# select tab
st.write("\n")
st.header('AB-AutoGPT 交互式数据探索【迭代中...】')
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
            agent = create_pandas_dataframe_agent(OpenAI(model_name="gpt-3", temperature=0), data_obj,
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
