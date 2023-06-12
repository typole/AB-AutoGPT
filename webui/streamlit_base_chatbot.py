import streamlit as st
from get_offline_file import load_offline_csvfile
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

st.set_page_config(page_title="ChatGPT Clone - 一个大语言模型加持的 Streamlit 应用", layout='wide')

# 侧边栏内容
with st.sidebar:
    st.title('🤖 ChatGPT Clone 应用')
    st.markdown('''
    ## 关于
    应用是基于大语言模型的聊天机器人，由以下技术构建:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/en/latest/modules/agents/agent_executors/examples/chatgpt_clone.html)
    - [OpenAI LLM model](https://chat.openai.com/)

    💡 注意： API key 必需的!
    ''')
    add_vertical_space(5)
    st.write('创作 🙆‍♂️ 来源： [小智Robo](https://space.bilibili.com/390067647/)')

# 生成空列表，为了存储用户的输入和机器人的回复
# 生成内容存储机器人的回复
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["您好！我是小智, 有什么可以帮您吗?"]
# 历史存储用户的输入
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# 输入、响应容器框架
api_container = st.container()
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()
template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)


# 用户输入
# 该函数将用户提供的提示词作为输入；
def get_text():
    input_text = st.text_input("请输入: ", "", key="input")
    return input_text


# 应用用户输入的提示词内容
with input_container:
    user_input = get_text()


# 响应输出
# 该函数将用户提供的提示词作为输入，来生成AI响应内容；
def generate_response():
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.9),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=10),
    )
    return chatgpt_chain.predict(human_input=user_input)


# 将AI响应内容输出到应用，同时将用户输入的提示词和AI响应内容存储到列表中；
with response_container:
    if user_input:
        load_offline_csvfile(user_input)  # TODO 需要将加载文件和与文件交互解耦
        response = generate_response()
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
