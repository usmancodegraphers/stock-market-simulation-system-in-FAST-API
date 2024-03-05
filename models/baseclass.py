import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from db.database import Base


class BaseModel(Base):
    """
    Base model for SQLAlchemy entities.

    Attributes:
       - id (str): The primary key identifier generated using UUID.
       - created_at (DateTime): The timestamp indicating the creation time.

    Methods:
        formatted_created_at() -> str:
            Returns the formatted creation timestamp as a string.
    """
    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
