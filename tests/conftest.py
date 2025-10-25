import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient


from main import app
from app.core.db import get_db, Base
from app.users.models import UserModel
from app.expenses.models import ExpenseModel
from app.core.jwt_utils import generate_access_token, generate_refresh_token


SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="package")
def override_get_db():
    session = Session(bind=test_engine, autoflush=False, autocommit=False)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module", autouse=True)
def override_dependencies(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="package", autouse=True)
def create_mock_data(override_get_db):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    normal_user = UserModel(
        username=user_data["username"], email=user_data["email"].lower()
    )
    normal_user.set_password(user_data["password"])
    override_get_db.add(normal_user)
    override_get_db.commit()
    override_get_db.refresh(normal_user)
    expense1 = ExpenseModel(
        title="Groceries",
        amount=150.75,
        description="Weekly grocery shopping",
        user_id=normal_user.id,
    )
    override_get_db.add(expense1)
    override_get_db.commit()
    override_get_db.refresh(expense1)
    user_data = {
        "username": "authuser",
        "email": "authuser@example.com",
        "password": "testpassword",
    }
    auth_user = UserModel(
        username=user_data["username"], email=user_data["email"].lower()
    )
    auth_user.set_password(user_data["password"])
    override_get_db.add(auth_user)
    override_get_db.commit()
    override_get_db.refresh(auth_user)
    expense2 = ExpenseModel(
        title="auth Groceries",
        amount=250.75,
        description="Auth Weekly grocery shopping",
        user_id=auth_user.id,
    )
    override_get_db.add(expense2)
    override_get_db.commit()
    override_get_db.refresh(expense2)


@pytest.fixture(scope="function")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def auth_client(override_get_db):
    auth_user = (
        override_get_db.query(UserModel).filter_by(email="authuser@example.com").first()
    )
    access_token = generate_access_token(auth_user.id)
    refresh_token = generate_refresh_token(auth_user.id)
    client = TestClient(app)
    client.cookies.set("access_token", access_token)
    client.cookies.set("refresh_token", refresh_token)

    yield client
