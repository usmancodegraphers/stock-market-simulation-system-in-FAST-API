from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.stockdata import StockData
from schemas.stockdata_schema import StockDataSchema
from constants import TICKER_EXIST

routes = APIRouter()


@routes.post(
    '/stocks/',
    response_model=StockDataSchema,
    status_code=status.HTTP_201_CREATED
)
def create_stock(
        data: StockDataSchema,
        db: Session = Depends(get_db)
) -> StockDataSchema:
    """
    Create a new stock entry.

    Args:
        data (StockDataSchema): The data representing the stock to be created.
        db (Session): The database session.

    Returns:
        StockDataSchema: The newly created stock data.
    """

    exist_ticker = db.query(StockData).filter(StockData.ticker == data.ticker).first()
    if exist_ticker:
        raise HTTPException(status_code=400, detail=TICKER_EXIST)
    stock_data = StockData(
        ticker=data.ticker,
        open_price=data.open_price,
        close_price=data.close_price,
        high=data.high,
        low=data.low,
        volume=data.volume,
        timestamp=data.timestamp,
    )

    db.add(stock_data)
    db.commit()
    return stock_data


@routes.get(
    '/stocks/',
    response_model=List[StockDataSchema],
    status_code=status.HTTP_200_OK)
def all_stocks(db: Session = Depends(get_db)):
    """
    Retrieve a list of all stock data entries.

    Args:
        db (Session): The database session.

    Returns:
        List[StockDataSchema]: A list containing all stock data entries.
    """
    return db.query(StockData).all()


@routes.get(
    '/stocks/{ticker}',
    response_model=StockDataSchema,
    status_code=status.HTTP_200_OK
)
def get_stock(ticker: str,
              db: Session = Depends(get_db)
              ) -> StockDataSchema:
    """
    Retrieve stock data for a specific ticker.

    Args:
        ticker (str): The stock ticker symbol.
        db (Session): The database session.

    Returns:
        StockDataSchema: The stock data entry for the specified ticker.

    Raises:
        HTTPException: Raised if the specified ticker is not found (HTTP 404 Not Found).
    """
    data = db.query(StockData).filter(StockData.ticker == ticker).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data
