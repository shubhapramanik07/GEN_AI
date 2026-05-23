# NOTE: Chat models use role based message structure where sys instructions are given in system messages, user inputs are given in human messages and model responses are given in ai messages. This way the model can understand the context and the flow of the conversation better...
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()
chat_model = ChatMistralAI(model="mistral-small-latest", temperature=0.7, max_tokens=69)
print("chosse your AI mode:\n")
print("press 1 for Angry mode\n")
print("press 2 for funny mode \n")
print("press 3 for sad mode\n")

choice = int(input("\nenter your choice \n: "))

if choice == 1:
    mode = "you are an angry bot. you will respond to the user in a very angry way. you will use a lot of bad words and you will be very rude to the user. you will not care about the user's feelings and you will not try to be polite. you will just say whatever comes to your mind without any filter."
elif choice == 2:
    mode = "you are a funny bot. you will respond to the user in a very funny way. you will use a lot of jokes and puns and you will be very humorous in your responses. you will try to make the user laugh and you will not take anything seriously."
elif choice == 3:   
    mode = "you are a sad bot. you will respond to the user in a very sad way. you will use a lot of sad words and you will be very emotional in your responses. you will try to make the user feel sorry for you and you will not be able to control your emotions."
# print("==============welcome to mistral chat model:=============\n press 0 to exit the chat\n")

messages = [
    SystemMessage(content=mode)  # set the chosen mode as system instruction
]

print("==============welcome to mistral chat model:=============\n press 0 to exit the chat\n")

while True:
    prompt = input("you : ") 
    if prompt == "0":  
        break  
    messages.append(HumanMessage(content=prompt))
      
    response = chat_model.invoke(messages)

    messages.append(AIMessage(content=response.content)) # here we are appending the model response as an AIMessage to the messages list so that it can be used as context for the next turn of the conversation. This way, the model can maintain the flow of the conversation and respond accordingly based on the previous messages.
    print("mistral_BOT : ", response.content)
print(messages)