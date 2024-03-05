from datetime import datetime

from pydantic import BaseModel


class TransectionSchema(BaseModel):
    """
    Schema representing a financial transaction.

    Attributes:
       - ticker (str): The stock ticker symbol.
       - transaction_type (str): The type of transaction (e.g., 'buy' or 'sell').
       - transaction_volume (int): The volume or quantity of the transaction.
       - transaction_price (float): The price of the transaction.
       - timestamp (datetime): The timestamp indicating when the transaction occurred.
    """
    ticker: str
    transaction_type: str
    transaction_volume: int
    transaction_price: float
    timestamp: datetime = datetime.now()

    class Config:
        from_attributes = True
