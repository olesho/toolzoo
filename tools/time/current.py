import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests

class CurrentTimeTool(BaseTool):
    name: str = "current_time_in"
    description: str = "Get the current time"

    def _run(self, region: str):
        """Get current time in specified region"""
        print("api call...")
        #"http://worldtimeapi.org/api/timezone/America/Argentina/Cordoba"

        response = requests.get(f"http://worldtimeapi.org/api/timezone/America/Argentina/{region}")
        return response.content

if __name__ == "__main__":
    tool = CurrentTimeTool()
    print(tool.invoke({"region": "Cordoba"}))