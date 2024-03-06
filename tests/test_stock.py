from fastapi.testclient import TestClient

from db.database import Base, engine
from main import app

client = TestClient(app)

Base.metadata.create_all(bind=engine)


class TestStockRoutes:
    def test_create_stocks(self, db_session):
        data = {
            "ticker": "Total",
            "open_price": 10,
            "close_price": 10,
            "high": 10,
            "low": 10,
            "volume": 10,
            "timestamp": "2024-03-05T08:59:46.994966",
        }

        response = client.post("/stocks/", json=data)
        assert response.status_code == 201

    def test_create_stocks_with_same_ticker(self, create_stocks):
        data = {
            "ticker": create_stocks,
            "open_price": 10,
            "close_price": 10,
            "high": 10,
            "low": 10,
            "volume": 10,
            "timestamp": "2024-03-05T08:59:46.994966",
        }

        response = client.post("/stocks/", json=data)
        assert response.status_code == 400

    def test_get_ticker(self, create_stocks):
        ticker = create_stocks

        response = client.get(f"/stocks/{ticker}")
        assert response.status_code == 200

    def test_get_not_register_ticker(self, db_session):
        ticker = "Dell"
        response = client.get(f"/stocks/{ticker}")

        assert response.status_code == 404
