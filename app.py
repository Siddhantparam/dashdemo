import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.callbacks import BaseCallback
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser

load_dotenv()

class StreamlitCallback(BaseCallback):
    def __init__(self, container) -> None:
        """Initialize callback handler."""
        self.container = container

    def on_code(self, response: str):
        self.container.code(response)


class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.write(result["value"])
        return


st.write("# Chat with Credit Card Fraud Dataset 🦙")
uploaded_file = st.file_uploader('Upload your csv for analytics')

if uploaded_file is not None:
    df = pd.read_csv('customer_data.csv')

    with st.expander("🔎 Dataframe Preview"):
        st.write(df.tail(5))

query1 = "Plot the opening balance for the march of 2022"
query2 = "summarize about average , total , mode , least and max opening price for january 2022"
query3 = "Plot the closing balance for the march of 2022"
query4 = "summarize about average , total , mode , least and max closing price for january 2022"
query5 = "Plot the recieved quantity for the march of 2022"
query6="summarize about average , total , mode , least and max recieving quantity for january 2022"
query7="Plot the consumption quantity for the march of 2022"
query8="summarize about average , total , mode , least and max consumption quantity for january 2022"
container = st.container()

if query1:
    llm = OpenAI(api_token=os.environ["OPENAI_API_KEY"])
    query_engine = SmartDataframe(
        df,
        config={
            "llm": llm,
            "response_parser": StreamlitResponse,
        },
    )
    st.header('Analytics for Q1 2022')
    answer1 = query_engine.chat(query1)
    answer2=query_engine.chat(query2)
    answer3=query_engine.chat(query3)
    answer4=query_engine.chat(query4)
    answer5=query_engine.chat(query5)
    answer6=query_engine.chat(query6)
    answer7=query_engine.chat(query7)
    answer8=query_engine.chat(query8)


