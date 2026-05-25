from langchain.tools import tool


@tool #decorator for creating tool 
def get_greeting(name : str) -> str: #type hints
    """Generate a greeting message for a user""" #docstring (we give it just for better understanding of the tool, it's not mandatory but it's a good practice to have it.)

    return f"Hello {name}, Welcome to the AI world"


result = get_greeting.invoke({"name":"shubha pramanik"})
print(result)

print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args)

#? it's a example of how a tool created using the @tool decorator can be invoked and how we can access the tool's name, description and arguments.

#?  The get_greeting function is a simple tool that takes a name as input and returns a greeting message.

# ? We invoke the tool with a dictionary containing the name argument and print the result.                                                     We also print the tool's name, description and arguments to see how they are defined.