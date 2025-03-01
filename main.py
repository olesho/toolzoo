from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.globals import set_llm_cache
# from langchain_community.cache import SQLiteCache
from langchain_community.cache import InMemoryCache
from dotenv import load_dotenv

import argparse
import langchain
import os

from tools.polygon.news import TickerNews
from tools.polygon.market_status import MarketStatus
from tools.math.multiply import Multiply
from tools.time.current import CurrentTimeTool

# Load environment variables from .env file
load_dotenv()

polygon_api_key = os.getenv("POLYGON_API_KEY")

parser = argparse.ArgumentParser(description='LangChain script with debug and cache options')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
parser.add_argument('-c', '--cache', action='store_true', help='Enable caching')

args = parser.parse_args()

DEBUG = os.getenv("DEBUG", "false").lower() == "true" or args.debug
CACHE = os.getenv("CACHE", "false").lower() == "true" or args.cache

langchain.debug = DEBUG
if CACHE:
    set_llm_cache(InMemoryCache())


#llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# llm = OllamaLLM(model='llama3.2:3b-instruct-fp16', temperature=0)
# llm_with_tools = llm.bind_tools([multiply])

ticker_news = TickerNews(api_key=polygon_api_key)
multiply = Multiply()
current_time_in = CurrentTimeTool()
market_status = MarketStatus(api_key=polygon_api_key)

llm = ChatOllama(model='llama3.2', temperature=0)
llm_with_tools = llm.bind_tools([multiply, current_time_in, ticker_news, market_status])

query = "What is 2 multiplied by 3? Also could you help me to calculate multiplication for 34 by 12"

query = "What is a market status today?"
# query = "Can you help me to get news for AMZN ticker ?"
messages = [HumanMessage(query)]

print(f"Query: {query}")

ai_msg = llm_with_tools.invoke(messages)

messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {
        "multiply": multiply,
        "current_time_in": current_time_in,
        "ticker_news": ticker_news,
        "market_status": market_status }[tool_call['name'].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

result_msg = llm_with_tools.invoke(messages)

#print(f"Result with tools: {result_msg}")
print(f"AI answer: {result_msg.content}")

# if result.tool_calls:
#     tool_call = result.tool_calls[0]
#     print(f"Tool called: {tool_call['name']}")
#     print(f"Arguments: {tool_call['args']}")
#     print(f"Tool call = {tool_call}")
# else:
#     print("Tool_calls is empty")