import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import json

class MarketStatus(BaseTool):
    name: str = "market_status"
    description: str = "Get the current trading status of the exchanges and overall financial markets."
    api_key: str = Field(..., exclude=True)

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self):
        response = requests.get(f"https://api.polygon.io/v1/marketstatus/now?apiKey={self.api_key}")

        data = response.json()
        return json.dumps(data, indent=2)

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("Error: POLYGON_API_KEY environment variable is not set")
        print("Please set it with your Polygon.io API key")
        exit(1)
    tool = MarketStatus(api_key=api_key)
    print(tool.invoke({}))
