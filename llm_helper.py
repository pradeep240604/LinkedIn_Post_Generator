from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="meta-llama/llama-4-scout-17b-16e-instruct")
llm = ChatGroq(model = "meta-llama/llama-4-scout-17b-16e-instruct", timeout=60.0)
if __name__ == "__main__":
    response = llm.invoke("What is the capital of India?")
    print(response.content)