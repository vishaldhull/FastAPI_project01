from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos



SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass = StaticPool,
    )

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "test_user", "id": 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test Todo",
        description="This is a test todo item",
        priority=3,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json() == [{"complete": False, 
                                "description": "This is a test todo item", 
                                "id": 1, 
                                "owner_id": 1, 
                                "priority": 3, 
                                "title": "Test Todo"
                                }]
    
def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete": False, 
                                "description": "This is a test todo item", 
                                "id": 1, 
                                "owner_id": 1, 
                                "priority": 3, 
                                "title": "Test Todo"
                                }
    
def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    

def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "This is a new todo item",
        "priority": 2,
        "complete": False
    }
    response = client.post("/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id ==2).first()
    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]


def test_update_todo(test_todo):
    request_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 5,
        "complete": False
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 5,
        "complete": False
    }
    response = client.put("/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

