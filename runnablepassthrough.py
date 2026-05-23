# in this file we are going to learn about the RunnablePassthrough which is a special type of runnable that simply passes the input to the next runnable without any modification. This is useful when we want to use the same input for multiple runnables in a parallel runnable.
# in real life application where it used like when we want to generate multiple responses for the same input but with different prompts or models, we can use the RunnablePassthrough to pass the input to all the runnables in the parallel runnable without having to call the model multiple times.
from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# like here we are going to see a project where chatbot is going to generate both code and separately explanation for the same input question. So we can use the RunnablePassthrough to pass the input question to both the code generation runnable and the explanation generation runnable without having to call the model multiple times.

# model 
model = ChatMistralAI(model="mistral-small-2506")
parser = StrOutputParser()

# prompt for code generation
code_prompt = ChatPromptTemplate.from_messages([("system", "you are a code generator."), ("human", "{input}")])
# prompt for explanation generation
explanation_prompt = ChatPromptTemplate.from_messages([("system", "you are a code explainer in simple terms."), ("human", "explain the following code in simple words:\n {code}")])


# just add a seq runnable to generate both code and explanation in one go...
seq = code_prompt | model | parser

seq2 = RunnableParallel(
    {
        "code": RunnablePassthrough(),
        "explanation": explanation_prompt | model | parser
    }
)

chain = seq | seq2

result = chain.invoke({"input": "write a python function to calculate the sum of two numbers"})

print(result['code'])
print(result['explanation'])