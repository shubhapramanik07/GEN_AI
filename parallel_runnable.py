from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
# prompt template
prompt = ChatPromptTemplate.from_template("explain {topic} very easy way within 2 lines.")
prompt2 = ChatPromptTemplate.from_template("explain {topic} within 10 lines.")

# model
model = ChatMistralAI(model="mistral-small-2506")

# output parser
output_parser = StrOutputParser()

# let's create a parallel runnable to generate both short and long explanations in one go
chain = RunnableParallel({
    "short": RunnableLambda(lambda x:x['short']) | prompt | model | output_parser,
    "long": RunnableLambda(lambda x:x['long']) | prompt2 | model | output_parser
})

#! chain = (lambda x:x)| prompt | model | output_parser
#! chain2 = (lambda x:x) | prompt2 | model | output_parser

result = chain.invoke({"short":"AI engineer roadmap", "long":"AI engineer roadmap"})

#! response = chain.invoke("AI engineer roadmap")
#! response2 = chain2.invoke("AI engineer roadmap")

print(result["short"])
print(result["long"])

# here in this file we just saw how the parallel runnable works and how we can generate multiple outputs in one go using the same input. This is very useful when we want to generate different types of responses for the same input without having to call the model multiple times.