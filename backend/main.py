"""App FastAPI minima: target verificabile della pipeline di sicurezza."""

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Todo, User, seed


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="security-demo", version="0.1.0", lifespan=lifespan)


def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db


DB = Annotated[Session, Depends(get_db)]


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool
    owner_id: int


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    todos: list[TodoOut]


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from security-demo"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def list_users(db: DB) -> list[UserOut]:
    return [UserOut.model_validate(u) for u in db.query(User).order_by(User.id).all()]


@app.get("/todos")
def list_todos(db: DB, done: bool | None = None) -> list[TodoOut]:
    query = db.query(Todo).order_by(Todo.id)
    if done is not None:
        query = query.filter(Todo.done == done)
    return [TodoOut.model_validate(t) for t in query.all()]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: DB) -> TodoOut:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return TodoOut.model_validate(todo)
