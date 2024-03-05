import pytest
from fastapi.testclient import TestClient

from db.database import Base, engine
from main import app

client = TestClient(app)

Base.metadata.create_all(bind=engine)


class TestUserRoutes:
    @pytest.fixture
    def created_user(self, db_session):
        data = {"username": "usman", "password": "usman123", "balance": 10900}
        response = client.post("/users/", json=data)
        assert response.status_code == 201
        return data["username"]

    def test_create_user(self, db_session):
        data = {"username": "test", "password": "test123", "balance": 100}
        response = client.post("/users/", json=data)
        assert response.status_code == 201

    def test_create_same_user(self, created_user):
        data = {"username": created_user, "password": "usman", "balance": 10900}
        response = client.post("/users/", json=data)
        assert response.status_code == 400

    def test_login_user(self, created_user):
        data = {"username": created_user, "password": "usman123"}
        response = client.post("/login", json=data)

        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_not_exist_user(self, db_session):
        data = {"username": "test", "password": "usman123"}
        response = client.post("/login", json=data)

        assert response.status_code == 401

    def test_get_user(self, created_user):
        created_user: str
        username = "usman"
        response = client.get(f"/users/{username}")
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == username

    def test_get_not_exist_user(self, db_session):
        username = "usman"
        response = client.get(f"/users/{username}")
        assert response.status_code == 404
