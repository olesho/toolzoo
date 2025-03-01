import os
from langchain.tools import BaseTool
from datetime import datetime
from typing import Dict
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ToolInputSchema(BaseModel):
    dummy: Optional[str] = Field(None, description="Not used")

    class Config:
        extra = "forbid"

class CurrentTimeTool(BaseTool):
    name: str = "current_time"
    description: str = "Get the current time in UTC"
    args_schema: type[BaseModel] = ToolInputSchema

    def _run(self, dummy: Optional[str] = None) -> str:
        current_utc = datetime.utcnow()
        return current_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

if __name__ == "__main__":
    tool = CurrentTimeTool()
    print(tool.invoke({}))