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
    @pytest.fixture
    def create_transaction(self, create_and_login_user, create_stocks, db_session):
        user_id, access_token = create_and_login_user
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

    def test_create_transaction(self, create_and_login_user, create_stocks, db_session):
        user_id, access_token = create_and_login_user
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
        self, create_and_login_user, create_stocks, create_transaction, db_session
    ):
        user_id, access_token = create_and_login_user
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

    def test_get_user_transactions_no_transactions(
        self, create_and_login_user, db_session
    ):
        user_id, access_token = create_and_login_user

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get(f"/transactions/{user_id}/", headers=headers)
        assert response.status_code == 404

        db_session.query(User).filter_by(id=user_id).delete()
        db_session.commit()
        db_session.close()
