#app/tests/test_langsmith.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.config import setting
import os

os.environ['LANGCHAIN_TRACING_V2']="true" 
os.environ['LANGCHAIN_API_KEY']=setting.langchain_api_key
os.environ['LANGCHAIN_PROJECT']=setting.langchain_project

llm=ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    google_api_key=setting.google_api_key
)

response=llm.invoke([HumanMessage(content='What is 2+2? Reply with just the number.')])
print(response.content)
