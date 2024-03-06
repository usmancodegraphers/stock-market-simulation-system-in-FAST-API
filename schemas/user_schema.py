from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    balance: float

    class Config:
        from_attributes = True


class GetUser(BaseModel):
    username: str
    balance: float

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
