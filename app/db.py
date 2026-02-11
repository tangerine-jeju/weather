from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()


def init_db(database_url: str) -> None:
    global engine
    engine = create_engine(database_url, future=True)
    SessionLocal.configure(bind=engine)

    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
