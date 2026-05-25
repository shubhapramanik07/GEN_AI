
#? here we are going to create a city intelligence agent:----------------->

#* to make it, we need the following stuff:----------------->

#* 1. Weather Tool 
    #! OpenWeatherMap API
#* 2. news tool
    #! Tavily API

#* going to do human in the loop agent, so we need to create a human tool as well.

# *--------------------------------------------------------
#? now api key make tools for both
#? then set the model up and create the agent and test it.

# *--------------------------------------------------------from dotenv import load_dotenv


# =========================================================
# AI CITY + WEATHER AGENT
# =========================================================
# Features:
# 1. Search any city information using Tavily API
# 2. Get live weather using WeatherAPI
# 3. Uses Mistral LLM
# 4. Uses LangChain Agent
# =========================================================
from dotenv import load_dotenv
import os
import json
import requests
from rich import print
from rich.prompt import Prompt
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from tavily import TavilyClient

load_dotenv()

# =========================
# 🌦️ Weather Tool
# =========================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    return (
        f"Weather in {city.title()}:\n"
        f"  🌡️  Temp      : {temp}°C (feels like {feels_like}°C)\n"
        f"  🌤️  Condition : {desc.capitalize()}\n"
        f"  💧 Humidity  : {humidity}%\n"
        f"  🌬️  Wind      : {wind} m/s"
    )


# =========================
# 📰 News Tool (Tavily)
# =========================
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about a city don't give any old news, only give the latest news"""
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3,
    )
    results = response.get("results", [])

    if not results:
        return f"No news found for {city}."

    news_list = []
    for r in results:
        title   = r.get("title", "No title")
        url     = r.get("url", "")
        snippet = r.get("content", "")[:150]
        news_list.append(f"• [bold]{title}[/bold]\n  🔗 {url}\n  📝 {snippet}...")

    return f"Latest news in {city.title()}:\n\n" + "\n\n".join(news_list)


# =========================
# 🔧 Tool Registry
# =========================
TOOLS = {
    "get_weather": get_weather,
    "get_news":    get_news,
}

# Bind tools to the LLM so it knows their schemas
llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tools = llm.bind_tools(list(TOOLS.values()))


# =========================
# ✋ Human-in-the-Loop
# =========================
def ask_human_approval(tool_name: str, tool_args: dict) -> bool:
    """Ask the user whether to allow a tool call."""
    print(f"\n[bold yellow]⚠️  Agent wants to call tool:[/bold yellow] [cyan]{tool_name}[/cyan]")
    print(f"   [dim]Arguments: {json.dumps(tool_args, ensure_ascii=False)}[/dim]")
    answer = Prompt.ask("   Approve?", choices=["yes", "no"], default="yes")
    return answer.lower() == "yes"


# =========================
# 🔁 Manual Agentic Loop
# =========================
def run_agent(user_input: str, chat_history: list) -> str:
    """
    Run a single user turn through the manual tool-call loop.
    chat_history is mutated in place so context persists across turns.
    """
    # Append the new user message
    chat_history.append(HumanMessage(content=user_input))

    while True:
        # --- LLM call ---
        response: AIMessage = llm_with_tools.invoke(chat_history)
        chat_history.append(response)

        # If there are no tool calls, we're done — return the text reply
        if not response.tool_calls:
            return response.content

        # --- Process every tool call the model requested ---
        for tc in response.tool_calls:
            tool_name: str  = tc["name"]
            tool_args: dict = tc["args"]
            tool_id: str    = tc["id"]

            if tool_name not in TOOLS:
                # Unknown tool → tell the model
                chat_history.append(
                    ToolMessage(
                        content=f"Error: tool '{tool_name}' is not available.",
                        tool_call_id=tool_id,
                    )
                )
                continue

            # Human approval gate
            approved = ask_human_approval(tool_name, tool_args)

            if not approved:
                print("[red]   ✗ Tool call denied by user.[/red]\n")
                chat_history.append(
                    ToolMessage(
                        content="Tool call was denied by the user. Do not retry this tool.",
                        tool_call_id=tool_id,
                    )
                )
                continue

            # Execute the tool
            print(f"[green]   ✓ Executing {tool_name}…[/green]\n")
            result: str = TOOLS[tool_name].invoke(tool_args)
            chat_history.append(
                ToolMessage(content=result, tool_call_id=tool_id)
            )

        # Loop back → let the LLM generate the final answer (or more tool calls)


# =========================
# 🚀 Main Chat Loop
# =========================
def main():
    system_message = SystemMessage(
        content=(
            "You are a helpful city assistant. "
            "When the user asks about weather or news for any city, "
            "use the provided tools. Always be concise and friendly."
        )
    )
    chat_history: list = [system_message]

    print("\n[bold green]🏙️  City Agent[/bold green]  [dim](type 'exit' to quit)[/dim]\n")

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]").strip()

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("\n[dim]Goodbye! 👋[/dim]\n")
            break

        try:
            reply = run_agent(user_input, chat_history)
            print(f"\n[bold magenta]Bot[/bold magenta]: {reply}\n")
        except Exception as e:
            print(f"\n[bold red]Error:[/bold red] {e}\n")


if __name__ == "__main__":
    main()



    #! the above code is a bruteforce type like generally people used to do these type of thing previously now there is "create_agent" function in langchain which can do all these stuff in one line of code but i have done it manually to understand the whole process of how agent works and how tools are called and how we can give human in the loop approval for tool calls, so yeah it's a good practice to do it manually at least once to understand the whole process and then we can use the "create_agent" function for faster development.
    #? also we bind the llm and tools using few lines of code but using create_agent it does just one line of code.

        #* and another thing is that i have made this code using myself :) just give proper prompt to gpt and gpt make the whole stuff, but yeah prompt also matter other wise in such ways they cant give code




        #* No create_agent — fully manual loop (run_agent)
        #? The core is a while True loop that:---------------------------------------------------------

        #! Calls the LLM with the full chat history
        #! Checks if the response has .tool_calls
        #! If yes → asks for human approval for each tool call individually
        #! Executes approved tools, appends ToolMessage results back to history
        #! Loops again so the LLM can generate its final text answer
