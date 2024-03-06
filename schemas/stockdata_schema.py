from datetime import datetime

from pydantic import BaseModel


class StockDataSchema(BaseModel):
    ticker: str
    open_price: float
    close_price: float
    high: float
    low: float
    volume: int
    timestamp: datetime = datetime.now()

    class Config:
        from_attributes = True
