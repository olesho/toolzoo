import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from typing import Optional, List

class TickersInputSchema(BaseModel):
    ticker: Optional[str] = Field(None, description="Specify a ticker symbol to filter results")
    type: Optional[str] = Field(None, description="Filter by ticker type (e.g., CS, ETF, FUND)")
    market: Optional[str] = Field(None, description="Filter by market type (stocks, crypto, fx, otc, indices)")
    exchange: Optional[str] = Field(None, description="Filter by primary exchange in ISO code format")
    cusip: Optional[str] = Field(None, description="Filter by CUSIP code")
    cik: Optional[str] = Field(None, description="Filter by CIK number")
    date: Optional[str] = Field(None, description="Point in time to retrieve tickers (YYYY-MM-DD format)")
    search: Optional[str] = Field(None, description="Search terms within ticker or company name")
    active: Optional[bool] = Field(True, description="Whether to return only actively traded tickers")
    sort: Optional[str] = Field(None, description="Field to sort results by")
    order: Optional[str] = Field(None, description="Sort order (asc or desc)")
    limit: Optional[int] = Field(100, description="Limit number of results (max 1000)")

class PolygonTickers(BaseTool):
    name: str = "polygon_tickers"
    description: str = "Query ticker symbols supported by Polygon.io including Stocks/Equities, Indices, Forex, and Crypto"
    args_schema: type[BaseModel] = TickersInputSchema
    api_key: str = Field(..., exclude=True)

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self, 
             ticker: Optional[str] = None,
             type: Optional[str] = None,
             market: Optional[str] = None,
             exchange: Optional[str] = None,
             cusip: Optional[str] = None,
             cik: Optional[str] = None,
             date: Optional[str] = None,
             search: Optional[str] = None,
             active: Optional[bool] = True,
             sort: Optional[str] = None,
             order: Optional[str] = None,
             limit: Optional[int] = 100):
        
        url = "https://api.polygon.io/v3/reference/tickers"
        
        params = {
            "apiKey": self.api_key,
            "active": active,
            "limit": limit
        }
        
        # Add optional parameters if provided
        if ticker:
            params["ticker"] = ticker
        if type:
            params["type"] = type
        if market:
            params["market"] = market
        if exchange:
            params["exchange"] = exchange
        if cusip:
            params["cusip"] = cusip
        if cik:
            params["cik"] = cik
        if date:
            params["date"] = date
        if search:
            params["search"] = search
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
            
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}", "details": response.text}

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    tool = PolygonTickers(api_key=api_key)
    print(tool.invoke({"limit": 5}))