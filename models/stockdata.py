from datetime import datetime

from sqlalchemy import String, Integer, Column, Float, DateTime

from .baseclass import BaseModel


class StockData(BaseModel):
    __tablename__ = "stockdata"
    ticker = Column(String, nullable=False, primary_key=True)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
