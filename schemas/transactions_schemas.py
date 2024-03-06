from datetime import datetime

from pydantic import BaseModel


class TransectionSchema(BaseModel):
    ticker: str
    transaction_type: str
    transaction_volume: int
    transaction_price: float
    timestamp: datetime = datetime.now()

    class Config:
        from_attributes = True
