from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

os.environ["hf_tokan"] = os.getenv("hf_tokan")
os.environ["LANGCAHIN_API_KEY"] = os.getenv("LANGCAHIN_API_KEY")
os.environ["LANGCAHIN_PROJECT"] = os.getenv("LANGCAHIN_PROJECT")
os.environ["LANGCAHIN_TRACING_V2"] = "true"

hf_tokan = os.getenv("hf_tokan")

st.title("my ai")
st.markdown("powered by huggingface and langchain")

topic = st.text_input("Enter a topic") 
prompt = ChatPromptTemplate(
    [
        ("system", "Hey assistant,you are a standup comedian,generate jokes based on inputs given to you"),
        ("user", "topic: {topic}")
    ]
)
llm = HuggingFaceEndpoint(
     endpoint_url="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
     huggingfacehub_api_token=hf_tokan
)

OUTPUT_PARSER = StrOutputParser()
chain = prompt | llm | OUTPUT_PARSER

if topic:
    with st.spinner("Generating jokes..."):
        result = chain.invoke({"topic": topic})
        st.success("here is your generated joke")
        st.write(result.strip())

