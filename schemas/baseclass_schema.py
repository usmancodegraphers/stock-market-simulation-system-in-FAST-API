import datetime

from pydantic import BaseModel as Base


class BaseModel(Base):
    """
    Base model class with common attributes for other models.

    Attributes:
       - created_on (datetime.datetime): The timestamp indicating when the record was created.
    """

    created_on: datetime.datetime = datetime.datetime.now()
