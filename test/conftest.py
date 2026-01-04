import pytest
from dotenv import load_dotenv
import os

os.environ["ENV_FILE"] = "test/.env.test"
load_dotenv(".env.test", override=True)

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import Settings
from app.core.config import Settings
test_settings = Settings()

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        url=test_settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    SQLModel.metadata.drop_all(engine)
    engine.dispose()
    
@pytest.fixture(scope="function")
def session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session
    
    session.close()
    transaction.rollback()
    connection.close()    

@pytest.fixture(scope="function")
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture
def create_user(client):
    def _create_user(
            username: str, 
            password:str, 
            is_admin: bool = False
    ):
        registration_response = client.post(
            "/register/",
            data={
                "username": username, 
                "password": password,
                "is_admin": is_admin
                },
        )
        assert registration_response.status_code == 200
        assert registration_response.cookies.get("access_token") != ""
        token = registration_response.cookies.get("access_token")
        user_id = registration_response.json()["user"]["id"]

        return {
            "user_id": user_id, 
            "username": username, 
            "password": password,
            "is_admin": is_admin,
            "token": token
        }
    return _create_user


@pytest.fixture
def create_task(client):
    def _create_task(
            token: str,
            params: list[tuple]
    ):
        client.cookies["access_token"] = token
        response = client.get(
            "/post/",
            params=params
        )
        assert response.status_code == 201

        return response
    
    return _create_task

@pytest.fixture
def default_start_test_sequence(create_user, create_task):
    default_user = create_user(
        username="user",
        password="123"
    )

    response_create_2_tasks = create_task(
        token = default_user["token"],
        params = [
            ("task_content", "First task"),
            ("task_content", "Second task"),
        ]
    )
    assert response_create_2_tasks.status_code == 201
    return default_user, response_create_2_tasks
