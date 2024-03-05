from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
       - username (str): The username of the user.
       - password (str): The password of the user.
       - balance (float): The initial balance of the user.
    """

    username: str
    password: str
    balance: float

    class Config:
        from_attributes = True


class GetUser(BaseModel):
    """
    Schema for getting user details.

    Attributes:
       - username (str): The username of the user.
       - balance (float): The current balance of the user.
    """

    username: str
    balance: float

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
       - username (str): The username of the user.
       - password (str): The password of the user.
    """

    username: str
    password: str


class Token(BaseModel):
    """
    Schema for a JWT token.

    Attributes:
       - access_token (str): The JWT access token.
       - token_type (str): The type of the token (e.g., 'bearer').
    """

    access_token: str
    token_type: str
