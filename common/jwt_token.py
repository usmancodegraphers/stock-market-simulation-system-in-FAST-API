from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JOSEError, jwt
from sqlalchemy.orm import Session

from config.config import settings
from db.database import get_db
from models.user import User

security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash the input password
     Args:
        password (str): The plain-text password to be hashed.
    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify the input password against the hashed password.

    Args:
        password (str): The plain-text password to be verified.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def generate_token(user_id: str) -> str:
    """
    Generate a JSON Web Token (JWT) for the given user ID.

    Args:
        user_id (str): The user ID for which the token is generated.

    Returns:
        str: The generated JWT.
    """
    expiration = datetime.utcnow() + timedelta(hours=int(settings.EXPIRY))
    payload = {"sub": str(user_id), "exp": expiration}
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the current logged-in user.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials obtained from the request.
        db (Session): The database session.

    Returns:
        User: The user corresponding to the provided JWT token.

    Raises:
        HTTPException: Raised if the credentials are invalid or the user does not exist.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub")
    except JOSEError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise credentials_exception
    return user
