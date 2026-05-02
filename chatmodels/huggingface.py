from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceHub
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    temperature=0.7)
model = ChatHuggingFace(llm=llm)
response = model.invoke("What is the capital of France?")
print(response.content)