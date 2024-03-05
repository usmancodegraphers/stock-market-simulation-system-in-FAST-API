from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from common.jwt_token import hash_password, verify_password, generate_token
from constants import USER_EXIST, Invalid_Cradentials, USER_NOT_EXIST
from db.database import get_db
from models.user import User
from schemas.user_schema import UserSchema, UserLogin, Token, GetUser

routes = APIRouter()


@routes.post('/users/',
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema,
                      db: Session = Depends(get_db)
                      ) -> UserSchema:
    """
      Create a new user.

      Args:
          user (UserSchema): The user data provided in the request body.
          db (Session): The database session.

      Returns:
          UserSchema: The created user data.

      Raises:
          HTTPException: Raised if a user with the same username already exists (HTTP 400 Bad Request).
      """
    exist_user = db.query(User).filter(User.username == user.username).first()
    if exist_user:
        raise HTTPException(status_code=400, detail=USER_EXIST)

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        balance=user.balance,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    return user


@routes.post("/login")
def login(user_data: UserLogin,
          db: Session = Depends(get_db)) -> Token:
    """
        User login endpoint.

        Args:
            user_data (UserLogin): The user login data provided in the request body.
            db (Session): The database session.

        Returns:
            Token: The access token for the authenticated user.

        Raises:
            HTTPException: Raised if the provided credentials are invalid (HTTP 401 Unauthorized).
        """
    user = db.query(User).filter(User.username == user_data.username).first()
    hashed_password = hash_password(user_data.password)
    if user is None or not verify_password(user_data.password, hashed_password):
        raise HTTPException(status_code=401, detail=Invalid_Cradentials)
    user_id = user.id
    token = generate_token(user_id)
    return Token(access_token=token, token_type="bearer")


@routes.get('/users/{username}',
            response_model=GetUser,
            status_code=status.HTTP_200_OK)
def create_user(username: str,
                db: Session = Depends(get_db)
                ) -> GetUser:
    """
     Retrieve user details by username.

     Args:
         username (str): The username to retrieve user details for.
         db (Session): The database session.

     Returns:
         GetCreate: The response model containing user details.

     Raises:
         HTTPException: Raised if the user with the specified username is not found (HTTP 404 Not Found).
     """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_EXIST)
    return user
