import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class ToolInputSchema(BaseModel):
    a: int = Field(..., description="The first number to multiply")
    b: int = Field(..., description="The second number to multiply")

class Multiply(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"
    args_schema: type[BaseModel] = ToolInputSchema

    def _run(self, a: int, b: int):
        return a * b

if __name__ == "__main__":
    tool = Multiply()
    print(tool.invoke({"a": 4, "b": 2}))