import os
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.callbacks import BaseCallback
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser


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


st.write("# PARAM GENAI Alerts 🦙")
uploaded_file = st.file_uploader('Upload your csv for analytics')

df = pd.read_csv(uploaded_file)

with st.expander("🔎 Dataframe Preview"):
    st.write(df.tail(5))
if st.button('Generate'):
        query1 = "Plot the opening balance for the march of 2022"
        query2 = "Opening balance being more than 80 is a warining give an alert message for those dates plz write this in the form of a micro blog for march 2022 "
        query3 = "Plot the closing balance for the march of 2022"
        query4 = "Closing balance being lower than 20 is a warining give an alert message for those dates plz write this in the form of a micro blog for marc h 2022"
        query5 = "Plot the recieved quantity for the march of 2022"
        query6 = "recieved below 5 is problem plz give an alert for those days of march 2022"
        container = st.container()
        
        if query1:
            llm = OpenAI(api_token='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')
            query_engine = SmartDataframe(
                df,
                config={
                    "llm": llm,
                    "response_parser": StreamlitResponse,
                },
            )
            st.header('Alerts for march 2022')
            answer1 = query_engine.chat(query1)
            answer2=query_engine.chat(query2)
            answer3=query_engine.chat(query3)
            answer4=query_engine.chat(query4)
            answer5=query_engine.chat(query5)
            answer6=query_engine.chat(query6)
        
        
