from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()
chat_model = ChatMistralAI(model="mistral-small-latest", temperature=0.7)
cache_memory = [
    
]
print("==============welcome to mistral chat model:=============\n press 0 to exit the chat\n")
while True:
    prompt = input("you : ") #?we are taking the input from user...

    cache_memory.append(prompt) 
    #?we are storing the user input in cache memory so that we can use it later for context or for any other purpose. This way we can keep track of the conversation history and use it to improve the responses or to provide better context for the model.

    if prompt == "0":  #?if the user enters 0 then we will exit the chat
        break    
    response = chat_model.invoke(cache_memory)
    #! this is the most vital part as we are sending the entire conversation history (cache_memory) to the model as input along with the new prompt.
    #  
    cache_memory.append(response.content) 
    
    #?we are storing the response in cache memory so that we can use it later for context or for any other purpose. This way we can keep track of the conversation history and use it to improve the responses or to provide better context for the model.

    # ! here is the main problem:  chat_model.invoke() expects LangChain message objects, not plain strings. When you pass raw strings, the model has no idea which messages are from the user and which are from the bot — so it loses context entirely. 
    #* To fix this, you need to wrap your inputs in the appropriate message classes (e.g., HumanMessage for user input and AIMessage for model responses) before invoking the model. This way, the model can understand the structure of the conversation and maintain context across turns.


    print("mistral_BOT : ", response.content)
print(cache_memory)