# # here we are going to see how to use tool calling in langchain, then the tool binding and then we will see how to call them in a chain.

# from dotenv import load_dotenv
# load_dotenv()
# from langchain_mistralai import ChatMistralAI
# from langchain.tools import tool
# #! from langchain_core.output_parsers import StrOutputParser -----?we dont need output parser here because the tool will return the output in the format we want. 
# # ** it is required when we want to parse the output of the model but in this case we are going to use the tool which will return the output in the format we want so we dont need to parse it.
# from langchain_core.messages import HumanMessage

# from rich import print
# # here we are using rich library to print the output in a better way. means we can use colors and formatting to make the output more readable and visually appealing.

# # now first lets create a tool that will return the length of the input text..
# @tool
# def get_text_length(text: str) -> int:
#     """Returns the length of the input text."""
#     return len(text)
# # now we have created a tool that will return the length of the input text, now we can use this tool in our chain to get the length of the input text.

# tools = {
#     "get_text_length": get_text_length
#     # why this is required because when we want to call the tool in the chain we need to use the name of the tool which is "get_text_length" in this case, so we need to have a mapping of the tool name and the tool function. otherwise we will not be able to call the tool in the chain because we will not have the reference to the tool function.
# }

# llm = ChatMistralAI(model="mistral-small-2506")

# # tool binding:
# llm_with_tools = llm.bind_tools([get_text_length])
# # we are just binding the tool to the llm, so that we can call the tool in the chain using the llm.

# message = [] #it's a kind of local memory storage...
# prompt = input("You: ")
# query = HumanMessage(content=prompt)
# message.append(query)

# result = llm_with_tools.invoke(message)
# # this line will invoke the llm with the message and it will return the output of the llm which will include the output of the tool if the tool is called in the chain.

# message.append(result)
# # result also should append to the message because it will be used in the next turn of the conversation, so we need to have the output of the llm in the message so that we can use it in the next turn of the conversation.

# if result.tool_calls:
#     tool_name = result.tool_calls[0]["name"] #this will give us the name of the tool that was called in the chain, in this case it will be "get_text_length"
#     tool_message = tools[tool_name].invoke(result.tool_calls[0]) #this will give us the message that was passed to the tool, in this case it will be the input text for which we want to get the length.
#     message.append(tool_message) # we also need to append the tool message to the message because it will be used in the next turn of the conversation. except it will be used as an input to the tool in the next turn of the conversation.
# result = llm_with_tools.invoke(message)
# print(result.content)




# User prompt
    # → LLM decides to call get_text_length
        # → We actually run the tool
            # → Wrap output in ToolMessage
                # → LLM gives final answer using the tool result


from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool 
from langchain_core.messages import HumanMessage
from rich import print 

#1 creating a tool 

@tool
def get_text_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)

tools = {
    "get_text_length" : get_text_length
}
llm = ChatMistralAI(model = "mistral-small-2506")

#tool binding 
llm_with_tool = llm.bind_tools([get_text_length])

message = []
prompt = input("You: ")
query = HumanMessage(prompt)
message.append(query)

# ✅ CORRECT
result = llm_with_tool.invoke(message)
message.append(result)

print(result.tool_calls)  # 👈 add this debug line to see internal workflow..

if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_message = tools[tool_name].invoke(result.tool_calls[0])
    message.append(tool_message)
    result = llm_with_tool.invoke(message)  # ← INSIDE if block
    print(result.content)
else:
    print(result.content)  # ← direct reply, no tool needed

# You: i am giving u a name: sona and find the length of the name
# [
#     {
#         'name': 'get_text_length',
#         'args': {'text': 'sona'},
#         'id': '8RuGqrlSO',
#         'type': 'tool_call'
#     }
# ]
# The length of the name "sona" is 4 characters.
# (gen-ai) PS C:\Users\shubh\Desktop\GEN_AI> 