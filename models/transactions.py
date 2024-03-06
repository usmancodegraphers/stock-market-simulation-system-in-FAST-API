from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship

from .baseclass import BaseModel


class Transactions(BaseModel):

    __tablename__ = "transactions"
    ticker = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_volume = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")
    transaction_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
