from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize the search tool
search_tool = TavilySearchResults(max_results=2)

# now we are going to use the search tool to find recent news articles about the stock market

# model
model = ChatMistralAI(model="mistral-small-2506")
# prompt template
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant

summarize the following news into clear bullet points maximum 5 points. Make sure to include the source of the news as well.

{news}
"""
)
# output parser
output_parser = StrOutputParser()
# generate summary
chain = prompt | model | output_parser

# invoke the search tool to get news about AI/ML and then pass it to the chain to get the summary
news_content = search_tool.invoke("AI/ML news")


response = chain.invoke({"news": news_content})
print(response)

print("Done \n\n\n")

print(search_tool.description)
print(search_tool.name)
print(search_tool.args)