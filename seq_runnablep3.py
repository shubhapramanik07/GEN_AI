from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 
# prompt template
prompt = ChatPromptTemplate.from_template("explain {topic} very easy way in short.")
# model
model = ChatMistralAI(model="mistral-small-2506")
# output parser
output_parser = StrOutputParser()
# generate response
chain = prompt | model | output_parser
response = chain.invoke("AI engineer roadmap")
print(response)

# this was the first code file of GEN AI course p -03.