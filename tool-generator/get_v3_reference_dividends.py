import os
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from typing import Optional

class ToolInputSchema(BaseModel):
    ticker: Optional[str] = Field(None, description="The stock ticker symbol to get dividends for (e.g., AAPL)", pattern="^[A-Z]+$", min_length=1, max_length=5)
    ex_dividend_date: Optional[str] = Field(None, description="Query by ex-dividend date with the format YYYY-MM-DD")
    record_date: Optional[str] = Field(None, description="Query by record date with the format YYYY-MM-DD")
    declaration_date: Optional[str] = Field(None, description="Query by declaration date with the format YYYY-MM-DD")
    pay_date: Optional[str] = Field(None, description="Query by pay date with the format YYYY-MM-DD")
    frequency: Optional[int] = Field(None, description="Query by the number of times per year the dividend is paid out. Possible values are 0 (one-time), 1 (annually), 2 (bi-annually), 4 (quarterly), and 12 (monthly)")
    cash_amount: Optional[float] = Field(None, description="Query by the cash amount of the dividend")
    dividend_type: Optional[str] = Field(None, description="Query by the type of dividend. CD for consistent dividends, SC for special cash dividends, LT for long-term capital gain, ST for short-term capital gain")
    limit: Optional[int] = Field(10, description="Limit the number of results returned, default is 10 and max is 1000")
    sort: Optional[str] = Field(None, description="Sort field used for ordering. Options: ex_dividend_date, pay_date, declaration_date, record_date, cash_amount, ticker")
    order: Optional[str] = Field(None, description="Order results based on the sort field. Options: asc, desc")

class DividendsV3(BaseTool):
    name: str = "dividends_v3"
    description: str = "Get a list of historical cash dividends, including the ticker symbol, declaration date, ex-dividend date, record date, pay date, frequency, and amount"
    args_schema: type[BaseModel] = ToolInputSchema
    api_key: str = Field(..., exclude=True)

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _run(self, ticker: Optional[str] = None, ex_dividend_date: Optional[str] = None, 
             record_date: Optional[str] = None, declaration_date: Optional[str] = None, 
             pay_date: Optional[str] = None, frequency: Optional[int] = None, 
             cash_amount: Optional[float] = None, dividend_type: Optional[str] = None,
             limit: int = 10, sort: Optional[str] = None, order: Optional[str] = None):
        # Tool implementation
        print(f"TOOL CALL: Getting dividends data")
        
        # Build query parameters
        params = {"apiKey": self.api_key, "limit": limit}
        
        if ticker:
            params["ticker"] = ticker
        if ex_dividend_date:
            params["ex_dividend_date"] = ex_dividend_date
        if record_date:
            params["record_date"] = record_date
        if declaration_date:
            params["declaration_date"] = declaration_date
        if pay_date:
            params["pay_date"] = pay_date
        if frequency is not None:
            params["frequency"] = frequency
        if cash_amount is not None:
            params["cash_amount"] = cash_amount
        if dividend_type:
            params["dividend_type"] = dividend_type
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        
        response = requests.get("https://api.polygon.io/v3/reference/dividends", params=params)
        
        print(f"TOOL RESPONSE: Status code {response.status_code}")
        
        return response.json()

if __name__ == "__main__":
    api_key = os.getenv("POLYGON_API_KEY")
    tool = DividendsV3(api_key=api_key)
    # Example: Get dividends for Apple
    print(tool.invoke({"ticker": "AAPL", "limit": 5}))
