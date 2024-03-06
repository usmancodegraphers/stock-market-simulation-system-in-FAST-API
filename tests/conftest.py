import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.database import engine, Base
from main import app
from models.user import User
from tests.database import test_db_session

client = TestClient(app)


@pytest.fixture
def db_session():
    return next(test_db_session())


@pytest.fixture(scope="function", autouse=True)
def truncate_db(db_session):
    session = Session(bind=engine)
    session.begin_nested()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
        session.commit()
    yield
    session.rollback()
    session.close()


@pytest.fixture
def created_user(self, db_session):
    data = {"username": "usman", "password": "usman123", "balance": 10900}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    return data["username"]


@pytest.fixture()
def create_and_login_user(self, db_session):
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


Base.metadata.create_all(bind=engine)
