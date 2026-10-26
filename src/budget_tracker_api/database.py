from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from budget_tracker_api.config import settings
from budget_tracker_api.models import Base

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}, 
)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON") 
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)