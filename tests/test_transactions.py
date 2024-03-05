import pytest
from fastapi.testclient import TestClient

from db.database import Base, engine
from main import app
from models.stockdata import StockData
from models.transactions import Transactions
from models.user import User

client = TestClient(app)

Base.metadata.create_all(bind=engine)


class TestTransactionRecords:
    @pytest.fixture()
    def create_user(self, db_session):
        user_data = {"username": "tester", "password": "password", "balance": 10000.0}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        user = db_session.query(User).filter_by(username="tester").first()
        user_id = user.id

        login_data = {"username": "tester", "password": "password"}
        response = client.post("/login", json=login_data)
        assert response.status_code == 200
        access_token = response.json()["access_token"]

        return user_id, access_token

    @pytest.fixture
    def create_stocks(self, db_session):
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

        return data["ticker"]

    @pytest.fixture
    def create_transaction(self, create_user, create_stocks, db_session):
        user_id, access_token = create_user
        # create_stocks: str
        transaction_data = {
            "ticker": "Total",
            "transaction_type": "buy",
            "transaction_volume": 5,
            "transaction_price": 12.0,
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/transactions/", json=transaction_data, headers=headers)
        assert response.status_code == 201

        yield {
            "user_id": user_id,
            "ticker": create_stocks,
            "access_token": access_token,
        }

        db_session.query(Transactions).filter_by(
            user_id=user_id, ticker="Total"
        ).delete()
        db_session.query(User).filter_by(id=user_id).delete()

        db_session.query(StockData).filter_by(ticker="Total").delete()
        db_session.commit()
        db_session.close()

    def test_create_transaction(self, create_user, create_stocks, db_session):
        user_id, access_token = create_user
        create_stocks: str
        transaction_data = {
            "ticker": "Total",
            "transaction_type": "buy",
            "transaction_volume": 5,
            "transaction_price": 12.0,
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/transactions/", json=transaction_data, headers=headers)
        assert response.status_code == 201

        db_session.query(Transactions).filter_by(
            user_id=user_id, ticker="Total"
        ).delete()
        db_session.query(User).filter_by(id=user_id).delete()

        db_session.query(StockData).filter_by(ticker="Total").delete()
        db_session.commit()
        db_session.close()

    def test_get_user_transactions(
        self, create_user, create_stocks, create_transaction, db_session
    ):
        user_id, access_token = create_user
        ticker = create_stocks
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/transactions/{user_id}/", headers=headers)
        assert response.status_code == 200

        db_session.query(Transactions).filter_by(
            user_id=user_id, ticker=ticker
        ).delete()
        db_session.query(User).filter_by(id=user_id).delete()
        db_session.query(StockData).filter_by(ticker=ticker).delete()
        db_session.commit()
        db_session.close()

    def test_get_user_transactions_no_transactions(self, create_user, db_session):
        user_id, access_token = create_user

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/transactions/{user_id}/", headers=headers)
        assert response.status_code == 404

        db_session.query(User).filter_by(id=user_id).delete()
        db_session.commit()
        db_session.close()
