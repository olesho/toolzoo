import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests

class ToolInputSchema(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol to get news for", pattern="^[A-Z]+$", min_length=1, max_length=5)

class TickerNews(BaseTool):
    name: str = "ticker_news"
    description: str = "Provides news for a multiple tickers"
    args_schema: type[BaseModel] = ToolInputSchema
    api_key: str = Field(..., exclude=True)

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self, ticker: str):
        # Tool implementation
        print(f"TOOL CALL: Getting news for {ticker}")
        
        response = requests.get(f"https://api.polygon.io/vX/reference/tickers/{ticker}/events?apiKey={self.api_key}")

        print(f"TOOL RESPONSE: {response.content}")

        return response.content

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    tool = TickerNews(api_key=api_key)
    print(tool.invoke({"ticker": "META"}))