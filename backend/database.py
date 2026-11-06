"""Connessione al DB: SQLite in locale, sostituibile via DATABASE_URL (es. PostgreSQL)."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL: "postgresql://username:password@hostname:port/database_name
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@hostname:port/database_name)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo.db")

# check_same_thread=False: FastAPI esegue le route sync in un threadpool,
# quindi la connessione SQLite può essere usata da thread diversi.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
