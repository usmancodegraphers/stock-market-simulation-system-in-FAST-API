from sqlalchemy import String, Column, Float
from sqlalchemy.orm import relationship

from .baseclass import BaseModel


class User(BaseModel):

    __tablename__ = "users"
    username = Column(String, nullable=False, unique=True)
    balance = Column(Float)
    password = Column(String(255))
    transactions = relationship("Transactions", back_populates="owner")
