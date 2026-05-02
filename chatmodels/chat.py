from dotenv import load_dotenv
load_dotenv()
# from langchain.chat_models import init_chat_model
# model = init_chat_model("mistral-small-latest")

#  #this init_chat_model function is a helper function that initializes the chat model based on the model name passed as an argument. It also takes care of loading the API keys from the environment variables and setting up the necessary configurations for the model. This way, we can easily switch between different chat models by just changing the model name in the code without having to worry about the underlying implementation details.

#we can use both of them the upper one also the lower one. The upper one is more general and can be used for any chat model, while the lower one is specific to the mistral-small-latest model. We can use the upper one to initialize the model and then use the lower one to invoke it with some input and get the response. This way, we can easily switch between different models by just changing the model name in the init_chat_model function without having to change the rest of the code. 

# lets try chatmistralai which is a new model from mistral. It is a smaller version of their original model but still has good performance. It is also cheaper to use than the original model. We will see how it performs on some tasks.
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-latest",temperature=0.7,max_tokens=10)
# agent = create_deep_agent(model=model)
# Invoke with the user's model selection
result = model.invoke("say hii")
print(result.content)