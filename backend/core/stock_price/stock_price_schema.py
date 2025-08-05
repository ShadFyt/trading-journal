from pydantic import BaseModel, Field, ConfigDict


class StockQuote(BaseModel):
    """Pydantic model for FinnHub stock quote response."""
    symbol: str = Field(str, alias='s', description="Stock symbol")
    current_price: float = Field(float, alias='c', description="Current price")
    change: float = Field(float, alias='d', description="Price change")
    percent_change: float = Field(float, alias='dp', description="Percent change")
    high: float = Field(float, alias='h', description="High price of the day")
    low: float = Field(float, alias='l', description="Low price of the day")
    open_price: float = Field(float, alias='o', description="Open price of the day")
    previous_close: float = Field(float, alias='pc', description="Previous close price")
    timestamp: int = Field(int, alias='t', description="Unix timestamp")

    model_config = ConfigDict(
        populate_by_name=True
    )

