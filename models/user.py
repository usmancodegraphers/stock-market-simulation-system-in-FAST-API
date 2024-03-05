from sqlalchemy import String, Column, Float
from sqlalchemy.orm import relationship

from .baseclass import BaseModel


class User(BaseModel):
    """
    Database table representation for users.

    Attributes:
       - username (str): User's username (unique).
       - balance (float): User's balance.
       - password (str): Hashed password for user authentication.
       - transactions (relationship): Relationship with Transactions table.

    Note:
        This class assumes that you have a BaseModel defined elsewhere.

    See Also:
        `BaseModel`: A base class for common database model functionality.
    """
    __tablename__ = 'users'
    username = Column(String, nullable=False, unique=True)
    balance = Column(Float)
    password = Column(String(255))
    transactions = relationship("Transactions", back_populates='owner')
