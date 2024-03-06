from datetime import datetime
from typing import List, Type

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from celery_service.tasks.saving_transactions import saving_transactions
from common.jwt_token import get_current_user
from common.methods import calculate_price
from db.database import get_db
from models.stockdata import StockData
from models.transactions import Transactions
from models.user import User
from schemas.transactions_schemas import TransectionSchema
from constants import USER_NOT_EXIST, INSUFFICIENT_BALANCE, ZERO_Transactions

routes = APIRouter()


@routes.post(
    "/transactions/",
    response_model=TransectionSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_transactions(
    data: TransectionSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransectionSchema:
    """
    Create a new transaction.

    Args:
        data (TransectionSchema): The transaction data from the request body.
        db (Session): The database session.
        current_user (User): The current logged-in user.

    Returns:
        TransectionSchema: The created transaction data.

    Raises:
        HTTPException: Raised if the specified stock is not found (HTTP 404 Not Found)
                       or if the user has insufficient balance (HTTP 400 Bad Request).
    """
    stock = db.query(StockData).filter(StockData.ticker == data.ticker).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    price = calculate_price(stock, data.transaction_type, data.transaction_volume)
    if data.transaction_type == "buy":
        new_balance = current_user.balance - price
    else:
        new_balance = current_user.balance + price

    if new_balance < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=INSUFFICIENT_BALANCE
        )

    new_transection = Transactions(
        user_id=current_user.id,
        ticker=data.ticker,
        transaction_type=data.transaction_type,
        transaction_volume=data.transaction_volume,
        transaction_price=data.transaction_price,
    )
    saving_transactions.delay(current_user.id, new_balance)
    db.add(new_transection)
    db.commit()
    return data


@routes.get(
    "/transactions/{user_id}/",
    response_model=List[TransectionSchema],
    status_code=status.HTTP_200_OK,
)
def get_user_transactions(
    user_id: str, db: Session = Depends(get_db)
) -> list[Type[Transactions]]:
    """
    Get all transactions for a specific user.

    Args:
        user_id (str): The ID of the user for whom transactions are requested.
        db (Session): The database session.

    Returns:
        List[TransectionSchema]: A list of transaction data for the specified user.

    Raises:
        HTTPException: Raised if no transactions are found for the specified user
        (HTTP 404 Not Found).
    """
    user_transection = (
        db.query(Transactions).filter(Transactions.user_id == user_id).all()
    )
    if not user_transection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_EXIST
        )
    return user_transection


@routes.get(
    "/transactions/{user_id}/{start_timestamp}/{end_timestamp}",
    response_model=List[TransectionSchema],
    status_code=status.HTTP_200_OK,
)
def get_user_transactions_in_time(
    user_id: str,
    start_timestamp: datetime,
    end_timestamp: datetime,
    db: Session = Depends(get_db),
) -> list[Type[Transactions]]:
    """
    Get transactions for a specific user within a specified time range.

    Args:
        user_id (str): The ID of the user for whom transactions are requested.
        start_timestamp (datetime): The start timestamp for the time range.
        end_timestamp (datetime): The end timestamp for the time range.
        db (Session): The database session.

    Returns:
        List[TransectionSchema]: A list of transaction data for the specified
        user within the specified time range.

    Raises:
        HTTPException: Raised if no transactions are found for the specified
        user and time range (HTTP 404 Not Found).
    """
    user_transactions = (
        db.query(Transactions)
        .filter(
            (Transactions.user_id == user_id)
            & (Transactions.timestamp >= start_timestamp)
            & (Transactions.timestamp <= end_timestamp)
        )
        .all()
    )
    if not user_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ZERO_Transactions
        )
    return user_transactions
