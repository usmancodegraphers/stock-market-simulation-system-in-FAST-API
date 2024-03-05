from datetime import datetime

from sqlalchemy import String, Integer, Column, Float, DateTime

from .baseclass import BaseModel


class StockData(BaseModel):
    """
    Stock data table representation.

    Attributes:
       - ticker (str): Ticker symbol for the stock data.
       - open_price (float): Opening price of the stock.
       - close_price (float): Closing price of the stock.
       - high (float): Highest price of the stock.
       - low (float): Lowest price of the stock.
       - volume (int): Volume of the stock.
       - timestamp (DateTime): Timestamp of the stock data (default: current UTC time).

    Note:
        This class assumes that you have a BaseModel defined elsewhere.

    See Also:
        `BaseModel`: A base class for common database model functionality.
    """
    __tablename__ = 'stockdata'
    ticker = Column(String, nullable=False, primary_key=True)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
