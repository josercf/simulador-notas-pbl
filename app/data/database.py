from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///simulador.db"


class Base(DeclarativeBase):
    """Base declarativa para modelos SQLAlchemy."""


engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Cria as tabelas no banco SQLite."""
    from app.data import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
