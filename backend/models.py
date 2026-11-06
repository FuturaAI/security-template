"""Tabelle demo con dati fake, popolate all'avvio se vuote."""

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)

    todos: Mapped[list["Todo"]] = relationship(back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="todos")


def seed(db: Session) -> None:
    """Inserisce i dati fake solo se il DB è vuoto (idempotente ai riavvii)."""
    if db.query(User).first():
        return
    alice = User(name="Alice Rossi", email="alice@example.com")
    bob = User(name="Bob Bianchi", email="bob@example.com")
    alice.todos = [
        Todo(title="Configurare la pipeline CI", done=True),
        Todo(title="Aggiornare le dipendenze", done=False),
    ]
    bob.todos = [
        Todo(title="Scrivere i test del backend", done=False),
        Todo(title="Rivedere il Caddyfile", done=True),
        Todo(title="Preparare la demo", done=False),
    ]
    db.add_all([alice, bob])
    db.commit()
