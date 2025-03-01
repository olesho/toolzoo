from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from dotenv import load_dotenv

from prompt import get_generation_prompt, get_html_api_ref, get_tool_example

import argparse
import langchain
import os

load_dotenv()

prompt = get_generation_prompt(
    get_html_api_ref(),
    get_tool_example()
)

model = ChatOllama(model='llama3.2', temperature=0)
#model = ChatAnthropic(model='claude-3-7-sonnet-20250219', temperature=0)
response = model.invoke([HumanMessage(prompt)])

with open('temp/output.py', 'w') as file:
    file.write(response.content)

print(response)