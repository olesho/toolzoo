from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

llm = ChatOllama(model='llama3.2', temperature=0)

check_field_presence_prompt = """
User asked this question:
{user_query}

Here is the field description:
{field_description}

Here is the field type:
{field_type}

Here is the field value:
{field_value}

You are a helpful assistant that can help me to check if the field is present in the user query. 
You will be given a user query and a field name and description.
You need to check if the field whith specified type is present in the user query.

If fields type doesn't match, you need to return False.
If field is not present, you need to return False.
Otherwise return True.
"""
class CheckFieldPresence(BaseModel):
    presence: bool = Field(None, description="Defines if the field is present in the file.")

# Augment the LLM with schema for structured output
field_presence_llm = llm.with_structured_output(CheckFieldPresence)

# # Augment the LLM with schema for structured output
# field_presence_llm = llm.with_structured_output(CheckFieldPresence)
fp = field_presence_llm.invoke(check_field_presence_prompt.format(
    user_query="What is 2 multiplied by 3?",
    field_name="a",
    field_value="2",
    field_type="integer",
    field_description="First number to multiply"
))

print(fp)