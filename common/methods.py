from models.stockdata import StockData


def calculate_price(
    stock_data: StockData, transaction_type: str, transaction_volume: int
) -> float:
    """
    Calculate the transaction price based on stock data, transaction type, and volume.

    Args:
        stock_data (StockData): The stock data for the transaction.
        transaction_type (str): The type of transaction, either "buy" or "sell".
        transaction_volume (float): The volume of the transaction.

    Returns:
        float: The calculated transaction price.
    """
    if transaction_type == "buy":
        return stock_data.low * transaction_volume

    return stock_data.high * transaction_volume
