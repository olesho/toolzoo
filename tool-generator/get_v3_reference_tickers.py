import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from typing import Optional

class TickerReferenceInputSchema(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol to get reference data for", pattern="^[A-Z]+$", min_length=1, max_length=5)
    date: Optional[str] = Field(None, description="The date for which to retrieve data in YYYY-MM-DD format")

class TickerReference(BaseTool):
    name: str = "ticker_reference"
    description: str = "Provides reference data for a specific ticker symbol"
    args_schema: type[BaseModel] = TickerReferenceInputSchema
    api_key: str = Field(..., exclude=True)

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self, ticker: str, date: Optional[str] = None):
        # Tool implementation
        print(f"TOOL CALL: Getting reference data for {ticker}")
        
        url = f"https://api.polygon.io/v3/reference/tickers/{ticker}"
        if date:
            url += f"?date={date}"
        
        url += f"&apiKey={self.api_key}" if "?" in url else f"?apiKey={self.api_key}"
        
        response = requests.get(url)
        
        print(f"TOOL RESPONSE: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}", "details": response.text}

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    tool = TickerReference(api_key=api_key)
    print(tool.invoke({"ticker": "AAPL"}))
