from io import StringIO
import pandas as pd
import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import os


def load_offline_csvfile(user_input):
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dataframe, verbose=True)
        response = agent.run(user_input)
        st.write(response)
