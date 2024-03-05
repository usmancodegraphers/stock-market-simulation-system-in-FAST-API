from datetime import datetime

from pydantic import BaseModel


class StockDataSchema(BaseModel):
    """
    Pydantic model for representing stock data.

    Attributes:
       - ticker (str): Ticker symbol of the stock.
       - open_price (float): Opening price of the stock.
       - close_price (float): Closing price of the stock.
       - high (float): Highest price of the stock during the period.
       - low (float): Lowest price of the stock during the period.
       - volume (int): Volume of stock traded.
       - timestamp (datetime): Timestamp of the stock data (default is the current timestamp).

    Config:
        from_attributes (bool): Use attributes for model initialization.
    """

    ticker: str
    open_price: float
    close_price: float
    high: float
    low: float
    volume: int
    timestamp: datetime = datetime.now()

    class Config:
        """
        Pydantic configuration for the model.
        """

        from_attributes = True
