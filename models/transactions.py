from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship

from .baseclass import BaseModel


class Transactions(BaseModel):
    """
    Database table representation for transactions.

    Attributes:
       - ticker (str): Ticker symbol for the transaction.
       - transaction_type (str): Type of transaction (buy/sell).
       - transaction_volume (int): Volume of the transaction.
       - user_id (str): User ID associated with the transaction.
       - owner (relationship): Relationship with the User table.
       - transaction_price (float): Price of the transaction.
       - timestamp (DateTime): Timestamp of the transaction (default: current UTC time).

    Note:
        This class assumes that you have a BaseModel defined elsewhere and a User table.

    See Also:
        `BaseModel`: A base class for common database model functionality.
        `User`: Database table representation for users.
    """

    __tablename__ = "transactions"
    ticker = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    transaction_volume = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")
    transaction_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
